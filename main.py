from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
import numpy as np
import cv2
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader

Builder.load_file('myvisioneyeslayout.kv')

class AndroidCamera(Camera):
    camera_resolution = (640, 480)
    cam_ratio = camera_resolution[0] / camera_resolution[1]

class MyVisionEyesLayout(BoxLayout):
    pass


class MyVisionEyes(App):
    riskTitle = None
    globalImage = None
    countDetect = 0
    cat_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')
    person_cascade = cv2.CascadeClassifier('haarcascade_frontalface.xml')
    welcome = SoundLoader.load('welcome.mp3')
    detected_risk = SoundLoader.load('detected_risk.mp3')
    person_risk = SoundLoader.load('person.mp3')
    cat_risk = SoundLoader.load('cat.mp3')

    def build(self):
        return MyVisionEyesLayout()

    def on_start(self):
        if self.welcome:
            self.welcome.play()
        Clock.schedule_once(self.get_frame, 5)
                    

    def get_frame(self, dt):        
        cam = self.root.ids.a_cam
        image_object = cam.export_as_image(scale=round((400 / int(cam.height)), 2))
        w, h = image_object._texture.size
        frame = np.frombuffer(image_object._texture.pixels, 'uint8').reshape(h, w, 4)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
        self.root.ids.frame_risk.text = f'Riesgo: {self.riskTitle}'
        
        cat = self.cat_cascade.detectMultiScale(gray, 1.3, 5)
        person = self.person_cascade.detectMultiScale(gray, 1.3, 5)

        if len(cat)>0:
            self.object_detector(cat, "Gato")
            self.countDetect +=1
            if self.countDetect==1:
                self.cat_risk.bind(on_stop=self.play_detected_risk)
                self.cat_risk.play() 
        elif len(person)>0:
            self.object_detector(person, "Persona")
            self.countDetect +=1
            if self.countDetect==1:
                self.person_risk.bind(on_stop=self.play_detected_risk)
                self.person_risk.play()
        else:
            self.clear()   
        
        Clock.schedule_once(self.get_frame, 0.25)

    def object_detector(self, objet_list, title):
        for (x,y,w,h) in objet_list:
            self.globalImage = True
            self.riskTitle = title          
    def clear(self):
        if self.globalImage!=None:
            self.globalImage = None
            self.riskTitle = None
            self.countDetect = 0  
    def play_detected_risk(self, instance):
        self.detected_risk.play()                 

if __name__ == "__main__":
    MyVisionEyes().run()