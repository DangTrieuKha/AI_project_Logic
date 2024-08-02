from pysat.formula import CNF
from pysat.solvers import Glucose3
import itertools
import copy

class AgentKB:
    def __init__(self):
        self.kb = CNF()

    def add_clause(self, clause):
        # Thêm một mệnh đề vào CNF
        self.kb.append(clause)

    def pl_resolve(self, ci, cj):
        resolvents = []
        for di in ci:
            for dj in cj:
                if di == -dj:
                    resolvent = list(set(ci + cj) - {di, dj})
                    if not resolvent:
                        resolvents.append([])
                    else:
                        resolvents.append(resolvent)
        return resolvents

    def ask(self, query):
        clauses = copy.deepcopy(self.kb.clauses)
        clauses.append([-literal for literal in query])  # Thêm phủ định của query

        new = []
        while True:
            pairs = itertools.combinations(clauses, 2)
            for (ci, cj) in pairs:
                resolvents = self.pl_resolve(ci, cj)
                if [] in resolvents:
                    return True  # Mâu thuẫn, tức là có thể suy ra query
                new.extend(resolvents)
            new = list(filter(lambda x: x not in clauses, new))
            if not new:
                return False  # Không có mâu thuẫn, không thể suy ra query
            clauses.extend(new)

    def tell(self, percepts):
        for percept in percepts:
            if percept == 'Breeze':
                x, y = percepts[percept]
                # Breeze tại (x, y) -> Pit tại (x-1, y) OR (x+1, y) OR (x, y-1) OR (x, y+1)
                self.add_clause([self.pos_literal(x-1, y), self.pos_literal(x+1, y), 
                                 self.pos_literal(x, y-1), self.pos_literal(x, y+1)])
            elif percept == 'Stench':
                x, y = percepts[percept]
                # Stench tại (x, y) -> Wumpus tại (x-1, y) OR (x+1, y) OR (x, y-1) OR (x, y+1)
                self.add_clause([self.pos_literal_wumpus(x-1, y), self.pos_literal_wumpus(x+1, y), 
                                 self.pos_literal_wumpus(x, y-1), self.pos_literal_wumpus(x, y+1)])

    def pos_literal(self, x, y):
        # Chuyển (x, y) thành literal tích cực cho Pit
        return (x * 10 + y) + 1  # Thêm 1 để đảm bảo các literals không trùng lặp

    def pos_literal_wumpus(self, x, y):
        # Chuyển (x, y) thành literal tích cực cho Wumpus
        return (x * 10 + y) + 100  # Offset bởi 100 để phân biệt với literals của Pit

    def neg_literal(self, x, y):
        # Chuyển (x, y) thành literal âm cho Pit
        return -self.pos_literal(x, y)

    def neg_literal_wumpus(self, x, y):
        # Chuyển (x, y) thành literal âm cho Wumpus
        return -self.pos_literal_wumpus(x, y)

    def is_there_pit(self, x, y):
        # Kiểm tra liệu có chắc chắn có Pit tại (x, y)
        query_pit = [self.pos_literal(x, y)]
        result_pit = self.ask(query_pit)
        return result_pit  # Trả về True nếu có Pit tại (x, y), False nếu không biết

# Khởi tạo Agent KB
agent_kb = AgentKB()

# Thêm các quy tắc ban đầu vào KB
agent_kb.tell({'Breeze': (1, 1)})
agent_kb.add_clause([agent_kb.pos_literal(1, 2)])

# Kiểm tra liệu có Pit tại (1,2)
result_pit = agent_kb.is_there_pit(1, 2)
print(f"Is there a pit at (1,2)? {'Yes' if result_pit else 'do not know'}")
