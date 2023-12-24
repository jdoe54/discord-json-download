import os
import json
import requests
import random

media = []
links = []
mediaCount = {}

MAX = 100

# Change this to the directory that the file is in.
os.chdir()

print("BEGIN DOWNLOAD!")

# Links.json will be the JSON file you would like to go through and download.

with open('links.json', encoding="utf8") as f:
   data = json.load(f)


def download(URL):
    # This takes in an acceptable URL and download the file into the same directory as the folder.
    correctURL = URL.split('\n')

    response = requests.get(correctURL[len(correctURL)-1], [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')])
    open("file" + str(random.random() * 100000000) + ".png", "wb").write(response.content)
                    

def findLink(part):
    """
        Checks to see if part is a string. If it is, then it will split it and try to download the domain part of the URL.

        Arg:
            part is an object passed from the JSON file.
    """
    if isinstance(part, str):
        divider = part.split("//")
        if divider and len(divider) > 1:
            domain = divider[1].split("/")
            if domain:
                media.append(domain[0])
                links.append(part)

                if len(media) < MAX:
                    download(part)

                if domain[0] in mediaCount:
                    mediaCount[domain[0]] = mediaCount[domain[0]] + 1
                else:
                    mediaCount[domain[0]] = 1
            
         
def findData(segment):
    """
        Goes through the entire JSON file using recursion. If it finds a string then it checks to see if the
        string is an acceptable URL for downloading.

        Args:
            segment is an object passed from the JSON file.
    """
    if isinstance(segment, dict) or isinstance(segment, list):
        for val in segment:
            if isinstance(val, dict) or isinstance(val, list):
                findData(val)
            else:
                findData(segment[val])
    else:
        findLink(segment)

for section in data:
    findData(data[section])

print("COMPLETE!")

