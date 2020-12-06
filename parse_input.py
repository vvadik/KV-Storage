def parse(line):
    if line[0] in '"\'':
        return _parse_add(line)
    else:
        return _parse_com(line)


def _parse_add(line):
    split_value = line[0]
    args = line.split(split_value)
    if len(args) != 5:
        return '', ''
    if '=' in args[2] and args[1] and args[3]:
        return args[2][1], (args[1], args[3])


def _parse_com(line):
    args = line.split(' ')
    if len(args) == 1:
        return args[0], ''
    else:
        return line[:len(args[0])], line[len(args[0]) + 1:]
