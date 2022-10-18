import os
import time
import requests
import random

def setRandomWallPaper():
    available = getAvailableWallPapers()
    if len(available)>0:
        randWallpaper = available[random.randint(0,len(available)-1)]
        os.rename("/home/gtm/Desktop/Wallpapers/{0}".format(randWallpaper), "/home/{username}/Desktop/Wallpapers/wp.jpg")

    #for ubuntu
    os.system("gsettings set org.gnome.desktop.background picture-uri-dark 'file:///home/{username}/Desktop/Wallpapers/wp.jpg'")

def checkWpExists(i):
    if os.path.isfile("/home/gtm/Desktop/Wallpapers/{0}.jpg".format(i)):
        return True
    else:
        return False

def getAvailableWallPapers():
    wallpapers = []
    for file in os.listdir("/home/{username}/Desktop/Wallpapers"):
        if file.endswith(".jpg") and file.startswith("wp")==False:
            wallpapers.append(file)
    return wallpapers

def downloadWallPapers():
    available = getAvailableWallPapers()
    if len(available) == 0:
        changeAfterDownloading = True
    else:
        changeAfterDownloading = False
    try:
        for i in range (1,maxSavedWallpapers+1):
            if checkWpExists(i)==False:
                r1 = requests.get("https://source.unsplash.com/random/1920x1080/?mountains,code")   #can also use like ?city,night (comma-seperated)
                with open("/home/{username}/Desktop/Wallpapers/{0}.jpg".format(i), 'wb') as f:
                    f.write(r1.content)
        
        if changeAfterDownloading:
            setRandomWallPaper()
            downloadWallPapers()

    except requests.ConnectionError:
        notify("Wallpapers not downloaded","Not connected to the Internet.")
        if keepTrying:
            time.sleep(pingRate)
            downloadWallPapers()

def notify(title, text):
    os.system('notify-send "'+title+'" "'+text+'"')


if __name__ == "__main__":
    maxSavedWallpapers = 5
    pingRate = 300
    keepTrying = False
    available = getAvailableWallPapers()
    setRandomWallPaper()
    time.sleep(120) #2 mins is probable enough to get online
    downloadWallPapers()
