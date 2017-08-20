# i3-used-keybinds
Show i3 keybinds already in use.

Simple python script that parses through an i3 config file to find assigned keybinds. This makes it easier for the user to assign new keybinds in i3 without having to grep the config file.

Currently requires tabulate to do table printing.

### Features

* Trys, albeit not very hard, to find an i3 config automatically.
* If keybinds are set using a variable inplace of Mod1 or Mod4, e.g. `set $mod Mod4`, it will still work. Hopefully.
* There is a very primitive search function implemented. 
`i3keybinds.py -k s` will return all keybinds with a 's' in them. This includes Shifts and symbols like minus. If you are looking for `Shift+q` you must add the `+`. 
`i3keybinds.py -c kill` will return all keybinds that execute the command 'kill'.
* It differentiates between super (Mod4) and meta (Mod1) keybinds.

The script spits out the keybinds in the same format as i3, in alphabetical order:

```
Keybind               Modifier    Command
--------------------  ----------  ---------------
Control+l             Mod1        /usr/bin/i3lock
Up                    Mod4        move up
semicolon             Mod1        exec --no-startup-id weechat
0                     Mod4        workspace 10
Shift+q               Mod4        kill
```

#### Todo
* make output better (in progress)
  * testing other python table modules
* gtk version
