def AssignValue(message, value):
    if value is None:
        pass
    elif isinstance(value, str):
        message.string_value = value
    elif isinstance(value, int):
        message.long_value = value
    elif isinstance(value, bool):
        message.bool_value = value
    elif isinstance(value, float):
        message.double_value = value
    elif isinstance(value, list):
        for item in value:
            AssignValue(message.list_value.values.add(), item)
    elif isinstance(value, tuple):
        for item in value:
            AssignValue(message.tuple_value.values.add(), item)
    else:
        raise TypeError
    return message


def ExtractValue(message):
    if message.HasField("string_value"):
        return message.string_value
    elif message.HasField("long_value"):
        return message.long_value
    elif message.HasField("bool_value"):
        return message.bool_value
    elif message.HasField("double_value"):
        return message.double_value
    elif message.HasField("list_value"):
        return list(ExtractValue(value) for value in message.list_value.values)
    elif message.HasField("tuple_value"):
        return tuple(ExtractValue(value) for value in message.tuple_value.values)
