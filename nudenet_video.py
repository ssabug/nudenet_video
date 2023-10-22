from nudenet_mod import NudeDetector;
import cv2;
import sys;
import os;
import math;
import copy;
import datetime;
import platform;
import io;
from string import Template;

videoFileExtensions=["mp4","avi","mkv","wmv"];
forbiddenAlerts=["MALE_GENITALIA_EXPOSED","FEMALE_GENITALIA_EXPOSED","ANUS_EXPOSED"];
analysisRate=1.0;
groupingTimeWindow=10;
timeMargin=1.0;
writeToFile=True;
cutVideoFile=True;
blurRadius=40; #100 doesnt work on some files (see tests)


#========================= UTILITIES =======================================================================================================
def displayParameters():
	print("/// Parameters :");
	print("/// Analyse video each " + str(analysisRate) + " seconds");
	print("/// Regroup alerts range : " + str(groupingTimeWindow) + " seconds");
	print("/// Time margin for blurring  : " + str(timeMargin) + " seconds");
	print("/// Write result to text file : " + str(writeToFile) );
	print("/// Render censored videos : " + str(cutVideoFile) );
	print("/// Blur radius : " + str(blurRadius) );
	print("/// Blurred content : ");
	print(forbiddenAlerts);
	
	print();

class DeltaTemplate(Template):
    delimiter = "%"
    
def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

def brosweDirectory(path):
	#dir_path = r'E:\account';
	result=[];
	if os.path.exists(path):

		for file in os.listdir(path):
			for extension in videoFileExtensions:
				if file.endswith("."+ extension) and file.find("censored_") < 0:
					result.append(file);
	return result;
	
	
def checkInputArguments():
	if len(sys.argv)<2:
		print("ERROR : please provide the folder to scan videos as command argument (ex : python nudenet_video.py C:\Videos\Hentai\ )" );
		return -1;
		
	if not os.path.exists (sys.argv[1]):
		print("ERROR : folder " +  sys.argv[1] + " does not exist" );
		print("NOTE: this program does not support path/filenames containing spaces for now");
		return -2;
		
	if os.path.isfile(sys.argv[1]):
		return 2;
	else :
		return 1
		
	return 0	;
	
#=============================== VIDEO ANALYSIS =================================================================================================	
def analyzeVideo(videoPath):
	analysisStartTime=datetime.datetime.now();
	print("/// Analysis started @ " + str(analysisStartTime));
	#open video
	video = cv2.VideoCapture(videoPath);
	# count the number of frames
	fps = video.get(cv2.CAP_PROP_FPS)
	totalNoFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
	durationInSeconds = totalNoFrames // fps
	print("/// video duration : " + str(durationInSeconds/60) + " minutes");

	nude_detector = NudeDetector();

	frameno = 0;
	nudeDetections = [];
	lastTimecode=0;
	while(True):
		ret,frame = video.read()
		if ret:
			timecode = frameno / fps;

			if timecode-lastTimecode > analysisRate:
				# if video is still left continue creating images
				name = 'buffer.jpg'
				#print ('new frame captured...' + name)
				#cv2.imwrite(name, frame);
				is_success, buffer = cv2.imencode(".jpg", frame)
				io_buf = io.BytesIO(buffer)

				
				frameNudeDetections=filterNudeDetection(nude_detector.detect(io_buf),timecode);
				for el in frameNudeDetections: 
					nudeDetections.append(el);
				lastTimecode=timecode;
			frameno += 1;
			
		else:
			break

	#video.release()
	#cv2.destroyAllWindows()
	analysisDuration=datetime.datetime.now()-analysisStartTime;
	print("/// Analysis ended, duration " + str(analysisDuration) );
	return nudeDetections

#=============================== DATA PRINTING =================================================================================================

