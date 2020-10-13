import json
import argparse
import os.path as path

class KVStorage:
    def __init__(self, command, name):
        self.avalible_commands = {'init': self.init, 'open': self.open,
                                  'add': self.add, 'list': self.list,
                                  'delete': self.delete, 'load': self.load,
                                  'save': self.save, 'help': self.help}
        if command not in self.avalible_commands:
            raise Exception('No such command, use -h')
        self.command = self.avalible_commands[command]
        self.name = name
        self.data = {}

    def run(self):
        self.command()

    def init(self):
        if path.isfile(f'{self.name}.json'):
            print('Storage already exists')
            return
        with open(f'{self.name}.json', 'w', encoding='utf-8') as file:
            file.write('')

    def open(self):
        with open(f'{self.name}.json', encoding='utf-8') as file:
            try:
                self.data = json.loads(file.read())
            except json.decoder.JSONDecodeError:
                self.data = {}
        self.parse_commands()

    def list(self, commands):
        for i in self.data:
            print(f'{i}: {self.data[i]}')

    def add(self, commands):
        self.data[commands[1]] = commands[2]

    def delete(self, commands):
        try:
            del self.data[commands[1]]
        except KeyError:
            return 'No such key'

    def load(self, commands):
        try:
            return self.data[commands[1]]
        except KeyError:
            return 'No such key'

    def save(self, commands):
        with open(f'{self.name}.json', 'a', encoding='utf-8') as file:
            file.write(json.dumps(self.data))

    def help(self, commands):
        return 'this is help'

    def parse_commands(self):
        while True:
            commands = input().split()
            if commands[0] == 'exit':
                break
            if commands[0] not in self.avalible_commands:
                print("Invalid command, type help")
            result = self.avalible_commands[commands[0]](commands)
            print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-Storage')
    parser.add_argument('command', type=str, metavar='',
                        help='whaat to do')
    parser.add_argument('name', type=str, metavar='',
                        help='Set True for infinity pinging')

    args = parser.parse_args()

    storage = KVStorage(args.command, args.name)
    storage.run()
