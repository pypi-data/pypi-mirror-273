import requests


def streamnew():
    url = "https://stream.new/api/uploads"
    with open("test.mp4", "rb") as f:
        # files = {"file": f}
        r = requests.post(url, data=f)
        print(r)


streamnew()
