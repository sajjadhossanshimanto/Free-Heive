__version__ = "0.3.0"

from kivy.base import ExceptionHandler, ExceptionManager
from kivy.config import Config
import sys
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from script.vimeo import Vimeo
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from custom.item_list import SectionItem, SubjectItem, ChapterItem, VideoItem, QuelityItem
from script.data_base import DB

try:
    import android
    from jnius import autoclass
    from plyer.platforms.android import activity
except ImportError:
    android = None

FROZEN = getattr(sys, "frozen", False) or android
if not FROZEN:
    from traceback import format_exception
    # from iamlaizy import reload_me

    # hiden_dependencies =['kvs', 'custom']
    # reload_me(*hiden_dependencies,  filter_extc=['.kv'])

    H = 700
    W = H * (1080/1920)# 1920/1080 ratio

    Window.size = (W, H)

# Setting size to resizable
Config.set('graphics', 'resizable', 1)
excepthook=None

def log(title, text):
    MDDialog(
        title=title,
        type="simple",
        text=text
    ).open()


d = DB('data/eduheive/hsc.db')
class EduHive(MDApp):
    bng_fnt = 'data/font/NotoSerifBengla.ttf'
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
        # d.select_subject('উচ্চতর গণিত')
        # self.list_video('অনুশীলনী ১.১ঃ ম্যাট্রিক্স')
        # return

        self.root.ids.chapter_name.ids.label_title.font_name = self.bng_fnt
        self.root.ids.subject_name.ids.label_title.font_name = self.bng_fnt
        self.root.ids.section_name.ids.label_title.font_name = self.bng_fnt

        for i in d.list_subject():
            self.root.ids.subjects.add_widget(SubjectItem(
                title=i,
                font_name=self.bng_fnt,
                img=f'data/image/{i}.jpg',
                manager=self
            ))

    def change_screen(self, sc_name):
        # TODO: show loading process, change scrren before loading widget
        self.root.current = sc_name

    def forward_link(self, url):
        if not android:
            print(url)
            return 

        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')

        intent = Intent()
        intent.setAction(Intent.ACTION_VIEW)
        intent.setData(Uri.parse(url))

        activity.startActivity(intent)

    def play_video(self, video_id):# '622338938'
        if not video_id.isdecimal():
            log('Info', 'sorry this item is not playable')
            return
        
        v = Vimeo(video_id)
        items = [
            QuelityItem(text=str(t), link=l) 
            for t, l in v.get_quality().items()
        ]
        MDDialog(
            title="Select Quality",
            type="simple",
            items=items
        ).open()

    def list_video(self, section_name):
        # TODO; clear thumblain, 
        self.root.ids.section_name.title = section_name

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
        
        log('ERROR', str(type(inst)))
        return ExceptionManager.PASS

ExceptionManager.add_handler(E())


EduHive().run()

