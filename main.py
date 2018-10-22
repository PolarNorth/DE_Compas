from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
)
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class MainApp (App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        return sm

class MainScreen (Screen):
    inp_x0 = ObjectProperty(None)
    inp_y0 = ObjectProperty(None)
    inp_n = ObjectProperty(None)
    inp_xn = ObjectProperty(None)
    submit_btn = ObjectProperty(None)
    graph_box = ObjectProperty(None)
    title_label = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        initial_plot = ([0,1],[0,1])
        plt.plot(*initial_plot)
        self.plot = FigureCanvasKivyAgg(plt.gcf())
        self.graph_box.add_widget(self.plot)

if __name__ == '__main__':
    MainApp().run()

