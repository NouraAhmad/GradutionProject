import os
from ocr import ocr
import time
import shutil
import numpy as np
# change it to . beacuse error
import PIL.Image
from glob import glob
import pyttsx3
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
# !/usr/bin/env python
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image, AsyncImage
from kivy.graphics import Color, Rectangle
from tkinter.filedialog import askdirectory, askopenfile, asksaveasfilename, askopenfilenames, askopenfilename, \
    askopenfiles, asksaveasfile
from tkinter import Tk
import time
from kivy.utils import platform
from kivy.clock import Clock
from os.path import isdir
from os import mkdir
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.core.text import LabelBase
LabelBase.register(name="Regular",
                   fn_regular="KaushanScript-Regular.otf")
txt_file=""
try:
    from android.permissions import request_permissions, check_permission, \
        Permission
    from android.storage import primary_external_storage_path
except:
    pass

Window.clearcolor = (1, 1, 1, 1)
Window.size = (360, 600)

screen_helper = """
#: import XCamera kivy.garden.xcamera.XCamera

ScreenManager:
    WelcomeScreen:
    HomeScreen:
    CheckScreen:
    ProcessScreen:
    SayItSecreen:


<WelcomeScreen>:
        # on_release: app.startWelcomingPage()

    name: 'welcome' 
    
    # Adding Box Layoyt
    BoxLayout:
        size_hint: [.9, .9]
        pos_hint: { 'top' : .95, 'right': .95}
        orientation: 'vertical'

        # Adding image from the system
        Image:
            source: 'tts.png'
            # Giving the size of image
            size_hint: 1.4, 1.4
            # allow stretching of image
            allow_stretch: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.75}


        # Giving Label to images
        Label:
            text:"Welcome To"
            font_size:30
            bold:True
            color:(0/255, 200/255, 247/255, 0.7)

        Label:
            text:"[b]RECOGNIZE & SAY IT[/b]"
            font_size:50
            bold:True
            color:(0, 155/255, 255/255, 1)
            font_name:"Regular"
            markup: True
        Label:
            text:"APPLICATION"
            font_size:30
            bold:True
            color:(0/255, 200/255, 247/255, 0.7)
    # MDRectangleFlatButton:
    #     text: 'Start '
    #     pos_hint: {'center_x':0.5,'center_y':0.2}  
    #     on_press: root.manager.current='home'



<HomeScreen>:
    name: 'home'
    MDLabel: 
        text: 'Recognize & Say it'
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.91}
        color: 0,0,0, 1


    Image:
        source:'tts.png'
        halign: 'center' 
        pos_hint: {'center_x':0.5,'center_y':0.73}

    MDRaisedButton:
        text: 'Scanning a new image '
        size_hint: (.5, .11)
        pos_hint: {'center_x':0.5,'center_y':0.4}
        md_bg_color: 0,0,0, 1
        on_press: root.manager.current='camerapage'

    MDRectangleFlatButton:
        text: 'contact us '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.3,'center_y':0.2}  
        on_press: root.manager.current='welcome'
    MDRectangleFlatButton:
        text: 'instructions '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.7,'center_y':0.2}  
        on_press: root.manager.current='welcome' 
               

<CheckScreen>:
    name:'camerapage'


    XCamera:
        id: xcamera
        on_picture_taken: 
            app.picture_taken(*args)
            root.manager.current='processpage'
            on_cemera_ready: app.cemera_ready()

    BoxLayout:
        orientation: 'horizontal'
        size_hint: 1, None

        height: sp(50)

        Button:
            text: 'Back'
            on_release: root.manager.current='home' 




<ProcessScreen>:
    name: 'processpage'

    MDLabel:    
        text: 'Recognize & Say it'
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.91}


    Image:
        source: "test_images/4.jpeg"
        # source: '(%s)'%(app.picture_taken)
        halign: 'center' 
        pos_hint: {'center_x':0.5,'center_y':0.6}


    MDRectangleFlatButton:
        text: 'process '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.3,'center_y':0.2}  
        on_press: root.manager.current='sayitpage'
    MDRectangleFlatButton:
        text: 'Home Page '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.7,'center_y':0.2}  
        on_press: root.manager.current='home'

<SayItSecreen>:
    name: 'sayitpage'

    MDLabel:    
        text: 'Recognize & Say it'
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.91}

    # Image:
    #     source: "test_result/4.jpeg"
    #     halign: 'center' 
    #     pos_hint: {'center_x':0.5,'center_y':0.6}
    Label:
        id: Label1
        font_size:30
        bold:True
        color:(0/255, 200/255, 247/255, 0.7)

    MDRectangleFlatButton:
        bold:True
        size_hint: (.31, .08)
        text:'Say it'
        background_color:0,1,1,1
        pos_hint: {'center_x':0.3,'center_y':0.2}
        on_release: app.play_music()

    MDRectangleFlatButton:
        text: 'Home Page '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.7,'center_y':0.2}  
        on_press: root.manager.current='home'







"""


