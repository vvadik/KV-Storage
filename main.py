from os import path
import argparse
import struct
from hashlib import md5


class Local_Strorage:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = ''
        self.start = 8
        self.end = 0
        self.commands = {'=': self.add_key,
                         '?': self.get_key,
                         '??': self.is_exists,
                         'x': self.remove_key,
                         'close': self.close}
        self.storage = {}
        self.deleted_sectors = {}  # {start: end}

    def read(self, start):
        self.file.seek(start)
        length = struct.unpack('!Q', self.file.read(8))[0]
        data = self.file.read(length)
        return data

    def add_key(self, key, value):
        hash_key = md5(key.encode()).hexdigest()
        if hash_key in self.storage:
            self.remove_key(key)
        # if key already exists we should delete them
        value_len = struct.pack('!Q', len(value))
        start = path.getsize(self.file_name)
        self.storage[hash_key] = start
        self.file.write(value_len + value.encode())

    def _get_key(self, key):
        start = self.storage[key]
        print('Start the value', start)
        data = self.read(start)
        return data

    def get_key(self, key):
        hash_key = md5(key.encode()).hexdigest()
        if not self._is_exists(hash_key):
            print('no such key')
            return
        data = self._get_key(hash_key)
        print(data.decode())

    def _is_exists(self, key):
        return key in self.storage

    def is_exists(self, key):
        result = self._is_exists(md5(key.encode()).hexdigest())
        print(result)

    def remove_key(self, key):
        hash_key = md5(key.encode()).hexdigest()
        if not self._is_exists(hash_key):
            print('no such key')
            return
        start = self.storage[hash_key]
        self.file.seek(start)
        length = struct.unpack('!Q', self.file.read(8))[0]
        self.deleted_sectors[start] = length + 8
        del(self.storage[md5(key.encode()).hexdigest()])

    def close(self):
        print('close')
        start = path.getsize(self.file_name)
        self.file.seek(0, 2)
        for i in self.storage:
            self.file.write(i.encode() + struct.pack('!Q', self.storage[i]))
        self.file.write(b' ')
        for i in self.deleted_sectors:
            self.file.write(struct.pack('!Q', i) +
                            struct.pack('!Q', self.storage[i]))
        self.file.seek(0)
        end = path.getsize(self.file_name)
        length = end - start
        self.file.write(struct.pack('!QQ', start, length))

    def restore_file(self):
        with open(f'{self.file_name}', 'rb') as file:
            file.seek(-16, 2)
            start, length = struct.unpack('!QQ', file.read())
            print(start, length)
            file.seek(start)
            data = file.read(length)

            storage, spaces = data.split(b' ')
            print(storage, spaces)
            for i in range(0, len(storage), 40):
                key_hash = storage[i:i+32].decode()
                value_start = struct.unpack('!Q', storage[i+32:i+40])[0]
                self.storage[key_hash] = value_start
            for i in range(0, len(spaces), 16):
                del_start, del_end = struct.unpack('!QQ',
                                                   spaces[i:i+8],
                                                   spaces[i+8:i+16])
                print(del_start, del_end)
                self.deleted_sectors[del_start] = del_end
            self.deleted_sectors[start] = start + length
            # delete backupped

    def create_storage(self):
        with open(f'{self.file_name}', 'wb') as file:
            pass

    def run(self):
        if path.exists(self.file_name) and path.getsize(self.file_name) > 8:
            self.restore_file()
        else:
            self.create_storage()
        # create or open existed
        with open(f'{self.file_name}', 'ab+') as self.file:
            while True:
                command = input().split()
                try:
                    if len(command) == 3:
                        self.commands[command[1]](command[0], command[2])
                    elif len(command) == 2:
                        self.commands[command[0]](command[1])
                    else:
                        self.commands[command[0]]()
                        break
                    self.file.seek(0)
                    # self.file.read()
                except KeyError:
                    print('unknown command')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-Storage')
    parser.add_argument('name', type=str, help='Storage name')
    args = parser.parse_args()
    storage = Local_Strorage(args.name)
    storage.run()
