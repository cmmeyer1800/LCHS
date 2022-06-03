import json

def getSetting(setting: str):
    """
    Opens the settings.json file containing program parameters and gets the value of the
    passed key "setting"
    """
    
    with open("settings.json", "r") as FILE:
        js = json.load(FILE)
    
    return js[setting]