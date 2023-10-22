# Feature list & bugs
## Features
- [x] Automatically find video files in a given directory
- [x] Provide a list with all detected content timecodes
- [x] Render blurred video file accordingly to detected events (whole screen) 
- [ ] Render blur only on zones where events detected (should slow processing)
- [x] Semi automatic mode (manual NSFW timecodes filling + auto render) to circumvent nudenet detection errors
- [x] Linux support ( and may work on BSD/MAC as well )
- [x] Windows support ( tested on windows 11 )
- [x] Use Binary buffer instead of hard drive for video image storing
- [x] Embed nudenet modified API (with Binary buffer) + onnx file 
- [x] Do not analyze/process video filenames containing "censored_"
- [x] Tested formats : mkv, avi, mp4
- [x] Filenames including spaces support
- [ ] Create a way to filter Automatic nude detection false positives / negatives
- [ ] if Human Centipede detected, replace with empty file
## Bugs
- [x]  Blur radius = 100 fails on some files (max 64)
- [ ] Automatic nude detection false positives / negatives

# History
## V0.1 22102023
- [x] Updated instructions in HTML and Markdown formats
- [x] Gif tutorials (some may not be up to date/complete , sorry for dummies)
- [x] IPFS storage CID : QmUYs1ffkXiXkUr8EZRTgfFmPjRNcX3QFdyoFumpVp6xsz
- [x] Subfolders to clean directories a bit
- [x] Full space containing path compatibility
- [x] Tested & Validated on Win 10, Win 11, Linux 

## Tests
### Blue is the warmest color:
180mn 720 p : 27 minutes analysis, 27 minutes rendering
#### results: 
 - >=1   false negative MALE_GENITALS_EXPOSED
 - >=1   false negative FEMALE_GENITALS_EXPOSED
 - >=10  false positive MALE_GENITALS_EXPOSED
 - >=2   false positive FEMALE_GENITALS_EXPOSED
#### observations:
 - most false positives duration = 1 second
 - most frequent false positive : MALE_GENITALS_EXPOSED

### C'est arrive pres de chez vous:
90mn 420 p : 6 minutes analysis, 10 minutes rendering
#### results: 
 - 1 blur too short (1'03'20 r4p3 scene)
 to be continued
#### observations:
 - FFMPEG rendering failed cause radius >64 (100)
 
### Enter the void CD1:
80mn 420 p : 6 minutes analysis, 10 minutes rendering
#### results: 
 - 1 blur too short (1'03'20 r4p3 scene)
 to be continued
#### observations:
 - FFMPEG rendering failed cause radius >64 (100)
