import tts
import reddit
import subtitles
from moviepy.editor import *
import random
from moviepy.config import change_settings
import time

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"}) # change the imagemagick file location

def VideoFromAudio(audiofile,output,delete:bool=False,short:bool=True):
    if short:
        path="backgrounddata/shortsvideos/" # get a short background video 1080x1920
    else:
        path="backgrounddata/fullvideos/" # get a normal background video 1920x1080
    
    videos=os.listdir(path) # get all the background videos
    video=random.choice(videos) # choose a random background video

    audio = AudioFileClip(f"{audiofile}.wav") # load the audio clip
    audiolength=audio.duration # the audio length
    
    video = VideoFileClip(f"{path}/{video}") # load the video clip
    videoduration=video.duration # the video duration
    
    
    randomdur=round(videoduration-audiolength+.5) # get the maximum starting point in the video where the audio can fit -.1 just in case
    
    
    subclipstart=random.randint(0,randomdur) # get where the video will start
    subclipend=subclipstart+audiolength # get where the video will end
    subclip=video.subclip(subclipstart,subclipend) # generate the subclip
    
    audiosubclip = subclip.set_audio(audio) # set the subclip audio to the audio
    audiosubclip.write_videofile(f"{output}.mp4") # write the video file
    
    if delete:
        os.remove(f"{audiofile}.wav") # delete the audio file

def AudioMerger(outputfile:str,audiofiles:list,bufferaudio:str=None,titlefile:str=None,delete:bool=False):
    audioclips=[]
    if bufferaudio is not None: # if a buffer audio file is provided
        bufferclip=AudioFileClip(f"{bufferaudio}.wav") # render the buffer audio
    
    if titlefile is not None: # if a title audio file is provided
        audioclips.append(AudioFileClip(f"{titlefile}.wav")) # render the title audio
    
    for file in audiofiles: # for audiofile
        audioclips.append(AudioFileClip(f"{file}.wav")) # render the audio file and add it into the queue
        if bufferaudio is not None: # if there is a buffer audio
            audioclips.append(bufferclip) # add the buffer audio file
    
    mergedaudio=concatenate_audioclips(audioclips) # merge the audio files in order they appear in the list
    
    mergedaudio.write_audiofile(f"{outputfile}.wav") # write the audio file
    
    if delete: # if delete
        for file in audiofiles: # for audiofile
            os.remove(f"{file}.wav") # delete the audio file
        if bufferaudio: # if there is a buffer audio file
            os.remove(f"{bufferaudio}.wav") # delete the buffer audio file
        if titlefile: # if there is a title audio file
            os.remove(f"{titlefile}.wav") # delete the title audio file

def SubtitleVideoCreator(subtitles,video,output,delete:bool=False,short:bool=True):
    nextstart=0 # the start of the next word
    videofile=VideoFileClip(f"{video}.mp4") # render the video
    videowidth,videohieght=videofile.size # get the video size
    output=f"{output}.mp4" # set the output file
    text_clips=[] # a list of the text vlips
    fontsize=125 if not short else 75
    for index,subtitle in enumerate(subtitles): # for subtitle in subtitles
        try: 
            nextstart=subtitles[index+1]["start"] # set the next start to the start of the next word if possible
        except:
            nextstart=videofile.duration # if not possible then set it as the end of the file
        txt_clip = TextClip(subtitle["word"], fontsize=fontsize,color="white",font="Grold-Rounded-Slim-Black",stroke_width=3,stroke_color="black") # generate the text
        txt_clip = txt_clip.set_position('center').set_start(subtitle["start"]).set_end(nextstart) # set the attributes of the text
        shadow_text_clip = TextClip(subtitle["word"], fontsize=fontsize,color="black",font="Grold-Rounded-Slim-Black",stroke_width=3,stroke_color="black") # generate the shadow text
        shadowwidth,shadowhieght=shadow_text_clip.size # get the size of the shadow text
        shadow_text_clip = shadow_text_clip.set_start(subtitle["start"]).set_end(nextstart) # set the start and end of the shadow text
        shadow_text_clip = shadow_text_clip.set_position(((videowidth/2-shadowwidth/2)+5,(videohieght/2-shadowhieght/2)+5)).set_opacity(0.6) # set the position and opacity of the shadow text
        text_clips.append(shadow_text_clip) # append the shadow text so itll show up behind the normal text
        text_clips.append(txt_clip) # append the text so itll be in front of the shadow text
    text_clips.insert(0,videofile) # insert the video file so that itll be layer 0
    subtitledvideo = CompositeVideoClip(text_clips) # join the video files
    subtitledvideo.write_videofile(output) # write the video file
    if delete:
        os.remove(f"{video}.mp4") # delete the old video
        
def TitleImageOverlay(image:str, video:str, duration:int):
    output=f"{video}.mp4"
    image=f"{image}.png"
    
    vidifiedimage=ImageClip(image).set_start(0).set_end(duration).set_pos(("center","center")).add_mask()
    
    final=CompositeVideoClip([VideoFileClip(f"{video}.mp4"),vidifiedimage])
    final.write_videofile(output)
