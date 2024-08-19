from pysat.formula import CNF
from pysat.solvers import Minisat22
import itertools
import copy

class AgentKB:
    def __init__(self):
        self.kb = CNF()

    def add_clause(self, clause):
        # Thêm một mệnh đề vào CNF
        # for child_clause in clause:
        #     self.add_single_clause(child_clause)
        self.kb.append(clause)

    def ask(self, query):
        clauses = copy.deepcopy(self.kb.clauses)
        clauses.append([-literal for literal in query])  # Thêm phủ định của query

        solver = Minisat22()
        solver.append_formula(clauses)

        res = solver.solve()

        solver.delete()

        return not res

    def isValid(self, x, y):
        if x >= 1 and x <= 10 and y >= 1 and y <= 10:
            return True
        return False
    
    #This function use to add a single clause to KB. 
    #when add a single clause to KB can lead to conflict so create this function. parameter clause has form as: self.neg/pos_literrial_...(x,y)
    def add_single_clause(self, clause):
        new_kb = CNF()
        pos_clause = -clause

        # if 411 <= clause <= 810:
        #     self.kb.append([clause])
        #     return

        for k in self.kb.clauses:
            if pos_clause in k and (pos_clause in range(411, 811) or pos_clause in range(-810,-411 + 1) or pos_clause in range(111, 211) or pos_clause in range(311, 411) or pos_clause in range(-410, -311 + 1) or pos_clause in range(-210, -111 + 1)) and len(k) == 1:
                
                # new_clause = [lit for lit in k if lit != pos_clause]
                # if len(new_clause) == 1:
                #     if pos_clause in range(111, 211 + 1) or pos_clause in range(311, 411 + 1) or pos_clause in range(-411, -311 + 1) or pos_clause in range(-211, -111 + 1):
                #         new_clause = None
                # if new_clause:
                #     new_kb.append(new_clause)
                continue
            else:
                new_kb.append(k)

        new_kb.append([clause])
        self.kb = new_kb

    # this function is used to confirm cell (x,y) do not have wumpus after shoot
    def assertNoWumpusPostShoot(self, x,y):
        # add not wumpus at (x,y)
        self.add_single_clause(self.neg_literal_wumpus(x,y))
        #add not reliable stench at adjacent celss
        dx = [-1, 1, 0, 0]
        dy = [0,0,-1,1]
        for k in range(4):
            x_new = x + dx[k]
            y_new = y + dy[k]
            if self.isValid(x_new,y_new):
                self.add_single_clause(self.neg_literal_reliable_stench(x_new,y_new))
    # this function is used to confirm cell (x,y) do not have healing after grab
    def assertNoHealingPostGrab(self,x,y):
        self.add_single_clause(self.neg_literal_healing(x,y))
        dx = [-1, 1, 0, 0]
        dy = [0,0,-1,1]
        for k in range(4):
            x_new = x + dx[k]
            y_new = y + dy[k]
            if self.isValid(x_new,y_new):
                self.add_single_clause(self.neg_literal_reliable_glow(x_new,y_new))

    def tell(self, percepts, x,y):
        dx = [-1, 1, 0, 0]
        dy = [0,0,-1,1]
        if 'B' in percepts:
            tmp = []
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    tmp.append(self.pos_literal_pit(x_new, y_new))
            self.add_clause(tmp)
        else:
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    self.add_single_clause(self.neg_literal_pit(x_new,y_new))
    
        if 'S' in percepts:
            # Stench tại (x, y) -> Wumpus tại (x-1, y) OR (x+1, y) OR (x, y-1) OR (x, y+1)
            tmp = [self.neg_literal_reliable_stench(x,y),self.neg_literal_stench(x,y)]
            
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    #add (S and R_S) -> W
                    tmp.append(self.pos_literal_wumpus(x_new, y_new))
           
                    
            self.add_clause(tmp)
            #add S
            self.add_single_clause(self.pos_literal_stench(x,y))
            # add R_S
            self.add_single_clause(self.pos_literal_reliable_stench(x,y))
        else:
            #add not wumpus
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    # add not W
                    self.add_single_clause(self.neg_literal_wumpus(x_new,y_new))
            # add not S
            self.add_single_clause(self.neg_literal_stench(x,y))
            # add R_S
            self.add_single_clause(self.pos_literal_reliable_stench(x,y))

        if 'W_H' in percepts:
            tmp = []
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    tmp.append(self.pos_literal_poison(x_new, y_new))
            self.add_clause(tmp)
        else:
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    self.add_single_clause(self.neg_literal_poison(x_new,y_new))
                
                
        if 'G_L' in percepts:
            
            tmp = [self.neg_literal_glow(x,y), self.neg_literal_reliable_glow(x,y)]
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    # add (G and R_G) -> H, add G, add R_G
                    tmp.append(self.pos_literal_healing(x_new, y_new))
            
                    
            self.add_clause(tmp)
            #add G
            self.add_single_clause(self.pos_literal_glow(x,y))
            # add R_G
            self.add_single_clause(self.pos_literal_reliable_glow(x,y))
        else:
            # add not H
            for k in range(4):
                x_new = x + dx[k]
                y_new = y + dy[k]
                if self.isValid(x_new,y_new):
                    self.add_single_clause(self.neg_literal_healing(x_new, y_new))
            #add not G
            self.add_single_clause(self.neg_literal_glow(x,y))
            # add R_G
            self.add_single_clause(self.pos_literal_reliable_glow(x,y))

        if 'P' in percepts:
            self.add_single_clause(self.pos_literal_pit(x,y))
        else:
            self.add_single_clause(self.neg_literal_pit(x,y))
        if 'W' in percepts:
            self.add_single_clause(self.pos_literal_wumpus(x,y))
        else:
            self.add_single_clause(self.neg_literal_wumpus(x,y))
        
        if  'P_G' in percepts:
            self.add_single_clause(self.pos_literal_poison(x,y))
        else:
            self.add_single_clause(self.neg_literal_poison(x,y))
     
        
        if 'H_P' in percepts:
            self.add_single_clause(self.pos_literal_healing(x,y))
        else:
            self.add_single_clause(self.neg_literal_healing(x,y))

    # Khẳng định
    def pos_literal_pit(self, x, y):
        # Chuyển (x, y) thành literal tích cực cho Pit
        return (x * 10 + y) 

    def pos_literal_wumpus(self, x, y):
        # Chuyển (x, y) thành literal tích cực cho Wumpus
        return (x * 10 + y) + 100  # Offset bởi 100 để phân biệt với literals của Pit
    def pos_literal_poison(self, x, y):
        # Chuyển (x, y) thành literal tích cực cho poison
        return (x * 10 + y) + 200
    def pos_literal_healing(self, x, y):
        # Chuyển (x, y) thành literal tích cực cho poison
        return (x * 10 + y) + 300  
    def pos_literal_stench(self,x,y):
        return (x*10 + y) + 400
    def pos_literal_glow(self,x,y):
        return (x*10 + y) + 500
    def pos_literal_reliable_stench(self,x,y):
        return (x*10 + y) + 600
    def pos_literal_reliable_glow(self,x,y):
        return (x*10 + y) + 700
    
    # Phủ định
    def neg_literal_pit(self, x, y):
        # Chuyển (x, y) thành literal âm cho Pit
        return -self.pos_literal_pit(x, y)
    def neg_literal_wumpus(self, x, y):
        # Chuyển (x, y) thành literal âm cho Wumpus
        return -self.pos_literal_wumpus(x, y)
    def neg_literal_poison(self, x, y):
        
        return -self.pos_literal_poison(x, y)
    def neg_literal_healing(self, x, y):
        
        return -self.pos_literal_healing(x, y)
    def neg_literal_stench(self,x,y):
        return -self.pos_literal_stench(x,y)
    def neg_literal_glow(self,x,y):
        return -self.pos_literal_glow(x,y)
    def neg_literal_reliable_stench(self,x,y):
        return - self.pos_literal_reliable_stench(x,y)
    def neg_literal_reliable_glow(self,x,y):
        return -self.pos_literal_reliable_glow(x,y)

    # Truy vấn
    def is_there_pit(self, x, y):
        # Kiểm tra liệu có chắc chắn có Pit tại (x, y)
        query_pit = [self.pos_literal_pit(x, y)]
        result_pit = self.ask(query_pit)
        return result_pit  # Trả về True nếu có Pit tại (x, y), False nếu không biết
    def is_there_not_pit(self, x,y):
        query_pit = [self.neg_literal_pit(x, y)]
        result_pit = self.ask(query_pit)
        return result_pit  # Trả về True nếu ko có Pit tại (x, y), False nếu không biết
    def is_there_wumpus(self, x,y):
        query = [self.pos_literal_wumpus(x, y)]
        result = self.ask(query)
        return result
    def is_there_not_wumpus(self, x,y):
        query = [self.neg_literal_wumpus(x, y)]
        result = self.ask(query)
        return result
    def is_there_poison(self, x, y):
        query = [self.pos_literal_poison(x, y)]
        result = self.ask(query)
        return result
    def is_there_not_poison(self, x, y):
        query = [self.neg_literal_poison(x, y)]
        result = self.ask(query)
        return result
    def is_there_healing(self, x, y):
        query = [self.pos_literal_healing(x, y)]
        result = self.ask(query)
        return result
    def is_there_not_healing(self, x, y):
        query = [self.neg_literal_healing(x, y)]
        result = self.ask(query)
        return result
    def is_there_stench(self,x,y):
        query = [self.pos_literal_stench(x, y)]
        result = self.ask(query)
        return result
    def is_there_not_stench(self,x,y):
        query = [self.neg_literal_stench(x, y)]
        result = self.ask(query)
        return result
    def is_there_glow(self,x,y):
        query = [self.pos_literal_glow(x, y)]
        result = self.ask(query)
        return result
    def is_there_not_glow(self,x,y):
        query = [self.neg_literal_glow(x, y)]
        result = self.ask(query)
        return result





