from State import State

class Program:
    def __init__(self, map_file):
        self.map = self.load_map(map_file)
        self.update_percepts()
        self.agent_state = State()
        self.agent_score = 0
        self.scream = False # is there scream at current cell of agent
        self.result = []
    
    def load_map(self, map_file) -> list[list[list[str]]]:
        self.test_index = map_file.split('.')[0][-1]
        with open(map_file, 'r') as file:
            lines = file.readlines()
            n = int(lines[0])
            grid = []
            for line in lines[1:]:
                grid.append([cell.split(' ') for cell in line.strip().split('.')])
        return grid

    def update_percepts(self):
        # Update the map with percepts like Breeze, Stench, etc.
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if 'W' in self.map[i][j]:
                    self.add_stench(i, j)
                if  'P' in self.map[i][j]:
                    self.add_breeze(i, j)
                if 'P_G' in self.map[i][j]:
                    self.add_whiff(i, j)
                if 'H_P' in self.map[i][j]:
                    self.add_glow(i, j)

    def add_stench(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if '-' in self.map[i][j]:
                self.map[i][j][0] = 'S'
            elif 'S' not in self.map[i][j]:
                self.map[i][j].append('S')

    def add_breeze(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if '-' in self.map[i][j]:
                self.map[i][j][0] = 'B'
            elif 'B' not in self.map[i][j]:
                self.map[i][j].append('B')

    def add_whiff(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if '-' in self.map[i][j]:
                self.map[i][j][0] = 'W_H'
            elif 'W_H' not in self.map[i][j]:
                self.map[i][j].append('W_H')

    def add_glow(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if '-' in self.map[i][j]:
                self.map[i][j][0] = 'G_L'
            elif 'G_L' not in self.map[i][j]:
                self.map[i][j].append('G_L')

    def get_adjacent_cells(self, x, y) -> list[tuple[int, int]]:
        adjacent = []
        if x > 0:
            adjacent.append((x-1, y))
        if x < len(self.map) - 1:
            adjacent.append((x+1, y))
        if y > 0:
            adjacent.append((x, y-1))
        if y < len(self.map[x]) - 1:
            adjacent.append((x, y+1))
        return adjacent

    def get_env_info(self):
        # Return the percepts of the current cell
        x, y = self.agent_state.get_position()
        x_map = 10 - y
        y_map = x - 1
        return self.map[x_map][y_map]
    
    def update_map(self):
        x, y = self.agent_state.position
        x_map = 10 - y
        y_map = x - 1
        direction = self.agent_state.direction
        if self.agent_state.actions['GRAB']:
            adjacent = self.get_adjacent_cells(x_map,y_map)
            if 'H_P' in self.map[x_map][y_map]:
                self.map[x_map][y_map].remove('H_P')
                if self.map[x_map][y_map] == []:
                    self.map[x_map][y_map] = ['-']
                
                for i_x, i_y in adjacent:
                    if 'G_L' in self.map[i_x][i_y]:
                        adjacent_gl = self.get_adjacent_cells(i_x, i_y)
                        check_not_gl = True
                        for cell_x,cell_y in adjacent_gl:
                            if 'H_P' in self.map[cell_x][cell_y]:
                                check_not_gl = False
                        if check_not_gl:
                            self.map[i_x][i_y].remove('G_L')

                self.agent_state.agent_number_of_HL += 1
                return
            
            if 'G' in self.map[x_map][y_map]:
                self.map[x_map][y_map].remove('G')
                if self.map[x_map][y_map] == []:
                    self.map[x_map][y_map] = ['-']
                self.update_score(5000)
                return

        elif self.agent_state.actions['SHOOT']:
            if direction == 'UP':
                x_wumpus = x_map - 1
                y_wumpus = y_map
            elif direction == 'DOWN':
                x_wumpus = x_map + 1
                y_wumpus = y_map
            elif direction == 'LEFT':
                x_wumpus = x_map
                y_wumpus = y_map - 1
            elif direction == 'RIGHT':
                x_wumpus = x_map
                y_wumpus = y_map + 1
            
            if x_wumpus >= 0 and x_wumpus <= 9 and y_wumpus >=0 and y_wumpus <= 9:
                if 'W' in self.map[x_wumpus][y_wumpus]:
                    self.scream = True
                    self.map[x_wumpus][y_wumpus].remove('W')
                    adjacent = self.get_adjacent_cells(x_wumpus, y_wumpus)
                    for i_x, i_y in adjacent:
                        if 'S' in self.map[i_x][i_y]:
                            adjacent_stench = self.get_adjacent_cells(i_x,i_y)
                            check_not_wumpus = True
                            for cell_x,cell_y in adjacent_stench:
                                if 'W' in self.map[cell_x][cell_y]:
                                    check_not_wumpus = False
                            if check_not_wumpus:
                                self.map[i_x][i_y].remove('S')

                        if self.map[i_x][i_y] == []:
                            self.map[i_x][i_y] = ['-']

                    if self.map[x_wumpus][y_wumpus] == []:
                        self.map[x_wumpus][y_wumpus] = ['-']

    
    def is_scream(self):
        return self.scream
    
    def update_score(self, value):
        self.agent_score += value
    
    def get_score(self):
        return self.agent_score

    def end_game(self):
        print(f"Game End! Score: {self.agent_score}")
        with open(f"result{self.test_index}.txt", 'w') as file:
            output = '\n'.join(self.result)
            file.write(output)
        return "Finished"

    def run(self):
        self.scream = False
        actions = self.agent_state.get_actions()
        if actions['CLIMB']:
            self.update_score(10)
            return self.end_game()
        elif actions['MOVE_FORWARD']:
            self.update_score(-10)
            self.agent_state.actions['MOVE_FORWARD'] = False
        elif actions['SHOOT']:
            self.update_score(-100)
            self.update_map()
            self.agent_state.actions['SHOOT'] = False
        elif actions['GRAB']:
            self.update_score(-10)
            self.update_map()
            self.agent_state.actions['GRAB'] = False
        elif actions['TURN_LEFT']:
            self.update_score(-10)
            self.agent_state.actions['TURN_LEFT'] = False
        elif actions['TURN_RIGHT']:
            self.update_score(-10)
            self.agent_state.actions['TURN_RIGHT'] = False
        
        self.result.append(f"Position: {self.agent_state.get_prev_position()}, Direction: {self.agent_state.get_direction()}, Actions: {[action for action, value in actions.items() if value][0]}, Score: {self.agent_score}")

        x, y = self.agent_state.get_position()

        if 'W' in self.map[10 - y][x - 1] or 'P' in self.map[10 - y][x - 1]:
            self.update_score(-10000)
            return self.end_game()
        
        if 'P_G' in self.map[10 - y][x - 1]:
            self.agent_state.poison()
        
        return False