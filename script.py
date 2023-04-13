import requests
from tkinter import filedialog
import os
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def checkValidTags(data):
    if len(data["posts"]) == 0:
        cls()
        input("You might have entered invalid tag...")
        exit()

def postCount(tags, limit):
    tagList = tags.split("+")
    rTags = requests.get(url = f"https://e621.net/tags.json?search[name_matches]={tagList[0]}", headers=UserAgent)
    postCountData = rTags.json()
    
    if limit == 320:
        try:
            if postCountData[0]["post_count"] != "None":
                number = postCountData[0]["post_count"]
        except:
            pass

        for i in range(0, len(tags)):
            try:
                if postCountData[0]["post_count"] != "None":
                    rTags = requests.get(url = f"https://e621.net/tags.json?search[name_matches]={tagList[i]}", headers=UserAgent)
                    postCountData = rTags.json()

                    if int(postCountData[0]["post_count"]) < number:
                        number = postCountData[0]["post_count"]
            except:
                i -= 1
            

        return number
    else:
        return limit

    

UserAgent = {"User-Agent": "e621Downloader/1.0 (by AmongUsPopIt on e621)"} 

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

print("-Made by Gerdvibis on GitHub")
print("INFO: Using any tag from the Cheatsheet will result in not showing the amount of files that will be downloaded")
tags = input("What are the tags: ")
tags = tags.replace(" ", "+")
limit = int(input("How many posts do you want to save (0 for unlimited): "))
if limit == 0:
    limit = 320

i = 0
imageOrder = 1
postAmount = postCount(tags, limit)
filepath = filedialog.askdirectory()

while True:
    i += 1
    URL = f"https://e621.net/posts.json?page=a{i}&limit={limit}&tags={tags}"
    #request
    r = requests.get(url = URL, headers=UserAgent)
    data = r.json()
    checkValidTags(data)

    fileList = []

    #add links to a list
    for x in range(0, len(data["posts"])):
        if data["posts"][x]["file"]["url"] != "None":
            fileList.append(data["posts"][x]["file"]["url"])

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
