class Action:
    def __init__(self) -> None:
        self.position = (1, 1)
        self.direction = 'UP'
        self.actions = {'SHOOT': False, 'GRAB': False, 'CLIMB': False, 'MOVE_FORWARD': False, 'TURN_LEFT': False, 'TURN_RIGHT': False}

    def act(self, action):
        self.actions[action] = True
        if action == 'TURN_LEFT':
            self.turn_left()
        elif action == 'TURN_RIGHT':
            self.turn_right()
        elif action == 'MOVE_FORWARD':
            self.move_forward()
        elif action == 'CLIMB':
            if self.position == (1, 1):
                return True
            else:
                self.actions['CLIMB'] = False

    def turn_left(self):
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]

    def turn_right(self):
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        self.direction = directions[(directions.index(self.direction) + 3) % 4]

    def move_forward(self):
        if self.direction == 'UP' and self.position[0] < 10:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == 'DOWN' and self.position[0] > 1:
            self.position = (self.position[0] - 1, self.position[1])
        elif self.direction == 'LEFT' and self.position[1] > 1:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == 'RIGHT' and self.position[1] < 10:
            self.position = (self.position[0], self.position[1] + 1)

    def get_position(self):
        return self.position
    
    def get_direction(self):
        return self.direction
    
    def get_actions(self):
        return self.actions