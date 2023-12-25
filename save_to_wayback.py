import requests
from urllib.parse import urlparse

counter = 0

def delete_line(data):
    with open("urls.txt", "w") as file:
        for line in data:
            file.write(line)

with open("urls.txt", "r") as file:
    data = file.readlines()
    wayback = "https://web.archive.org/save/"

    for url in data:
        url = urlparse(url.strip("\n"))
        
        if (
            "personnel/character" in url.path
            or "assets/images" in url.path
            or "sim/viewpost" in url.path
            and counter < 12
        ):
            res = requests.get(wayback + url.geturl())
            print(res)
            
            data.remove(url.geturl()+"\n")
            delete_line(data)
            counter = counter + 1

        elif counter == 12:
            break