__version__ = "0.3.0"

from kivy.base import ExceptionHandler, ExceptionManager
from kivy.config import Config
from kivy.clock import Clock
import sys
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar.toolbar import MDTopAppBar
from custom.item_list import SectionItem, SubjectItem, ChapterItem, VideoItem
from functools import partial
from kivymd.uix.list import OneLineListItem, TwoLineAvatarIconListItem
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
        # self.change_screen('video_screen')
        self.root.ids.siver_bar.toolbar_cls = MDTopAppBar(
            # title = "Headline medium"
            left_action_items = [["arrow-left", lambda x: x]],
            right_action_items = [
                ["satellite-uplink", lambda x: x],
            ]
        )
        # return

        self.root.ids.chapter_name.ids.label_title.font_name = self.bng_fnt
        self.root.ids.subject_name.ids.label_title.font_name = self.bng_fnt

        for i in d.list_subject():
            self.root.ids.subjects.add_widget(SubjectItem(
                title=i,
                font_name=self.bng_fnt,
                img='data/image/bio.img',
                manager=self
            ))

    def change_screen(self, sc_name):
        self.root.current = sc_name

    def play_video(self, video_id):
        print(video_id)

    def list_video(self, section_name):
        # TODO; clear thumblain, 
        list_view = self.root.ids.video_list
        list_view.children=[]
        list_view.canvas.clear()

        videos=d.list_listion(section_name)
        for name in videos.index:
            video_id, duration = videos.loc[name]
            item = VideoItem(
                text = name,
                font_name = self.bng_fnt,
                secondary_text = f"{duration} Min",
                video_id = str(video_id)
            )

            list_view.add_widget(item)

        self.change_screen('video_screen')


    def list_section(self, chapter_name):
        self.root.ids.chapter_name.title = chapter_name

        list_view = self.root.ids.sub_chapter
        list_view.children=[]
        list_view.canvas.clear()
        
        for i in d.list_section(chapter_name):
            i=i[0]
            item = SectionItem(text=i, manager=self)
            list_view.add_widget(item)

        self.change_screen('sections')

    def list_chapter(self, sub_name):
        # self.root.ids.subject_name.
        self.root.ids.subject_name.title = sub_name
        d.select_subject(sub_name)
        
        list_view = self.root.ids.container
        
        list_view.children=[]
        list_view.canvas.clear()
 
        for i in d.list_all_chapter().index:
            item = ChapterItem(
                manager=self,
                text = i
            )
            list_view.add_widget(item)
    
        self.change_screen('chapters')
    
class E(ExceptionHandler):
    def handle_exception(self, inst):
        if not FROZEN:
            return ExceptionManager.RAISE
        
        excepthook()
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())


EduHive().run()

