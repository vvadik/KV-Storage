def parse_add(line):
    if not len(line):
        return None
    split_value = line[0]
    args = line.split(split_value)
    if len(args) != 5:
        return None
    if '=' in args[2] and args[1] and args[3]:
        return args[1], args[3]
