class Program:
    def __init__(self, map_file, agent_action):
        self.map = self.load_map(map_file)
        self.update_percepts()
        self.agent_action = agent_action
        self.agent_score = 0

    def load_map(self, map_file):
        with open(map_file, 'r') as file:
            lines = file.readlines()
            grid = []
            for line in lines:
                grid.append(line.strip().split('.'))
        return grid

    def update_percepts(self):
        # Update the map with percepts like Breeze, Stench, etc.
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'W':
                    self.add_stench(i, j)
                elif self.map[i][j] == 'P':
                    self.add_breeze(i, j)
                elif self.map[i][j] == 'P_G':
                    self.add_whiff(i, j)
                elif self.map[i][j] == 'H_P':
                    self.add_glow(i, j)

    def add_stench(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if self.map[i][j] == '-':
                self.map[i][j] = 'S'
            elif 'S' not in self.map[i][j]:
                self.map[i][j] += 'S'

    def add_breeze(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if self.map[i][j] == '-':
                self.map[i][j] = 'B'
            elif 'B' not in self.map[i][j]:
                self.map[i][j] += 'B'

    def add_whiff(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if self.map[i][j] == '-':
                self.map[i][j] = 'W'
            elif 'W' not in self.map[i][j]:
                self.map[i][j] += 'W'

    def add_glow(self, x, y):
        for i, j in self.get_adjacent_cells(x, y):
            if self.map[i][j] == '-':
                self.map[i][j] = 'G_L'
            elif 'G_L' not in self.map[i][j]:
                self.map[i][j] += 'G_L'

    def get_adjacent_cells(self, x, y):
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
        return self.map[self.agent_action.get_position()[0]][self.agent_action.get_position()[1]]
    
    def update_map(self):
        x,y = self.agent_action.position
        x_map = 10 - x
        y_map = y - 1
        direction = self.agent_action.direction
        if self.agent_action.actions['GRAB']:
            adjacent = self.get_adjacent_cells(x_map,y_map)
            if 'H_P' in self.map[x_map][y_map]:
                self.map[x_map][y_map].remove('H_P')
            for i,j in adjacent:
                if 'G_L' in self.map[x_map][y_map]:
                    self.map[x_map][y_map].remove('G_L')
        elif self.agent_action.actions['SHOOT']:
            if direction == 'UP':
                x_wumpus = x_map
                y_wumpus = y_map - 1
            elif direction == 'DOWN':
                x_wumpus = x_map
                y_wumpus = y_map + 1
            elif direction == 'LEFT':
                x_wumpus = x_map - 1
                y_wumpus = y_map
            elif direction == 'RIGHT':
                x_wumpus = x_map + 1
                y_wumpus = y_map
            
            if x_wumpus >= 0 and x_wumpus <= 9 and y_wumpus >=0 and y_wumpus <= 9:
                if 'W' in self.map[x_wumpus][y_wumpus]:
                    self.map[x_wumpus][y_wumpus].remove('W')
                adjacent = self.get_adjacent_cells(x_wumpus, y_wumpus)
                for i,j in adjacent:
                    if 'S' in self.map[i][j]:
                        self.map[i][j].remove('S')
        


            



    def update_score(self, value):
        self.agent_score += value

    def end_game(self):
        print(f"Game End! Score: {self.agent_score}")
        return "Finished"

    def run(self):
        actions = self.agent_action.get_actions()
        if actions['CLIMB']:
            self.update_score(10)
            return self.end_game()
        elif actions['MOVE_FORWARD']:
            self.update_score(-10)
        elif actions['SHOOT']:
            self.update_score(-100)
            self.update_map()
            #self.update_percepts()
        elif actions['GRAB']:
            self.update_score(-10)
            if self.map[self.agent_action.get_position()[0]][self.agent_action.get_position()[1]] == 'G':
                self.update_score(5000)
            self.update_map()
            #self.update_percepts()
        elif actions['TURN_LEFT']:
            self.update_score(-10)
        elif actions['TURN_RIGHT']:
            self.update_score(-10)

        return False