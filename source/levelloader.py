import json

class LevelLoader:
    def __init__(self):
        f = open("levels.json")
        self.level_data = json.load(f)

    def get_Level(self,i):
        data = self.level_data["Level"+str(i)]
        return [data["fighters"],data["Ejets"]]

if __name__ == '__main__':
    ll = LevelLoader()