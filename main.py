import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader 
from kivy.uix.button import Button 
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.popup import Popup  
from kivy.uix.label import Label 
from threading import Thread
import os
from gtts import gTTS 
import PyPDF2
from android.permissions import request_permissions, Permission
# request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

class FirstWindow(Screen):
    filename = ""

    def text_process(self,text):
        text = text.replace("\n", "")
        return text


    def text_to_speech(self):
        layout = GridLayout(cols = 1, padding = 10)
  
        popupLabel = Label(text = "Process Started...")
        closeButton = Button(text = "OK")
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
        popup = Popup(title ='Notify',
                      content = layout,size_hint =(None, None), size =(600, 600))  
        popup.open()   
        closeButton.bind(on_press = popup.dismiss)  
        pdfReader = PyPDF2.PdfFileReader(open(self.filename, 'rb'))
        text = ""
        for page_num in range(pdfReader.numPages):
            text +=  pdfReader.getPage(page_num).extractText()

        text = self.text_process(text)
        myobj = gTTS(text=text, lang='en',tld='co.in', slow=False)
        LINUX_PATH = "media/output/"
        ANDROID_PATH = "/storage/emulated/0/AudioBook/"
        if(kivy.utils.platform=='android'):
            if(os.path.exists(ANDROID_PATH)):
                file1 = open(ANDROID_PATH+self.filename.split('/')[-1].split('.')[0]+".txt","w")
                file1.write(text)
                myobj.save(ANDROID_PATH+self.filename.split('/')[-1].split('.')[0]+".wav") 
            else:
                os.mkdir(ANDROID_PATH)
                file1 = open(ANDROID_PATH+self.filename.split('/')[-1].split('.')[0]+".txt","w")
                file1.write(text)
                myobj.save(ANDROID_PATH+self.filename.split('/')[-1].split('.')[0]+".wav") 
        else:
            if(os.path.exists(LINUX_PATH)):
                file1 = open(LINUX_PATH+self.filename.split('/')[-1].split('.')[0]+".txt","w")
                file1.write(text)
                myobj.save(LINUX_PATH+self.filename.split('/')[-1].split('.')[0]+".wav") 
            else:
                os.mkdir(LINUX_PATH)
                file1 = open(LINUX_PATH+self.filename.split('/')[-1].split('.')[0]+".txt","w")
                file1.write(text)
                with open(LINUX_PATH+self.filename.split('/')[-1].split('.')[0]+".wav", 'wb') as f:
                    myobj.write_to_fp(f)


    def process(self):
        # self.text_to_speech()
        t = Thread(target=self.text_to_speech)
        t.daemon = True
        t.start() 

    def play(self):
        if(kivy.utils.platform=='android'):
            ANDROID_PATH = "/storage/emulated/0/AudioBook/1611.wav"
            sound = SoundLoader.load(ANDROID_PATH) 
        else:
            LINUX_PATH = "media/output/"
            sound = SoundLoader.load(LINUX_PATH+self.filename.split('/')[-1].split('.')[0]+".wav") 
        if sound:
            layout = GridLayout(cols = 1, padding = 10)
  
            popupLabel = Label(text = "Audio Playin....")
            closeButton = Button(text = "OK")
    
            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)       
            popup = Popup(title ='Notify',
                        content = layout,size_hint =(None, None), size =(600, 600))  
            popup.open()   
            closeButton.bind(on_press = popup.dismiss)  
            sound.play() 


class SecondWindow(Screen):
    filename = ""
    def selected(self,filename): 
        try:
            self.filename = filename[0]
            self.manager.get_screen('first').ids.my_image.source = filename[0]
        except:
            pass

    def process(self):
        self.manager.get_screen('first').filename = self.filename
        self.manager.get_screen('first').ids.file_choosen.text = (self.filename).split('/')[-1]
        # self.manager.get_screen('first').ids.process.disabled = False

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('window.kv')

class AudioBook(App):
    def build(self):
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        Window.clearcolor= (1,1,1,0.5)
        return kv
    


if __name__=='__main__':
    AudioBook().run()