import json

class Wave():
    def __init__(self, wave: int):
        f = open("info/waves.json")
        data = json.load(f)