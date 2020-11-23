import os
import glob
import pydub
from moviepy.editor import *
from scipy import signal
from scipy.io import wavfile
import numpy as np

#from scipy import fft
#import matplotlib.pyplot as plt

# !!! Deletes .mp3s and .wav with same name as .mp4 files !!!
# Finds all mp4 files,
# Filters their sound
# Joins filtered sound with original image
# Saves in /results


mp4_files = glob.glob('./*.mp4')                        #Find all mp4 files
print(mp4_files)

for mp4_file in mp4_files:
    mp3_file = os.path.splitext(mp4_file)[0] + '.mp3'   #Check for leftover files not removed from debug or
    wav_file = os.path.splitext(mp4_file)[0] + '.wav'
    if os.path.exists(wav_file):
        os.remove(wav_file)                             #Remove them to avoid errors
    sound = pydub.AudioSegment.from_file(mp4_file, "mp4")
    sound.export(wav_file, format='wav', )
    print("Created", wav_file)
    print("Generating signal from .wav file")


    #FILTERING
    Fs,sound_signal = wavfile.read(wav_file)
    Wlow = 8000/Fs; #Perhaps use bandstop?              #Cutoff @ 8 Khz 2 be sure
    print("Filtering")
    b, a = signal.butter(2, Wlow ,'lowpass')            #butterworth filter parameters
    outputL = signal.lfilter(b,a,sound_signal[:,0]).astype(np.int16)
    outputR = signal.lfilter(b,a,sound_signal[:,1]).astype(np.int16)
    x = np.stack((outputL,outputR), axis=1)             #join left and right channels in numpy array
    print("Filtering - Done")
    wavfile.write(wav_file,Fs,x)
    print("Saved  ",wav_file," file")


    #Merge & Save Results to MP4
    results_path=os.getcwd()+"\\results"                #results folder in cwd
    if not(os.path.exists(results_path)):               #if folder doesn't exist make it
        os.makedirs(results_path)
    save_path = os.path.join(results_path,mp4_file.split('\\')[1])

    video = VideoFileClip(mp4_file)                     #get mp4
    audio = AudioFileClip(wav_file,Fs)                  #get  correct audio from saved wav dile
    result_video = video.set_audio(audio)               #connect audio to video
    result_video.write_videofile(save_path,threads=2)   #generate mp4
    os.remove(wav_file)                                 #rmv temp files