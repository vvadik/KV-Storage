from os import path, remove, rename
from itertools import count
import argparse
import struct
from hashlib import md5
from parse_input import parse


class LocalStrorage:
    def __init__(self, file_name):
        self.file_name = file_name
        self.storage = {}
        self.deleted_sectors = {}  # {start: end}
        if path.exists(self.file_name) and path.getsize(self.file_name) > 24:
            self.restore_file()
        else:
            self.create_storage()
        self.file = open(f'{self.file_name}', 'rb+')
        self.commands = {'=': self.add_key,
                         '?': self.get_key,
                         '??': self.is_exists,
                         'x': self._remove_key,
                         'close': self.close,
                         'defragment': self.defragmentation}
        self._work = True

    def read(self, start, key):
        next_ = start
        while next_:
            self.file.seek(next_)
            key_len, next_, value_len = struct.unpack('!QQQ',
                                                      self.file.read(24))
            key_from_storage = self.file.read(key_len)
            if key != key_from_storage.decode():
                continue
            value = self.file.read(value_len)
            return value
        return b'no such key'

    def add_key(self, pair):
        key, value = pair
        hash_key = md5(key.encode()).hexdigest()
        first_key = 0
        if hash_key in self.storage:
            first_key = self._remove_key(key)
        key_len = struct.pack('!Q', len(key))
        value_len = struct.pack('!Q', len(value))
        next_ = struct.pack('!Q', first_key)

        self.file.seek(0)
        start = path.getsize(self.file_name)
        self.storage[hash_key] = start
        self.file.seek(0, 2)
        self.file.write(key_len + next_ + value_len
                        + key.encode() + value.encode())
        self.file.seek(0)

    def _get_key(self, key):
        if not self._is_exists(key):
            return 'no such key'
        hash_key = md5(key.encode()).hexdigest()
        start = self.storage[hash_key]
        data = self.read(start, key)
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
        if not self._is_exists(key):
            print('no such key')
            return
        self._remove_key(key)

    def _remove_key(self, key):
        found_duplicate_key = False
        hash_key = md5(key.encode()).hexdigest()
        start = self.storage[hash_key]
        self.file.seek(start)
        next_ = 1
        counter = count()
        previous_field_next_value = 0
        while next_:
            next(counter)
            key_len, next_, value_len = struct.unpack('!QQQ',
                                                      self.file.read(24))
            key_from_storage = self.file.read(key_len)
            if key_from_storage.decode() == key:
                found_duplicate_key = True
                self.deleted_sectors[start] = key_len + value_len + 24
                if previous_field_next_value:
                    self.file.seek(previous_field_next_value)
                    self.file.write(struct.pack('!Q', next_))
                break
            previous_field_next_value = start + 8
            start = next_
            self.file.seek(next_)
        if next(counter) == 1 and found_duplicate_key:
            if next_ == 0:
                del self.storage[hash_key]
            return next_

        return self.storage[hash_key]

    def defragmentation(self, type_=None):
        if not self.deleted_sectors:
            return
        with open(f".{self.file_name}", 'wb+') as tmp:
            tmp.write(b'\x00')
            tmp.seek(0)
            for key, value in self.storage.items():
                next_ = 1
                size = path.getsize(f".{self.file_name}")
                self.storage[key] = size
                while next_:
                    self.file.seek(value)
                    key_len, next_, value_len = \
                        struct.unpack('!QQQ', self.file.read(24))
                    value = next_
                    key_from_storage = self.file.read(key_len)
                    value_from_storage = self.file.read(value_len)
                    tmp.seek(0)
                    size = path.getsize(f".{self.file_name}")
                    if next_ == 0:
                        next_new = 0
                    else:
                        next_new = size + 8
                    tmp.seek(0, 2)
                    tmp.write(struct.pack('!QQQ',
                                          key_len, next_new, value_len)
                              + key_from_storage
                              + value_from_storage)
                    tmp.seek(0)
        self.deleted_sectors = {}

        self.file.close()
        remove(self.file_name)
        rename(f'.{self.file_name}', self.file_name)
        self.file = open(f'{self.file_name}', 'rb+')

    def close(self, type_=None):
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
            file.seek(start)
            data = file.read(length)
            storage, spaces = data.split(b' ')
            for i in range(0, len(storage), 40):
                key_hash = storage[i:i+32].decode()
                value_start = struct.unpack('!Q', storage[i+32:i+40])[0]
                self.storage[key_hash] = value_start
            for i in range(0, len(spaces), 16):
                del_start, del_end = struct.unpack('!QQ', spaces[i:i+16])
                self.deleted_sectors[del_start] = del_end

            file.seek(start)
            file.truncate()

    def create_storage(self):
        with open(f'{self.file_name}', 'wb') as file:
            file.write(b'\x00')

    def run(self):
        while self._work:
            self.file.seek(0)
            command, args = parse(input())
            if command not in self.commands:
                print('unknown command or incorrect input')
                continue
            self.commands[command](args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-Storage')
    parser.add_argument('name', type=str, help='Storage name')
    args_p = parser.parse_args()
    storage = LocalStrorage(args_p.name)
    storage.run()
