#!/usr/bin/env python

import argparse
from tabulate import tabulate
from pathlib import Path
import re
import sys

binds = []
args = ''


def cat(list):
    return ' '.join(list)


def get_arg():
    global args
    parser = argparse.ArgumentParser(
            description='Find all used keybinds in i3.')
    parser.add_argument(
            '-k', '--keybind', help='Search for a specific keybind')
    parser.add_argument('-c', '--command', help='Search for a command')
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
                                    key = words[2].replace(mod+'+', "")
                                    cmd = cat(words[3:])
                                    l = [key, "Mod1", cmd]
                                    binds.append(l)
                                else:
                                    key = words[2].replace(mod+'+', "")
                                    cmd = cat(words[3:])
                                    l = [key, "Mod4", cmd]
                                    binds.append(l)
                            else:
                                if meta:
                                    key = words[1].replace(mod+'+', "")
                                    cmd = cat(words[2:])
                                    l = [key, "Mod1", cmd]
                                    binds.append(l)
                                else:
                                    key = words[1].replace(mod+'+', "")
                                    cmd = cat(words[2:])
                                    l = [key, "Mod4", cmd]
                                    binds.append(l)

                        else:
                            if 'Mod1' in words:
                                key = words[1].replace('Mod1', "")
                                cmd = cat(words[2:])
                                l = [key, "Mod1", cmd]
                                binds.append(l)
                            elif 'Mod4' in words:
                                key = words[1].replace('Mod4', "")
                                cmd = cat(words[2:])
                                l = [key, "Mod4", cmd]
                                binds.append(l)


def output(keybind="", command=""):
    headers = ['Keybind', 'Modifier', 'Command']
    t_data = []
    if binds:
        binds.sort()
        for l in binds:
            if keybind:
                if keybind in l[0].lower():
                    t_data.append(l)
                    # print(cat(l))
            elif command:
                if command in l[2].lower():
                    t_data.append(l)
                    # print(cat(l))
            else:
                t_data.append(l)
                # print(cat(l))
        table = tabulate(t_data, headers=headers)
        print(table)


def main():
    get_arg()
    config = find_config()
    parse(config)
    keybind = args.keybind
    command = args.command
    output(keybind, command)


if __name__ == '__main__':
    main()
