# Nudenet_video.py


## Description
This python script uses the [NudeNet API](https://github.com/notAI-tech/NudeNet) to detect nudity & [FFMPEG](https://ffmpeg.org/) to render blurred video files.

**NOTE** : The Nudenet algorithm is far from perfect, there will be false positives & negatives, **always verify your files** or use the **semi automatic** method for 100% accuracy.

**NOTE** There are some gifs tutorials in the **tutorials** subfolder, but some may be not up to date, the README file always contains the reference instructions.

**IMPORTANT** for now nothing is optimized, keep in mind the durations of :
 - video analysis : around 1 minute for 5 minutes of 720p 30fps video (180 mn video => 27 mn analysis)
 - video file rendering : will depend of your machine capabilities too and takes time as well 

## Features, history and bugs
see ![HISTORY&DEBUG](HISTORY&DEBUG.md) file for more details.

## Requirements
 - python ( prefer installation via microsoft store or download [here](https://www.python.org/downloads/) )
 - pip (should be asked to be installed during windows python setup)
 - ffmpeg ( download [here] (https://ffmpeg.org/download.html) )
 - python libs ( will be automatically installed ) : nudenet, opencv-python, datetime

## Installation
1. Download the zip / git clone the repo.
2. Extract it if necessary.
3. Install python (if not already present) . On Windows, use the **Microsoft Store** and search for **python** . Choose the latest version (3.11 is alright) . If the setup ask you wether to install **pip** , accept.
4. Run a terminal into the extracted directory, to do so:
   - in Windows start menu, search for app **powershell** (you can also use older **command prompt**).
   - Run it.
   - To reach the folder in the terminal type :

    `cd "path_to_nudenet_folder" `

**path_to_nudenet_folder** being where nudenet files were extracted.

Example : if its in **C:\Users\fijishenisdrip\Downloads\Nude_filter**, type:

` cd "C:\Users\fijishenisdrip\Downloads\Nude_filter\" `

   - validate with **Return** key.
   - If you're using Windows 11, you can ignore the previous steps and do it from a file broswer by right clicking into the folder and choosing **Run in terminal**.
5. In the terminal type and validate with **Return** key :

 `pip install -r requirements.txt`

  It will install all python librairies required by the script. It may take a little time.

6. **(Windows only)** Download ffmpeg binaries from https://ffmpeg.org/download.html . If ffmpeg is already installed on the system, go to next step.
7. **(Windows only)** In the downloaded ffmpeg files, find **ffmpeg.exe**.
8. **(Windows only)** copy this file in the nudenet extracted directory.

Im assuming that if you use Linux, you'll know how to use command line and install python/ffmpeg properly.
 
## How to use
### Full automatic mode:
1. Create a empty folder ( example : **C:\CensoredVideos** ).
2. Put all video files you want to analyze & render innit.
3. Run a terminal into the nudenet script directory ( refer to **Installation** step 4 if you don't know how to do it ).
4. Type in the terminal: 

`python nudenet_video.py "path"`

  **path** being the full path to the created folder with videos , ending with / on Linux/Mac or \ on Windows, example :  

  `python nudenet_video.py "C:\CensoredVideos\" `

5. The script will analyze & render a censored video file for each video present in the directory. Details of each operation will be written on the terminal screen.
6. Wait ! Analysis and rendering takes time. It depends of your computer specs.
7. The output videos will be in the same folder as original files, with **censored_** at the beginning of the filename. 

### Semi automatic mode:
1. In the nudenet script directory, do a copy of the file **manual_search.txt** in the **timecode_files** subfolder. 
2. Rename the file if you want, like **censor_list_01.txt**.
3. Open it with a text editor, it should contain blocks of this format:

`file=/home/pwner/Videos/a convertir/092105.mp4;`

`['00:00:01', '00:00:10', {'class': 'MALE_GENITALIA_EXPOSED', 'score': 0.28773850202560425, 'box': [702, 348, 169, 131]}]`

`['00:00:15', '00:00:20', {'class': 'MALE_GENITALIA_EXPOSED', 'score': 0.28749483823776245, 'box': [513, 419, 273, 125]}]`
4. The first part is the complete path to one video to blur. 

If the video file is **C:\Videos\humancentipede.mkv**, line would be :

`file=C:\Videos\humancentipede.mkv;`
5. For the second part, each line contains timecodes to blur.

For instance if you want to blur from **00:01:01** to **00:01:30**, the line would be:

 `['00:01:01', '00:01:30', {'class': 'MALE_GENITALIA_EXPOSED', 'score': 0.28773850202560425, 'box': [702, 348, 169, 131]}]`

  ( the part after the second comma is not taken into account, so leave it as is ).
6. Add as much lines as blurred sections you need.
7. You can add as much videos as you want in the file, just add, for each video, the two sections as defined in steps 4 to 6.
8. Save the file.
9. Type, in a terminal from the nudenet directory ( refer to **Installation** step 4 if you don't know how to do it ).

`python nudenet_video.py "full_path_to_your_file"`

**full_path_to_your_file** being the path to the created text file, example :

`python nudenet_video.py "C:\Users\fijishenisdrip\Downloads\Nude_filter\timecode_files\censor_list_01.txt"`

10. The script will  render a censored video file for each video present in the text file. 

Details of each operation will be written on the terminal screen.
11. Wait ! Rendering takes time. It depends of your computer specs.
12. The output videos will be in the same folder as original files, with **censored_** at the beginning of the filename. 

