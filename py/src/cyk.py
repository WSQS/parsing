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


def eliminate_epsilon_non_terminal(g: Grammar, non_terminal: str):
    new_rule = g.rule[:]
    for l, rs in g.rule:
        if non_terminal not in rs:
            continue
        rs_queue = [rs]
        rs_result: list[list[str]] = []
        while len(rs_queue):
            cur_rs = rs_queue[0]
            for i, r in enumerate(cur_rs):
                if r == non_terminal:
                    new_rs = cur_rs[:i] + cur_rs[i + 1 :]
                    if non_terminal in new_rs:
                        rs_queue.append(new_rs)
                    elif new_rs not in rs_result and len(new_rs) > 0:
                        rs_result.append(new_rs)
        for i_rs in rs_result:
            new_rule.append((l, i_rs))


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
