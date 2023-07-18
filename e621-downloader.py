import requests
from tkinter import filedialog
import os
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def checkValidTags(data):
    if len(data["posts"]) == 0:
        cls()
        input("You entered invalid tags...")
        exit()

def postCount(tags, limit):
    #tagList = tags.split("+")
    amount = 0
    i = 0

    if limit == 320:
        while True:
            cls()
            print("Calculating amount of posts.. (The calculating time depends on the amount of posts)")

            time.sleep(1.2)
            i += 1
            URL = f"https://e621.net/posts.json?page={i}&limit={limit}&tags={tags}"
            rTags = requests.get(url = URL, headers=UserAgent)
            postData = rTags.json()
            checkValidTags(postData)

            if len(postData["posts"]) == 320:
                amount += 320
                isDone = False
            else:
                amount += len(postData["posts"])
                isDone = True
        
            if isDone == True:
                time.sleep(5)
                break
        return amount

    else:
        return limit


print("                    %                   ")
print("                 %%%%%.                 ")
print("                @@@@@%%                 ")
print("              (@@   @@@                 ")
print("                                        ")
print("        ,,,,,,,,,,,,,,,,,,      .@@%%%% ")
print("      ,,,,,,,,@@@@@@&,,,,,,.  ,@@@@@&%%%")
print("     ,,,,,,@@@@@*,#@@@@*,,,,,     @@%%% ")
print("   ,,,,,,,@@@,,,,,,,,@@@/,,,,,    @@    ")
print("  ,,,,,,,,@@@@@@@@@@@@@@&,,,,,,         ")
print(" ,,,,,,,,,@@@@,,,,,,(,,,,,,,,,,,,       ")
print(" ,,,,,,,,,,,@@@@@@@@@@,,,,,,,,,,        ")
print("   ,,,,,,,,,,,,,,,,,,,,,,,,,,,,         ")
print("    ,,,,,,,,,,,,,,,,,,,,,,,,,           ")
print("      ,,,,,,,,,,,,,,,,,,,,,,            ")
print("       ,,,,,,,,,,,,,,,,,,,,             ")
print()

UserAgent = {"User-Agent": "e621Downloader/1.0 (by AmongUsPopIt on e621)"} 

print("-Made by Gerdvibis on GitHub")
tags = input("What are the tags: ")
tags = tags.replace(" ", "+")
limit = int(input("How many posts do you want to save (0 for unlimited): "))
if limit == 0:
    limit = 320

postAmount = postCount(tags, limit)

print("How do you want to choose the directory?")
try:
    filePathMode = int(input("1. Cli, 2. Window: "))
except:
    input("You have to enter a number")
    exit()

cls()

if filePathMode == 1:
    filepath = input("Paste the directory of your desired location here: ")
if filePathMode == 2:
    print("Opening window..")
    filepath = filedialog.askdirectory()

i = -1
imageOrder = 0

postID_Url = f"https://e621.net/posts.json?limit=1&tags={tags}"
postID_Request = requests.get(url = postID_Url, headers=UserAgent)
postID_Data = postID_Request.json()
currentID = postID_Data["posts"][0]["id"]

while True:
    i += 1
    URL = f"https://e621.net/posts.json?page=b{currentID}&limit={limit}&tags={tags}"
    #request
    r = requests.get(url = URL, headers=UserAgent)
    data = r.json()

    length = len(data["posts"]) - 1
    currentID = data["posts"][length]["id"]

    fileList = []

    #add links to a list
    for x in range(0, len(data["posts"])):
        if data["posts"][x]["file"]["url"] != "None":
            fileList.append(data["posts"][x]["file"]["url"])

    #checking if directory is valid
    try:
        open(f"{filepath}/e621.txt" ,"w").write("Thank you for using my script \nhttps://github.com/JustSypth/e621-Downloader")
    except:
        cls()
        input("You either entered an invalid directory or you don't have permissions..")
        exit()


    #export files from the list
    for y in range(0, len(fileList)):
        cls()
        print(f"Downloading File {imageOrder} of {postAmount}")

        percentage = round(imageOrder / postAmount * 100)

        if percentage <= 10:
            print(f"|■---------| {percentage}%")
        elif percentage <= 20:
            print(f"|■■--------| {percentage}%")
        elif percentage <= 30:
            print(f"|■■■-------| {percentage}%")
        elif percentage <= 40:
            print(f"|■■■■------| {percentage}%")
        elif percentage <= 50:
            print(f"|■■■■■-----| {percentage}%")
        elif percentage <= 60:
            print(f"|■■■■■■----| {percentage}%")
        elif percentage <= 70:
            print(f"|■■■■■■■---| {percentage}%")
        elif percentage <= 80:
            print(f"|■■■■■■■■--| {percentage}%")
        elif percentage < 100:
            print(f"|■■■■■■■■■-| {percentage}%")
        elif percentage == 100:
            print(f"|■■■■■■■■■■| {percentage}%")
        
        try:
            rFiles = requests.get(fileList[y])
            imageOrder += 1
            isNone = False
        except:
            isNone = True

        extension = str(data["posts"][y]["file"]["ext"])

        if isNone == False:
            if extension == "jpg" or extension == "jpeg":
                open(f"{filepath}/file{imageOrder}.jpg" ,"wb").write(rFiles.content)
            elif extension == "png":
                open(f"{filepath}/file{imageOrder}.png" ,"wb").write(rFiles.content)
            elif extension == "gif":
                open(f"{filepath}/file{imageOrder}.gif","wb").write(rFiles.content)
            elif extension == "webm":
                open(f"{filepath}/file{imageOrder}.webm","wb").write(rFiles.content)

        if int(imageOrder) >= int(postAmount):
            time.sleep(2)
            isDone = True
            break
        else:
            isDone = False

    if isDone == True:
        break
