from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem, OneLineRightIconListItem
from custom.item_list import QuelityItem

KV = '''
MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_simple_dialog()
'''


class Item(OneLineAvatarListItem):
    divider = None
    link = StringProperty()
    source = StringProperty()

    def on_release(self):
        print('ok')


class Example(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"

        return Builder.load_string(KV)

    def show_simple_dialog(self):
        if not self.dialog:
            MDDialog(
                title="Set backup account",
                type="simple",
                items=[
                    # Item(text=str(i), link='llll') 
                    QuelityItem (text=str(i), link='llll') 
                    for i in range(3)
                ],
            ).open()
        # self.dialog.open()


Example().run()