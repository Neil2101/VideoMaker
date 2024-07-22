from PIL import Image, ImageDraw, ImageFont
import datetime
import reddit
import os

def AddText(position:tuple,text:str,image:str,output:str,fontsize:int):    
    baseimage=Image.open(image)
    draw=ImageDraw.Draw(baseimage)
    font=ImageFont.truetype("arialbd.ttf",fontsize)
    
    draw.text(position,text,font=font)
    baseimage.save(output)
    
def CalcSize(text:str,fontsize:int):
    font=ImageFont.truetype("arialbd.ttf",fontsize)
    return font.getlength(text)

def FixText(text:str,fontsize:int,imagewidth:int):
    textwidth=CalcSize(text,fontsize)
    Sentences=[]
    words=text.split(" ")
    if textwidth>imagewidth:
        Sentence=""
        
        for index,word in enumerate(words):
            
            if index==len(words)-1:
                if CalcSize(Sentence+word+" ",30)<imagewidth:
                    Sentence+=word+" "
                    Sentences.append(Sentence)
                else:
                    Sentences.append(Sentence)
                    Sentences.append(word)
            
            if CalcSize(Sentence+word+" ",30)<imagewidth:
                Sentence+=word+" "
            else:
                Sentences.append(Sentence)
                Sentence=""
                Sentence+=word+" "
                
    return Sentences

def ComposeData(subreddit:str,title:str,channel:str,output:str,input:str):
    output=f"{output}.png"
    input=f"{input}.png"
    subreddit=f"r/{subreddit}"
    stepfile="Step.png"
    
    subredditposition=(50,10) # font size 15
    channelposition=(350,207)
    dateposition=(CalcSize(subreddit,15)+77,10) # subreddit length + subreddit start + buffer
    bufferposition=(dateposition[0]-17,7) # subreddit length + subreddit start + 10px buffer + 7 px length
    
    im = Image.open(input)
    width, height = im.size
    
    AddText(subredditposition,subreddit,input,stepfile,15)
    AddText(bufferposition,"·",stepfile,stepfile,20)
    AddText(dateposition,str(datetime.date.today()),stepfile,stepfile,15)
    AddText(channelposition,"by "+channel,stepfile,stepfile,20)
    
    reddit.GetSubredditImage(subreddit)
    
    foreground = Image.open("subreddit.png")
    foreground.resize((24,24))
    foreground.save("subreddit.png")
    
    background = Image.open("Step.png")
    final1 = Image.new("RGBA", background.size)
    final1.paste(background, (0,0), background)
    final1.paste(foreground, (20,7), foreground)
    final1.save("Step.png")
    
    bettertitle=FixText(title,30,width)
    
    y_value=40
    for sentence in bettertitle:
        if sentence!=bettertitle[-1]:
            AddText((25,y_value),sentence,stepfile,stepfile,30)
        else:
            AddText((25,y_value),sentence,stepfile,output,30)
        y_value+=40
    
    os.remove("Step.png")

#ComposeData("AskReddit","Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum","MAM Reddit Stories","testoutput","backgrounddata/customimages/title")
