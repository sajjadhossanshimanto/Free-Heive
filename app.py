__version__ = "0.3.0"

from kivy.base import ExceptionHandler, ExceptionManager
from kivy.config import Config
import sys
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from custom.item_list import SubjectItem
from kivymd.uix.list import OneLineRightIconListItem, IconRightWidget, MDList

from script.data_base import DB

try:
    import android
except ImportError:
    android = None

FROZEN = getattr(sys, "frozen", False) or android
if not FROZEN:
    from traceback import format_exception
    from iamlaizy import reload_me

    hiden_dependencies =['kvs', 'custom']
    reload_me(*hiden_dependencies,  filter_extc=['.kv'])

    H = 700
    W = H * (1080/1920)# 1920/1080 ratio

    Window.size = (W, H)

# Setting size to resizable
Config.set('graphics', 'resizable', 1)
excepthook=None



d = DB('data/eduheive/hsc.db')
class EduHive(MDApp):
    bng_fnt = 'font/NotoSerifBengla.ttf'
    app_name = 'Free Hive'
    color_scheme = {
        "bg": get_color_from_hex('#282F37'),# 91% black
        "blue": '#263347',
        'green': '#03C03C',
        'white': [1, 1, 1, 1]
    }

    def build(self):
        self.theme_cls.theme_style = "Dark"

        return Builder.load_file('kvs/app.kv')

    def on_start(self):
        
        #TODO: add with loop
        for i in d.list_subject():
            self.root.ids.subjects.add_widget(SubjectItem(
                title=i,
                font_name=self.bng_fnt,
                img='data/image/bio.img',
                manager=self
            ))

    def change_screen(self, sc_name):
        self.root.current = sc_name

    def list_section(self, chapter_name):
        pass

    def list_chapter(self, sub_name):
        # fix it
        # print(sub_name)
        self.root.ids.subject_name.title = sub_name
        d.select_subject(sub_name)

        #TODO; cleat list
        list_view = self.root.ids.container
        chapters = d.list_all_chapter()
        if not d.paper_count():
            # whatif already removed !!
            # self.root.remove_widget(self.root.ids.)
            for i in chapters.index:
                item = OneLineRightIconListItem(text=i)
                item.on_release = lambda x: self.list_section(i)
                item.add_widget(IconRightWidget(icon='arrow-right'))
                
                list_view.add_widget(item)
        else:
            for i in chapters.index:
                item = OneLineRightIconListItem(text=i)
                item.on_release = lambda x: self.list_section(i)
                item.add_widget(IconRightWidget(icon='arrow-right'))
                
                list_view.add_widget(item)


        self.change_screen('chapters')
        return 
    
class E(ExceptionHandler):
    def handle_exception(self, inst):
        if not FROZEN:
            return ExceptionManager.RAISE
        
        excepthook()
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())


EduHive().run()






# Creating App class
class CalculatorApp(MDApp):
    color_scheme = {
        "background": get_color_from_hex('#282F37'),# 91% black
        "blue": '#263347',
        'green': '#03C03C',
        'white': [1, 1, 1, 1]
    }

    def build(self):
        
        return Builder.load_file('kvs/app.kv')


