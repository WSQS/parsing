from parsing.cyk import eliminate_epsilon_rules
from parsing.grammar import parse_grammar


def test_eliminate_epsilon_rules():
    f_4_10 = """
S -> L a M
L -> L M
L -> 
M -> M M
M ->"""

    f_4_11 = """
S -> L' a M'
S -> a M'
S -> L' a
S -> a
L -> L' M'
L -> L'
L -> M'
L ->
M -> M' M'
M -> M'
M -> 
L' -> L' M'
L' -> L'
L' -> M'
M' -> M' M'
M' -> M'
"""

    g = parse_grammar(f_4_10)
    eliminate_epsilon_rules(g)
    rg = parse_grammar(f_4_11)
    for l, rs in g.rule:
        assert (l, rs) in rg.rule
    for l, rs in rg.rule:
        assert (l, rs) in g.rule


test_eliminate_epsilon_rules()
