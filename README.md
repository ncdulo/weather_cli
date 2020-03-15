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

# Demo
Short series of demo commands to show off a bit. Why not. The arguments can be specified in a variety of ways, as can be seen in the commands being entered. Full documentation for the available arguments can be found by passing the `--help` argument as noted in the installation instructions.
```
$ weather current Mars -Cthw --units imperial
Light rain | ↑34°F, 32.76°F, ↓32°F | 87%RH | NNW at 3.36mph
$ weather current Mars -Cthw -u standard --pretty long
Current conditions for Mars are
    Light rain at ↑274.26°K, 273.5°K, ↓272.59°K
      87%RH, winds NNW at 1.5m/s
$ weather current Mars -Cthw --units=metric -p verbose              
Location: Mars
Conditions: Light rain
Temperature (High, Current, Low): ↑1.11°C, 0.42°C, ↓0°C
Relative Humidity: 87%RH
Wind (Direction, Speed): NNW, 1.5m/s
```

# API Key
This program requires a *free* OpenWeatherMap API Key. Once you have your key,
it may be passed into the program by either a configuration file or a command
line argument. It is recommended to run `weather` in interactive mode and allow
it to save the API key to configuration file. Using interactive mode will prevent
you from entering your key into the terminal, which would leave it sitting in
your history file for any with access to see.

```bash
# Install API key interactively
$ weather config
Please enter your OpenWeatherMap API key: YOUR_API_KEY [return]
# Install API key from command line
$ weather --api-key YOUR_API_KEY config
```
Obtain your API key here: https://openweathermap.org/appid

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

# Write your API key to configuration file interactively (recommended)
.env/bin/weather config
# -- or as a single command --
.env/bin/weather --api-key YOUR_API_KEY config

# Check use instructions
.env/bin/weather --help
.env/bin/weather config --help
.env/bin/weather current --help

# Optional, install symlink to executable within your $PATH
# ~/.local/bin must be in your system $PATH
ln -s `pwd`/.env/bin/weather ~/.local/bin/weather
# With the symlink in place, `weather` may be called from any location
# without typing the full path to the executable
```
