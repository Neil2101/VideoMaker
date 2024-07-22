import whisper
import string

numbers="1234567890"
allowed_characters=string.ascii_letters+" .!?()[]:;,*#$%&\'"+numbers

def SubtitleGenerator(audio):
    model = whisper.load_model("base.en") # load the model
    result = model.transcribe(f"{audio}.wav",word_timestamps=True) # generate subtitles
    return result # return the subtitles

def SubtitleCleanUp(subtitles):
    CleanSubtitles=[]
    for segment in subtitles["segments"]: # for phrase in subtitles
        words=segment["words"] # the individual words are
        for word_data in words: # for word_data in words (probability, start, word, end)
            del word_data["probability"] # del the probability (start, word, end)
            adjusted_text=""
            for letter in word_data["word"]: # for letter in the word
                if letter in allowed_characters: # if the letter is allowed
                    adjusted_text+=letter # add the letter
            word_data["word"]=adjusted_text # the new word with allowed text
            CleanSubtitles.append(word_data) # append the word data
    return CleanSubtitles # return the new subtitles

def CorrectWords(subtitles,words): # fix this shit
    FixWords=words

    for removed in ["\n","\t"]:
        FixWords=FixWords.replace(removed," ") # remove new lines and tabs
    for replaced in ".!?":
        FixWords=FixWords.replace(f"{replaced} ",replaced).replace(replaced,f"{replaced} ") # replace all punctuation to (. ) or ! ot ?
    FixWords=FixWords.split(" ") # list the words
    for word,subtitle in zip(FixWords,subtitles): # for word and subtitle
        currentword=subtitle["word"] # get the current word in the subtitle
        index=FixWords.index(word) # get the index of the items
        if currentword in word and currentword!=word: # if the subtitle word is in the word but not the word
            a=currentword+subtitles[index+1]["word"] # add the next word
            if a==word: # check if the word is now equal
                start=subtitles[index]["start"] # set the start
                end=subtitles[index+1]["end"] # set the end
                subtitle["start"]=start # change the start
                subtitle["end"]=end # change the end
                subtitle["word"]=word # change the word
                subtitles.pop(index+1) # remove the next subtitle
    FixWords=" ".join(FixWords) # rejoin the words
    FixWords=list(FixWords) # get all the characters
    for index,letter in enumerate(FixWords): # for index and letter in the words
        if letter=="," and FixWords[index-1] not in numbers: # if the letter is a comma and the previous is not a number
            if FixWords[index+1]!=" ": # if the next letter is not a space
                FixWords[index]=", " # set the comma to a comma with a space
        else:
            continue
    FixWords="".join(FixWords) # rejoin the words
    WordList=[Word for Word in FixWords.split(" ") if Word.strip()] # turn into a list of words
    for subtitle,word in zip(subtitles,WordList): # for every subtitle and word
        subtitle["word"]=word # set the word
    return subtitles # return fixed words

def OffSetSubtitles(subtitles,offset):
    for subtitle in subtitles:
        subtitle["start"]+=offset
        subtitle["end"]+=offset
    return subtitles
