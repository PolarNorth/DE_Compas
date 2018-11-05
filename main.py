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

class SettingsTextInput (TextInput):
    pass

class SettingsLabel (Label):
    pass

class MainScreen (Screen):
    inp_x0 = ObjectProperty(None)
    inp_y0 = ObjectProperty(None)
    # inp_h = ObjectProperty(None)
    inp_n1 = ObjectProperty(None)
    inp_n2 = ObjectProperty(None)
    inp_k = ObjectProperty(None)
    inp_xn = ObjectProperty(None)
    inp_n = ObjectProperty(None)
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
            'N' : 100,
            'N1' : 100,
            'N2' : 1000,
            'k' : 10,
        }
        self.inp_x0.text = str(default_values['x0'])
        self.inp_y0.text = str(default_values['y0'])
        self.inp_xn.text = str(default_values['xn'])
        self.inp_n.text = str(default_values['N'])
        self.inp_n1.text = str(default_values['N1'])
        self.inp_n2.text = str(default_values['N2'])
        self.inp_k.text = str(default_values['k'])
        
        self.submit_btn.on_release = self.submit
    
    def submit(self):
        self.plot_box_widget.equation_lbl.text = "Calculating..."
        step = (float(self.inp_xn.text) - float(self.inp_x0.text))/float(self.inp_n.text)
        ivp = (self.current_de, float(self.inp_x0.text), float(self.inp_y0.text), step, float(self.inp_xn.text))
        div_range = (int(self.inp_n1.text), int(self.inp_n2.text), int(self.inp_k.text))
        self.plot_box_widget.set_plots(ivp, div_range, self.euler_btn.active, self.ieuler_btn.active, self.runge_btn.active)
        # self.plot_box_widget.show_plots()
        self.plot_box_widget.show_numerical_solution_plot()


class PlotBox (BoxLayout):
    equation_lbl = ObjectProperty(None)
    # show_diff_equation_btn = ObjectProperty(None)
    show_numerical_solution_btn = ObjectProperty(None)
    show_total_error_btn = ObjectProperty(None)
    show_truncation_error_btn= ObjectProperty(None)
    figure_box = ObjectProperty(None)

    numerical_solution_plot = None
    total_truncation_error_plot = None
    local_truncation_error_plot = None


    def set_plots(self, ivp, div_range, euler, ieuler, runge):  # TODO : Don't forget new argument div_range

        solutions = []

        if euler:
            solutions.append(numerical_methods['Euler'].solve(*ivp))
        if ieuler:
            solutions.append(numerical_methods['Improved Euler'].solve(*ivp))
        if runge:
            solutions.append(numerical_methods['Runge-Kutta'].solve(*ivp))

        # Numerical solution
        self.numerical_solution_plot = Figure()
        axis = self.numerical_solution_plot.add_subplot(111)
        axis.plot(solutions[0].x_exact, solutions[0].y_exact, label='Exact')
        for solution in solutions:
            axis.plot(solution.x_solution, solution.y_solution, label=solution.str_method_name)
            axis.legend()

        # Truncation error of the solution
        self.local_truncation_error_plot = Figure()
        axis = self.local_truncation_error_plot.add_subplot(111)
        for solution in solutions:
            axis.plot(solution.x_error, solution.y_error, label=solution.str_method_name)
            axis.legend()

        # Total truncation error
        # Calculate max errors for methods with different number of iterations
        self.total_truncation_error_plot = Figure()
        axis = self.total_truncation_error_plot.add_subplot(111)
        er_x = []
        er_y = {name : [] for name in numerical_methods.keys()}
        iter_step = (div_range[1] - div_range[0]) / div_range[2] 
        curr_n_iterations = div_range[0]
        # for n_iterations in range(0, div_range[2]):    # TODO
        while curr_n_iterations < div_range[1]:
            current_ivp = list(ivp)
            step = (ivp[4] - ivp[1]) / curr_n_iterations
            # print ("Step = " + str(step))
            current_ivp[-2] = step
            er_x.append(step)
            if euler:
                # solutions.append(numerical_methods['Euler'].solve(*current_ivp))

                er_y['Euler'].append(max(numerical_methods['Euler'].solve(*current_ivp).y_error))
            if ieuler:
                # solutions.append(numerical_methods['Improved Euler'].solve(*current_ivp))
                er_y['Improved Euler'].append(max(numerical_methods['Improved Euler'].solve(*current_ivp).y_error))
            if runge:
                # solutions.append(numerical_methods['Runge-Kutta'].solve(*current_ivp))
                er_y['Runge-Kutta'].append(max(numerical_methods['Runge-Kutta'].solve(*current_ivp).y_error))
            curr_n_iterations += iter_step
        
        for name, y in er_y.items():
            if not y:
                continue
            axis.plot(er_x, y, label=name)
            axis.legend()

        # Label on top
        if len(solutions) > 0:
            self.equation_lbl.text = solutions[0].str_name
        else:
            self.equation_lbl.text = "Choose at least 1 method"
    
    def show_truncation_error_plot (self):
        self.select_plot(self.local_truncation_error_plot)

    def show_total_error_plot (self):
        self.select_plot(self.total_truncation_error_plot)

    def show_numerical_solution_plot (self):
        self.select_plot(self.numerical_solution_plot)
    
    def select_plot(self, plot):
        if plot is None:
            return
        self.figure_box.clear_widgets()
        canvas = FigureCanvasKivyAgg(plot)
        self.figure_box.add_widget(canvas)
        self.figure_box.add_widget(NavigationToolbar2Kivy(canvas).actionbar)


if __name__ == '__main__':
    # matplotlib.interactive(True)
    # matplotlib.pyplot.ion()from kivy.config import Config
    MainApp().run()

