from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.list import OneLineListItem, IconLeftWidget, OneLineRightIconListItem, TwoLineAvatarIconListItem, IconRightWidget, MDList
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior


KV = '''
<SubjectItem>
    size_hint_y: None
    height: "200dp"
    radius: 24

    MDSmartTile:
        id: tile
        radius: 24
        box_radius: 0, 0, 24, 24
        box_color: 0, 0, 0, .5
        source: root.img
        size_hint: None, None
        size: root.size
        mipmap: True
        on_release: root.on_release()

        Label:
            text: root.title
            font_name: root.font_name
            bold: True
            font_style: "H6"
            opposite_colors: True

'''
Builder.load_string(KV)

class SubjectItem(MDBoxLayout):
    img = StringProperty()
    font_name = StringProperty()
    title = StringProperty()
    manager = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.tile.ids.image.ripple_duration_in_fast = 0.05

    def on_release(self):
        self.manager.list_chapter(self.title)



KV = '''
<ChapterItem>
    IconRightWidget:
        icon: 'arrow-right'
'''
Builder.load_string(KV)

class ChapterItem(OneLineRightIconListItem):
    manager = ObjectProperty()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids._lbl_primary.font_name = self.manager.bng_fnt

    def on_release(self):
        return self.manager.list_section(self.text)


class SectionItem(OneLineListItem):
    manager = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids._lbl_primary.font_name = self.manager.bng_fnt

    def on_release(self):
        return self.manager.list_video(self.text)



KV = '''
<VideoItem>
    on_release: app.play_video(self.video_id)

    IconLeftWidget:
        icon: "plus"

    IconRightWidget:
        icon: "minus"

'''
Builder.load_string(KV)

class VideoItem(TwoLineAvatarIconListItem, RoundedRectangularElevationBehavior):
    #TODO: on_release: fetch info, update_thumblain, 
    video_id = StringProperty()

    def __init__(self, font_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids._lbl_primary.font_name = font_name
        # self.add_widget(IconLeftWidget(
            # source='data/image/play.jpg'
        # ))

