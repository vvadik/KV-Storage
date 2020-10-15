import json
import argparse
from os import path


def open_storage(name):
    data = {}
    with open(f'{name}.json', encoding='utf-8') as file:
        try:
            data = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            pass
    return data


class KVStorage:
    def __init__(self, name, command, key=None, value=None):
        self.avalible_commands = {'init': self.init,
                                  'add': self.add,
                                  'list': self.list,
                                  'delete': self.delete,
                                  'load': self.load_key}
        if command not in self.avalible_commands:
            print('No such command')
        self.name = name
        self.key = key
        self.value = value
        self.avalible_commands[command]()

    def init(self):
        if path.isfile(f'{self.name}.json'):
            print('Storage already exists')
            return
        with open(f'{self.name}.json', 'w', encoding='utf-8') as file:
            file.write('')

    def list(self):
        data = open_storage(self.name)
        for i in data:
            print(f'{i}: {data[i]}')

    def add(self):
        if not self.key or not self.value:
            print('No key or value')
            return
        data = open_storage(self.name)
        data[self.key] = self.value
        self.close_storage(data)

    def delete(self):
        data = open_storage(self.name)
        try:
            del data[self.key]
        except KeyError:
            print('No such key')
        self.close_storage(data)

    def load_key(self):
        data = open_storage(self.name)
        try:
            print(data[self.key])
        except KeyError:
            print('No such key')

    def close_storage(self, data):
        with open(f'{self.name}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-Storage')
    parser.add_argument('name', type=str, metavar='',
                        help='Storage name')
    parser.add_argument('command', type=str, metavar='',
                        help='command to execute')
    parser.add_argument('-k', '--key', type=str, metavar='',
                        required=False, help='Key to load or add',
                        default=None)
    parser.add_argument('-v', '--value', type=str, metavar='',
                        required=False, help='Value to add or modify',
                        default=None)

    args = parser.parse_args()
    storage = KVStorage(args.name, args.command, args.key, args.value)
