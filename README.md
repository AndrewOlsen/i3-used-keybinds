# i3-used-keybinds
Show i3 keybinds already in use.

Simple python script that parses through an i3 config file to find assigned keybinds. This makes it easier for the user to assign new keybinds in i3 without having to grep the config file.

### Features

* Trys, albeit not very hard, to find an i3 config automatically.
* If keybinds are set using a variable inplace of Mod1 or Mod4, e.g. `set $mod Mod4`, it will still work. Hopefully.
* There is a very primitive search function implemented. `i3keybinds.py -s s` will return all keybinds with a 's' in them. This includes Shifts and symbols like minus. If you are looking for `Shift+q` you must add the `+`. 
* It differentiates between super (Mod4) and meta (Mod1) keybinds.

The script spits out the keybinds in the same format as i3, in alphabetical order:

```
-------SUPER BINDS IN USE---------
Control+l
Up
semicolon
0
Shift+q
```
