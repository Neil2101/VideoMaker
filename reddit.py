import seleniumbase as sb
import time
from selenium.webdriver.common.by import By
import string
import requests

allowed_characters=string.punctuation+string.ascii_letters+" 1234567890"

def GetSubRedditPosts(subreddit,nsfw:bool):
    global sb
    with sb.SB() as driver: # open the captcha bypassing chromium
        driver.open(f"https://www.reddit.com/r/{subreddit}/top/?t=day") # open the top today
        time.sleep(5) # wait for the page to load
        # top 3 feed
        if nsfw: # doesnt work but will check for nsfw
            # grabs the first 3 posts
            feed=[{"link":"https://www.reddit.com"+element.get_attribute("permalink"),"title":element.get_attribute("post-title")} for element in driver.find_elements(selector="/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/*/*",by="Xpath") if element.get_attribute("permalink") and "user" not in element.get_attribute("permalink") and element.get_attribute("post-type")=="text"]
        else:
            # grabs the first 3 posts excluding nsfw
            feed=[{"link":"https://www.reddit.com"+element.get_attribute("permalink"),"title":element.get_attribute("post-title")} for element in driver.find_elements(selector="/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/*/*",by="Xpath") if element.get_attribute("permalink") and "user" not in element.get_attribute("permalink") and element.get_attribute("post-type")=="text" and element.get_attribute("nsfw")==""]
        # next 25
        driver.execute_script("window.scrollTo(0, 1080)") # scroll down
        if nsfw: # doesnt work but will check for nsfw
            # get the next batch of posts
            next_batch=[{"link":"https://www.reddit.com"+element.get_attribute("permalink"),"title":element.get_attribute("post-title")} for element in driver.find_elements("/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/*/*",by="Xpath") if element.get_attribute("permalink") and "user" not in element.get_attribute("permalink")]
        else:
            # get the next batch of posts excluding nsfw
            next_batch=[{"link":"https://www.reddit.com"+element.get_attribute("permalink"),"title":element.get_attribute("post-title")} for element in driver.find_elements("/html/body/shreddit-app/div/div[1]/div[2]/main/div[2]/shreddit-feed/faceplate-batch/*/*",by="Xpath") if element.get_attribute("permalink") and "user" not in element.get_attribute("permalink") and element.get_attribute("nsfw")==""]
        feed+=next_batch # add the next batch to the feed
        
    return {"feed":feed,"amount":len(feed)} # return the feed and the amount

def GetPostComments(post):
    global sb
    post_link=post["link"] # get the post link
    with sb.SB() as driver: # open the undetcted chromium
        driver.open(post_link) # open the post link
        time.sleep(5) # wait for the page to load
        driver.execute_script("window.scrollTo(0, 5000)") # scroll down max amount
        time.sleep(3) # let it load
        driver.execute_script("window.scrollTo(0, 5000)") # scroll down max amount
        time.sleep(5) # let it load
        # get all the comments
        comments=[comment for comment in driver.find_elements(selector="/html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/*",by="Xpath") if comment.get_attribute("content-type")=="text"]
        # get all the data of the comments seperated by \n
        comment_data=[div for comment in comments for div in comment.find_elements(By.XPATH, './*/div') if div.get_attribute("id")=="-post-rtjson-content"]
        # the result text once fixed
        comments_text=[]
        
        for data in comment_data: # for every comment check the data
            comment=[]
            for paragraph in data.find_elements(By.XPATH, './/*'): # in all the data's descendents
                new_paragraph="" # the fixed comment (removes emojis etc)
                for letter in paragraph.text: # check the paragraph in the descendt
                    if letter in allowed_characters: # if the letter is allowed
                        new_paragraph+=letter # allow the letter
                comment.append(new_paragraph) # add this to the comment
            comments_text.append("\n".join(comment)) # add to the comment text
        
    return {"comments":comments_text,"amount":len(comments_text)} # return the comments text and the amount

def GetSubredditImage(subreddit):
    global sb
    with sb.SB() as driver:
        driver.open(f"https://www.reddit.com/{subreddit}/")
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 5000)")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(3)
        image_link=[element.get_attribute("src") for element in driver.find_elements(By.XPATH,"/html/body//*")]
        print(image_link)
    img_data = requests.get(image_link).content
    with open('subreddit.png', 'wb') as handler:
        handler.write(img_data)
# .//* gets all descendents
# ./* gets all children
