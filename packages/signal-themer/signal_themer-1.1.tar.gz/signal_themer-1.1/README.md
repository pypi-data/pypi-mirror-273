# Signal Desktop Themer
A script for injecting theme into [signal-desktop](https://github.com/signalapp/Signal-Desktop).
## Requirements
- python
- python-pip
- pipx
## Installation
1. Install applications in requirements section if you don't have them. [Guide](#install-requirements-guide)
2. Install this script with `pipx install signal-themer`
## Usage
### Linux
**Note: Running this script requires sudo permission in linux. If you are unsure about this, the script is only a few lines and you can go thorough it really quickly.**
1. Close signal. (including from tray)
2. Run `sudo signal-themer <path/to/theme.css>`
3. Launch Signal and enjoy!
### Windows
1. Close signal. (including from tray)
2. Run `signal-themer <path\to\theme.css>`
3. Launch Signal and enjoy!
## Install Requirements Guide
### Windows
1. Download python if you don't have it from [their websise](https://www.python.org/downloads/) or from microsoft store.
2. Run `py -m pip install --user pipx` if you install python from website or replace `py` with `python3` if you downloaded from microsoft store inorder to install pipx.
3. Add pipx to path by running `%LOCALAPPDATA%\python\python<version>\Scripts\pipx.exe ensurepath` replace `<version>` with the version of python you have installed.
4. Close and open terminal again.
### Linux
Your distro probably has a package for python and pipx. (pipx is called python-pipx in some distros)
## Removal
Currently there is no 'clean' way to remove the theme but it might be added in the future.
For now, create an empty css file and use that as theme.
## Theme List
- [whatsapp](https://github.com/CapnSparrow/signal-desktop-themes)
- [yuri and zero two](https://github.com/Foxunderground0/Signal-Themes)
- [catppuccin](https://github.com/CalfMoon/signal-desktop)
