import timeit

class Agent:
    def __init__(self, action, get_env_info) -> None:
        self.action = action
        self.get_env_info = get_env_info

    def run(self):
        tmp = self.get_env_info()

        # Logic for the agent to make decisions
        # if tmp == '':
        #     self.action.act('MOVE_FORWARD')

        self.action.act('CLIMB')