from ocr import ocr
import numpy as np
import PIL.Image
import pyttsx3
# !/usr/bin/env python
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import time
from kivy.clock import Clock
from kivy.core.text import LabelBase
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
    # Adding Box Layoyt
    BoxLayout:
        orientation: 'vertical'
        # background for logo problem:
        canvas.before:  
            Color:
                rgba: rgba('#ffffff')
            Rectangle:
                pos: 10, 10
                size: 360 , 600
            Color:
                rgba: 0,0,0,0.4
            Line:
                points: self.pos[0]+(0.1*self.width), self.pos[1]+(0.5*self.height), self.pos[0]+(0.9*self.width), self.pos[1]+(0.5*self.height)
    MDLabel: 
        text: 'Recognize & Say it'
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

    # Adding image from the system
    Image:
        source:'logo.png'
        halign: 'center' 
        pos_hint: {'center_x':0.5,'center_y':0.7}
        # Giving the size of image
        size_hint: 0.7, 0.7
        # allow stretching of image
        allow_stretch: True

    MDLabel: 
        text: 'Welcome To'
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.4}     
        font_size:30
        bold:True
        color:(0/255, 200/255, 247/255, 0.7)

    MDLabel: 
        text: '[b]RECOGNIZE & SAY IT[/b]'
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.3}     
        font_size:30
        bold:True
        color:(0, 155/255, 255/255, 1)
        font_name:"Regular"
        markup: True

    MDLabel: 
        text: 'APPLICATION'
        halign: 'center'
        pos_hint: {'center_x':0.5,'center_y':0.2}     
        font_size:30
        bold:True
        color:(0/255, 200/255, 247/255, 0.7)


<HomeScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        canvas.before:  
            Color:
                rgba: rgba('#ffffff')
            Rectangle:
                pos: 10, 10
                size: 360 , 600    
            Color:
                rgba: rgba('#EFEFEF')
            Triangle:
                points:[self.size[0],self.size[1]-(.8*self.size[1]) ,self.size[0],0, 0, 0]

            Color:
                rgba: rgba('#DAE5FA')
            Triangle:
                points:[0, self.size[1]-(.85*self.size[1]) ,self.size[0]-(.3*self.size[1]),0, 0,0]
            Color:
                rgba: 0,0,0,0.4
            Line:
                points: self.pos[0]+(0.1*self.width), self.pos[1]+(0.2*self.height), self.pos[0]+(0.9*self.width), self.pos[1]+(0.2*self.height)
    MDLabel: 
        text: 'Recognize & Say it'
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
        pos_hint: {'center_x':0.5,'center_y':0.7}
        # Giving the size of image
        size_hint: 0.7, 0.7
        # allow stretching of image
        allow_stretch: True
    MDRectangleFlatButton:
        text: 'Scanning a new image'
        font_size: "22sp"
        size_hint: (.65, .125)
        pos_hint: {'center_x':0.5,'center_y':0.4}
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 1
        line_color: 0, 0, 0, 1
        on_press: 
            root.manager.transition.direction = 'left'
            root.manager.transition.duration = 1
            root.manager.current='camera'
        background_color: (243/255 , 243/255 , 243/255 ,1)
        canvas.before:
            Color: 
                rgba: self.background_color
            Rectangle:
                size : self.size
                pos: self.pos

    MDRectangleFlatButton:
        text: 'contact us '
        font_size: "19sp"
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.3,'center_y':0.12}  
        on_press: root.manager.current='concat'
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 0.75
        line_color: 0, 0, 0, 0
    MDRectangleFlatButton:
        text: 'instructions '
        font_size: "19sp"
        size_hint: (.31, .08)
        pos_hint: {'center_x':0.7,'center_y':0.12}  
        on_press: root.manager.current='welcome'  
        theme_text_color: "Custom"
        text_color: 0, 0, 0, 0.75
        line_color: 0, 0, 0, 0

<CheckScreen>:
    name:'camera'
    id: entry

    canvas:
        Color:
            rgb: [1,1,1]
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:

        Camera:
            id: camera
            index: 0
            resolution: (1280,720)
            play: True  
        MDRectangleFlatButton:
            text: 'Take photo'
            font_size: "19sp"
            size_hint: (.50, .07)
            pos_hint: {'center_x':0.5,'center_y':0.08}  
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
            line_color: 0, 0, 0, 1
            on_press: 
                root.capture()   #TAKE PHOTO
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'process'
            background_color: (210/255 , 210/255 , 210/255 ,1)
            canvas.before:
                Color: 
                    rgba: self.background_color
                Rectangle:
                    size : self.size
                    pos: self.pos


        MDIconButton:
            icon: 'chevron-double-left'
            pos_hint: {'center_x':.09, 'center_y':.94}
            user_font_size: "40sp"


            on_press:
                root.manager.transition.direction = 'right'
                root.manager.transition.duration = 1
                root.manager.current = 'home'


