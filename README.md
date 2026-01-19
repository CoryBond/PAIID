# 🍱 PAIID

The Pi AI Image Displayer is a program originally designed for a single board computer (a raspberry pi 3 specifically) that displays Ai Generated Images to a connected screen. PAIID is currently in 1.0 release with all original project features added. 

This is a side project I am working on as I upgraded my retropie gaming system to the new raspbery pi 5 and want to do a cool project with my old raspberry pi 3. In particular I am interested in doing something AI related as the latest developments in AI tools (like ChatGPT 4) seem to have lots of pratical utility in peoples lives. Setting aside the controversies arising from AI tools I want to get more involved in developing with them both for my professional work and for fun.

[Preview Of PAIID](https://github.com/CoryBond/PAIID/assets/12073642/4df1c238-1190-4543-9074-5119fb786043)

## 🗺️ Roadmap

**Version 1.0** [✅]

1. Run a python GUI on a monitor [✅]
2. Create a git repo for the project [✅]
3. Boot the PAIID GUI on device start [✅]
4. Connect 7 inch touchscreen display to the pi [✅]
5. Boot GUI to connected touchscreen [✅]
6. Wire the touchscreen to the board [✅]
7. Install the Dalle Python client. [✅]
8. Pay for a client subscription. [✅]
9. Display Dalle Images to screen via hardcoded prompts. [✅]
10. Connect usb microphone to the device (might be more difficult then it ... sounds) [✅]
11. Support voice commands when a user touches a "make image" button. [✅]
12. Allow users to type in prompts via virtual keyboard [✅]
13. Creating loading ~~screen~~ popup that tells the user to wait (also have all controls disbaled) [✅]
14. Error messages when generating an image goes wrong. [✅]
15. Zoom into images with touch gestures [✅]
16. Pan images on image viewer [✅]
17. Clear prompt button [✅]
18. Replace tkinker qith PyQT [✅]
  * Tkinker doesn't currently support touch gestures though there is a draft for it : https://core.tcl-lang.org/tips/doc/trunk/tip/570.md

**Version 2.0**

Featrues:

1. Menu Bar containing: [✅]
  1. Home
  2. Gallery
  3. Settings
2. Refactor MainWindow content between a QT MainWindow and a "Home Widget" making it possible to switch between pages in the MainWindow [✅]
3. Refactor current MainWindow (Home Widget) into 3 seperate widgets: [✅]
  1. Image Generator Sidebar
  2. Image Viewer (already exists)
  3. AI Result Meta Sidebar
4. Image Generator [✅]
  1. Add Image Generator Control To Select Engine (default Dalle-3)
    1. Does not need implementation. Can be forced to use Dalle-3 for now.
  2. Add ability to select how many images to make per request
    1. Does not need implementation. Can be just "1" for Dalle-3.
  3. Refactor Image Generator to allow pluginable controls per engine (options may differ per engine)
  4. Turn Image Generator into a sidebar for a better UX experience
5. AI Result Meta Sidbar [✅]
  1. Takes in the current meta info (prompt, current image num, date created, time created, engine used)
  2. Option to select 1-4+ images that were generated for the prompt at the given dateTime with the engine
    1. Selection modifies what is shown in ImageViewer at any one point
    2. Updates the num selection info in the AI Result Meta Sidebar
    3. Sidebar can be collapsed and re-expanded if needed or not
6. Gallery [✅]
  1. Menu item switches from the Home page to the Gallery
  2. Gallery is layed out by prompt + timestamp
  3. Under each unique section you can see preview images of the actual images created
  4. Selecting any image loads the image into Home, populating the Image Viewer and The AI Result Meta Sidebar whiel auto-hiding the Image Creator sidebar
7. Settings does nothing for now [❌]
  1. Potential backlog in future versions:
    1. Switch theme
    2. Add wifi (increase PAIID mobility)


**Version 2.1**

Featrues:

1. Ability to delete image on Home page. [✅]
2. **Ver 2.1.1** Settings page (Changing wifi of device supported.) [✅]


Bug Fixes:

1. Meta prompt display not word wrapping properly for prompts that have big words. [✅]
1. Create and clear buttons on image generator don't start off as disabled. [✅]


**Version 2.2**

Featrues:

1. On Gallery Page
  1. Ability to delete entire time prompt directories
  2. Page refreshes on deleted entry


**Version 3.0**

Featrues:

1. Filtering On Gallery
  1. Date range
  2. Time Range
  3. Previous Prompts
2. Ability to switch between AI generators
3. Stable Diffusion Provider implemented
4. Better way to configure API Keys


Additional Stretch Goals (not required for 3.0 release):

1. Replace or improve voice input 
  1. Use another tool besides the Google AI.
  2. Maybe buy tokens for a better service.
  3. Make it more clear if a transcription faild and the user needs to repeat themselves.
2. Clean up either the requirements.txt or myproject.toml to use specific versions of packages.

Bug Fixes:

1. Make it so the loading popup doesn't go away if the user clicks out of it
3. Recorder dialog sometimes hangs or crashes when try to open it. 
  * Might be the previous recording still hasn't closed yet from the last dialog
  * Might need to pre-load only 1 dialog or handle some way for the SpeechRecognizer to wait until the last recording session has ended.

## Running The Program

This project was built in Python3.9 on a Raspberry Pi 3 with a arm7 (32 bit) chipset. Python 3.9 is the default version used by the Raspberry Pi OS Bookworm.
Its recommended to make a virtual python env with `Python3 -m venv myenv`. Activate this virtual environment, install all necessary packages and run the entry file in `src/main.py`

## 🏴󠁶󠁥󠁷󠁿 Dependencies

Almost all python packages required by this project can be found in the requirements.txt and can be imported into a python environment using:
`pip install -r requirements.txt --verbose` after starting your pytho env `source myenv/bin/activate`.

Some dependencies, especially PyQt don't have a wheel (at least not for my machine) and take a long time to compile. If you `sudo apt install python3-pyqt5` the pyqt5 binary and other adjacent libraries you can get around installing a virtual environment specific copy. You will need to modify the `my/pyenv.cfg` file to have

```
include-system-site-packages = true
```

in it though.

### Additional Package Installs

Some packages, like speech_recognition, also require additional system specific packages if they don't already exist. You might have to install
these manually on your device prior to using PAIID.
For example:

| System | Package | Install Command                      | Required By        |
| ------ | ------- | ------------------------------------ | ------------------ |
| Linux  | PYQT5   | sudo apt install python3-pyqt5       | pyqt5              |
| Linux  | PYQT5   | sudo apt install qtbase5-dev       | pyqt5              |
| Linux  | PYQT5-VirtualKeyboard   | sudo apt install qtvirtualkeyboard-plugin       | pyqt5              |
| Linux  | PYQT5   | sudo apt install qml-module-qtquick-controls       | pyqt5              |
| Linux  | PYQT5   | sudo apt install qml-module-qtquick-layouts       | pyqt5              |
| Linux  | PYQT5   | sudo apt install qml-module-qt-labs-folderlistmodel       | pyqt5              |
| Linux  | PYQT5   | sudo apt install python3-pyqt5       | pyqt5              |
| Linux   | PyAudio | sudo apt-get install python3-pyaudio | pyaudio            |
| Linux   | Flac    | sudo apt-get install flac            | speech_recognition |
| Linux   | ESpeak  | sudo apt-get install espeak          | speech_recognition |

And maybe more beyond listed here. PyQt, being a wrapper around the c++ Qt, will need to have a lot of external dependencies installed.

### PiWheels

Newer versions of packages can take absurd amounts of time to compile and download on a rasbperry pi. To avoid this only use the numpy version specified in the requirements file and setup pre-compiled pi [wheels](https://www.piwheels.org/) installations in the `etc/pip.config`.

## 📶 How to display GUI through SSH / Remote VSCode

If on a windows machine and you want to display this GUI back through SSH to the client then do the following:

1. Install and run https://sourceforge.net/projects/xming/
2. Make sure the SSH session uses ForwardX11 :
3. The following configs in VSCode can be set : -ForwardAgent yes -ForwardX11 yes -ForwardX11Trusted yes

And this should make it work!

## 🖥️ How to display GUI on connected monitor

Dalle Displayer can run in either Desktop Environments or in Window Manger environments though the later will require some extra work to setup.

### No Desktop Environment

Before you can display this program onto a connected monitor you must first setup a display server and window manager for the GUI. Assuming you work in a headless environment you can use xinit + openbox for this as follows:

1. Install xinit openbox
   (NOTE: [xinit](https://en.wikipedia.org/wiki/Xinit) is display server while [openbox]() is a graphical window manager. Together these will allow rendering the python GUI to a connected monitor. )
2. Create a directory/file called at `~/.config/openbox/autostart`
   1. Add an entry in that file as ` ~path_to_PAIID_root~/myenv/bin/python ~path_to_PAIID_root~/src/main.py` (autostart runs everytime the openbox-session [not the openbox command line] runs)

After following these steps you can now run `xinit openbox-session` and it will should start up the PAIID and render the GUI to the connected monitor.
If the PAIID closes while openbox-session is still up you can do a few things to restart it:

1. Restart xinit + openbox
2. Run the script directly while openbox session is open with `DISPLAY=:0.0 python3 ~path_to_PAIID_root~/src/main.py`

#### Boot

Several linux tools allow xinit + openbox + PAIID to start at boot though I recommend using crontab. Using rc.local to load startx did not cause openbox to detect the user specific `~/.config/openbox/autostart`` script.

After opening `crontab -e` all you need to do is add a line like `@reboot xinit openbox-session`. If you also setup PAIID in the openbox autostart file then it will load at boot as well.

#### Script

This project also includes a script that does the following:

1. Kill openbox instances that would be running the displayer (this will also kill entire openbox sessions!)
2. Restart openbox specificlaly opening only this python application.

Simply run the script with `startx ./tools/openBoxStarter.bash`.

#### Calibrating Touchscreen

For touchscreens its possible for the input to off.... sometimes very off. In a headless environment there is a tool
that uses xinit to recalibrate the input. Simply install [xinput_calibrator](xinput_calibrator) and run it with `startx`

## 🧪 Tests

There is included a test package of pytests for various functions and classes used throughout the project. To run tests either run `pytest` normally or with increased verbosity with `pytest -vv -s`

### Dev UI

There exists a test UI which uses mock APIs rather then real ones for dev purposes. Simply run the application in this mode run the openbox script with the t flag (ex: `startx ./tools/openBoxStarter.bash -t`)

## 🐛 Bugs

Some known bugs include:

| Bug | Type | Description                      | Solution        |
| ------ | ------- | ------------------------------------ | ------------------ |
| Virtual Keyboard Not Functional With Inputs For Dialogs/Popups  | Functionality   | When using any QDialog based widgets that have a input for keyboards, the keyboard will load up but becomes un-interactable. This is apparently because QDialogs absorb all key events that would go anywhere other then the Dialog window.      | Currently no solution right now. Have to use a physical keyboard for interactions. There is discussion on this issue at https://qt-project.atlassian.net/browse/QTBUG-56918 which have a non-trivial solution             |
