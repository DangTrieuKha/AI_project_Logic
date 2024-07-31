class Program:
    def __init__(self, map_file):
        self.map = self.load_map(map_file)
        self.update_percepts()

    def load_map(self, map_file):
        with open(map_file, 'r') as file:
            size = int(file.readline().strip())
            grid = []
            for _ in range(size):
                line = file.readline().strip().split('.')
                grid.append(line)
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

    def get_cell_info(self, x, y):
        return self.map[x][y]
