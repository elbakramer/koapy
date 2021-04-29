def convert_arguments_from_protobuf_to_python(arguments):
    args = []
    for argument in arguments:
        if argument.HasField("string_value"):
            args.append(argument.string_value)
        elif argument.HasField("long_value"):
            args.append(argument.long_value)
        elif argument.HasField("bool_value"):
            args.append(argument.bool_value)
        else:
            raise ValueError("No expecting field found.")
    return args


def convert_arguments_from_python_to_protobuf(arguments, arguments_message):
    for i, arg in enumerate(arguments):
        if isinstance(arg, str):
            arguments_message.add().string_value = arg  # pylint: disable=no-member
        elif isinstance(arg, int):
            arguments_message.add().long_value = arg  # pylint: disable=no-member
        elif isinstance(arg, bool):
            arguments_message.add().bool_value = arg  # pylint: disable=no-member
        else:
            raise TypeError("Unexpected type for argument %d: %s" % (i, type(arg)))
    return arguments_message
