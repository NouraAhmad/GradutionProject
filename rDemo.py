import os
from ocr import ocr
import time
import shutil
import numpy as np
# change it to . beacuse error
import PIL.Image
from glob import glob
import pyttsx3
from kivy.uix.camera import Camera
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

LabelBase.register(name="Regular",
                   fn_regular="KaushanScript-Regular.otf")
txt_file = ""

try:
    from android.permissions import request_permissions, check_permission, \
        Permission
    from android.storage import primary_external_storage_path
except:
    pass

Window.clearcolor = (1, 1, 1, 1)
Window.size = (360, 600)

Builder.load_string("""

#: import rgba kivy.utils.rgba

<ScreenManager>:
    WelcomeScreen:
        name:"welcome"
    HomeScreen:
        name:"home"       
    CheckScreen:
        name:"camera" 
        id: entry
    ProcessScreen:
        name:"process"       
    SayItSecreen:
        name:"sayit"

    ConcatInfo:
        name:"concat"

<WelcomeScreen>:
    # on_release: app.startWelcomingPage()



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
        source:'logo.png'
        halign: 'center' 
        pos_hint: {'center_x':0.5,'center_y':0.73}

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
        on_press: root.manager.current='camera'

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
    name:'camera'
    id: entry

    canvas:
        Color:
            rgb: [.30,.50,.99]
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Camera:
            id: camera
            index: 0
            resolution: (1280,720)
            play: True  
        MDFillRoundFlatButton:
            text: "take photo"
            pos_hint: {'center_x': 0.50, 'center_y': .10}
            on_press:
                root.capture()   #TAKE PHOTO
                root.manager.transition.direction = 'up'
                root.manager.transition.duration = 1
                root.manager.current = 'process'    
        MDIconButton:
            icon: 'chevron-double-right'
            pos_hint: {'center_x':.95, 'center_y':.10}
            on_press:
                root.manager.transition.direction = 'down'
                root.manager.transition.duration = 1
                root.manager.current = 'home'



<ProcessScreen>:
    name: 'process'
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
    FloatLayout:
        Image:
            id: img
            halign: 'center' 
             # we need size 
            #size: self.texture_size
            pos_hint: {'center_x':0.5,'center_y':0.6}


    MDRectangleFlatButton:
        text: 'process '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.3,'center_y':0.2}  
        on_press: root.manager.current='sayit'; app.Demo()


    MDRectangleFlatButton:
        text: 'Home Page '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.7,'center_y':0.2}  
        on_press: root.manager.current='home'


<SayItSecreen>:
    name: 'sayit'
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

    MDRectangleFlatButton:
        text: 'Home Page '
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.5,'center_y':0.2}  
        on_press: root.manager.current='home'
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        line_color: 0, 0, 0, 1    






""")


class WelcomeScreen(Screen):
    def switch(self, *args):
        self.parent.current = "home"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 5)


class HomeScreen(Screen):
    pass


class CheckScreen(Screen):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    main_widget = None
    photo = StringProperty('')

    def capture(self):
        camera = self.ids['camera']
        self.photo = f"test_images/IMG_{time.strftime('%Y%m%d_%H%M%S')}.png"
        camera.export_to_png(self.photo)

        print("Captured")


class ProcessScreen(Screen):

    def on_pre_enter(self, *args):
        self.ids.img.source = self.manager.ids.entry.photo


class SayItSecreen(Screen):
    def on_pre_enter(self, *args):
        MainApp.showText(self)

    pass


class ConcatInfo(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


def single_pic_proc(image_file):
    image = np.array(PIL.Image.open(image_file).convert('RGB'))
    result, image_framed = ocr(image)
    return result, image_framed


class MainApp(MDApp):
    def build(self):
        return ScreenManagement()

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
            global output_file
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
            txt_f.close()

    def play_music(self):
        with open(txt_file + '.txt', 'r') as f:
            line = f.read()
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[1].id)
            engine.save_to_file(line, txt_file + '.mp3')
            # engine.say(line)
            engine.runAndWait()
        music = SoundLoader.load(txt_file + '.mp3')
        if music:
            music.play()

    def showText(self):
        # with open('Noura.txt', 'r') as f:
        #         self.ids['Label1'].text = f.read()
        MainApp.Demo(self)
        with open(txt_file + '.txt', 'r') as f:
            self.ids['Label1'].text = f.read()


if __name__ == '__main__':
    MainApp().run()
    print("")
