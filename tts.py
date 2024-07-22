from gtts import gTTS
import os
from moviepy.editor import *
from pydub import AudioSegment
import ffmpy
import wave
import time

def ToWav(mp3file):
    sound = AudioSegment.from_mp3(f"{mp3file}.mp3") # get the mp3
    sound.export(f"{mp3file}.wav", format="wav") # convert the mp3 to .wav

def AdjustVoice(file,fm):
    if fm==1: # if the frequency multiplier is 1 aka no change
        os.rename(f"{file}.wav",f"{file}Voice.wav") # rename the file to the output of if it wasnt 1
        return
    
    spf = wave.open(f"{file}.wav", 'rb') # read the wav file
    RATE=spf.getframerate() # get the speed of the file
    signal = spf.readframes(-1) # idefk

    wf = wave.open(f'{file}1.wav', 'wb') #make the new file
    wf.setnchannels(1) # idk
    wf.setsampwidth(2) #idk
    wf.setframerate(RATE*fm) # change the file speed
    wf.writeframes(signal) # write to the file
    wf.close() # close the file
    
    speedupdata = ffmpy.FFmpeg(inputs={f"{file}1.wav": None}, outputs={f"{file}Voice.wav": ["-filter:a", f"atempo={1/fm}"]}) # respeed the file to the original speed but with the changed frequency
    speedupdata.run() # update the file

def FinishFile(file,output,speed,frequencymultiplier:int):
    ToWav(file) # turn the file to a wav file
    AdjustVoice(file,frequencymultiplier) # change the file's frequency
    
    
    if frequencymultiplier!=1: # if the adjustvoice made the step files
        os.remove(f"{file}.wav") # remove the og wav
        os.remove(f"{file}1.wav") # remove the step file
    
    speedupdata = ffmpy.FFmpeg(inputs={f"{file}Voice.wav": None}, outputs={f"{output}.wav": ["-filter:a", f"atempo={speed}","-y"]}) # change the speed of the file
    speedupdata.run() # run the data

    os.remove(f"{file}Voice.wav") # remove the voice step file

def GenerateTTS(text:str,output:str):
    commenttts=gTTS(text=text, lang="en", slow=False) # set up the tts for the comment
    commenttts.save(f"{output}.mp3") # save the tts sound

def CreateTTSFile(text:str,output:str,targetwps:int=0,frequencymultiplier:int=1):
    GenerateTTS(text,"GeneratedTTS") # generate the tts
    
    if targetwps==0:
        speed=1
    else:
        word_amount=len(text.split(" ")) # check the word amount
        audio = AudioFileClip(f"GeneratedTTS.mp3") # create the MP3 class to get the length
        length=audio.duration # get the length
        wps=word_amount/length # calculate the words per second
        speed=targetwps/wps
    
    
    FinishFile("GeneratedTTS",output=output,speed=speed,frequencymultiplier=frequencymultiplier)
    
    return output
