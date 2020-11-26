from hashlib import md5
import struct
from os import path

with open('test1.txt', 'w') as file:
    file.write(md5(b'a').hexdigest())  # 32

# with open('test2.txt', 'w') as file:
#     file.write(md5(b'a'))

with open('test3.txt', 'w') as file:
    file.write(f'{int(md5(b"a").hexdigest(), 16)}')  # 38
#
# with open('test4.txt', 'wb') as file:
#     data = int(md5(b'a').hexdigest(), 16)
#     data = struct.pack('!Q', data)
#     print(data)
#     file.write(data)

if __name__ == '__main__':
    length = path.getsize('test.dat')
    print(length)
    with open('test.dat', 'r') as file:
        print(file.read()[12])