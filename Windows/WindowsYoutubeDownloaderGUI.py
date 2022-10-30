#
#
#             This GUI was made my Jacob Joseph Bejarano
#                  Contact: JacobJBejarano@gmail.com
#                         GitHub: JakeJayB
#          
#      LinkedIn: https://www.linkedin.com/in/jacob-j-bejarano-74347b230/
#          GitHub: https://github.com/JakeJayB?tab=repositories
#       
#
#                     Updated as of: October 30, 2022 
#
#           Dependencies: pytube, youtubesearchpython, moviepy.editor
#          Note: dependencies must be installed for this program to work
#
###############################################################################################################################

import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
from moviepy.editor import *

# A class that stores the user-specified video information
class Video:
    def __init__(self, link, title, date, views, thumbnail) -> None:
        self.videoLink = link
        self.videoTitle = title
        self.videoDate = date
        self.videoViews = views
        self.videoThumbnail = thumbnail

    def get_link(self):
        return self.videoLink

    def get_title(self):
        return self.videoTitle

    def get_date(self):
        if self.videoDate == None:
            return "N/A"
        return self.videoDate
    def get_views(self):
        return self.videoViews

    def get_thumbnail(self):  
        return self.videoThumbnail
    

# used to store download into user-specified path
userPath = None

# this is a "Video" object
# this object is used for storing and printing the user-specified video information
vidObject = None

# downloadOptions lists all download options the user can choose from
downloadOptions = ["Download Whole Video with Audio" , "Download Audio Only", "Cancel Download"]

# This is used when downloading audio only
# unusableChar is used to check the title of the youtube video to ensure they don't have certain characters
# Reasoning: Window's file explorer and pytube doesn't allow certain characters in a file's name. 
unusableChar = {'/', '\\', ':', '.', ',', "'", '*', '?', '"', '<', '>', '|'}

maxHorizontalLength = 7 * 14
maxVerticalLength = 33
currentLinesUsed = 0
isDownloadDone = True
isPathSet = False
isVideoSelected = False
userVideo = None
downloadOptionSelected = False
userAction = None


def outputSubmitButton():
    global outputReponseBox
    global isPathSet
    global isVideoSelected
    global downloadOptionSelected

    if isPathSet == False:
        global userPath
        userPath.set(outputReponseBox.get()) 
        outputReponseBox.delete(0, END)
        isPathSet = True
    elif isVideoSelected == False:
        global userVideo
        userVideo.set(outputReponseBox.get())
        outputReponseBox.delete(0, END)
        isVideoSelected = True
    elif downloadOptionSelected == False:
        global userAction
        userAction.set(outputReponseBox.get())
        outputReponseBox.delete(0, END)
        downloadOptionSelected = True
    
    
def checkOutputBoxHeight(addon):
    global currentLinesUsed
    global outputBox

    currentLinesUsed = currentLinesUsed + addon
    if currentLinesUsed > maxVerticalLength:
        outputBox.config(anchor=N, text= "")
        currentLinesUsed = addon
    

def ModifyPath():
    global userPath
    global outputBox

    checkOutputBoxHeight(1)
    outputBox.config(anchor=N, text= outputBox.cget("text") + "Where would you like to store your videos? (Copy and Paste a path)\n")

    userPath = StringVar()
    root.wait_variable(userPath)

    userPath = userPath.get().replace("\\", "/")
    userPath = userPath.replace('"', '')


def download(modifiedStream):
    global vidObject

    try:
        modifiedStream.download(output_path=userPath)
    except:
        checkOutputBoxHeight(2)
        outputBox.config(anchor=N, text= outputBox.cget("text") + "Video failed to download. Please try again or download a different video." + "\n")
        outputBox.config(anchor=N, text= outputBox.cget("text") + "-" * maxHorizontalLength + "\n")
        del vidObject
        return
    
    count = 2
    try:
        checkOutputBoxHeight(5)
        outputBox.config(anchor=N, text= outputBox.cget("text") + "Title: " + vidObject.get_title() + "\n")
        count -= 1
        outputBox.config(anchor=N, text= outputBox.cget("text") + "Uploaded: " + vidObject.get_date() + " Views: " + str(vidObject.get_views()) + "\n")   
    except:
        checkOutputBoxHeight(-count)
        pass
    
    outputBox.config(anchor=N, text= outputBox.cget("text") + "Downloading..." + "\n")
    
    outputBox.config(anchor=N, text= outputBox.cget("text") + "Download Completed!" + "\n")
    outputBox.config(anchor=N, text= outputBox.cget("text") + "-" * maxHorizontalLength + "\n")
    del vidObject


