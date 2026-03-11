import argparse
from copy import copy
from dataclasses import dataclass, field
from typing import Any, Generator
from grammar import Grammar, is_non_terminal, parse_grammar


@dataclass
class Sentence:
    token: list[str]
    start_index: int = field(default=1)


@dataclass
class Context:
    substring_stack: list[str] = field(default_factory=list[str])
    negative_substrings: list[str] = field(default_factory=list[str])
    non_terminal_min_len: dict[str, int] = field(default_factory=dict[str, int])


def precompute(g: Grammar, context: Context):
    context.non_terminal_min_len.clear()
    update = True
    while update:
        update = False
        for l, rs in g.rule:
            length = 0
            for r in rs:
                if is_non_terminal(r):
                    if r not in context.non_terminal_min_len:
                        length = -1
                        break
                    length += context.non_terminal_min_len[r]
                else:
                    length += 1
            if length == -1:
                continue
            if (
                l not in context.non_terminal_min_len
                or context.non_terminal_min_len[l] > length
            ):
                update = True
                context.non_terminal_min_len[l] = length


def group_into(n_element: int, groups: list[int]) -> Generator[list[int], Any, None]:
    if n_element < 0:
        msg = f"n_element = {n_element} < 0"
        raise ValueError(msg)
    if len(groups) == 0:
        if n_element == 0:
            # for the epsilon rule.
            yield []
        return
    if len(groups) == 1:
        yield [n_element]
        return
    for i in range(groups[0], n_element + 1):
        for l in group_into(n_element - i, groups[1:]):
            yield [i] + l


def parse_substring(g: Grammar, ts: Sentence, symbol: str, context: Context):
    result = Grammar()
    if (
        f"{symbol}_{ts.start_index}_{len(ts.token)}" in context.substring_stack
        or f"{symbol}_{ts.start_index}_{len(ts.token)}" in context.negative_substrings
    ):
        return result
    new_context = copy(context)
    new_context.substring_stack = context.substring_stack[:]
    new_context.substring_stack.append(f"{symbol}_{ts.start_index}_{len(ts.token)}")
    for l, rs in g.rule:
        if l != symbol:
            continue
        print(f"rule:{l, rs}")
        groups: list[int] = []
        for r in rs:
            if is_non_terminal(r):
                if r not in context.non_terminal_min_len:
                    msg = f"Can't get min length for non terminal: {r!r}"
                    raise ValueError(msg)
                groups.append(context.non_terminal_min_len[r])
            else:
                groups.append(1)
        for group_info in group_into(len(ts.token), groups):
            print("group_info", group_info)
            group_grammar = Grammar()
            ts_copy = ts.token[:]
            substrings: list[list[str]] = []
            for substring_length in group_info:
                if substring_length == 0:
                    substrings.append([])
                    continue
                substrings.append(ts_copy[:substring_length])
                ts_copy = ts_copy[substring_length:]
            print("substring", substrings)
            new_rs: list[str] = []
            offset = 0
            for r, substring in zip(rs, substrings):
                if is_non_terminal(r):
                    subgrammar = parse_substring(
                        g, Sentence(substring, ts.start_index + offset), r, new_context
                    )
                    if not subgrammar.rule:
                        break
                    group_grammar.rule += subgrammar.rule
                else:
                    if len(substring) != 1 or substring[0] != r:
                        break
                    group_grammar.rule.append(
                        (f"{r}_{ts.start_index + offset}_{len(substring)}", [r])
                    )
                new_rs.append(f"{r}_{ts.start_index + offset}_{len(substring)}")
                offset += len(substring)
            else:
                # the group is match successfully
                if not new_rs:
                    # In output grammar, the non terminal output a empty terminal
                    new_rs.append(f"_{ts.start_index}_{len(ts.token)}")
                    group_grammar.rule.append(
                        (f"_{ts.start_index}_{len(ts.token)}", ["epsilon"])
                    )
                result.rule += group_grammar.rule
                result.rule.append((f"{l}_{ts.start_index}_{len(ts.token)}", new_rs))
                continue
    if not result.rule:
        new_context.negative_substrings.append(
            f"{symbol}_{ts.start_index}_{len(ts.token)}"
        )
    return result


def parse(g: Grammar, ts: Sentence, context: Context):
    return parse_substring(g, ts, g.start_symbol, context)


def main():
    parser = argparse.ArgumentParser(
        description="Python implementation for Unger's parsing method."
    )
    parser.add_argument("grammar", type=str, help="Grammar File")
    parser.add_argument("input", type=str, help="Input File")
    args = parser.parse_args()
    with open(args.grammar, "r", encoding="utf-8") as f:
        s_g = f.read()
    g = parse_grammar(s_g)
    context = Context()
    precompute(g, context)
    print(g)
    with open(args.input, "r", encoding="utf-8") as f:
        s_i = f.read()
    tokens = s_i.split()
    for token in tokens:
        if token not in g.terminal:
            msg = f"It's not a non terminal in grammar:{token!r}"
            raise ValueError(msg)
    parse_tree_grammar = parse(g, Sentence(tokens), context)
    print(parse_tree_grammar)
    for l, rs in parse_tree_grammar.rule:
        for r in rs:
            print(l, "-->", r)


if __name__ == "__main__":
    main()
