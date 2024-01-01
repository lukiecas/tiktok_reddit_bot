from TTS.api import TTS
import praw
import random
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By

#from gtts import gTTS
from moviepy.editor import *
reddit = praw.Reddit(client_id='*',
                     client_secret='*',
                     user_agent='<console:TIKTOKBOT:2.0>')
driver = webdriver.Firefox()

vcodec =   "libx264"
videoquality = "24"
#minecraft_vid_short = VideoFileClip("C:\\Users\\lucas\\Desktop\\python\\reddit\\minecraft_vid_short.mp4")
minecraft_vid_short = VideoFileClip("./minecraft_vid_long.mp4")
#minecraft_vid_long = VideoFileClip("C:\\User\\lucas\\Desktop\\python\\reddit\\minecraft_vid_long.mp4")
def get_script_reddit(link):
    post = reddit.submission(url=link)
    title = post.title
    text = post.selftext
    return title, text

def get_text_screenshot(link, id):
    driver.get(link)
    try:
        button = driver.find_element(By.XPATH, f'//*[@id="t3_{id}-read-more-button"]')
        button.click()
    except:
        pass
    title = driver.find_element(By.XPATH, f'//*[@id="post-title-t3_{id}"]')
    title.screenshot('title.png')
    body = driver.find_element(By.XPATH, f'//*[@id="t3_{id}-post-rtjson-content"]')
    body.screenshot("body.png")
def edit_video(title):
    title = title.replace(' ', '_')
    audio_title = AudioFileClip(f'title.wav')
    audio_body = AudioFileClip(f'body.wav')
    new_audioclip = CompositeAudioClip([audio_title, audio_body.set_start(audio_title.duration)])
    video = minecraft_vid_short.subclip(0, audio_title.duration + audio_body.duration)
    video.audio = new_audioclip
    image_title = ImageClip("title.png").set_start(0).set_duration(audio_title.duration).set_pos(("center", "center"))
    image_body = ImageClip("body.png").set_start(audio_title.duration).set_duration(audio_body.duration).set_pos(("center", "center"))
    video = CompositeVideoClip([video, image_title, image_body])
    video.write_videofile('test.mp4')
def get_id_of_link(link):
    link_splitted = link.split('/')
    id = link_splitted[6]
    return id
    
def text_to_speech(title, text):
    #myobj = gTTS(text=text, lang='en', slow=False)
    tts = TTS(model_name="tts_models/en/jenny/jenny")
    tts.tts_to_file(text=title, file_path="./title.wav")
    tts.tts_to_file(text=text, file_path="./body.wav")
    title = title.replace(' ', '_')
    #myobj.save('filetest.mp3')


def main():
    link = input("enter link to reddit post: ")
    title, text = get_script_reddit(link)
    text_to_speech(title, text)
    print(title, text)
    id = get_id_of_link(link)
    print(id)
    get_text_screenshot(link, id)
    edit_video(title)
    

if __name__ == '__main__':
    main()