from grammar import Grammar, is_non_terminal


def get_epsilon_non_terminal(g: Grammar):
    result: set[str] = set()
    while True:
        update = False
        for l, rs in g.rule:
            if l in result:
                continue
            length = 0
            for r in rs:
                if is_non_terminal(r):
                    if r not in result:
                        length = -1
                        break
                else:
                    length += 1
            if length == 0:
                result.add(l)
                update = True
        if not update:
            return result


def eliminate_epsilon_rules(g: Grammar):
    epsilon_non_terminals = get_epsilon_non_terminal(g)
    new_rule: list[tuple[str, list[str]]] = []
    while True:
        update = False
        for l, rs in g.rule:
            if l in epsilon_non_terminals:
                continue
            for i, r in enumerate(rs):
                if r in epsilon_non_terminals:
                    new_rule.append((l, rs[:i] + rs[i + 1 :]))
                    update = True
        if not update:
            break
    g.rule = new_rule


def to_cnf(g: Grammar):
    eliminate_epsilon_rules(g)
    pass


def parse(g: Grammar, ts: list[str]):
    to_cnf(g)
