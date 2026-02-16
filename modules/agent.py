from pathlib import Path
from modules.utils.misc import c


class Agent:

    user_greeting = "I am a coder AI-agent, please specify your " \
    "code description, requirements and I will do my best to write " \
    "it for you"

    def __init__(self, planner, coder, reviewer, output_folder):
        self.__output_folder = Path(output_folder)
        self.__states_output_folder = self.__output_folder / "states"
        self.__planner = planner
        self.__coder = coder
        self.__reviewer = reviewer

    def run(self):
        print(f"{c('System', 'red')}: {Agent.user_greeting}")
        user_input = input(f"{c('User', 'cyan')}: ")

        planner_state = self.__planner.run(
            user_input, self.__states_output_folder)

        print("Finished!")
