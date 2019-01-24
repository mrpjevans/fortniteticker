# fortniteticker
Code for accessing Fortnite API data and displaying it on a Sense HAT. Full tutorial in MagPi #78. [https://raspberyypi.org/mappi]()

## Magazine Example
Import score.json into Node-RED to create the flow. By default it gets my test account, but you can change it to anything you wish.

## Advanced Version
There's also fortnighttickerplus.py which shows how to do the same with Python and adds a few more features.

### Installation

Assuming you have git and pip installed:

```
$ cd
$ git clone https://github.com/mrpjevans/fortniteticker
$ sudo apt install sense-hat
$ pip install requests
```

### Run

```
$ cd ~/fortniteticker
$ python3 fortnighttickerplus.py
```

### Usage

If you have a Sense HAT installed, moving the joystick will display the scores of four people (or different platforms), one for each direction. Pressing the joystick down will get the current server status.

### Customise

You can edit the 'users' dictionary that appears early in the code make different directions access different usernames and/or platforms.

### Credits

Many thanks to the good people of [https://fortniteapi.com]() for their awesome service.
