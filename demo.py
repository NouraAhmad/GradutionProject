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
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout
from os.path import dirname
from kivymd.theming import ThemeManager
from kivy.properties import StringProperty
from kivymd.icon_definitions import md_icons
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
    ConcatInfo:


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
            source: 'logo.png'
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
    BoxLayout:
        orientation: 'vertical'
        # just change the points of the tow tringles
        canvas.before:      
            Color:
                rgba: rgba('#EFEFEF')
            Triangle:
                points:[0, self.size[1] ,self.size[0],0, 0, 0]
                
            Color:
                rgba: rgba('#DAE5FA')
            Triangle:
                points:[0, self.size[1],self.size[0]-(.3*self.size[1]),self.size[1], 0,self.size[1]-(.4*self.size[1])]
              
    MDLabel: 
        text: 'Recognize & Say it'
        # halign: 'center'
        # pos_hint: {'center_x':0.5,'center_y':0.91}
        # color: 0,0,0, 1
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.95}
        background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/20
        canvas.before:
            Color: 
                rgba: self.background_color
            Rectangle:
                size : self.size
                pos: self.pos


    Image:
        source: 'logo.png'
        # Giving the size of image
        size_hint: 0.7, 0.7
        # allow stretching of image
        allow_stretch: True
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}

    # MDRaisedButton:
    MDRectangleFlatButton:
        # need background color
        text: 'Scanning a new image '
        size_hint: (.5, .11)
        pos_hint: {'center_x':0.5,'center_y':0.4}
        # md_bg_color: 0,0,0, 1
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        line_color: 0, 0, 0, 1
        # color: 0,0,0, 1
        # md_bg_color:222/255 , 222/255 ,222/255 ,1
        on_press: root.manager.current='camerapage'
        
    # need draw line
    
    MDRectangleFlatButton:
        text: 'contact us '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.3,'center_y':0.2}  
        on_press: root.manager.current='concat'
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        line_color: 0, 0, 0, 0

    MDRectangleFlatButton:
        text: 'instructions '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.7,'center_y':0.2}  
        on_press: root.manager.current='welcome'  
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        line_color: 0, 0, 0, 0  
 
               

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
    BoxLayout:
        orientation: 'vertical'
        canvas.before:      
            Color:
                rgba: rgba('#EFEFEF')
            Triangle:
                points:[0, self.size[1] ,self.size[0],0, 0, 0]
            Color:
                rgba: rgba('#DAE5FA')
            Triangle:
                points:[0, self.size[1],self.size[0]-(.3*self.size[1]),self.size[1], 0,self.size[1]-(.4*self.size[1])]
    MDLabel:    
        text: 'Recognize & Say it'
        # halign: 'center'
        # pos_hint: {'center_x':0.5,'center_y':0.91}
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.95}
        background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/20
        canvas.before:
            Color: 
                rgba: self.background_color
            Rectangle:
                size : self.size
                pos: self.pos


    Image:
        source: "test_images/4.png"
        # source: '(%s)'%(app.picture_taken)
        halign: 'center'
        # we need size 
        size: self.texture_size 
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
    BoxLayout:
        orientation: 'vertical'
        canvas.before:      
            Color:
                rgba: rgba('#EFEFEF')
            Triangle:
                points:[0, self.size[1] ,self.size[0],0, 0, 0]
                
            Color:
                rgba: rgba('#DAE5FA')
            Triangle:
                points:[0, self.size[1],self.size[0]-(.3*self.size[1]),self.size[1], 0,self.size[1]-(.4*self.size[1])]
                           
    MDLabel:    
        text: 'Recognize & Say it'
        halign: 'center'
        # pos_hint: {'center_x':0.5,'center_y':0.91}
        pos_hint: {'center_x':0.5,'center_y':0.95}
        background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/20
        canvas.before:
            Color: 
                rgba: self.background_color
            Rectangle:
                size : self.size
                pos: self.pos

    # Image:
    #     source: "test_result/4.png"
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

 
<ConcatInfo>:
    name: 'concat'
    BoxLayout:
        orientation: 'vertical'
        canvas.before:      
            Color:
                rgba: rgba('#EFEFEF')
            Triangle:
                points:[0, self.size[1] ,self.size[0],0, 0, 0]
                
            Color:
                rgba: rgba('#DAE5FA')
            Triangle:
                points:[0, self.size[1],self.size[0]-(.3*self.size[1]),self.size[1], 0,self.size[1]-(.4*self.size[1])]
                           
    MDLabel:    
        text: 'Concat Information'
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.95}
        background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/20
        canvas.before:
            Color: 
                rgba: self.background_color
            Rectangle:
                size : self.size
                pos: self.pos
    MDLabel:
        text: 'If you have any comments or suggestions, please contact us :'
        # halign: 'center'
        pos_hint: {'center_x':0.60,'center_y':0.80}
        # background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/20
        padding_x: 30
    Image:
        source: 'twitter.png'
        # Giving the size of image
        size_hint: 0.1, 0.1
        # allow stretching of image
        allow_stretch: True
        pos_hint: {'center_x': 0.2, 'center_y': 0.70}
    MDLabel:
        text: '@RecognizeAndSayIt'
        # halign: 'center'
        pos_hint: {'center_x': 0.75, 'center_y': 0.70}
        # background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/27
        padding_x: 20
    Image:
        source: 'email.png'
        # Giving the size of image
        size_hint: 0.09, 0.09
        # allow stretching of image
        allow_stretch: True
        pos_hint: {'center_x': 0.2, 'center_y': 0.60}
    MDLabel:
        text: 'RecognizeAndSayIt@gmail.com'
        # halign: 'center'
        pos_hint: {'center_x': 0.75, 'center_y': 0.60}
        # background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/27
        padding_x: 20
    Image:
        source: 'phone.png'
        # Giving the size of image
        size_hint: 0.06, 0.06
        # allow stretching of image
        allow_stretch: True
        pos_hint: {'center_x': 0.2, 'center_y': 0.507}
    MDLabel:
        text: '+966530956125'
        # halign: 'center'
        pos_hint: {'center_x': 0.75, 'center_y': 0.50}
        # background_color: (243/255 , 243/255 , 243/255 ,1)
        size_hint: 1, 0.1
        font_size: self.width/27
        padding_x: 20
    MDRectangleFlatButton:
        text: 'Home Page '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.5,'center_y':0.2}  
        on_press: root.manager.current='home'
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        line_color: 0, 0, 0, 1
    
    





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
class ConcatInfo(Screen):
    pass

sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcome'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(CheckScreen(name='camerapage'))
sm.add_widget(ProcessScreen(name='processpage'))
sm.add_widget(SayItSecreen(name='sayitpage'))
sm.add_widget(ConcatInfo(name='concat'))

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
            # txt_f.flush()
            # os.fsync(txt_f.fileno())
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
