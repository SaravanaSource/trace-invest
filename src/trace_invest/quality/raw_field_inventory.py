from typing import Dict


def build_raw_field_inventory(raw: Dict) -> Dict:
    """
    Collects all field/column names inside each raw block.
    Used to discover unused potential signals.
    """

    inventory = {}

    for section, block in raw.items():
        fields = {}

        if isinstance(block, dict):
            for k, v in block.items():
                fields[k] = type(v).__name__

        elif isinstance(block, list):
            if block and isinstance(block[0], dict):
                for k, v in block[0].items():
                    fields[k] = type(v).__name__

        inventory[section] = fields

    return inventory

