from State import *
from Program import *
from Agent import *

def main():
    program = Program('input1.txt')
    print(program.map)
    agent = Agent(program.get_env_info, program.is_scream)
    while True:
        agent.run()
        if program.run() == "Finished":
            break

if __name__ == '__main__':
    main()