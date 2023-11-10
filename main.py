from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
import requests, json
               
class DemoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"   
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.hue="700"
        return Builder.load_file("sub.kv") 
      
    def find(self):
        domain = self.root.ids.domain.text
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
        except FileNotFoundError and requests.exceptions.ConnectionError:
             self.root.ids.subdomains.text = "Error ! Check Your Internet Connection "
                
    def clear(self):
        self.root.ids.subdomains.text = ""
        
DemoApp().run()    
