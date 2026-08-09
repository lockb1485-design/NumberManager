__version__ = "1.0.0"

import os
import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.utils import platform


class NumberManager(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 12

        self.selected_files = []

        title = Label(
            text="Number Manager",
            font_size=28,
            size_hint_y=None,
            height=65
        )

        number = Label(
            text="Demo Number\n+20 10 1234 5678",
            font_size=20,
            size_hint_y=None,
            height=75
        )

        self.status = Label(
            text="Telegram: Not configured",
            font_size=18,
            size_hint_y=None,
            height=50
        )

        self.selected_status = Label(
            text="Selected: 0 photos",
            font_size=18,
            size_hint_y=None,
            height=50
        )

        select_button = Button(
            text="Select Photos",
            size_hint_y=None,
            height=60
        )

        select_button.bind(
            on_press=self.open_photo_picker
        )

        send_button = Button(
            text="Send Selected Photos",
            size_hint_y=None,
            height=60
        )

        send_button.bind(
            on_press=self.send_selected_photos
        )

        info = Label(
            text="Photos are sent only after you select them and press Send.",
            font_size=14
        )

        self.add_widget(title)
        self.add_widget(number)
        self.add_widget(self.status)
        self.add_widget(self.selected_status)
        self.add_widget(select_button)
        self.add_widget(send_button)
        self.add_widget(info)

    def open_photo_picker(self, instance):

        if platform == "android":
            start_path = "/storage/emulated/0/"
        else:
            start_path = os.path.expanduser("~")

        chooser = FileChooserIconView(
            path=start_path,
            filters=[
                "*.jpg",
                "*.jpeg",
                "*.png",
                "*.webp"
            ],
            multiselect=True
        )

        confirm_button = Button(
            text="Confirm Selection",
            size_hint_y=None,
            height=60
        )

        layout = BoxLayout(
            orientation="vertical"
        )

        layout.add_widget(chooser)
        layout.add_widget(confirm_button)

        popup = Popup(
            title="Select Photos",
            content=layout,
            size_hint=(0.95, 0.9)
        )

        confirm_button.bind(
            on_press=lambda x: self.confirm_selection(
                chooser,
                popup
            )
        )

        popup.open()

    def confirm_selection(self, chooser, popup):

        self.selected_files = list(chooser.selection)

        self.selected_status.text = (
            f"Selected: {len(self.selected_files)} photos"
        )

        popup.dismiss()

    def send_selected_photos(self, instance):

        if not self.selected_files:
            self.status.text = "Please select photos first."
            return

        self.status.text = "Ready to send."

        self.show_message(
            "Telegram",
            "The Telegram connection will be added after the APK interface is tested."
        )

    def show_message(self, title, message):

        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        )

        popup.open()


class NumberManagerApp(App):

    def build(self):
        return NumberManager()


if __name__ == "__main__":
    NumberManagerApp().run()