# 
# <ProcessScreen>:
#     name: 'process'
#     BoxLayout:
#         orientation: 'vertical'
#         canvas.before:      
#             Color:
#                 rgba: rgba('#EFEFEF')
#             Triangle:
#                 points:[0, self.size[1] ,self.size[0],0, 0, 0]
# 
#             Color:
#                 rgba: rgba('#DAE5FA')
#             Triangle:
#                 points:[0, self.size[1],self.size[0]-(.3*self.size[1]),self.size[1], 0,self.size[1]-(.4*self.size[1])]
# 
#     MDLabel:    
#         text: 'Recognize & Say it'
#         # halign: 'center'
#         # pos_hint: {'center_x':0.5,'center_y':0.91}
#         halign: 'center'
#         pos_hint: {'center_x':0.5,'center_y':0.95}
#         background_color: (243/255 , 243/255 , 243/255 ,1)
#         size_hint: 1, 0.1
#         font_size: self.width/20
#         canvas.before:
#             Color: 
#                 rgba: self.background_color
#             Rectangle:
#                 size : self.size
#                 pos: self.pos
#     FloatLayout:
#         Image:
#             id: img
#             halign: 'center' 
#              # we need size 
#             #size: self.texture_size
#             pos_hint: {'center_x':0.5,'center_y':0.6}
# 
# 
#     MDRectangleFlatButton:
#         text: 'process '
#         size_hint: (.31, .08)
#         pos_hint: {'center_x':0.3,'center_y':0.2}  
#         on_press: root.manager.current='sayit'; app.Demo()
# 
# 
#     MDRectangleFlatButton:
#         text: 'Home Page '
#         size_hint: (.31, .08)
#         pos_hint: {'center_x':0.7,'center_y':0.2}  
#         on_press: root.manager.current='home'
# 



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
            # Giving the size of image
            size_hint: 0.8, 0.8
            # allow stretching of image
            allow_stretch: True
            pos_hint: {'center_x':0.5,'center_y':0.6}

        MDRectangleFlatButton:
            text: 'process'
            font_size: "19sp"
            size_hint: (.50, .07)
            pos_hint: {'center_x':0.5,'center_y':0.18}  
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
            line_color: 0, 0, 0, 1

            background_color: (210/255 , 210/255 , 210/255 ,1)
            canvas.before:
                Color: 
                    rgba: self.background_color
                Rectangle:
                    size : self.size
                    pos: self.pos

            on_press: root.manager.current='sayit'; app.Demo()


        MDRectangleFlatButton:
            text: 'Home Page'
            font_size: "19sp"
            size_hint: (.50, .07)
            pos_hint: {'center_x':0.5,'center_y':0.08}  
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
            line_color: 0, 0, 0, 1
            on_press: root.manager.current='home'
            background_color: (210/255 , 210/255 , 210/255 ,1)
            canvas.before:
                Color: 
                    rgba: self.background_color
                Rectangle:
                    size : self.size
                    pos: self.pos





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
global Result

class WelcomeScreen(Screen):
    def switch(self, *args):
        self.parent.current = "home"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 3)


class HomeScreen(Screen):
    pass


class CheckScreen(Screen):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    main_widget = None
    photo = StringProperty('')

    def capture(self):
        camera = self.ids['camera']
        self.photo = f"IMG_{time.strftime('%Y%m%d_%H%M%S')}.png"
        camera.export_to_png(self.photo)
        global IMG
        IMG= self.photo
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
    global result
    result, image_framed = ocr(image)
    return result, image_framed


class MainApp(MDApp):
    def build(self):
        return ScreenManagement()

    def Demo(self):


        result, image_framed = single_pic_proc(IMG)

        Result=""

        print("Mission complete,")
        print("\nRecognition Result:\n")
            # print all the containt in images
            #for key in result:
        for key in result:
            print(result[key][1])
            Result+= result[key][1]


    def play_music(self):

        for key in result:
            engine = pyttsx3.init()
            engine.setProperty("rate", 150)
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[1].id)
            engine.say(result[key][1])
            engine.runAndWait()

    def showText(self):
        #it cant reach Result attribute until i called Demo method here
        MainApp.Demo(self)

        Result=""
        for key in result:
            Result+= result[key][1]

        self.ids.Label1.text = Result




if __name__ == '__main__':
    MainApp().run()
    print("")
