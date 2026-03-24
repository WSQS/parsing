from .grammar import Grammar, is_non_terminal


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
    new_rule: list[tuple[str, list[str]]] = []
    for l, rs in g.rule:
        if non_terminal not in rs:
            new_rule.append((l, rs))
            continue
        rs_queue = [rs]
        rs_result: list[list[str]] = []
        while len(rs_queue):
            cur_rs = rs_queue.pop(0)
            for i, r in enumerate(cur_rs):
                if r == non_terminal:
                    new_rs1 = cur_rs[:i] + cur_rs[i + 1 :]
                    if non_terminal in new_rs1:
                        rs_queue.append(new_rs1)
                    elif new_rs1 not in rs_result:
                        rs_result.append(new_rs1)
                    new_rs2 = cur_rs[:i] + [non_terminal + "'"] + cur_rs[i + 1 :]
                    if non_terminal in new_rs2:
                        rs_queue.append(new_rs2)
                    elif new_rs2 not in rs_result:
                        rs_result.append(new_rs2)
        for i_rs in rs_result:
            new_rule.append((l, i_rs))
    g.rule = new_rule
    new_rule = []
    for l, rs in g.rule:
        if l != non_terminal and len(rs) == 0:
            continue
        new_rule.append((l, rs))
    g.rule = new_rule


def eliminate_epsilon_rules(g: Grammar):
    epsilon_non_terminals = get_epsilon_non_terminal(g)
    for epsilon_non_terminal in epsilon_non_terminals:
        eliminate_epsilon_non_terminal(g,epsilon_non_terminal)


def to_cnf(g: Grammar):
    eliminate_epsilon_rules(g)
    pass


def parse(g: Grammar, ts: list[str]):
    to_cnf(g)
