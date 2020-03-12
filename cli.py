#!/usr/bin/env python

import os
import re
import click
import requests


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


def current_weather(location, api_key, units):
    url = 'http://api.openweathermap.org/data/2.5/weather'

    query_params = {
            # If using City ID, set the 'id' parameter
            #'id': location,
            # Otherwise, we are using City names, 'q' parameter
            'q': location,
            'units': units,
            'appid': api_key,
        }

    response = requests.get(url, params=query_params)

    #current_conditions =  response.json()['weather'][0]['description'] + \
    #        ' at ' + \
    #        str(response.json()['main']['temp']) + '°F' + \
    #        ' (' + \
    #        str(response.json()['main']['temp_max']) + '°F High, ' + \
    #        str(response.json()['main']['temp_min']) + '°F Low) at ' +\
    #        str(response.json()['main']['humidity']) + '% humidity'


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


@main.command()
@click.argument('location')
@click.option('--units', '-u',
        type=click.Choice(['imperial', 'metric', 'standard'],
            case_sensitive=False),
        default='imperial',
        help='Units for displayed data')
@click.option('--conditions', '-C', is_flag=True,
        help='Display current conditions text')
@click.option('--temperature', '-t', is_flag=True,
        help='Show current temperature (includes high/low)')
@click.option('--humidity', '-h', is_flag=True,
        help='Show current relative humidity')
@click.pass_context
def current(ctx, location, units, conditions, temperature, humidity):
    '''
    Show the current weather for a location using OpenWeatherMap data.
    '''
    api_key = ctx.obj['api_key']

    weather = current_weather(location, api_key, units)
    current_conditions = ''

    if conditions:
        current_conditions = weather['weather'][0]['description'] + ', '

    # TODO: Make sure proper units displayed alongside their value

    if temperature:
        current_conditions += \
                '↑' + str(weather['main']['temp_max']) + '°F, ' + \
                str(weather['main']['temp']) + '°F, ↓' + \
                str(weather['main']['temp_min']) + '°F, '

    if humidity:
        current_conditions += str(weather['main']['humidity']) + '%RH'

    print(f'Current conditions for {location}: {current_conditions}')

if __name__ == '__main__':
    main()
