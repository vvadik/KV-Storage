from os import path
import argparse
import struct
from hashlib import md5


class Local_Strorage:
    def __init__(self, file_name):
        self.file_name = file_name
        self.start = 8
        self.end = 0
        self.commands = {'=': self.add_key,
                         '?': self.get_key,
                         '??': self.is_exists,
                         'x': self.remove_key}
        self.storage = {}

    def write(self, data):
        with open(self.file_name, 'ab') as file:
            file.write(data)

    def add_key(self, key, value):
        hash_key = md5(key.encode()).hexdigest()
        print(hash_key)
        # if key already exists we should delete them
        value_len = struct.pack('!Q', len(value))
        start = path.getsize(self.file_name)
        self.storage[hash_key] = start
        self.write(value_len + value.encode())

    def get_key(self, key):
        pass

    def _is_exists(self, key):
        return key in self.storage

    def is_exists(self, key):
        result = self._is_exists(md5(key.encode()).hexdigest())
        print(result)

    def remove_key(self, key):
        pass

    def open_file(self, mode):
        with open(f'{self.file_name}', f'{mode}') as file:
            data = file.read()
        return data

    def run(self):
        # create or open existed
        with open(f'{self.file_name}', 'w'):
            pass
        while True:
            command = input().split()
            try:
                if len(command) == 3:
                    self.commands[command[1]](command[0], command[2])
                else:
                    self.commands[command[0]](command[1])
            except KeyError:
                print('unknown command')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-Storage')
    parser.add_argument('name', type=str, metavar='',
                        help='Storage name')

    args = parser.parse_args()
    storage = Local_Strorage(args.name)
    storage.run()