# # Khởi tạo Agent KB

# # Thêm nhận thức: có Breeze tại ô (1,1)
# agent_kb.tell('',1,1)
# # Thêm nhận thức: tại ô (1,2) có pit
# agent_kb.tell('B',1,2)
# agent_kb.tell('',2,2)
# agent_kb.tell('B S',2,3)
# # Kiểm tra liệu có Pit tại (1,2)
# result_pit = agent_kb.is_there_pit(1, 3)
# print(f"Is there a pit at (1,3)? {'Yes' if result_pit else 'do not know'}")

# agent_kb = AgentKB()
# agent_kb.tell('S', 2, 2)
# agent_kb.tell('-',2,1)
# agent_kb.tell('S', 1, 1)
# if agent_kb.is_there_stench(2,2):
#     print('yes')
# agent_kb.tell('S', 3, 4)
# agent_kb.tell('S', 4, 3)
# agent_kb.tell('S', 3, 2)

# print(f"Is there a wumpus at (3,3)? {agent_kb.is_there_wumpus(3, 3)}")

# agent_kb.tell('', 1, 2)
# # agent_kb.tell('', 2, 4)
# agent_kb.tell('', 1, 4)
# # agent_kb.tell('', 5, 3)
# # agent_kb.tell('', 4, 4)

# print(f"Is there a wumpus at (3,3)? {agent_kb.is_there_wumpus(3, 3)}")

# agent_kb = AgentKB()
# agent_kb.tell('W', 2, 2)
# agent_kb.tell('S P P_G', 2, 1)
# agent_kb.tell('S', 1, 2)
# agent_kb.tell('S', 2, 3)
# agent_kb.tell('S', 3, 2)
# print(agent_kb.is_there_stench(2, 1))
# print(agent_kb.is_there_not_wumpus(2,2))