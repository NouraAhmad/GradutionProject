# import os
# from ocr import ocr
# import time
# import shutil
# import numpy as np
# from PIL import Image
# from glob import glob
# import pyttsx3
#
# def single_pic_proc(image_file):
#     image = np.array(Image.open(image_file).convert('RGB'))
#     result, image_framed = ocr(image)
#     return result,image_framed
#
#
# if __name__ == '__main__':
#     image_files = glob('./test_images/*.*')
#     result_dir = './test_result'
#     if os.path.exists(result_dir):
#         shutil.rmtree(result_dir)
#     os.mkdir(result_dir)
#
#     for image_file in sorted(image_files):
#         t = time.time()
#         result, image_framed = single_pic_proc(image_file)
#         output_file = os.path.join(result_dir, image_file.split('/')[-1])
#         txt_file = os.path.join(result_dir, image_file.split('/')[-1].split('.')[0]+'.txt')
#         print(txt_file)
#         txt_f = open(txt_file, 'w')
#         Image.fromarray(image_framed).save(output_file)
#         print("Mission complete, it took {:.3f}s".format(time.time() - t))
#         print("\nRecognition Result:\n")
#         for key in result:
#             print(result[key][1])
#             txt_f.write(result[key][1]+'\n')
#         txt_f.close()
#         # Start - initialisation
#         # testing
#         with open(txt_file, 'r') as f:
#             line = f.read()
#             engine = pyttsx3.init()
#             engine.setProperty("rate", 150)
#             voices = engine.getProperty("voices")
#             engine.setProperty("voice", voices[10].id)
#             engine.say(line)
#             engine.runAndWait()
#         # engine.save_to_file(lines, 'speech.mp3')

# from kivy.app import App
# from kivy.uix.label import Label
#
#
# class SimpleApp(App):
#     def build(self):
#         l = Label(text="Welcome to recoginze & say it!", font_size=20)
#         return l
#
#
# if __name__ == "__main__":
#     SimpleApp().run()
import kivy
from kivy.app import App
# this packge to connect kv file with main
from kivy.lang import Builder
# this packge to mange the screen
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.config import Config
from kivy.core.text import LabelBase
LabelBase.register(name="Regular",
                   fn_regular="KaushanScript-Regular.otf")

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)
class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv= Builder.load_file("App.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()