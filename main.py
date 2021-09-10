import time
from threading import Thread

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.spinner import MDSpinner
from weather import search

Window.size = (300, 500)


class WeatherApp(MDApp):
    def build(self):
        Clock.schedule_once(self.animate_window)
        self.theme_cls.theme_style = "Dark"
        self.toast_duration = 1.0
        self.searching = False
        self.dialog = MDDialog(title=" ", auto_dismiss=False, type='simple',
                               buttons=[MDFlatButton(text="Done", theme_text_color="Custom",
                                                     text_color=self.theme_cls.primary_color,
                                                     on_release=self.search_for_city_weather_info),
                                        MDFlatButton(text="Cancel", theme_text_color='Custom',
                                                     text_color=self.theme_cls.primary_color,
                                                     on_release=self.cancel), ], )
        self.search_for = MDTextField(pos_hint={"center_x": .5}, size_hint_x=0.8, hint_text="Enter to city name")
        self.dialog.add_widget(self.search_for)
        return Builder.load_file("weather.kv")

    def animate_window(self, dt):
        anim = Animation(opacity=1)
        anim.start(self.root)
        write = Thread(target=self.write, daemon=True)
        write.start()

    def write(self):
        text = "Search for a location to\n display weather information"
        text = ''.join(text)
        self.root.ids.temp.text = ""
        for letter in text:
            self.root.ids.temp.text += letter
            time.sleep(0.05)

    def cancel(self, btn):
        self.dialog.dismiss()

    def search_for_city_weather_info(self, btn):
        if self.search_for.text:
            self.dialog.dismiss()
            self.city_name = self.search_for.text
            self.search_for.text = ""
            th = Thread(target=self.do_search, daemon=True)
            th.start()
        else:
            toast("Type in something", duration=self.toast_duration)

    def do_search(self):
        if not self.searching:
            self.searching = True
            spinner = MDSpinner(size_hint=(None, None), size=(30, 30), pos_hint={"center_y": .5}, active=True)
            self.root.ids.bar.add_widget(spinner)
            self.weather_information = search(self.city_name)

            if self.weather_information == 404:
                toast("Connection error!", duration=self.toast_duration)

            elif self.weather_information[0] == "City not found":
                toast("City not found", duration=self.toast_duration)

            else:
                anim = Animation(opacity=0)
                anim.bind(on_complete = self.update_labels)
                anim.start(self.root)

            spinner.active = False
            self.root.ids.bar.remove_widget(spinner)
            self.searching = False

        else:
            toast("Wait...", duration=self.toast_duration)
        quit()

    def update_labels(self, *instance):
        info = self.weather_information
        self.root.ids.weather_title.text = f"{info[0]}"
        self.root.ids.weather_description.text = f"{info[1]}"
        self.root.ids.temp.text = f"{info[3]} deg C"
        self.root.ids.temp.font_style = "H3"
        self.root.ids.humidity.text = f"Humidity {info[4]}%"
        self.root.ids.city.text = f"{info[2]}"
        anim = Animation(opacity=1)
        anim.start(self.root)




if __name__ == "__main__":
    WeatherApp().run()
