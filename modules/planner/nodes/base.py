from abc import ABC, abstractmethod
from modules.utils.misc import save_state


class BasePlannerNode(ABC):

    def __init__(self, llm):
        self._llm = llm

    def __call__(self, state):
        if state.next_node == self.__class__.__name__:
            state = self.run(state)
            save_state(state, state.output_path)
        else:
            error_msg = f"""
            Looks like something is wrong with node mapping
            state.next_node = {state.next_node}
            self.__class__.__name__ = {self.__class__.__name__}
            """
            raise KeyError(error_msg)
        return state

    @abstractmethod
    def run(self, state):
        raise NotImplementedError

