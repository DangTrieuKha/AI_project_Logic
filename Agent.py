import timeit
from Agent_KB import AgentKB
from State import State

class Agent:
    def __init__(self, get_env_info) -> None:
        self.state = State()
        self.get_env_info = get_env_info
        self.kb = AgentKB()
        self.pending_position = {(1, 2)}
        self.pending_action = ''
        self.map_explored = [['-1' for _ in range(10)] for _ in range(10)]

    def evaluate_cost(self, path):
        pass

    def run(self):
        if self.state.agent_health == 25:
            self.state.act('HEAL')
            return

        if self.pending_action != '':
            self.state.act(self.pending_action)
            self.pending_action = ''
            return

        tmp = self.get_env_info()
        if tmp == 'P_G':
            self.map_explored[self.state.position[0]][self.state.position[1]] = '-1'
        else:
            self.map_explored[self.state.position[0]][self.state.position[1]] = '0'

        self.kb.tell(tmp, self.state.position[0], self.state.position[1])

        if 'S' not in tmp and 'B' not in tmp:
            self.state.act('MOVE_FORWARD')
            return
        
        (next_x, next_y), neighbors = self.state.get_forward_and_neighbors()
        if self.kb.is_there_wumpus(next_x, next_y):
            for neighbor in neighbors:
                if self.kb.is_there_not_pit(neighbor[0], neighbor[1]):
                    self.pending_position.add(neighbor)

            for position in self.pending_position:
                # Implement logic to compare the cost of the path and choose the best one
                pass

            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('SHOOT')
                # if not is_scream:
                self.pending_action = 'MOVE_FORWARD'
                self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
                return

        elif self.kb.is_there_not_wumpus(next_x, next_y):
            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('MOVE_FORWARD')
                return

            for neighbor in neighbors:
                if self.kb.is_there_not_pit(neighbor[0], neighbor[1]):
                    self.pending_position.add(neighbor)
            
            for position in self.pending_position:
                # Implement logic to compare the cost of the path and choose the best one
                pass

        else:
            if tmp == 'S':
                self.state.act('SHOOT')
                # if not is_scream:
                self.pending_action = 'MOVE_FORWARD'
                return
            
            if tmp == 'B':
                for neighbor in neighbors:
                    if self.kb.is_there_not_pit(neighbor[0], neighbor[1]):
                        self.pending_position.add(neighbor)

                for position in self.pending_position:
                    # Implement logic to compare the cost of the path and choose the best one
                    pass

            if tmp == 'W':
                for neighbor in neighbors:
                    if self.kb.is_there_not_pit(neighbor[0], neighbor[1]):
                        self.pending_position.add(neighbor)

                for position in self.pending_position:
                    # Implement logic to compare the cost of the path and choose the best one
                    pass

            if tmp == 'G_L':
                # Implement logic to go around to grab the healing potion
                return
            
            if tmp == 'H_P':
                self.state.act('GRAB')
                return
            
            # Temporary logic to move forward
            self.state.act('MOVE_FORWARD')
            return

        # Find path to (1, 1) and climb
        self.state.act('CLIMB')