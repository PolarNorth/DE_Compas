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
from backend import *

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
    title_label = ObjectProperty(None)
    plot_box_widget = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self.current_de = equations[0]
        self.plot_box_widget.set_plot(ImprovedEulerMethod.solve(self.current_de, 2, 0, 1, 0.1))
        self.submit_btn.on_release = self.plot_box_widget.show_plot

class PlotBox (BoxLayout):
    equation_lbl = ObjectProperty(None)
    show_diff_equation_btn = ObjectProperty(None)
    show_numerical_solution_btn = ObjectProperty(None)
    show_exact_solution_btn = ObjectProperty(None)
    show_truncation_error_btn= ObjectProperty(None)
    figure_box = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(BoxLayout, self).__init__(*args, **kwargs)
        self.plot = None
        self.plot_coordinates = None
        # initial_plot = ([0,1],[0,1])
        # plt.plot(*initial_plot)
        # self.plot = FigureCanvasKivyAgg(plt.gcf())
        # self.figure_box.add_widget(self.plot)
    
    def set_plot(self, solution):
        self.plot_coordinates = (solution.x_solution, solution.y_solution)

    def show_plot(self):
        # initial_plot = ([0,1],[0,1])
        plt.plot(*self.plot_coordinates)
        self.plot = FigureCanvasKivyAgg(plt.gcf())
        self.figure_box.clear_widgets()
        self.figure_box.add_widget(self.plot)


if __name__ == '__main__':
    MainApp().run()

