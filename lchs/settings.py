import json
import os

settingsPath = os.environ["SETTINGSPATH"]

def getSetting(setting: str):
    """
    Opens the settings.json file containing program parameters and gets the value of the
    passed key "setting"
    """
    
    with open(settingsPath, "r") as FILE:
        js = json.load(FILE)
    
    return js[setting]


def getSettings() -> list:
    """Get all settings and store as list of tuples"""
    with open(settingsPath, "r") as FILE:
        js = dict(json.load(FILE))

    return js.items()


def writeSettings(d: dict) -> None:
    with open(settingsPath, "w") as FILE:
        json.dump(d, FILE)