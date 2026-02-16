from modules.planner import BasePlannerNode, DRAFTER, END


class ReflectionNode(BasePlannerNode):

    prompt = """
    You are an AI-agent specialized in programming. Your job is to evaluate
    the proposed system design, whether you accept or not. You need to be
    critical, straight to the point, and objective. You DO NOT need to write
    any code, just explain.
    
    If you approve the design answer "ACCEPTED".
    Otherwise, explain what classes are missing (if any) or some valuable
    tips to improve the design.
    """

    def __init__(self, llm):
        super().__init__(llm)

    def build_plan_dict_query(self, state):
        name = state.plan_dict['module_name']
        plan_query_str = f"I am thinking about my module named '{name}'."
        plan_query_str += "This module would have a:\n"

        for class_name, class_info in state.plan_dict['classes'].items():
            desc = class_info['description']
            relation = class_info['relationship']
            plan_query_str += f"\t- '{class_name}': {desc}. {relation}\n"

        return plan_query_str

    def run(self, state):
        messages = [
            {"role": "system", "content": ReflectionNode.prompt},
            {"role": "user", "content": state.user_input},
            {"role": "user", "content": self.build_plan_dict_query(state)}
        ]

        response = self._llm.chat(messages)
        state.last_reflection_response = response

        ## if the draft seems ok
        if "accepted" in response.lower():
            state.plan_approved = True
            state.next_node = END
        else:
            state.reflection_retry += 1
            state.next_node = DRAFTER

            ## add the plan feedback as user message
            state.messages.append(
                {"role": "user", "content": response}
            )

        return state
