from modules.planner import BasePlannerNode, PARSER


class DrafterNode(BasePlannerNode):

    prompt = """
    You are an AI-agent specialized in programming. The user will request
    some complex system for you to program. Your job is to PLAN the main
    classes and their relationship so that another agent will be in charge
    of writing the respective code.

    Important rules to follow:
    - Be objective and direct;
    - Think about modularity and scalability;
    - Your answer MUST be formated as a valid JSON;

    JSON example:
    {
        "module_name": "description of the module",
        "classes": {
            "First Class": {
                "description": "Detailed description of the class",
                "relationship": "the relationship between this class and the others",
            },
            "Second Class": {
                "description": "Detailed description of the class",
                "relationship": "the relationship between this class and the others",
            },
            ...
            "N-th Class": {
                "description": "Detailed description of the class",
                "relationship": "the relationship between this class and the others",
            },
        }
    }

    Remember to answer ONLY A JSON-LIKE STRING.
    """

    def __init__(self, llm, parse_lim, reflection_lim):
        super().__init__(llm)
        self.__parse_lim = parse_lim
        self.__reflection_lim = reflection_lim

    def run(self, state):

        ## failed to parse and did not get to reflection yet
        if state.parse_retry == self.__parse_lim and \
                len(state.plan_dict) == 0:
            state.messages = []
        
        ## failed to parse or failed reflection after achieving reflection
        if state.parse_retry == self.__parse_lim or \
            state.reflection_retry == self.__reflection_lim and \
                len(state.plan_dict) > 0:
            ## clear messages a little, leave only the most relevant
            state.messages = [
                {"role": "system", "content": DrafterNode.prompt},
                {"role": "user", "content": state.user_input},
                {"role": "assistant", "content": str(state.plan_dict)},
                {"role": "user", "content": state.last_reflection}
            ]

        ## first interaction
        if len(state.messages) == 0:
            state.messages.append(
                {"role": "system", "content": DrafterNode.prompt}
            )
            state.messages.append(
                {"role": "user", "content": state.user_input}
            )

        response = self._llm.chat(state.messages)

        ## store raw llm response for parsing
        state.last_draft = response
        state.next_node = PARSER

        ## add to the memory
        state.messages.append(
            {"role": "assistant", "content": response}
        )

        return state
