from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
import requests
import threading
from kivy.clock import mainthread

class SettingsContent(MDBoxLayout):
    pass
 
class SdApp(MDApp):
    def build(self):
        self.title = "Subdomain-Finder"
        self.theme_cls.theme_style = "Light"   
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.hue="700"
        return Builder.load_file("sub.kv") 
        
    @mainthread
    def search(self, text):
        t1 = threading.Thread(target=self.find, args=(text,), daemon=True)
        t1.start()

    def find(self, text):
        domain = self.root.ids.domain.text
        self.root.ids.rc_spin.active = True
       # if domain == "":
#            enter_domain = MDDialog(title="error" ,text='Please enter a domain')
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
             self.root.ids.subdomains.text = (
                "Sorry unable to find "
                + self.root.ids.domain.text
            )
        self.root.ids.rc_spin.active = False
             
    def open_settings(self):
        self.settings = MDDialog(
            content_cls=SettingsContent(),
            type="custom",
        )
        self.settings.open()
        
    def clear(self):
        self.root.ids.subdomains.text = ""
    def copy(self):
        self.root.ids.subdomains.copy()
    def dark(self):
        self.theme_cls.theme_style = self.theme_cls.theme_style == "Dark" and "Light" or "Dark"
        #self.message = "Switched to Light/Dark" 
        #self.root.ids.mod.text = self.message
        
SdApp().run()