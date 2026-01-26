from typing import Dict


def inspect_raw_schema(raw: Dict) -> Dict:
    """
    Structural view of raw fundamentals.
    Shows type and immediate keys for each section.
    """

    schema = {
        "top_level_keys": list(raw.keys()),
        "sections": {}
    }

    for key, value in raw.items():
        section_info = {
            "type": type(value).__name__
        }

        if isinstance(value, dict):
            section_info["keys"] = list(value.keys())

        elif isinstance(value, list):
            section_info["length"] = len(value)
            if value and isinstance(value[0], dict):
                section_info["sample_keys"] = list(value[0].keys())

        schema["sections"][key] = section_info

    return schema

