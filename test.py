from hashlib import md5
import struct
import io
from os import path, truncate, stat
#
# with open('test1.txt', 'w') as file:
#     file.write(md5(b'a').hexdigest())  # 32

# with open('test2.txt', 'w') as file:
#     file.write(md5(b'a'))

# with open('test3.txt', 'w') as file:
#     file.write(f'{int(md5(b"a").hexdigest(), 16)}')  # 38
#
# with open('test4.txt', 'wb') as file:
#     data = int(md5(b'a').hexdigest(), 16)
#     data = struct.pack('!Q', data)
#     print(data)
#     file.write(data)


# def test():
#     with open('test.dat', 'rb+') as file:
#         # file.write('abc'.encode())
#         # file.seek(0)
#         pass
#         # file.write(b'DEB')
#         # file.write(b'DEB')
#         # data = file.read(5)
#         # print(data)
#         # file.seek(-3, 2)
#         # print(file.read())


def test2():
    with open('test.dat', 'r') as file1:
        with open('test.dat', 'a') as file2:
            file2.write('TEST')
        file1.seek(13)
        data = file1.read(2)
        print(data)
        file1.seek(5)
        data = file1.read(2)
        print(data)


def test3():
    length = path.getsize('test1.txt')
    print(length)
    # res = stat('test1.txt').st_size
    # print(res)
    # s = 10
    # truncate('test1.txt', length - s)

    with open('test1.txt', 'r+') as file:
        # data = file.read()
        # print((type(data), data))
        file.seek(length - 1)
        file.truncate()
        # file.seek(0)
        # file.seek(0, 2)


def test4():
    a = input()
    print(a)


if __name__ == '__main__':
    test4()
    exit()
    length = path.getsize('test.dat')
    print(length)
    with open('test.dat', 'r') as file:
        print(file.read()[12])
