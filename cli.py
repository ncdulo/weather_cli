#!/usr/bin/env python

import os
import re
import click
import requests
from string import Template


class ApiKey(click.ParamType):
    name = 'api-key'

    def convert(self, value, param, ctx):
        found = re.match(r'[0-9a-f]{32}', value)

        if not found:
            self.fail(
                    f'{value} is not a 32-character hexadecimal string',
                    param,
                    ctx,
                )

        return value

def degrees_to_cardinal(degrees):
    '''
    Return the cardinal direction representing a given 'degrees'
    '''
    cardinal = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    cardinal_len = len(cardinal)
    ix = round(degrees / (360.0 / cardinal_len))
    return cardinal[ix % cardinal_len]


def current_weather(location, api_key, units):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    query_params = {
            # If using City ID, set the 'id' parameter
            #'id': location,
            # Otherwise, we are using City names, 'q' parameter
            # TODO: Make the above into a flag so the user can choose
            # between City ID or City Name
            'q': location,
            'units': units,
            'appid': api_key,
        }
    response = requests.get(url, params=query_params)

    # Check the HTTP response. If we receive a 4XX or 5XX error, raise
    # an exception so it may be dealt with.
    response.raise_for_status()

    return response.json()

@click.group()
@click.option(
        '--api-key', '-a',
        type=ApiKey(),
        help='Your OpenWeatherMap API key')
@click.option(
        '--config-file', '-c',
        type=click.Path(),
        default='~/.weather.cfg')
@click.pass_context
def main(ctx, api_key, config_file):
    '''
    A simple weather tool that shows the current weather condition in a
    LOCATION of your choice. Provide the city name, and optionally a two-digit
    country code. If the city name contains spaces, it should be enclosed in
    quotation marks. Examples:

    1. "New York City,US"

    2. Berlin

    You need a valid API key from OpenWeatherMap for this tool to work. You
    can sign up for a free account at https://openweathermap.org/appid.
    '''
    filename = os.path.expanduser(config_file)

    if not api_key and os.path.exists(filename):
        with open(filename) as cfg:
            api_key = cfg.read()

    ctx.obj = {
            'api_key': api_key,
            'config_file': filename,
        }


@main.command()
@click.pass_context
def config(ctx):
    '''
    Store the OpenWeatherMap API key in configuration file.
    '''
    config_file = ctx.obj['config_file']

    api_key = click.prompt(
            'Please enter your OpenWeatherMap API key',
            default=ctx.obj.get('api_key', '')
        )

    with open(config_file, 'w') as cfg:
        cfg.write(api_key)

# TODO: More flags to add -- not necessarily all, but these look good
#  - sunrise/sunset
#  - air pressure
#  - visibility
#  - data updated time
#  - cloud cover
@main.command()
@click.argument('location')
@click.option('--units', '-u',
        type=click.Choice(['standard', 'metric', 'imperial'],
            case_sensitive=False),
        default='standard',
        help='Units for displayed data')
@click.option('--pretty', '-p',
        type=click.Choice(['short', 'long', 'verbose',],
            case_sensitive=False),
        default='short',
        help='Enable extra output text, and formatting')
@click.option('--conditions', '-C', is_flag=True,
        help='Display current conditions text')
@click.option('--temperature', '-t', is_flag=True,
        help='Show current temperature (includes high/low)')
@click.option('--humidity', '-h', is_flag=True,
        help='Show current relative humidity')
@click.option('--wind', '-w', is_flag=True,
        help='Show current wind speed and direction')
@click.pass_context
def current(ctx, location, units, pretty, conditions, temperature, humidity,\
        wind):
    '''
    Show the current weather for a location using OpenWeatherMap data.
    '''
    api_key = ctx.obj['api_key']

    try:
        weather = current_weather(location, api_key, units)
    except requests.HTTPError as error:
        print(f'HTTP Error!\n{error}')
        return
    except requests.ConnectionError as error:
        print(f'Connection Error!\n{error}')
        return
    except requests.Timeout as error:
        print(f'Timed Out!\n{error}')
        return

    current_conditions = {'location': location,}

    # Choose an output template based on the chosen option
    if pretty == 'short':
        # Default, short & to the point
        template = Template(
'''$conditions | $temperature | $humidity | $wind_dir at $wind_speed'''
            )
    elif pretty == 'long':
        # Longer form, additional formatting
        template = Template(
'''Current conditions for ${location} are
    $conditions at $temperature
      ${humidity}, winds $wind_dir at $wind_speed'''
            )
    elif pretty == 'verbose':
        # Describe the full output
        # TODO: Pretty print into a table!
        template = Template(
'''Location: $location
Conditions: $conditions
Temperature (High, Current, Low): $temperature
Relative Humidity: $humidity
Wind (Direction, Speed): $wind_dir, $wind_speed'''
            )

    if conditions:
        if 'weather' in weather:
            current_conditions['conditions'] = \
                    weather['weather'][0]['description'].capitalize()

    if temperature:
        if 'temp_max' in weather['main'] and \
                'temp_min' in weather['main'] and \
                'temp' in weather['main']:
            temp_units = {
                    'imperial': 'F',
                    'metric': 'C',
                    'standard': 'K',
                }
            # TODO: Should we break these values out individually too?
            current_conditions['temperature'] = '↑' + \
                    str(weather['main']['temp_max']) + f'°{temp_units[units]}, ' +\
                    str(weather['main']['temp']) + f'°{temp_units[units]}, ↓' + \
                    str(weather['main']['temp_min']) + f'°{temp_units[units]}'

    if humidity:
        if 'humidity' in weather['main']:
            current_conditions['humidity'] = \
                    str(weather['main']['humidity']) + '%RH'

    if wind:
        if 'wind' in weather:
            if 'speed' in weather['wind'] and 'deg' in weather['wind']:
                wind_units = {
                        'imperial': 'mph',
                        'metric': 'm/s',
                        'standard': 'm/s',
                    }
                wind_cardinal = degrees_to_cardinal(weather['wind']['deg'])
                current_conditions['wind_dir'] = wind_cardinal
                current_conditions['wind_speed'] = \
                        str(weather['wind']['speed']) + f'{wind_units[units]}'

    # Pass our conditions dictionary into the 'pretty' template and
    # substitue our weather data in for display.
    output_text = template.safe_substitute(**current_conditions)
    print(output_text)


if __name__ == '__main__':
    main()
