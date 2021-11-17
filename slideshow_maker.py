#!/usr/bin/env python
import os
import subprocess
from shutil import copyfile
from pathlib import Path
import ffmpeg

#### video from images
#### 5 second per image (1/5)

### Directory containing folders of photos
dir = r"./"

### File list
files = []

def slideshow_files():
    file_list = []

    subdirs = [x[0] for x in os.walk(dir)]
    
    with open('/tmp/slideshow_maker/titles.srt', 'a') as titles:
        tits = {}
        counter = 1
        for subdir in subdirs:
            files = os.walk(subdir).__next__()[2]
            
            if (len(files) > 0):
                for idx, file in enumerate(files):
                    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                        title = subdir
                        
                        tits[str(counter)] = {}
                        tits[str(counter)] = {'title': title, 'count', 10}

                        if title in tits[len(tits)]:
                            tits[str(counter)][title] += 10
                        else:
                            print("New title")

                        file_list.append(file)
                        counter += 1
                    else:
                        continue
        
        

    print(tits)
    return file_list

def clean_up():
    ### delete tmp files
    for f in Path('/tmp/slideshow_maker').glob('*.*'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s :%S" % (f,e.strerror))
    ### delete local temp dir
    try:
        os.rmdir("/tmp/slideshow_maker")
    except OSError as e:
        print("Error: %s :%S" % (f,e.strerror))


### Create tmp dir if not present
try:
    os.mkdir("/tmp/slideshow_maker")
except:
    print("Temp folder already exists!")

files = slideshow_files()

title = []

for idx, photo in enumerate(files):
    ext = os.path.splitext(photo)[1]
    loc = "./photos/{}".format(photo)
    dest = "/tmp/slideshow_maker/img-{}{}".format(str(idx).zfill(3), ext)
    aname = os.path.dirname(loc).replace("./","")
    title.append(aname)

    try:
        copyfile(loc, dest)
    except:
        print("Error copying file - {}".format(photo))

    print(idx, photo, aname)

###Make film
def save():
    os.system('ffmpeg -framerate 1/10 -pattern_type glob -i "./tmp/*.jpg" -vcodec libx264 -crf 18 -preset veryfast -y -r 30 -pix_fmt yuvj420p ./tmp/out.mp4')

    os.system(f'ffmpeg -i "./tmp/out.mp4"  \
                -vf "subtitles=./tmp/titles.srt,format=yuv420p" \
                -vcodec libx264 -crf 18 -preset veryfast -y -r 30 out.mp4')



clean_up()

#save()
### Delete temp files

#ffmpeg -framerate 1/5 -i img%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
