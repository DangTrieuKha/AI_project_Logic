import timeit
from Agent_KB import AgentKB
from State import State

class Agent:
    def __init__(self, get_env_info, is_scream) -> None:
        self.state = State()
        self.get_env_info = get_env_info
        self.is_scream = is_scream
        self.kb = AgentKB()
        self.pending_position = {(1, 2)}
        self.pending_actions = []
        self.map_explored = [['-1' for _ in range(10)] for _ in range(10)]

    def update_map_explored(self, value):
        self.map_explored[self.state.position[1] - 1][10 - self.state.position[0]] = value
    
    def is_explored(self, x, y):
        return self.map_explored[y - 1][10 - x] == '0'

    def __depth_limited_search(self, start, goal, limit):
        if start == goal:
            return [start]
        
        if limit == 0:
            return None
        
        for neighbor in self.state.get_neighbors(start[0], start[1]):
            result = self.__depth_limited_search(neighbor, goal, limit - 1)
            if result is not None:
                result.append(start)
                return result
        
        return None
    
    def __iterative_deepening_search(self, start, goal):
        limit = 1
        while True:
            result = self.__depth_limited_search(start, goal, limit)
            if result is not None:
                return result
            limit += 1

    def __get_path(self, start, goal):
        return self.__iterative_deepening_search(start, goal)

    def __path_to_actions(self, path):
        actions = []
        for i in range(len(path) - 1):
            if path[i][0] == path[i + 1][0] and path[i][1] == path[i + 1][1] + 1:
                actions.append('MOVE_FORWARD')
            elif path[i][0] == path[i + 1][0] and path[i][1] == path[i + 1][1] - 1:
                actions.append('TURN_LEFT')
                actions.append('TURN_LEFT')
                actions.append('MOVE_FORWARD')
            elif path[i][0] == path[i + 1][0] + 1 and path[i][1] == path[i + 1][1]:
                actions.append('TURN_LEFT')
                actions.append('MOVE_FORWARD')
            elif path[i][0] == path[i + 1][0] - 1 and path[i][1] == path[i + 1][1]:
                actions.append('TURN_RIGHT')
                actions.append('MOVE_FORWARD')
        return actions

    def __evaluate_cost(self, list_actions):
        return 10 * len(list_actions)

    def run(self):
        if self.state.agent_health == 25:
            self.state.act('HEAL')
            return

        if self.pending_actions != []:
            self.state.act(self.pending_actions.pop(0))
            return

        tmp = self.get_env_info()
        if tmp == 'P_G':
            self.update_map_explored('-1')
        else:
            self.update_map_explored('0')

        self.kb.tell(tmp, self.state.position[0], self.state.position[1])

        if tmp == 'G':
            self.state.act('GRAB')
            return
        
        if 'S' not in tmp and 'B' not in tmp:
            self.state.act(self.state.get_next_action())
            return
        
        next, neighbors = self.state.get_forward_and_neighbors()
        if next is False:
            self.state.act('TURN_LEFT')
            return
        
        next_x, next_y = next

        if self.kb.is_there_wumpus(next_x, next_y):
            for neighbor in neighbors:
                if self.kb.is_there_not_pit(neighbor[0], neighbor[1]) and not self.is_explored(neighbor[0], neighbor[1]):
                    self.pending_position.add(neighbor)

            min_cost = 100
            min_actions = None
            for position in self.pending_position:
                path = self.__get_path(self.state.position, position)
                actions = self.__path_to_actions(path)
                cost = self.__evaluate_cost(actions)
                if cost < min_cost:
                    min_cost = cost
                    min_actions = actions
            if min_actions is not None:
                self.pending_actions = min_actions
                return

            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('SHOOT')
                if not self.is_scream():
                    self.pending_actions.append('MOVE_FORWARD')
                else:
                    self.pending_actions.append('SHOOT')
                self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
                return

        elif self.kb.is_there_not_wumpus(next_x, next_y):
            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('MOVE_FORWARD')
                return

            for neighbor in neighbors:
                if self.kb.is_there_not_pit(neighbor[0], neighbor[1]) and not self.is_explored(neighbor[0], neighbor[1]):
                    self.pending_position.add(neighbor)
            
            min_cost = 100
            min_actions = None
            for position in self.pending_position:
                path = self.__get_path(self.state.position, position)
                actions = self.__path_to_actions(path)
                cost = self.__evaluate_cost(actions)
                if cost < min_cost:
                    min_cost = cost
                    min_actions = actions
            if min_actions is not None:
                self.pending_actions = min_actions
                return

        else:
            if tmp == 'S':
                self.state.act('SHOOT')
                if not self.is_scream():
                    self.pending_actions.append('MOVE_FORWARD')
                else:
                    self.pending_actions.append('SHOOT')
                return
            
            if tmp == 'B':
                for neighbor in neighbors:
                    if self.kb.is_there_not_pit(neighbor[0], neighbor[1]) and not self.is_explored(neighbor[0], neighbor[1]):
                        self.pending_position.add(neighbor)

                min_cost = 100
                min_actions = None
                for position in self.pending_position:
                    path = self.__get_path(self.state.position, position)
                    actions = self.__path_to_actions(path)
                    cost = self.__evaluate_cost(actions)
                    if cost < min_cost:
                        min_cost = cost
                        min_actions = actions
                if min_actions is not None:
                    self.pending_actions = min_actions
                    return

            if tmp == 'W':
                for neighbor in neighbors:
                    if self.kb.is_there_not_pit(neighbor[0], neighbor[1]) and not self.is_explored(neighbor[0], neighbor[1]):
                        self.pending_position.add(neighbor)

                for position in self.pending_position:
                    path = self.__get_path(self.state.position, position)
                    actions = self.__path_to_actions(path)
                    cost = self.__evaluate_cost(actions)
                    if cost < min_cost:
                        min_cost = cost
                        min_actions = actions

            if tmp == 'G_L':
                # Implement logic to go around to grab the healing potion
                return
            
            if tmp == 'H_P':
                self.state.act('GRAB')
                return
            
            # Temporary logic to move forward
            self.state.act('MOVE_FORWARD')
            return

        path = self.__get_path(self.state.position, (1, 1))
        actions = self.__path_to_actions(path)
        self.pending_actions = actions
        self.pending_actions.append('CLIMB')