class WelcomeScreen(Screen):
    def switch(self, *args):
        self.parent.current = "home"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 5)


class HomeScreen(Screen):
    pass


class CheckScreen(Screen):
    pass


class ProcessScreen(Screen):
    pass


class SayItSecreen(Screen):
    def on_pre_enter(self, *args):
        MainApp.showText(self)
    pass


sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcome'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(CheckScreen(name='camerapage'))
sm.add_widget(ProcessScreen(name='processpage'))
sm.add_widget(SayItSecreen(name='sayitpage'))


def single_pic_proc(image_file):
    image = np.array(PIL.Image.open(image_file).convert('RGB'))
    result, image_framed = ocr(image)
    return result, image_framed


class MainApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen

    def on_start(self):
        if platform == 'android':
            self.root.ids.xcamera.index = 0
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                                 Permission.CAMERA],
                                self.setup_storage)
            self.setup_storage([], [])
        # Clock.schedule_once(HomeScreen, 5)

    # def startWelcomingPage(self):
    #     Clock.schedule_once(self, 13)
    def cemera_ready(self):
        pass

    def picture_taken(self, obj, filename):
        print('Picture taken and saved to {}'.format(filename))
        global ImageName
        ImageName = '{}'.format(filename)
        return ImageName

    def Demo(self):
        image_files = glob('./test_images/*.*')
        result_dir = './test_result'
        if os.path.exists(result_dir):
            shutil.rmtree(result_dir)
        os.mkdir(result_dir)

        # for loop for each image in the folder
        for image_file in sorted(image_files):
            t = time.time()
            result, image_framed = single_pic_proc(image_file)
            output_file = os.path.join(result_dir, image_file.split('/')[-1])
            global txt_file
            txt_file = os.path.join(result_dir, image_file.split('/')[-1].split('.')[0])
            print(txt_file)
            txt_f = open(txt_file + '.txt', 'w')
            PIL.Image.fromarray(image_framed).save(output_file)  # save the detect image
            print("Mission complete, it took {:.3f}s".format(time.time() - t))
            print("\nRecognition Result:\n")
            # print all the containt in images
            for key in result:
                print(result[key][1])
                txt_f.write(result[key][1] + '\n')
            # MainApp.showText(txt_f)
            # ++++++++++++++++++++++++++++++++++
            txt_f.flush()
            os.fsync(txt_f.fileno())
            # ++++++++++++++++++++++++++++++++++
            txt_f.close()

    def showText(self):
        # with open('Noura.txt', 'r') as f:
        #         self.ids['Label1'].text = f.read()
        MainApp.Demo(self)
        with open(txt_file + '.txt', 'r') as f:
            self.ids['Label1'].text = f.read()

    def play_music(self):
        with open(txt_file + '.txt', 'r') as f:
            line = f.read()
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[1].id)
            # engine.save_to_file(line, txt_file + '.mp3')
            engine.say(line)
            engine.runAndWait()
        # music = SoundLoader.load('test_result/4.mp3')
        # if music:
        #     music.play()


if __name__ == '__main__':
    MainApp().run()
    print(ImageName)
