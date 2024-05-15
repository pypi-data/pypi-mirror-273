import requests
class Media:
    def __init__(self, url="https://api.media.ccc.de/public/recordings/"):
        self.url = url
        self.r = requests.get(url=url)
        self.data = self.r.json()["recordings"]
        print(self.data)

if __name__=="__main__":
    obj = Media()