import json
import uuid
from typing import List
import ast

def postprocess_output(output_str: str) -> List[dict]:
    if not output_str.lstrip().startswith("<functions>"):
        return []
    str_to_parse = output_str.split("<functions>")[1]
    list_of_str_to_parse = str_to_parse.splitlines() # TODO: need better way to handle jsonl format
    function_call_json = []
    try: # every function call has to be valid json
        for l in list_of_str_to_parse:
            try:
                fc = json.loads(l)
            except Exception as e:
                print(f"Json Loads Error: {e}")
                try:
                    fc = ast.literal_eval(l)
                except Exception as e1:
                    print(f"Load with AST Literal Eval Failed: {e1}")
                    fc = {}
            if type(fc["arguments"]) != str:
                fc["arguments"] = json.dumps(fc["arguments"])
            function_call_json.append(fc)
    except Exception as e:
        print(f"Error : {e}")
        
    res = []
    for fc in function_call_json:
        res.append({
            "id": uuid.uuid4().hex[:8],
            "function": fc,
            "type": "function",
        })
    return res

if __name__ == "__main__":
    # output_str = "<functions>{\"name\": \"calculate_distance\", \"arguments\": \"{\\\"origin\\\":\\\"San \\nFrancisco\\\",\\\"destination\\\":\\\"Cupertino\\\",\\\"mode\\\":\\\"drive\\\"}\"}\n{\"name\": \"calculate_distance\", \"arguments\": \"{\\\"origin\\\":\\\"San \\nFrancisco\\\",\\\"destination\\\":\\\"Cupertino\\\",\\\"mode\\\":\\\"air\\\"}\"}"
    output_str = '<functions>{"name": "calculate_distance", "arguments": {"origin": "San Francisco", "destination": "Cupertino", "mode": "driving"}}\n{"name": "calculate_distance", "arguments": {"origin": "San Francisco", "destination": "Cupertino", "mode": "air"}}'
    parsed_json = postprocess_output(output_str)
    if parsed_json:
        print(f"PARSED_JSON type: {type(parsed_json)}")
        print(parsed_json)
    else :
        print(output_str)