def convertAudioToMP3(modifiedStream):
    song = vidObject.get_title()
    download(modifiedStream)

    count = 0
    for char in song:
        if char in unusableChar:
            song = song.replace(song[count], "", 1)
            continue
        count = count + 1


    webmPath = userPath + "/" + song + ".webm"
    audioClip = AudioFileClip(webmPath)

    finalPath = userPath + "/" + song + ".mp3"
    audioClip.write_audiofile(finalPath)
    audioClip.close()

    os.remove(webmPath)


def WhichCoding():
    global outputBox
    global userAction
    global downloadOptionSelected

    checkOutputBoxHeight(1)
    outputBox.config(anchor=N, text= outputBox.cget("text") + "-" * maxHorizontalLength + "\n")

    while True:
        checkOutputBoxHeight(4)
        for i, option in enumerate(downloadOptions):
            outputBox.config(anchor=N, text= outputBox.cget("text") + str(i+1) + ": " + option + "\n")
        outputBox.config(anchor=N, text= outputBox.cget("text") + "Pick a download option:\n")

        userAction = IntVar()
        try:
            root.wait_variable(userAction)
            userAction = int(userAction.get()) 
            if userAction < 1 or userAction > 3:
                checkOutputBoxHeight(1)
                outputBox.config(anchor=N, text= outputBox.cget("text") + "ERROR: Enter a number in the valid range..." + "\n")
                downloadOptionSelected = False  
                continue
            break
        except:
            checkOutputBoxHeight(1)
            outputBox.config(anchor=N, text= outputBox.cget("text") + "ERROR: Numeral Characters Only..." + "\n")
            downloadOptionSelected = False  
            continue
    checkOutputBoxHeight(1)
    outputBox.config(anchor=N, text= outputBox.cget("text") + "-" * maxHorizontalLength + "\n")
    return userAction-1


def ModifiyStreamYSP():
    global vidObject
    global userAction

    userAction = WhichCoding()
    
    match userAction:
        case 0:
            modifiedStream = YouTube(vidObject.get_link()).streams.filter(file_extension="mp4", type="video", progressive=True).get_highest_resolution()
            download(modifiedStream)
        case 1:
            modifiedStream = YouTube(vidObject.get_link()).streams.filter(only_audio = True, file_extension='webm').get_by_itag(251)
            convertAudioToMP3(modifiedStream)
        case 2:
            del vidObject
            return 


