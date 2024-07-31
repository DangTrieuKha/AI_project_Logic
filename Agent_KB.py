from pysat.formula import CNF
from pysat.solvers import Solver

class AgentKB:
    def __init__(self):
        self.kb = CNF()

    def add_clause(self, clause):
        self.kb.append(clause)

    def ask(self, query):
        with Solver(bootstrap_with=self.kb) as solver:
            result = solver.solve(assumptions=query)
            return result

    def tell(self, percepts):
        # Convert percepts to clauses and add to KB
        # Example: If there is a breeze at (1,1), it means there is a pit in one of the adjacent cells
        for percept in percepts:
            if percept == 'Breeze':
                x, y = percepts[percept]
                # Breeze at (x, y) -> Pit in (x-1, y), (x+1, y), (x, y-1), (x, y+1)
                self.add_clause([-self.pos_literal(x-1, y), -self.pos_literal(x+1, y), 
                                 -self.pos_literal(x, y-1), -self.pos_literal(x, y+1)])
            elif percept == 'Stench':
                # Stench at (x, y) -> Wumpus in (x-1, y), (x+1, y), (x, y-1), (x, y+1)
                self.add_clause([-self.pos_literal(x-1, y), -self.pos_literal(x+1, y), 
                                 -self.pos_literal(x, y-1), -self.pos_literal(x, y+1)])
            elif percept == 'Whiff':
                # Whiff at (x, y) -> Poisonous Gas in (x-1, y), (x+1, y), (x, y-1), (x, y+1)
                self.add_clause([-self.pos_literal(x-1, y), -self.pos_literal(x+1, y), 
                                 -self.pos_literal(x, y-1), -self.pos_literal(x, y+1)])
            elif percept == 'Glow':
                # Glow at (x, y) -> Healing Potions in (x-1, y), (x+1, y), (x, y-1), (x, y+1)
                self.add_clause([-self.pos_literal(x-1, y), -self.pos_literal(x+1, y), 
                                 -self.pos_literal(x, y-1), -self.pos_literal(x, y+1)])
            elif percept == 'Wumpus':
                # Directly state that Wumpus is at (x, y)
                self.add_clause([self.pos_literal(x, y)])
            elif percept == 'Pit':
                # Directly state that Pit is at (x, y)
                self.add_clause([self.pos_literal(x, y)])
            elif percept == 'Gold':
                # Directly state that Gold is at (x, y)
                self.add_clause([self.pos_literal(x, y)])
            elif percept == 'Poisonous Gas':
                # Directly state that Poisonous Gas is at (x, y)
                self.add_clause([self.pos_literal(x, y)])
            elif percept == 'Healing Potions':
                # Directly state that Healing Potions is at (x, y)
                self.add_clause([self.pos_literal(x, y)])
                

    def pos_literal(self, x, y):
        # Example function to map (x, y) to a positive literal
        return x * 10 + y

    def neg_literal(self, x, y):
        # Example function to map (x, y) to a negative literal
        return -self.pos_literal(x, y)

# Khởi tạo Agent KB
agent_kb = AgentKB()

# Thêm các quy tắc ban đầu vào KB
# Ví dụ: Breeze tại (1,1) -> Pit tại (1,2) hoặc (2,1) hoặc (0,1) hoặc (1,0)
agent_kb.tell({'Breeze': (1, 1)})

# Hỏi liệu có một Pit tại (1,2)
query = [agent_kb.pos_literal(1, 2)]
result = agent_kb.ask(query)
print(f"Is there a pit at (1,2)? {'Yes' if result else 'No'}")
