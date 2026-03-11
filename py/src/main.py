import argparse
from grammar import parse_grammar
from unger import parse


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
    print(g)
    with open(args.input, "r", encoding="utf-8") as f:
        s_i = f.read()
    tokens = s_i.split()
    for token in tokens:
        if token not in g.terminal:
            msg = f"It's not a non terminal in grammar:{token!r}"
            raise ValueError(msg)
    parse_tree_grammar = parse(g, tokens)
    print(parse_tree_grammar)
    for l, rs in parse_tree_grammar.rule:
        for r in rs:
            print(l, "-->", r)


if __name__ == "__main__":
    main()
