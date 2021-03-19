import cmd
import sys
import argparse
from parse_input import parse_add
from localstorage import LocalStrorage


class Run(cmd.Cmd):
    def __init__(self, storage):
        super().__init__()
        self.storage = storage

    def do_add(self, args):
        '''To add use quotes and syntax "key" = "value"'''
        pair = parse_add(args)
        if not pair:
            print('Incorrect input')
            return
        self.storage.add_key(pair)

    def do_get(self, args):
        '''Return value if key exists. Type key without quotes'''
        if not args:
            print('Incorrect input')
            return
        value = self.storage.get_key(args)
        print(value)

    def do_exists(self, args):
        '''Return True if key in storage, else False.
        Type key without quotes'''
        if not args:
            print('Incorrect input')
            return
        value = self.storage.is_exists(args)
        print(value)

    def do_delete(self, args):
        '''Remove key from storage. Type key without quotes'''
        if not args:
            print('Incorrect input')
            return
        self.storage.remove_key(args)

    def do_close(self, args):
        '''Proper way to close storage'''
        self.storage.close()
        sys.exit(0)

    def do_defragment(self, args):
        '''Simple defragmentator'''
        self.storage.defragmentation()

    def do_EOF(self, args):
        self.storage.close()
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KV-Storage')
    parser.add_argument('name', type=str, help='Storage name')
    args_p = parser.parse_args()
    storage = LocalStrorage(args_p.name)
    run = Run(storage)
    run.prompt = '> '
    try:
        run.cmdloop()
    except KeyboardInterrupt:
        storage.close()
