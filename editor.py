import time, os
from pystyle import *
from moviepy.editor import * 
from colorama import *
from rich.traceback import install
from rich.console import Console


from pathlib import Path

# Progress Bar
from tqdm import tqdm
from time import sleep

# Folder Naming
from datetime import date
from datetime import datetime




class Editor:
    clip_dir = ''
    # @clip_dir :: PATH to directory we are going to be 
    #              traversing and editing every file in
    #              said directory

    edit_dir = ''
    

    abs_clips = []
    # @abs_clips :: Stores ABSOLUTE PATHS to all clips in 
    #               @clip_dir

    sound_path = ''
    # @music_path :: PATH to directory populated by
    #                .mp3 files that are going to be 
    #                overlayed on clips
    


    name = ''
    # @name     :: name we want to use for naming the
    #              edited clips




    def __init__(self,input_dir,output_dir,name):
        self.clip_dir = input_dir 
        self.edit_dir = output_dir
        self.name = name


    # Get the absolute paths of all files in self.clip_dir
    def getPaths(self):
        all_clips = []
        for f in os.listdir(self.clip_dir):
            all_clips.append((self.clip_dir + '/'+f))
            
        
        self.abs_clips.clear()
        for f in all_clips:
            self.abs_clips.append(os.path.abspath(f))
            #print(os.path.abspath(f))



        # IF EDITED HAS VIDEOS, RANAME AND MAKE 'edited' AGAIN 
        if os.listdir(self.edit_dir):
            remake_dir = self.edit_dir

            rename_dir = ''
            split = self.edit_dir.split('/')
            for i in range(len(split)-2):
                rename_dir = rename_dir + split[i] + '/'

            date_time = datetime.today().strftime("%m:%d:%Y")
            testing_name = rename_dir + 'edited_' + date_time + '/'

            counter = 1
            while(os.path.exists(testing_name)):
                testing_name = rename_dir + 'edited_' + date_time + '_'+str(counter) + '/'
                counter+=1

            os.rename(self.edit_dir,testing_name)
            os.makedirs(remake_dir)

        return self.abs_clips



    def process(self,abs_input,abs_output):
        #path = Path(abs_input)

        clip = VideoFileClip(abs_input)


        #sound = clip.audio       # --> SET AUDIO 
        #clip.set_audio(sound)    # --> TRACK


        #clip = clip.fx(vfx.mirror_x)   # --> MIRROR VIDEO
        #clip = clip.fx(vfx.speedx,1.2)  # --> ALTER SPEED


        # CALCULATE TO ALWAYS MAKE CLIP UNDER 1 MIN 
        length = clip.duration 
        speed = 1+(((length-60)/6)*.1)
        #print(clip.filename + ' | ' + str(speed))

        if(speed < 1):
            pass
            # clip = clip.fx(vfx.speedx,1.1)
        else:
            clip = clip.fx(vfx.speedx,speed)

        
        # IF CLIP IS TOO SHORT, DONT SAVE IT 
        if(clip.duration <= 5):
            return
                 
        # SAVE CLIP 
        clip.write_videofile(abs_output,logger=None,  temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")

        clip.close()


    def processX(self,x):
        if not os.path.exists(self.edit_dir):
            os.makedirs(self.edit_dir)

        # Progress Bar:
        # ------------------------------------------------------------
        for i in tqdm(range(x), desc=f'{self.name}: ', colour='red'):
            cur = self.abs_clips[i]
            split = cur.split('/')
            new_name = (split[-1])[:-4] + '_edited.mp4'
            output_path = self.edit_dir + new_name

            #print(output_path)
            self.process(cur,output_path)

        # No Progress Bar: 
        # ------------------------------------------------------------
        # for i in range(x):
        #     cur = self.abs_clips[i]
        #     split = cur.split('/')
        #     new_name = (split[-1])[:-4] + '_edited.mp4'
        #     output_path = self.edit_dir + new_name

        #     #print(output_path)
        #     self.process(cur,output_path)





    def setSound(self, path):
        self.sound_path = path
        

