import re
from typing import Any, Dict, Union

ParsedJson = Dict[str, Any]

class ParseOptions:
    def __init__(self, has_null: bool = False):
        self.has_null = has_null

class FaultyJson:
    def __init__(self, faulty_json_string: str, parsed_json: ParsedJson):
        self.faulty_json_string = faulty_json_string
        self.parsed_json = parsed_json

def parse_partial_json(json_string: str, options: ParseOptions = ParseOptions()) -> ParsedJson:
    pattern = r'"([^"]+)":\s*(?:"([^"]*)"|(\d+)|true|false|null|undefined|\[|\{|\s*"?([^",\]}]*))?'
    matches = re.findall(pattern, json_string)
    result: ParsedJson = {}

    for match in matches:
        key = match[0]
        value = None

        if match[1]:
            value = match[1]
        elif match[2]:
            value = int(match[2])
        elif f'{key}: true' in json_string:
            value = True
        elif f'{key}: false' in json_string:
            value = False
        elif f'{key}: null' in json_string:
            value = None if options.has_null else None
        elif f'{key}: undefined' in json_string:
            value = None
        elif match[3]:
            value = match[3]

        result[key] = value

    return result

def log_faulty_json(json_string: str, parsed_json: ParsedJson) -> None:
    print(f"Warning: Faulty JSON string encountered: {json_string}")

def parse_partial_json_with_logging(json_string: str, options: ParseOptions = ParseOptions()) -> Union[ParsedJson, FaultyJson]:
    try:
        return parse_partial_json(json_string, options)
    except Exception as e:
        log_faulty_json(json_string, {})
        return FaultyJson(faulty_json_string=json_string, parsed_json={})
