import os
from ast import literal_eval
from configparser import ConfigParser
import pandas as pd

config = ConfigParser()
config.read("./config.ini")

files = [f for f in os.listdir('.') if os.path.isfile(f)]
print(files)


def readDefault():
    print(config)
    configs = config['DEFAULT']
    return configs['session_cookie'], configs['csrf_token']


def readScreenDefault():
    configs = config['SCREEN_DEFAULT']
    return literal_eval(configs['aspect_ratio']), int(configs['text_gap']), \
           int(configs['text_width']), int(configs['text_height'])


def readWheelDefault():
    configs = config['WHEEL_DEFAULT']
    return {'easy_point': float(configs['easy_point']), 'medium_point': float(configs['medium_point']),
            'hard_point': float(configs['hard_point']), 'cost': float(configs['cost'])}


def readSpinnerDefault():
    configs = config['SPINNER_DEFAULT']
    return float(configs['max_velocity']), float(configs['min_velocity']), float(configs['speed_decay']), \
           float(configs['start_degree']), bool(configs['spin_clockwise']), configs['spinner_image_path']


def readCustomisationDefault():
    configs = config['CUSTOMISATION_DEFAULT']
    return literal_eval(configs['screen_colours'])


def readRates():
    df = pd.read_csv('./rates.txt')
    return df['choice'].tolist(), df['weight'].tolist()