def youtubeSearchPython(videoTitle):
    global vidObject
    global userVideo
    global isVideoSelected
    
    checkOutputBoxHeight(1)
    outputBox.config(anchor=N, text= outputBox.cget("text") + "-" * maxHorizontalLength + "\n")
    
    videoSearch = VideosSearch(videoTitle, limit = 5)

    while True:
        userVideo = StringVar()
        checkOutputBoxHeight(8)
        outputBox.config(anchor=N, text= outputBox.cget("text") + "Video Options:\n")
        for i in range(5):
            outputBox.config(anchor=N, text= outputBox.cget("text") + str(i+1) + ": " + videoSearch.result()["result"][i]["title"] + "\n")
        outputBox.config(anchor=N, text= outputBox.cget("text") + "6: PRINT NEXT PAGE RESULTS\n")
        outputBox.config(anchor=N, text= outputBox.cget("text") + "Which video would you like to download?:\n")
        
        root.wait_variable(userVideo)
        try:
            userVideo = int(userVideo.get()) -1
            if userVideo < 0 or userVideo > 5:
                checkOutputBoxHeight(1)
                outputBox.config(anchor=N, text= outputBox.cget("text") + "ERROR: Enter a number in the valid range..." + "\n")
                isVideoSelected = False 
                continue
        except:
            checkOutputBoxHeight(1)
            outputBox.config(anchor=N, text= outputBox.cget("text") + "ERROR: Numeral Characters Only..." + "\n")
            isVideoSelected = False  
            continue
        
        # this match statement will assign the one videoObject object to the user-specified video 
        match userVideo:
            case 0:
                vidObject = Video(videoSearch.result()["result"][0]["link"], videoSearch.result()["result"][0]["title"], videoSearch.result()["result"][0]["publishedTime"], 
                            videoSearch.result()["result"][0]["viewCount"]["text"], videoSearch.result()["result"][0]["thumbnails"][0]["url"])
                ModifiyStreamYSP()
                return
            case 1:
                vidObject = Video(videoSearch.result()["result"][1]["link"], videoSearch.result()["result"][1]["title"], videoSearch.result()["result"][1]["publishedTime"], 
                            videoSearch.result()["result"][1]["viewCount"]["text"], videoSearch.result()["result"][1]["thumbnails"][0]["url"])
                ModifiyStreamYSP()
                return
            case 2:
                vidObject = Video(videoSearch.result()["result"][2]["link"], videoSearch.result()["result"][2]["title"], videoSearch.result()["result"][2]["publishedTime"], 
                            videoSearch.result()["result"][2]["viewCount"]["text"], videoSearch.result()["result"][2]["thumbnails"][0]["url"])
                ModifiyStreamYSP()
                return
            case 3:
                vidObject = Video(videoSearch.result()["result"][3]["link"], videoSearch.result()["result"][3]["title"], videoSearch.result()["result"][3]["publishedTime"],
                            videoSearch.result()["result"][3]["viewCount"]["text"], videoSearch.result()["result"][3]["thumbnails"][0]["url"])
                ModifiyStreamYSP()
                return
            case 4:
                vidObject = Video(videoSearch.result()["result"][4]["link"], videoSearch.result()["result"][4]["title"], videoSearch.result()["result"][1]["publishedTime"], 
                            videoSearch.result()["result"][4]["viewCount"]["text"], videoSearch.result()["result"][4]["thumbnails"][0]["url"])
                ModifiyStreamYSP()
                return
            case 5:
                videoSearch.next()
                isVideoSelected = False
                continue


def get_written_date(date_list):
    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    if len(date_list) !=3:
        return None
    if type(date_list[0]) != str:
        return None
    if type(date_list[1]) != str:
        return None
    if type(date_list[2]) != str:
        return None

    year_tup = int(date_list[0])
    month_voc = int(date_list[1])
    month_tup = month_names[month_voc]
    day_tup = int(date_list[2])
    # Return the date string in written format
    return(f'{month_tup} {day_tup}, {year_tup}')


def pytube(video):  
    global vidObject
    video = YouTube(video)

    userAction = WhichCoding()
    while True:
        match userAction:
            case 0:
                modifiedStream = video.streams.filter(file_extension="mp4", type="video", progressive=True).get_highest_resolution()
                vidObject = Video(None, video.title, get_written_date(str(video.publish_date)[:10].split('-')), video.views, video.thumbnail_url)
                download(modifiedStream)
                return
            case 1:
                modifiedStream = video.streams.filter(only_audio = True, file_extension="webm").get_by_itag(251) #video.streams.filter(only_audio = True, file_extension='mp4').get_audio_only()
                vidObject = Video(None, video.title, get_written_date(str(video.publish_date)[:10].split('-')), video.views, video.thumbnail_url)
                convertAudioToMP3(modifiedStream)
                return
            case 2:
                return  

