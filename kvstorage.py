from os import path
import argparse
import struct
from hashlib import md5
from parse_input import parse


class Local_Strorage:
    def __init__(self, file_name):
        self.file_name = file_name
        self.storage = {}
        self.deleted_sectors = {}  # {start: end}
        if path.exists(self.file_name) and path.getsize(self.file_name) > 8:
            self.restore_file()
        else:
            self.create_storage()
        self.file = open(f'{self.file_name}', 'rb+')
        self.commands = {'=': self.add_key,
                         '?': self.get_key,
                         '??': self.is_exists,
                         'x': self.remove_key,
                         'close': self.close}
        self._work = True

    def read(self, start):
        self.file.seek(start)
        length = struct.unpack('!Q', self.file.read(8))[0]
        data = self.file.read(length)
        return data

    def add_key(self, pair):
        key, value = pair
        hash_key = md5(key.encode()).hexdigest()
        if hash_key in self.storage:
            self.remove_key(key)
        # if key already exists we should delete them
        value_len = struct.pack('!Q', len(value))
        self.file.seek(0)
        start = path.getsize(self.file_name)
        self.storage[hash_key] = start
        self.file.seek(0, 2)
        self.file.write(value_len + value.encode())
        self.file.seek(0)

    def _get_key(self, key):
        hash_key = md5(key.encode()).hexdigest()
        if not self._is_exists(key):
            return 'no such key'
        start = self.storage[hash_key]
        print('Start the value', start)
        data = self.read(start)
        return data.decode()

    def get_key(self, key):
        data = self._get_key(key)
        print(data)

    def _is_exists(self, key):
        hash_key = md5(key.encode()).hexdigest()
        return hash_key in self.storage

    def is_exists(self, key):
        result = self._is_exists(key)
        print(result)

    def remove_key(self, key):
        hash_key = md5(key.encode()).hexdigest()
        if not self._is_exists(key):
            print('no such key')
            return
        start = self.storage[hash_key]
        self.file.seek(start)
        length = struct.unpack('!Q', self.file.read(8))[0]
        self.deleted_sectors[start] = start + length + 8
        del(self.storage[md5(key.encode()).hexdigest()])

    def close(self, type=None):
        self.file.seek(0)
        start = path.getsize(self.file_name)
        for i in self.storage:
            self.file.seek(0, 2)
            self.file.write(i.encode() + struct.pack('!Q', self.storage[i]))
        self.file.seek(0, 2)
        self.file.write(b' ')
        self.file.seek(0, 2)
        for i in self.deleted_sectors:
            self.file.seek(0, 2)
            self.file.write(struct.pack('!QQ', i, self.deleted_sectors[i]))
        self.file.seek(0)
        end = path.getsize(self.file_name)
        length = end - start
        self.file.seek(0, 2)
        self.file.write(struct.pack('!QQ', start, length))
        self.file.seek(0)

        self.file.close()
        self._work = False

    def restore_file(self):
        with open(f'{self.file_name}', 'rb+') as file:
            file.seek(-16, 2)
            start, length = struct.unpack('!QQ', file.read())
            print('Start, length', start, length)
            file.seek(start)
            data = file.read(length)
            print(data)
            storage, spaces = data.split(b' ')
            for i in range(0, len(storage), 40):
                key_hash = storage[i:i+32].decode()
                value_start = struct.unpack('!Q', storage[i+32:i+40])[0]
                self.storage[key_hash] = value_start
            for i in range(0, len(spaces), 16):
                del_start, del_end = struct.unpack('!QQ', spaces[i:i+16])
                # if del_end in self.deleted_sectors:
                #     self.deleted_sectors[del_start] = del_end
                self.deleted_sectors[del_start] = del_end
            print(self.storage)
            print('Deleted sectors', self.deleted_sectors)
            file.seek(start)
            file.truncate()

    def create_storage(self):
        with open(f'{self.file_name}', 'wb') as file:
            pass

    def run(self):
        while self._work:
            self.file.seek(0)
            command, args = parse(input())
            print(command, args)
            if command not in self.commands:
                print('unknown command or incorrect input')
                continue
            self.commands[command](args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-Storage')
    parser.add_argument('name', type=str, help='Storage name')
    args_p = parser.parse_args()
    storage = Local_Strorage(args_p.name)
    storage.run()
