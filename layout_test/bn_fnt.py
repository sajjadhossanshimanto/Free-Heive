from kivymd.app import MDApp
# from kivy.app import App
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
import arabic_reshaper
import bidi.algorithm


bn='উচ্চতর গণিত'
fnt='font/NotoSerifBengla.ttf'
class TestApp(MDApp):
    def build(self):
        text = bn
        # text = arabic_reshaper.reshape(bn)
        # text = bidi.algorithm.get_display(text)
        p = MDLabel(text=text, markup=True, color=(0, 0, 0, 1))
        p.font_name = fnt
        return p

TestApp().run()