def main():
    global inputBox
    global outputBox
    global downloadOptionSelected
    global isVideoSelected

    userVideo = inputBox.get()
    outputReponseBox.config(state=NORMAL)
    submitOutputButton.config(state=NORMAL)
    inputBox.config(state=DISABLED)
    submitInputButton.config(state=DISABLED)    
    if(isPathSet == False):
        ModifyPath() #"C:\Users\modre\Videos\Captures"

    try:
        YouTube(userVideo)
        isVideoSelected = True
        print("Pytube")
        pytube(userVideo)
    except:    
        youtubeSearchPython(userVideo)
        print("YoutubeSearch")
            
    checkOutputBoxHeight(2)
    outputBox.config(anchor=N, text= outputBox.cget("text") + "Thank you for using this program! You're now able to download more videos!\nReset the program if you want to change the destination path\n")
    submitInputButton.config(state=NORMAL)
    inputBox.config(state=NORMAL)
    outputReponseBox.config(state=DISABLED)
    submitOutputButton.config(state=DISABLED)
    inputBox.delete(0, END)
    downloadOptionSelected = False
    isVideoSelected = False



#                                          End of Youtube Downloader functionality...
##############################################################################################################################
#
#
#                           (Note:)
#       Everything down below is related to creating the GUI
#
#
#
from tkinter import *
from PIL import Image, ImageTk

#Header GUI
root = Tk()
root.title("Youtube Downloader GUI")
root.iconbitmap("Windows\Photos\YoutubeIcon.ico")
root.geometry("835x826")


# Tab GUI
menuBar = Menu(root)
root.config(menu=menuBar)

homeMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Home", menu=homeMenu)
homeMenu.add_command(label="Go Home")

infoMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Info", menu=infoMenu)
infoMenu.add_command(label="About")
infoMenu.add_separator()
infoMenu.add_command(label="Contact Creator")


#MainGUI
youtubeImage = PhotoImage(file="Windows\Photos\YoutubePNG.png")
mainFrame = Frame(root)
mainText = Label(mainFrame, bg="#205978",fg='white', font=('Arial', 25, 'bold'),relief=RAISED, bd=8, image=youtubeImage, compound='right', text="Welcome to Youtube Downloader GUI\nMade by Jacob J. Bejarano")
infoText = Label(mainFrame, width=50,  font=('Arial', 10, 'bold'), text="Enter a youtube video title or link you'd like to download:")

inputBoxFrame = Frame(root)
inputBox = Entry(inputBoxFrame, width=120, borderwidth=10, relief=RAISED, bd= 8)
submitInputButton = Button(inputBoxFrame, bg="#DBDBDB",text="Submit", command=lambda: main())


outputBoxFrame = Frame(root, bg="#205978", pady=20)
outputInfoText = Label(outputBoxFrame, width=100, bg="#205978", fg="white", font=('Arial', 9, 'italic', 'bold'), text="\tAfter Entering a URL or title, use the input box below to answer the prompted questions")
outputBox = Label(outputBoxFrame, bg="#8cd3fa", width=100, height=33, relief=SUNKEN, bd=5, anchor=N, text='') #DBDBDB
outputReponseBox = Entry(outputBoxFrame, width=100,  borderwidth=10, relief=RAISED, state=DISABLED, bd= 4) 
submitOutputButton = Button(outputBoxFrame, bg="#DBDBDB", text="Submit", state=DISABLED, command=outputSubmitButton)
# outputBox.config(anchor=NW, text= outputBox.cget("text")[(maxHorizontalLength + 1) * 5:])

mainFrame.grid(row=0, column=2, columnspan=2)
mainText.grid(row=0, column=2, columnspan=1, padx=10, pady=5, ipadx=10, ipady=10)
infoText.grid(row=1, column=2, rowspan=1)

inputBoxFrame.grid(row=1, column=2)
inputBox.grid(row=1, column=2)
submitInputButton.grid(row=1, column=3, columnspan=2) 

outputBoxFrame.grid(row=2, column=0, columnspan=5, padx=30, pady= 10)
outputInfoText.grid(row=0, column=0, columnspan=2, rowspan=2)
outputBox.grid(row=2, column=0, columnspan=5, padx=30)
outputReponseBox.grid(row=3, column=0,pady=5, columnspan=5)
submitOutputButton.grid(row=3, column=4) 


root.mainloop()