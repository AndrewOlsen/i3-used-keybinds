#!/usr/bin/env python

import argparse
from pathlib import Path
import re
import sys

super_binds = []
meta_binds = []
args = ''


def get_arg():
    global args
    parser = argparse.ArgumentParser(
            description='Find all used keybinds in i3.')
    parser.add_argument('-s', '--search', help='Search for a specific key')
    args = parser.parse_args()


def find_config():
    # Find the i3 config file
    print('Searching for i3 config file....')
    print('Looking in .i3 ...')
    homedir = str(Path.home())
    doti3 = homedir + '/.i3/config'
    dotconfig = homedir + '/.config/i3/config'
    config = Path(doti3)
    if (config.is_file()):
        print('Found .i3/config!')
        return config
    else:
        print('File not found. Trying another directory.')
        config = Path(dotconfig)
        if (config.is_file()):
            print('Found .config/i3/config!')
            return config
        else:
            print('No config files found.')
            print('Please make sure the file is in ~/.i3 or ~/.config')
            sys.exit(1)


def parse(config):
    # Do some parsing
    mod = ''
    with open(str(config)) as f:
        for line in f:
            # If line is not comment,
            if (line[:1] is not '#'):
                # See if there is a mod variable
                if ('Mod4' in line or 'Mod1' in line) and 'set' in line:
                    mod_var_check = re.search('\B\$\w+', line, re.IGNORECASE)
                    if mod_var_check:
                        mod = mod_var_check.group(0)
                        print('Modifier variable found: {0}'.format(mod))
                        if 'Mod1' in line:
                            print('{0} is equal to Mod1'.format(mod))
                            meta = True
                        else:
                            print('{0} is equal to Mod4'.format(mod))
                            meta = False
                    else:
                        print('No modifier variable found.')
                # Only top level bindings
                if 'bindsym' in line:
                    if re.match(r'\s', line):
                        pass
                    else:
                        words = line.split()
                        if mod:
                            if '--' in words[1]:
                                if meta:
                                    meta_binds.append(
                                            words[2].replace(mod+'+', ""))
                                else:
                                    super_binds.append(
                                            words[2].replace(mod+'+', ""))
                            else:
                                if meta:
                                    meta_binds.append(
                                            words[1].replace(mod+'+', ""))
                                else:
                                    super_binds.append(
                                            words[1].replace(mod+'+', ""))
                        else:
                            if 'Mod1' in words:
                                meta_binds.append(words[1].replace('Mod1', ""))
                            elif 'Mod4' in words:
                                super_binds.append(
                                        words[1].replace('Mod4', ""))


def output(search=""):
    if super_binds:
        print('----------SUPER BINDS IN USE----------')
        super_binds.sort()
        for s in super_binds:
            if search:
                if search in s.lower():
                    print(s)
            else:
                print(s)
    if meta_binds:
        print('---------META BINDS IN USE---------')
        meta_binds.sort()
        for m in meta_binds:
            if search:
                if search in s.lower():
                    print(s)
            else:
                print(s)


def main():
    get_arg()
    config = find_config()
    parse(config)
    search = args.search
    output(search)


main()