def printDetections(video,detections,path=""):

	headers=["file="  + path + video + ";","[[  start  ], [   end   ], [           event                     ]"];
	
	if writeToFile:
		f=open(path+'nude_detection.txt', 'a');
    
	for header in headers:
		if writeToFile:
			f.write(header+"\n");
		else:
			print(header);
  
	detections_deepcopy = copy.deepcopy(detections)	
  	
	for p in detections_deepcopy:
		p[0]=strfdelta(datetime.timedelta(0, p[0]), '%H:%M:%S');
		p[1]=strfdelta(datetime.timedelta(0, p[1]), '%H:%M:%S');
		#p[0]=datetime.timedelta(days=0, seconds=p[0], microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0).strftime("%H:%M:%S");
		#p[1]=datetime.timedelta(days=0, seconds=p[1], microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0).strftime("%H:%M:%S");
		if writeToFile:
			f.write(str(p)+"\n");
		else:
			print(p);
			
	if writeToFile:
		f.close;

#=============================== DATA PROCESSING =================================================================================================

def processDetections(nudeDetections):
	print("/// processing all detected content, " + str(len(nudeDetections))+ " found");
	analysisStartTime=datetime.datetime.now();
	processedDetections=[];
	for i,nude in enumerate(nudeDetections):
		detectedEventCount=len(processedDetections);
		if detectedEventCount != 0:
			lastElement=processedDetections[detectedEventCount-1];
			if nude[0] - lastElement[1] <= groupingTimeWindow : # and lastElement[2]["class"] == nude[1]["class"]
				lastElement[1]=nude[0];
			else:
				processedDetections.append([nude[0],nude[0],nude[1]]);
		else:
			processedDetections.append([nude[0],nude[0],nude[1]]);

	analysisDuration=datetime.datetime.now()-analysisStartTime;
	print("/// Processing ended,  " + str(analysisDuration));
	print("/// " + str(len(processedDetections)) +  " elements after processing");
	
	
	#for e in processedDetections:
	#	print(e);
	
	return processedDetections;

		
def filterNudeDetection(nudeDetection,timecode):
	result=[];
     
	for alert in nudeDetection:
		if alert["class"] in forbiddenAlerts:
			result.append([timecode,alert]);
        	
	return result; 

def analyzeVideoList(videoList):

	for video in videoList:
		nudeDetections=analyzeVideo(video);
		processDetections(nudeDetections);
		

#=============================== VIDEO PROCESSING =================================================================================================	
	
def renderCensoredVideo(path,video,processedDetections):

	outFile=path+"censored_"+video;
	analysisStartTime=datetime.datetime.now();
	print("/// Starting censored video file rendering using FFMpeg @ " + str(analysisStartTime) + "...");
	
	secondsRemoved=0;
	if len(processedDetections) >0 :
		command='ffmpeg -hide_banner -loglevel error -y -i "' + path + video + '" -filter_complex "';
		command+="[0:v]";
		i=0;
		for alert in enumerate(processedDetections):
			#command+='[0:v]trim=start='+str(alert[1][0])+':end='+str(alert[1][1])+',setpts=PTS-STARTPTS[vid' +str(i) + ']; $';
			#command+='[0:a]atrim=start='+str(alert[1][0])+':end='+str(alert[1][1])+',asetpts=PTS-STARTPTS[aud' +str(i) + ']; $';
			#"[0:v]boxblur=100:enable='between(t,0,5)',boxblur=100:enable='between(t,10,15)'[v]" \
			#-map "[v]" -map 0:a -c:v libx264 -c:a copy -movflags +faststart 70571_censored.mp4
			if alert[1][0] < timeMargin:
				fixedTimeMargin=0;
			else:
				fixedTimeMargin=timeMargin;
			command+="boxblur="+str(blurRadius)+":enable='between(t,"+str(alert[1][0]- fixedTimeMargin )+','+str(alert[1][1]+timeMargin)+")',";
			secondsRemoved+=fixedTimeMargin + timeMargin + alert[1][1]-alert[1][0];
			if i>0:
				#command+='[vid' + str(i-1) + ']' + '[vid' + str(i) + ']concat[vid' + str(i+1) + '];' ;
				#command+='[aud' + str(i-1) + ']' + '[aud' + str(i) + ']concat=v=0:a=1[aud' + str(i+1) + '];$' ;
				i+=1;
			i+=1;
			
		i-=1;
		command=command[:len(command)-1];
		#command+='" -map [vid' + str(i) + '] -map [aud' + str(i)+ '] '+ outFile ;
		#command=command.replace("$", str(chr (92))+ "\n" );
		command+='[v]"'
		command+=' -map "[v]" -map 0:a -c:v libx264 -c:a copy -movflags +faststart "' + outFile + '"';
		

		#for c in command.split('^')	:
		#	print (c);
		#print(command);
			
		ffmpeg=os.system(command)	
		print("/// FFMpeg returned exit code %d" % ffmpeg);
		
		analysisDuration=datetime.datetime.now()-analysisStartTime;
		print("/// FFMpeg rendering ended, duration " + str(analysisDuration));
		print ("/// " + str(secondsRemoved) + " seconds of video have been blurred");
		print("/// output file : " + outFile);		
	else:
		print("/// No alerts, no censored file created");

