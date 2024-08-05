from Action import *
from Program import *
from Agent import *

def main():
    program = Program('map.txt', Action())
    agent = Agent(program.agent_action, program.get_env_info)
    while True:
        agent.run()
        if program.run() == "Finished":
            break

if __name__ == '__main__':
    main()