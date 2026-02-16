from langgraph.graph import StateGraph, END as GRAPH_END, START as GRAPH_START

from modules.planner import PlannerState, DRAFTER, PARSER, REFLECTION, END
from modules.planner import DrafterNode, ParserNode, ReflectionNode

from modules.utils.misc import save_state, load_state


class PlannerGraph:

    def __init__(self, llm, parse_lim=10, reflection_lim=5):
        self.__llm = llm
        self.__parse_lim = parse_lim
        self.__reflection_lim = reflection_lim
        self._graph = self.__build()

    def __route(self, state):
        return state.next_node

    def __build(self):
        graph = StateGraph(PlannerState)

        ## draft node
        graph.add_node(DRAFTER, DrafterNode(
            self.__llm, self.__parse_lim, self.__reflection_lim))

        ## parse draft into json
        graph.add_node(PARSER, ParserNode(self.__llm))

        ## reflection about draft
        graph.add_node(REFLECTION, ReflectionNode(self.__llm))

        ## parse right after draft
        graph.add_edge(DRAFTER, PARSER)

        graph.add_conditional_edges(
            GRAPH_START,
            self.__route,
            {
                DRAFTER: DRAFTER,
                PARSER: PARSER,
                REFLECTION: REFLECTION,
                END: GRAPH_END,
            }
        )

        ## whether to draft again or reflect about plan
        graph.add_conditional_edges(
            PARSER,
            self.__route,
            {
                DRAFTER: DRAFTER,
                REFLECTION: REFLECTION
            }
        )

        ## whether to draft again or accept plan
        graph.add_conditional_edges(
            REFLECTION,
            self.__route,
            {
                DRAFTER: DRAFTER,
                END: GRAPH_END
            }
        )

        graph = graph.compile()

        return graph

    def run(self, user_input, output_folder):
        output_path = output_folder / "planner.json"

        if output_path.exists():
            state = load_state(output_path)
        else:
            state = PlannerState(
                user_input=user_input, output_path=str(output_path))

        ## invoke the graph
        final_state = self._graph.invoke(state)

        return final_state
