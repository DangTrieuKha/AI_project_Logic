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
        self.visited = {(1, 1)}    # = set(): Set of visited positions
        self.turn_count = 0

    def update_map_explored(self, value, x=None, y=None):
        if x is not None and y is not None:
            self.map_explored[10 - y][x - 1] = value
            return
        self.map_explored[10 - self.state.position[1]][self.state.position[0] - 1] = value
    
    def is_explored(self, x, y):
        return self.map_explored[10 - y][x - 1] == '0'
    
    def __is_cyclic(self, path):
        return len(path) != len(set(path))

    def __depth_limited_search(self, start, goal, limit):
        if start == goal:
            return [start]
        
        if limit == 0:
            return None
        
        for neighbor in self.state.get_neighbors(start[0], start[1]):
            if not self.is_explored(neighbor[0], neighbor[1]):
                continue
            result = self.__depth_limited_search(neighbor, goal, limit - 1)
            if result is not None:
                result.append(start)
                if not self.__is_cyclic(result):
                    return result
        
        return None
    
    def __iterative_deepening_search(self, start, goal):
        limit = 1
        while limit < 50:
            result = self.__depth_limited_search(start, goal, limit)
            if result is not None:
                return result
            limit += 1

    def __get_path(self, start, goal):
        # for line in self.map_explored:
        #     print(line)
        # print(self.pending_position)
        # print(start, goal)
        result = self.__iterative_deepening_search(start, goal)[::-1]
        # print(result)
        return result

    def __path_to_actions(self, path):
        actions = []
        current_direction = self.state.direction
        for i in range(len(path) - 1):
            if path[i][0] == path[i + 1][0]:
                if path[i][1] < path[i + 1][1]:
                    if current_direction == 'LEFT':
                        actions.append('TURN_RIGHT')
                    elif current_direction == 'RIGHT':
                        actions.append('TURN_LEFT')
                    elif current_direction == 'DOWN':
                        actions.append('TURN_RIGHT')
                        actions.append('TURN_RIGHT')
                    current_direction = 'UP'
                else:
                    if current_direction == 'LEFT':
                        actions.append('TURN_LEFT')
                    elif current_direction == 'RIGHT':
                        actions.append('TURN_RIGHT')
                    elif current_direction == 'UP':
                        actions.append('TURN_RIGHT')
                        actions.append('TURN_RIGHT')
                    current_direction = 'DOWN'
            else:
                if path[i][0] < path[i + 1][0]:
                    if current_direction == 'UP':
                        actions.append('TURN_RIGHT')
                    elif current_direction == 'DOWN':
                        actions.append('TURN_LEFT')
                    elif current_direction == 'LEFT':
                        actions.append('TURN_RIGHT')
                        actions.append('TURN_RIGHT')
                    current_direction = 'RIGHT'
                else:
                    if current_direction == 'UP':
                        actions.append('TURN_LEFT')
                    elif current_direction == 'DOWN':
                        actions.append('TURN_RIGHT')
                    elif current_direction == 'RIGHT':
                        actions.append('TURN_RIGHT')
                        actions.append('TURN_RIGHT')
                    current_direction = 'LEFT'
            actions.append('MOVE_FORWARD')
        return actions

    def __evaluate_cost(self, list_actions):
        return 10 * len(list_actions) if list_actions is not None else 10000

    def __climb_out(self):
        path = self.__get_path(self.state.position, (1, 1))
        actions = self.__path_to_actions(path)
        self.pending_actions = actions
        self.pending_actions.append('CLIMB')
        self.run()

    def move(self):
        if self.state.agent_health == 25:
            self.state.act('HEAL')
            return
        
        if self.is_scream():
            self.state.act('SHOOT')
            self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
            return

        if self.pending_actions != []:
            self.state.act(self.pending_actions.pop(0))
            return

        tmp = self.get_env_info()
        self.kb.tell(tmp, self.state.position[0], self.state.position[1])
        # # #[DEBUG ONLY, COMMENT OR DELETE WHEN DONE]
        print((self.state.position[0], self.state.position[1]), 'have percept: ', tmp )
        if self.kb.is_there_stench(self.state.position[0],self.state.position[1]):
            print((self.state.position[0],self.state.position[1]), 'have stench')
        else:
            print((self.state.position[0],self.state.position[1]), 'do not have stench')
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        for i in range(4):
            x = self.state.position[0] + dx[i]
            y = self.state.position[1] + dy[i]
            if x >= 1 and x <=10 and y >= 1 and y<= 10:
                if self.kb.is_there_stench(x,y):
                    print((x,y), 'have stench')
                else:
                    print((x,y), 'do not have stench')

                if self.kb.is_there_wumpus(x,y):
                    print((x,y), 'have wumpus')
                else:
                    print((x,y), 'do not have wumpus')

                if self.kb.is_there_pit(x,y):
                    print((x,y), 'have pit')
                else:
                    print((x,y), 'do not have pit')
                
                if self.kb.is_there_glow(x,y):
                    print((x,y), 'have glow')
                else:
                    print((x,y), 'do not have glow')
                
                if self.kb.is_there_healing(x,y):
                    print((x,y), 'have healing')
                else:
                    print((x,y), 'do not have healing')



        if 'P_G' in tmp:
            self.update_map_explored('-1')
        else:
            self.update_map_explored('0')
        
        if 'G' in tmp:
            self.state.act('GRAB')
            return
        
        next, neighbors = self.state.get_forward_and_neighbors()
        
        if next in self.visited:
            self.state.act('TURN_RIGHT')
            self.turn_count += 1
            if self.turn_count > 3:
                self.__climb_out()
            return
        else:
            self.turn_count = 0
        
        if 'S' not in tmp and 'B' not in tmp:
            self.state.act(self.state.get_next_action())
            for neighbor in neighbors:
                if self.is_explored(neighbor[0], neighbor[1]):
                    continue
                
                self.update_map_explored('0', neighbor[0], neighbor[1])

                if neighbor not in self.visited:
                    self.pending_position.add(neighbor)
            return
        
        next_x, next_y = next

        if self.kb.is_there_wumpus(next_x, next_y):
            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('SHOOT')
                self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
                self.pending_actions = ['MOVE_FORWARD']
                return

            if self.pending_position != set():
                position = list(self.pending_position)[-1]
                self.pending_position.remove(position)
                path = self.__get_path(self.state.position, position)
                actions = self.__path_to_actions(path)
                cost = self.__evaluate_cost(actions)

            if cost < 110:
                self.pending_actions = actions
                self.run()
                return
            else:
                self.state.act('SHOOT')
                self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
                self.pending_actions = ['MOVE_FORWARD']

        elif self.kb.is_there_not_wumpus(next_x, next_y):
            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('MOVE_FORWARD')
                return
            
            if self.pending_position != set():
                position = list(self.pending_position)[-1]
                self.pending_position.remove(position)
                path = self.__get_path(self.state.position, position)
                actions = self.__path_to_actions(path)
                cost = self.__evaluate_cost(actions)

                self.pending_actions = actions if actions is not None else []
                self.run()
                return
        else:
            if 'S' in tmp:
                self.state.act('SHOOT')
                self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
                self.pending_actions = ['MOVE_FORWARD']
                return
            
            if 'B' in tmp:
                if self.pending_position != set():
                    position = list(self.pending_position)[-1]
                    self.pending_position.remove(position)
                    path = self.__get_path(self.state.position, position)
                    actions = self.__path_to_actions(path)
                    cost = self.__evaluate_cost(actions)

                self.pending_actions = actions
                self.run()
                return

            if 'G_L' in tmp:
                # Implement logic to go around to grab the healing potion
                return
            
            if 'H_P' in tmp:
                self.state.act('GRAB')
                return
            
            # Temporary logic to move forward
            self.state.act('MOVE_FORWARD')
            return

    def update_visited(self):
        self.visited.add(self.state.position)
        if self.state.position in self.pending_position:
            self.pending_position.remove(self.state.position)

    def run(self):
        self.move()
        self.update_visited()