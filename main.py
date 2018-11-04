from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
)
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.garden.matplotlib.backend_kivyagg import NavigationToolbar2Kivy
from backend import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class MainApp (App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        return sm

class MainScreen (Screen):
    inp_x0 = ObjectProperty(None)
    inp_y0 = ObjectProperty(None)
    inp_h = ObjectProperty(None)
    inp_xn = ObjectProperty(None)
    submit_btn = ObjectProperty(None)
    title_label = ObjectProperty(None)
    plot_box_widget = ObjectProperty(None)

    euler_btn = ObjectProperty(None)
    ieuler_btn = ObjectProperty(None)
    runge_btn = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Screen, self).__init__(*args, **kwargs)
        self.current_de = equations[0]
        # self.plot_box_widget.set_plots(ImprovedEulerMethod.solve(self.current_de, 2, 0, 1, 0.1))
        default_values = {
            'x0' : 1,
            'y0' : 3,
            'xn' : 18.2,
            'h' : 0.1,
        }
        # self.inp_x0.text = '0'
        # self.inp_y0.text = '2'
        # self.inp_xn.text = '1'
        # self.inp_h.text =  '0.1'
        self.inp_x0.text = str(default_values['x0'])
        self.inp_y0.text = str(default_values['y0'])
        self.inp_xn.text = str(default_values['xn'])
        self.inp_h.text = str(default_values['h'])
        self.submit_btn.on_release = self.submit
    
    def submit(self):
        self.plot_box_widget.equation_lbl.text = "Calculating..."
        ivp = (self.current_de, float(self.inp_x0.text), float(self.inp_y0.text), float(self.inp_h.text), float(self.inp_xn.text))
        self.plot_box_widget.set_plots(ivp, self.euler_btn.active, self.ieuler_btn.active, self.runge_btn.active)
        # self.plot_box_widget.show_plots()
        self.plot_box_widget.show_numerical_solution_plot()


class PlotBox (BoxLayout):
    equation_lbl = ObjectProperty(None)
    # show_diff_equation_btn = ObjectProperty(None)
    show_numerical_solution_btn = ObjectProperty(None)
    show_exact_solution_btn = ObjectProperty(None)
    show_truncation_error_btn= ObjectProperty(None)
    figure_box = ObjectProperty(None)

    numerical_solution_plot = None
    exact_solution_plot = None
    truncation_error_plot = None


    # def __init__(self, *args, **kwargs):
    #     super(BoxLayout, self).__init__(*args, **kwargs)
    #     # Plots
    #     self.numerical_solution_plot = None
    #     self.exact_solution_plot = None
    #     self.truncation_error_plot = None
    #     # Solution
    #     # self.solution = None
    
    def set_plots(self, ivp, euler, ieuler, runge):
        # self.plot_coordinates = (solution.x_solution, solution.y_solution)
    #     self.solution = solution

    # def show_plots(self):
    #     # initial_plot = ([0,1],[0,1])
    #     # Plot

        solutions = []

        if euler:
            solutions.append(numerical_methods['Euler'].solve(*ivp))
        if ieuler:
            solutions.append(numerical_methods['Improved Euler'].solve(*ivp))
        if runge:
            solutions.append(numerical_methods['Runge-Kutta'].solve(*ivp))

        self.numerical_solution_plot = Figure()
        # print(matplotlib.is_interactive())
        # FigureCanvasAgg(self.numerical_solution_plot)
        axis = self.numerical_solution_plot.add_subplot(111)
        for solution in solutions:
            axis.plot(solution.x_solution, solution.y_solution, label=solution.str_method_name)
            axis.legend()
            # print(solution.str_method_name)


        self.exact_solution_plot = Figure()
        # FigureCanvasAgg(self.exact_solution_plot)
        axis = self.exact_solution_plot.add_subplot(111)
        for solution in solutions:
            axis.plot(solution.x_exact, solution.y_exact, label=solution.str_method_name)
            axis.legend()
            # print(solution.str_method_name)


        self.truncation_error_plot = Figure()
        # FigureCanvasAgg(self.truncation_error_plot)
        axis = self.truncation_error_plot.add_subplot(111)
        for solution in solutions:
            axis.plot(solution.x_error, solution.y_error, label=solution.str_method_name)
            axis.legend()
            # print(solution.str_method_name)

        # Label on top
        if len(solutions) > 0:
            self.equation_lbl.text = solutions[0].str_name
        else:
            self.equation_lbl.text = "Choose at least 1 method"
    
    def show_truncation_error_plot (self):
        # self.figure_box.clear_widgets()
        # # self.figure_box.add_widget(self.numerical_solution_plot)
        # self.figure_box.add_widget(FigureCanvasKivyAgg(self.truncation_error_plot))
        self.select_plot(self.truncation_error_plot)

    def show_exact_solution_plot (self):
        # self.figure_box.clear_widgets()
        # # self.figure_box.add_widget(self.exact_solution_plot)
        # self.figure_box.add_widget(FigureCanvasKivyAgg(self.exact_solution_plot))
        self.select_plot(self.exact_solution_plot)

    def show_numerical_solution_plot (self):
        # self.figure_box.clear_widgets()
        # # self.figure_box.add_widget(self.numerical_solution_plot)
        # self.figure_box.add_widget(FigureCanvasKivyAgg(self.numerical_solution_plot))
        self.select_plot(self.numerical_solution_plot)
    
    def select_plot(self, plot):
        self.figure_box.clear_widgets()
        canvas = FigureCanvasKivyAgg(plot)
        self.figure_box.add_widget(canvas)
        self.figure_box.add_widget(NavigationToolbar2Kivy(canvas).actionbar)



if __name__ == '__main__':
    # matplotlib.interactive(True)
    # matplotlib.pyplot.ion()from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    MainApp().run()

