# Imports
from kivy.core.clipboard import Clipboard
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
import requests
import threading
from kivy.clock import mainthread
from kivy.properties import StringProperty
import arabic_reshaper
from bidi.algorithm import get_display 


    
class MainScreen(MDScreen):
    bidi_text = StringProperty('')
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(**kwargs)
        reshaped_text = arabic_reshaper.reshape(u"الوضع المظلم")
        self.bidi_dark = get_display(reshaped_text)
        reshaped_text = arabic_reshaper.reshape(u"استخراج العناوين الفرعية")
        self.bidi_title = get_display(reshaped_text)
        reshaped_text = arabic_reshaper.reshape(u"google.com")
        self.bidi_text = get_display(reshaped_text)
        reshaped_text = arabic_reshaper.reshape(u"بحث")
        self.bidi_find = get_display(reshaped_text)
        reshaped_text = arabic_reshaper.reshape(u"تعذر ايجاد")
        self.bidi_unable  = get_display(reshaped_text)
        reshaped_text = arabic_reshaper.reshape(u"مسح")
        self.bidi_clear = get_display(reshaped_text)
        reshaped_text = arabic_reshaper.reshape(u"نسخ للحافظة")
        self.bidi_copy = get_display(reshaped_text)
        


# Min App Class        
class SdApp(MDApp):
    def build(self):
        self.title = "Subdomain-Finder"
        self.theme_cls.theme_style = "Light"   
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.hue="700"
        return Builder.load_file("sub.kv") 
        
    # Spinner Main Thread
    @mainthread
    def search(self, text):
        t1 = threading.Thread(target=self.find, args=(text,), daemon=True)
        t1.start()
        
    # Find subdomains function
    
    def find(self, text):
        domain = self.root.ids.domain.text
        self.root.ids.rc_spin.active = True
        try:
            r = requests.get("http://api.hackertarget.com/hostsearch/?q=" +domain)
            if r.status_code == 200:
                results = r.text.split("\n")
                with open(f"{domain}-sub.txt","w") as file:
                    for result in results:
                        subdomain = result.split(",")[0]
                        file.write(subdomain+"\n")
            with open(f"{domain}-sub.txt","r") as file:
                data = file.read()
                self.root.ids.subdomains.text = f"Subdomains of {domain} \n\n{data}"
        except Exception as e:
             print(e)
             self.root.ids.subdomains.text = f"{root.bidi_unable}+ {self.root.ids.domain.text}"
 
        self.root.ids.rc_spin.active = False
             
    # clear function
    
    def clear(self):
        self.root.ids.subdomains.text = ""
        
    # copy to Clipboard function
    
    def copy(self):
        Clipboard.copy(self.root.ids.subdomains.text)
    # Dark/Light switch function
    
    def dark(self):
        self.theme_cls.theme_style = self.theme_cls.theme_style == "Dark" and "Light" or "Dark"
        
SdApp().run()
