# Based on https://github.com/kpn-iot/senml-python-library


def map_senml_fields(entry):
    fields = {
        "u": ("unit", "unknown"),
        "v": ("value", 0),
        "vs": (
            "value",
            None,
        ),  # Use None to indicate absence if 'sv' is not present
        "vb": (
            "value",
            None,
        ),  # Use None to indicate absence if 'vb' is not present
        "vd": ("value", None),
    }

    result = {}

    for k in fields:  # Iterate over keys in the fields mapping dictionary
        if k in entry:  # Check if the key is present in the input entry
            # If key is present, add the mapped key with its actual value or default value to the result dictionary
            result[fields[k][0]] = entry.get(k, fields[k][1])

    return result


def convert_senML_dict(data):
    converted_data: list[dict] = []
    current_base: dict = {}
    for entry in data:
        if "bn" in entry:
            if current_base is not None:
                converted_data.append(current_base)
            current_base = {entry["bn"]: {}}
        else:
            current_base[next(iter(current_base))][entry["n"]] = map_senml_fields(entry)

    if current_base is not None:
        converted_data.append(current_base)

    return converted_data


def senml_package_type(data: dict) -> int:
    val = next(iter(data.values()))
    return 1 if val == {} else 0


class SenmlBase(object):
    """
    the base class for all senml objects.
    """