#=============================== render from file =====================================================================================
def stringTimecodeToSeconds(string):
	
	value=0;
	for i,e in enumerate(string.split(":")):
		value+=int(e)*(60**(2-i));
	
	#print (string + " " + str(value));
		
	return value;

def extractCensorData(line):
		#print(line);
		lineData=line.split(",");
		
		if len(lineData) >= 3:
			startTime=stringTimecodeToSeconds(lineData[0][2:-1]);
			endTime=stringTimecodeToSeconds(lineData[1][2:-1]);
			alert=lineData[2];
			#print (startTime + " " + endTime + " " + alert);
			return  [startTime,endTime,alert];
		else : 
			return [0,0,""];

def loadFile(inputFile):
	fileHeader="file=";
	endFileHeaderChar=";";
	
	f = open(inputFile, "r");

	videoFile="";
	currentFileData=[];
	outputData=[];
	for line in f:
		#print(line) ;
		if line.find(fileHeader) != -1 :
				if videoFile != "" :
					if len(currentFileData) > 1:
						outputData.append(currentFileData);
						currentFileData=[];
				videoFile=line[len(fileHeader):line.find(endFileHeaderChar)+1];
				currentFileData.append(videoFile);
			#print(videoFile);
		else :
			if videoFile != "" :
					lineData=extractCensorData(line);
					startTime=lineData[0];
					endTime=lineData[1];
					alert=lineData[2];
					currentFileData.append([float(startTime),float(endTime) ,alert]);
					
	if len(currentFileData)>1:
		 outputData.append(currentFileData);
					
	#for e in outputData:
	#	for i in e:
	#		print(i);
					
	return 	outputData;
		
#=============================== MAIN =================================================================================================		

def main():

	print("/////////////////////////////////////////////////////////////" );
	print("///                  VIDEO NUDE DETECTOR                  ///" );
	print("/////////////////////////////////////////////////////////////" );
	print();
	
	# FULL AUTOMATIC MODE (analysis + rendering)
	if checkInputArguments()==1 :
		
		path=sys.argv[1];
		fileList=brosweDirectory(path);
		
		print("/// Full Automatic mode selected ");
		print("/// Analyzing folder " + path +", "+ str(len(fileList))+ " videos found");
		displayParameters();
		
		for i,video in enumerate(fileList):
			print("/// Video " + str(i+1) +" / "+ str(len(fileList)) + " : " + path + video);
			videoPath=path+video;
			nudeDetections=analyzeVideo(videoPath);
			processedDetections=processDetections(nudeDetections);
			printDetections(video,processedDetections,path);
			
			if cutVideoFile:
				renderCensoredVideo(path,video,processedDetections);
				a=1;
				
			print();
	
	# SEMI AUTOMATIC MODE (manual analysis + auto rendering)		
	elif checkInputArguments()==2 :
	
		timecodeFile=sys.argv[1];
	
		print("/// Semi Automatic mode selected ");
		print("/// Analyzing timecode file " + timecodeFile );
		displayParameters();
		
		outputData=loadFile(timecodeFile);
		for fileData in outputData:
			filename=fileData[0][:-1];
			#print (filename);
			fileData=fileData[1:];
			#for e in fileData:
				#print(str(e));
			if len(fileData) != 0:
				if str(platform.platform()).lower().find ("linux") >=0:
					separator="/";
				else :
					separator=str(chr (92));
				
				video=filename.split(separator)[len(filename.split(separator))-1];
				path=filename[:filename.find(video)];

				print("/// Video " + path + video);

				renderCensoredVideo(path,video,fileData);
		
				print();
				
	print("/// Program ended ");


           
main();        	
         
         

