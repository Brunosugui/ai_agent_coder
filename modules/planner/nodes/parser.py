import json

from modules.planner import BasePlannerNode, REFLECTION, DRAFTER


class ParserNode(BasePlannerNode):

    first_keys = ["module_name", "classes"]
    sec_keys = ["description", "relationship"]

    def __init__(self, llm):
        super().__init__(llm)
    
    def run(self, state):
        response = state.last_draft

        json_start = response.find("{")
        json_end = response.rfind("}")

        if json_start != -1 and json_end != -1:
            try:
                parsed = json.loads(response[json_start: json_end + 1])

                ## checks if the json contains the keys $first_keys
                if any(
                    k not in parsed.keys()
                    for k in ParserNode.first_keys):
                    raise KeyError(
                        f"Could not find {'/'.join(ParserNode.first_keys)}")

                ## checks if for each of the 'classes' contains the $sec_keys
                for class_name, class_info in parsed["classes"].items():
                    if any(
                        k not in class_info.keys()
                        for k in ParserNode.sec_keys):
                        raise KeyError(
                            f"Could not find key {'/'.join(ParserNode.sec_keys)}"\
                            f" for class {class_name}")

                ## parse succeed setup
                state.plan_dict = parsed
                state.parse_retry = 0
                state.next_node = REFLECTION

            except Exception as e:
                state.parse_retry += 1
                state.next_node = DRAFTER
                state.messages.append(
                    {
                        "role": "user",
                        "content": f"""
                        Failed to parse JSON format: {e}
                        Correct the format."""
                    }
                )

        else:
            state.parse_retry += 1
            state.next_node = DRAFTER
            state.messages.append(
                {
                    "role": "user",
                    "content": "Could not find the JSON format. Correct your answer."
                }
            )
        return state