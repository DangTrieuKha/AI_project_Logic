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
        self.visited = {(1, 1)}
        self.turn_count = 0
        self.prev_action = None

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
        return None

    def __get_path(self, start, goal):
        result = self.__iterative_deepening_search(start, goal)
        if result is not None:
            result.reverse()
        return result

    def __path_to_actions(self, path):
        if path is None:
            return []
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

    def __climb_out(self):
        path = self.__get_path(self.state.position, (1, 1))
        actions = self.__path_to_actions(path)
        self.pending_actions = actions
        self.pending_actions.append('CLIMB')
        self.run()

    def __move_to_safe_position(self):
        if self.pending_position != set():
            position = list(self.pending_position)[-1]
            self.pending_position.remove(position)
            path = self.__get_path(self.state.position, position)
            actions = self.__path_to_actions(path)
            self.pending_actions = actions
            self.run()
            return True
        
        return False
        
    def __add_safe_position(self, neighbors):
        for neighbor in neighbors:
            if self.is_explored(neighbor[0], neighbor[1]):
                continue
            if self.kb.is_there_poison(neighbor[0], neighbor[1]) or not self.kb.is_there_not_poison(neighbor[0], neighbor[1]):
                continue
            self.update_map_explored('0', neighbor[0], neighbor[1])
            if neighbor not in self.visited:
                self.pending_position.add(neighbor)

    def move(self):
        next, neighbors = self.state.get_forward_and_neighbors()
        
        if self.is_scream():
            self.state.act('SHOOT')
            self.prev_action = 'SHOOT'
            self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
            if 'S' not in self.get_env_info():
                while self.kb.is_there_wumpus(next[0], next[1]):
                    self.kb.assertNoWumpusPostShoot(next[0], next[1])
            return
        elif self.prev_action == 'SHOOT':
            self.prev_action = None
            while self.kb.is_there_wumpus(next[0], next[1]):
                self.kb.assertNoWumpusPostShoot(next[0], next[1])

        tmp = self.get_env_info()
        self.kb.tell(tmp, self.state.position[0], self.state.position[1])

        if self.state.agent_health == 25 and 'W_H' in tmp:
            self.state.act('HEAL')
            return

        self.update_map_explored('0')

        if 'W_H' in tmp:
            if self.kb.is_there_poison(next[0], next[1]):
                self.visited.add(next)

        if self.pending_actions != []:
            if 'S' not in tmp and 'B' not in tmp:
                self.__add_safe_position(neighbors)
            if 'G' in tmp or 'H_P' in tmp:
                self.state.act('GRAB')
                if 'H_P' in tmp:
                    self.prev_action = 'GRAB_H_P'
                return
            self.state.act(self.pending_actions.pop(0))
            return
        
        if 'G' in tmp or 'H_P' in tmp:
            self.state.act('GRAB')
            if 'H_P' in tmp:
                self.prev_action = 'GRAB_H_P'
            return
        
        if self.prev_action == 'GRAB_H_P':
            self.prev_action = None
            while self.kb.is_there_healing(self.state.position[0], self.state.position[1]):
                self.kb.assertNoHealingPostGrab(self.state.position[0], self.state.position[1])
        
        if next == False:
            self.state.act('TURN_RIGHT')
            return
        elif next in self.visited:
            if self.__move_to_safe_position():
                return
            
            self.turn_count += 1
            if self.turn_count > 3:
                self.__climb_out()
            else:
                self.state.act('TURN_RIGHT')
            return
        else:
            self.turn_count = 0

        if 'S' not in tmp and 'B' not in tmp:
            self.state.act('MOVE_FORWARD')
            self.__add_safe_position(neighbors)
            return
        
        next_x, next_y = next

        if self.kb.is_there_wumpus(next_x, next_y):
            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('SHOOT')
                self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
                self.pending_actions = ['MOVE_FORWARD']
                return

            if self.__move_to_safe_position():
                return

        elif self.kb.is_there_not_wumpus(next_x, next_y):
            if self.kb.is_there_not_pit(next_x, next_y):
                self.state.act('MOVE_FORWARD')
                return
            
            if self.__move_to_safe_position():
                return
        else:
            if 'B' in tmp:
                if self.__move_to_safe_position():
                    return
                
            if 'S' in tmp:
                self.state.act('SHOOT')
                self.kb.tell(self.get_env_info(), self.state.position[0], self.state.position[1])
                self.pending_actions = ['MOVE_FORWARD']
                return

        self.__climb_out()

    def update_visited(self):
        self.visited.add(self.state.position)
        for cell in self.visited:
            self.pending_position.discard(cell)

    def run(self):
        self.move()
        self.update_visited()