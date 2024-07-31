class Agent:
    def __init__(self, program):
        self.program = program
        self.position = (0, 0)
        self.direction = 'UP'
        self.score = 0
        self.path = []

    def move_forward(self):
        x, y = self.position
        if self.direction == 'UP' and x > 0:
            x -= 1
        elif self.direction == 'DOWN' and x < len(self.program.map) - 1:
            x += 1
        elif self.direction == 'LEFT' and y > 0:
            y -= 1
        elif self.direction == 'RIGHT' and y < len(self.program.map[x]) - 1:
            y += 1
        self.position = (x, y)
        self.path.append((x, y))
        self.update_score(-10)

    def turn_left(self):
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]

    def turn_right(self):
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        self.direction = directions[(directions.index(self.direction) - 1) % 4]

    def grab(self):
        x, y = self.position
        cell_info = self.program.get_cell_info(x, y)
        if 'G' in cell_info:
            self.update_score(5000)
            self.program.map[x][y] = self.program.map[x][y].replace('G', '')

    def shoot(self):
        self.update_score(-100)
        # Implement shooting logic

    def climb(self):
        if self.position == (0, 0):
            self.update_score(10)
            self.end_game()

    def heal(self):
        x, y = self.position
        cell_info = self.program.get_cell_info(x, y)
        if 'H_P' in cell_info:
            self.update_score(10)
            self.program.map[x][y] = self.program.map[x][y].replace('H_P', '')

    def update_score(self, points):
        self.score += points

    def end_game(self):
        print(f"Game over! Final score: {self.score}")
        print(f"Path taken: {self.path}")

    def run(self):
        # Implement logic for agent's actions based on percepts and knowledge
        pass
