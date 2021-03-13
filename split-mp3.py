# if there is a yt video made up of multiple music videos and you have the name of the song and the start time of the song, 
# it will extract all the individual songs

from dataclasses import dataclass
import csv
from sys import prefix
from typing import Counter, List
import subprocess
import colorama

colorama.init(autoreset=True)

# name of the file to split. should be in the same directory
# youtube-dl --extract-audio --audio-format mp3 <URL>
fileName = ' lofi beats to code to-f02mOEt11OQ.mp3'

@dataclass
class CustomTime:
    hour: int
    minute: int
    second: int

    def  __str__(self):
        return f"{str(self.hour).rjust(2, '0')}:{str(self.minute).rjust(2, '0')}:{str(self.second).rjust(2, '0')}"

@dataclass
class Extract:
    start_time: CustomTime
    end_time: CustomTime
    name: str



extractList: List[Extract] = []
with open('input.csv', 'r', ) as f:
    # get data from CSV
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        name = row['name']
        start_time = row['start_time']
        start_time = start_time.split(':')

        #handle weird uniocode error
        start_time[-1] = start_time[-1].replace('\u200b', '')


        if len(start_time) == 2:
            # no hour component
            start_time_object = CustomTime(00,start_time[0], start_time[1])
        else:
            start_time_object = CustomTime(start_time[0], start_time[1], start_time[2])

        # store the start time and name. set the end time to be 0
        extractList.append(Extract(start_time_object, CustomTime(0,0,0), name))

# we calculate the end time for the last song which is how long the song is
fullTime = CustomTime(1, 0, 20)
extractList[-1].end_time = fullTime

# go through all the songs, for song at index i, we set the end time to be the start_time of song at index i + 1
# the end time is subtracted by 1 as we have already set the end time of the last song
for i in range(0, len(extractList) - 1):
    extractList[i].end_time = extractList[i + 1].start_time

count = len(extractList)
start = 0
for i in extractList:
    padWidth = len(str(count)) + 1
    prefix = str(start).rjust(padWidth, '0')
    outFileName = prefix + '-' + i.name + '.mp3'

    ffmpeg_command = ['ffmpeg', '-i', fileName, '-ss', str(i.start_time), '-to', str(i.end_time), outFileName]
    print(colorama.Fore.BLUE + colorama.Style.BRIGHT + str(ffmpeg_command))
    subprocess.run(ffmpeg_command)
    start = start + 1
