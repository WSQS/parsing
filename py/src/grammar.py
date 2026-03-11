from dataclasses import dataclass, field


def is_non_terminal(token: str):
    return token[0].isupper()


@dataclass
class Grammar:
    non_terminal: set[str] = field(default_factory=set[str])
    terminal: set[str] = field(default_factory=set[str])
    rule: list[tuple[str, list[str]]] = field(
        default_factory=list[tuple[str, list[str]]]
    )
    start_symbol: str = field(default_factory=str)
    non_terminal_min_len: dict[str, int] = field(default_factory=dict[str, int])

    def precompute(self):
        self.non_terminal_min_len.clear()
        update = True
        while update:
            update = False
            for l, rs in self.rule:
                length = 0
                for r in rs:
                    if is_non_terminal(r):
                        if r not in self.non_terminal_min_len:
                            length = -1
                            break
                        length += self.non_terminal_min_len[r]
                    else:
                        length += 1
                if length == -1:
                    continue
                if (
                    l not in self.non_terminal_min_len
                    or self.non_terminal_min_len[l] > length
                ):
                    update = True
                    self.non_terminal_min_len[l] = length
        # TODO: we need to clean up rule to avoid excetion later.


def parse_grammar(s_grammer: str):
    grammar = Grammar()
    for l_id, lg in enumerate(s_grammer.splitlines(), start=1):
        if not lg.strip():
            continue
        sides = lg.split("->", 1)
        if len(sides) != 2:
            msg = f"{l_id}:Missing '->' in {lg!r}"
            raise ValueError(msg)
        l, r = sides[0].strip(), sides[1].strip()
        if len(l) == 0:
            msg = f"{l_id}:It's empty in left side:{lg!r}"
            raise ValueError(msg)
        # No need to check right side, if right side is empty, it means epsilon
        if not is_non_terminal(l):
            msg = f"{l_id}:It's not a non terminal in left:{l!r}"
            raise ValueError(msg)
        if not grammar.start_symbol:
            grammar.start_symbol = l
        grammar.non_terminal.add(l)
        rs = r.split()
        for ri in rs:
            if is_non_terminal(ri):
                grammar.non_terminal.add(ri)
            else:
                grammar.terminal.add(ri)
        grammar.rule.append((l, rs))
    return grammar
