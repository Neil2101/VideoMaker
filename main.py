import reddit
import tts
import video
import subtitles
import os
import time
import image
from moviepy.editor import *
import psutil


target_wpm=200 # the target words per minute
ChangeSpeechRate=False # if false the tts rate wont be sped up
frequencymultiplier=1 # 1.05-1.1 is a good high pitch, 0.9-0.95 is a good low pitch, 1 is normal, 1.05 is really good
BufferAudioFile=False # if there is a buffer audio file
BufferAudioText="The next comment says" # the text of the buffer audio file if BufferAudioFile is True
subreddit="askreddit" # the subreddit
nsfw=True # if it should include nsfw posts (broken rn) 


target_wps=target_wpm/60 if ChangeSpeechRate is True else 0


feed=reddit.GetSubRedditPosts(subreddit=subreddit,nsfw=nsfw) # get the feed of the subreddit with the nsfw

postindex=1 # the post index

for post in feed["feed"]: # for post in the feed
    """if postindex==2: 
        break""" # if you want to only do one post
    
    postname = post["title"] # the name/title of the post

    tts.CreateTTSFile(postname,f"PostTitleFinal",target_wps) # create the tts for the post name

    comments=reddit.GetPostComments(post)["comments"] # grab the post comments

    tts_files=[] # the tts files
    tts_comments=[] # the tts comments
    remove_files=[] # files to remove
    commentindex=1 # the comment index
    
    for comment in comments: # for comment
        
        tts.CreateTTSFile(comment,f"Comment{commentindex}Final",target_wps) # generate the tts file for the comment
        
        tts_files.append(f"Comment{commentindex}Final") # add the tts file to the tts_files
        tts_comments.append(comment) # add the comment to tts_comments

        commentindex+=1 # increase the comment index
    
    os.makedirs(f"Post{postindex}Data",exist_ok=True) # create a new folder for the finished shorts and video of post 1
    
    shortindex=1 # the short index
    
    for file,comment in zip(tts_files,tts_comments): # for file and comment
        
        file1=AudioFileClip(f"{file}.wav")
        dataduration=file1.duration
        
        subs=subtitles.SubtitleGenerator(audio=file) # generate the subtitles for the short
        cleansubs=subtitles.SubtitleCleanUp(subs) # make the subtitles readable for the other code
        fixedwords=subtitles.CorrectWords(cleansubs,comment) # fix the words for the subtitles
        
        video.AudioMerger(outputfile=f"ShortPost{postindex}Comment{shortindex}",audiofiles=[file],titlefile="PostTitleFinal",delete=False) # merge the comment audio file and the post audio file
        
        durcheck=AudioFileClip(f"ShortPost{postindex}Comment{shortindex}.wav")
        
        if durcheck.duration >= 60 or durcheck.duration < 15: # if the duration does not fit ytshorts length
            remove_files.append(f"ShortPost{postindex}Comment{shortindex}.wav") #add to remove
            shortindex+=1 # increase short index
            continue # go to make the next short

        offset=durcheck.duration-dataduration
        
        subtitles.OffSetSubtitles(fixedwords,offset)
        
        video.VideoFromAudio(audiofile=f"ShortPost{postindex}Comment{shortindex}",output=f"ShortPost{postindex}Comment{shortindex}Video",delete=False) # turn the audio into a video

        video.TitleImageOverlay("Title",f"ShortPost{postindex}Comment{shortindex}Video",offset)
        
        video.SubtitleVideoCreator(subtitles=cleansubs,video=f"ShortPost{postindex}Comment{shortindex}Video",output=f"Post{postindex}Data/Short{shortindex}",delete=False) # add the subtitles and put in the final folder

        
        remove_files.append(f"ShortPost{postindex}Comment{shortindex}.wav") # add temp files to be removed
        remove_files.append(f"ShortPost{postindex}Comment{shortindex}Video.mp4") # add temp files to be removed
        file1.close()#closes the file
        durcheck.close()#closes the file
        shortindex+=1 # increase short index
    
    """video.AudioMerger(outputfile=f"FinalPost{postindex}",audiofiles=tts_files,titlefile="PostTitleFinal",delete=False) # make the full video audio
    
    subs=subtitles.SubtitleGenerator(audio=f"FinalPost{postindex}") # generate the subtitles for the full video
    cleansubs=subtitles.SubtitleCleanUp(subs) # clean the subtitles for the other code
    fixedwords=subtitles.CorrectWords(cleansubs,postname+" ".join(tts_comments)) # replace the words
    
    
    video.VideoFromAudio(audiofile=f"FinalPost{postindex}",output=f"FinalPost{postindex}Video",delete=False,short=False) # turn the audio to a video
        
    video.SubtitleVideoCreator(subtitles=cleansubs,video=f"FinalPost{postindex}Video",output=f"Post{postindex}Data/Final",delete=False) # add subtitles to the video"""
    
    for file in reversed(remove_files): # for file in remove_files
        os.remove(file) # remove the file
    os.remove("GeneratedTTS.mp3") # remove the temp generated tts file
    
    postindex+=1 # increase the post index
    
    
# needs imagemaick and ffmpeg and Grold-Rounded-Slim-Black font

# fix the speech break if 100 char limit
# fix the nsfw on reddit things
# add thumbnail
# add the reddit image when the title is said
# add the vertical aspect ratio for short videos
