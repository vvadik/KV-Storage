import json
import argparse
import os.path as path


class KVStorage:
    def __init__(self, args):
        self.avalible_commands = {'init': self.init,
                                  'add': self.add, 'list': self.list,
                                  'delete': self.delete,
                                  'load': self.load_key}
        if args.command not in self.avalible_commands:
            raise Exception('No such command')
        self.name = args.name
        self.key = args.key
        self.value = args.value
        self.avalible_commands[args.command]()

    def init(self):
        if path.isfile(f'{self.name}.json'):
            print('Storage already exists')
            return
        with open(f'{self.name}.json', 'w', encoding='utf-8') as file:
            file.write('')

    def open_storage(self):
        data = {}
        with open(f'{self.name}.json', encoding='utf-8') as file:
            try:
                data = json.loads(file.read())
            except json.decoder.JSONDecodeError:
                pass
        return data

    def list(self):
        data = self.open_storage()
        for i in data:
            print(f'{i}: {data[i]}')

    def add(self):
        if not self.key or not self.value:
            print('No key or value')
            return
        data = self.open_storage()
        data[self.key] = self.value
        self.close_storage(data)

    def delete(self):
        data = self.open_storage()
        try:
            del data[self.key]
        except KeyError:
            print('No such key')
        self.close_storage(data)

    def load_key(self):
        data = self.open_storage()
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
    storage = KVStorage(args)
