from State import *
from Program import *
from Agent import *

def main():
    program = Program('map.txt')
    agent = Agent(program.get_env_info)
    while True:
        agent.run()
        if program.run() == "Finished":
            break

if __name__ == '__main__':
    main()