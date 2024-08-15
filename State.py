class State:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(State, cls).__new__(cls)
            cls.__instance.__init__()
        return cls.__instance

    def __init__(self) -> None:
        self.position = (1, 1)
        self.direction = 'UP'
        self.actions = {'SHOOT': False, 'GRAB': False, 'CLIMB': False, 'MOVE_FORWARD': False, 'TURN_LEFT': False, 'TURN_RIGHT': False, 'HEAL':False}
        self.agent_health = 100
        self.agent_number_of_HL = 0 # the number of healing poison that belongs to agent

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
        elif action == 'HEAL':
            if self.agent_number_of_HL > 0:
                self.healing()
            else:
                self.actions['HEAL'] = False
        elif action == 'GRAB':
            self.agent_number_of_HL += 1

    def healing(self):
        self.agent_health += 25
        self.agent_number_of_HL -=1
        
    def turn_left(self):
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        self.direction = directions[(directions.index(self.direction) + 1) % 4]

    def turn_right(self):
        directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        self.direction = directions[(directions.index(self.direction) + 3) % 4]

    def get_forward_location(self):
        if self.direction == 'UP' and self.position[1] < 10:
            return (self.position[0], self.position[1] + 1)
        elif self.direction == 'DOWN' and self.position[1] > 1:
            return (self.position[0], self.position[1] - 1)
        elif self.direction == 'LEFT' and self.position[0] > 1:
            return (self.position[0] - 1, self.position[1])
        elif self.direction == 'RIGHT' and self.position[0] < 10:
            return (self.position[0] + 1, self.position[1])
        else:
            return False

    def get_forward_and_neighbors(self):
        next_location = self.get_forward_location()
        neighbors = []
        if self.position[1] < 10 and (self.position[0], self.position[1] + 1) != next_location:
            neighbors.append((self.position[0], self.position[1] + 1))
        if self.position[1] > 1 and (self.position[0], self.position[1] - 1) != next_location:
            neighbors.append((self.position[0], self.position[1] - 1))
        if self.position[0] > 1 and (self.position[0] - 1, self.position[1]) != next_location:
            neighbors.append((self.position[0] - 1, self.position[1]))
        if self.position[0] < 10 and (self.position[0] + 1, self.position[1]) != next_location:
            neighbors.append((self.position[0] + 1, self.position[1]))
        return next_location, neighbors
    
    def get_neighbors(self):
        neighbors = []
        if self.position[1] < 10:
            neighbors.append((self.position[0], self.position[1] + 1))
        if self.position[1] > 1:
            neighbors.append((self.position[0], self.position[1] - 1))
        if self.position[0] > 1:
            neighbors.append((self.position[0] - 1, self.position[1]))
        if self.position[0] < 10:
            neighbors.append((self.position[0] + 1, self.position[1]))
        return neighbors
    
    def get_next_action(self):
        if self.get_forward_location() != False:
            return 'MOVE_FORWARD'
        else:
            return 'TURN_RIGHT'

    def move_forward(self):
        if self.direction == 'UP' and self.position[1] < 10:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == 'DOWN' and self.position[1] > 1:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.direction == 'LEFT' and self.position[0] > 1:
            self.position = (self.position[0] - 1, self.position[1])
        elif self.direction == 'RIGHT' and self.position[0] < 10:
            self.position = (self.position[0] + 1, self.position[1])
        else:
            return False

    def get_position(self):
        return self.position
    
    def get_direction(self):
        return self.direction
    
    def get_actions(self):
        return self.actions
    
    def get_health(self):
        return self.agent_health
    
    def get_number_of_HL(self):
        return self.agent_number_of_HL