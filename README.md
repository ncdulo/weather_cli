# weather_cli
Command line tool which presents weather data in a customizable format. This
was originally created by following a series of tutorials on how to use `click`
for handling command line arguments. I have since expanded upon and made this
program into my own. Plan is to keep expanding upon it, and eventually add
a 5-day forecast mode.

Pull requests, issues, comments and criticisms are more than welcome.

The start of it all:
  - https://dbader.org/blog/python-commandline-tools-with-click
  - https://dbader.org/blog/mastering-click-advanced-python-command-line-apps

# Installation
The install and use should be fairly simple. I don't totally know what I'm
doing with `setuptools` but this works, and has been verified in local clones
of this repo. If errors are encountered with these instructions, an issue or
comment would be appreciated so I can fix it.

These instructions will install `weather_cli` into a virtual environment and
create an executable, `weather`, within that environment. When called, that
executable automatically enables the virtual environment, runs our program,
and deactivates the virtual environment.

```bash
# Clone the repo
git clone https://github.com/ncdulo/weather_cli.git
cd weather_cli

# Create a new virtual environment, and enable it
python -m venv .env
source .env/bin/activate

# Update Pip & friends. Optional, but recommended
python -m pip install --upgrade pip setuptools wheel

# Install dependencies and create executable
pip install .

# Deactivate the virtual environment
deactivate

# Write your API key to configuration file
cat 'API_KEY' > ~/.weather.cfg
# -- or --
.env/bin/weather --api-key API_KEY config

# Check use instructions
.env/bin/weather --help
.env/bin/weather config --help
.env/bin/weather current --help

# Optional, install symlink to executable within your $PATH
# ~/.local/bin must be in your system $PATH
ln -s .env/bin/weather ~/.local/bin/weather
# With the symlink in place, `weather` may be called from any location
# without typing the full path to the executable
```
