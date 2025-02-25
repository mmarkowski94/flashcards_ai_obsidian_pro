import json


def parse_output_to_json(raw_output: str) -> list:
    if raw_output.startswith("```json"):
        raw_output = raw_output[8:]

    if raw_output.endswith("```"):
        raw_output = raw_output[:-3]

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {e}")