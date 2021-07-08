import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter import filedialog as fd
import os
import glob
from sys import platform
from math import *
import re

import linear.config.config_win32 as windows
import linear.config.config_darwin as mac
from linear.config.common import *
from linear.settings import *
from linear.Penduluns import Pendulums


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()

        self.system = None
        if platform == SYSTEM_WINDOWS:
            self.system = windows
        elif platform == SYSTEM_MAC or platform == SYSTEM_LINUX:
            self.system = mac
        else:
            self.destroy()

        # basic config of app
        self.title(PROG_TITLE)
        self.resizable(False, False)
        self.geometry("{}x{}".format(self.system.WINDOW_WIDTH, self.system.WINDOW_HEIGHT))

        self.pendulums = None
        self.spinboxes_labels = None

        self.protocol("WM_DELETE_WINDOW", self.closing_window)

        self._create_menu()
        self._create_field_with_parameters()
        self._create_working_area()
        self._create_pendulums()
        self._create_graph()
        self._create_experiments_frame()

    def closing_window(self):
        if mb.askokcancel("Выход", "{:}\n{:}".format("Вы уверены, что хотите выйти?", "Все изменений несохраненные изменения пропадут")):
            self.destroy()

    def _create_menu(self):
        self.main_menu = tk.Menu(self)

        self.file_menu = tk.Menu(self.main_menu, tearoff=False)
        self.report_menu = tk.Menu(self.main_menu, tearoff=False)
        self.about_program_menu = tk.Menu(self.main_menu, tearoff=False)

        self.config(menu=self.main_menu)

        # file menu
        self.file_menu.add_command(label='Создать группу экспериментов', command=self.open_window_create_file)
        self.file_menu.add_command(label='Открыть группу экспериментов', command=self.open_file)
        self.file_menu.add_command(label='Сохранить', command=self.save_file)
        self.file_menu.add_command(label='Сохранить как', command=self.save_file_as)
        self.file_menu.add_command(label='Выход', command=exit)
        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)

        # report menu
        self.report_menu.add_command(label='Отчет')
        self.main_menu.add_cascade(label='Отчет', menu=self.report_menu)

        # about menu
        self.about_program_menu.add_command(label='Справка', command=self.show_help)
        self.about_program_menu.add_command(label='Авторы', command=self.show_authors)
        self.main_menu.add_cascade(label='О программе', menu=self.about_program_menu)

    def _create_working_area(self):
        # base frame and canvas
        self.working_area = tk.Frame(self, width=self.system.WORKING_AREA_SIZE, height=self.system.WORKING_AREA_SIZE)
        self.working_area.grid(row=0, column=0, columnspan=2, rowspan=2)
        self.working_area.propagate(False)

        self.canvas = tk.Canvas(self.working_area,
                                width=self.system.CANVAS_SIZE, height=self.system.CANVAS_SIZE, bg="gray")
        self.canvas.place(anchor='ne', relx=0.98, rely=0.02)

        # ruler bottom !!! что значат 0, 2? !!!!
        self.ruler_bottom_canvas = tk.Canvas(self.working_area,
                                             width=self.system.RULER_WIDTH, height=self.system.RULER_HEIGHT)
        self.photo_ruler_bottom = tk.PhotoImage(file=self.system.RULER_BOTTOM_FILE)
        self.ruler_bottom_canvas.create_image(0, 3, anchor="nw",
                                              image=self.photo_ruler_bottom)
        self.ruler_bottom_canvas.place(anchor='se', relx=0.98, rely=1)

        # ruler left
        self.ruler_left_canvas = tk.Canvas(self.working_area,
                                           width=self.system.RULER_HEIGHT, height=self.system.RULER_WIDTH)
        self.photo_ruler_left = tk.PhotoImage(file=self.system.RULER_LEFT_FILE)
        self.ruler_left_canvas.create_image(2, 3, anchor="nw",
                                            image=self.photo_ruler_left)
        self.ruler_left_canvas.place(relx=0.007, rely=0.02)

    def _create_pendulums(self):
        self.pendulums = Pendulums(self.canvas, pendulums_default_params)

    def _create_graph(self):
        self.graph_frame = tk.LabelFrame(self, text="График", width=self.system.GRAPH_FRAME_WIDTH,
                                         height=self.system.CANVAS_SIZE + 50)
        self.graph_frame.grid(row=0, column=2, rowspan=2)
        self.graph_frame.grid_propagate(False)

        graph = tk.Canvas(self.graph_frame, width=self.system.GRAPH_FRAME_WIDTH - 10,
                          height=self.system.GRAPH_FRAME_HEIGHT - 7, bg='white')
        graph.grid(column=1, row=1)

        self.draw_axis(graph)
        self.draw_graph(graph)
        self.graph_config(graph)

        self.ruler_graph_canvas = tk.Canvas(self.graph_frame,
                                            width=self.system.GRAPH_FRAME_WIDTH, height=30)

        self.photo_ruler_graph = tk.PhotoImage(file=self.system.RULER_GRAPH_FILE)
        self.ruler_graph_canvas.create_image(12, 4, anchor="nw",
                                             image=self.photo_ruler_graph)
        self.ruler_graph_canvas.place(anchor='se', relx=0.985, rely=0.9999)

    def draw_axis(self, graph):
        # Ось x
        graph.create_line(-self.system.GRAPH_FRAME_WIDTH // 2, 0,
                          self.system.GRAPH_FRAME_WIDTH // 2, 0, width=1, arrow=tk.LAST, fill='grey')
        # Ось y
        graph.create_line(0, (self.system.GRAPH_FRAME_HEIGHT - 7) // 2,
                          0, -((self.system.GRAPH_FRAME_HEIGHT - 7) // 2), width=1, arrow=tk.LAST, fill='grey')

        for i in range(-(self.system.GRAPH_FRAME_WIDTH - 50), self.system.GRAPH_FRAME_WIDTH - 49, 50):
            # 0.0
            if i == 0:
                size = 2
                graph.create_oval(i - size, i - size, i + size, i + size, fill='grey', outline='grey')
                graph.create_text(i + 12, -10, text=str(i / 50), fill="purple", font=("Helvetica", "7"))
                continue
            # Ось x
            graph.create_line(i, -3, i, 3, width=0.5, fill='grey')
            graph.create_text(i + 3, -10, text=str(i / 50), fill="purple", font=("Helvetica", "7"))

            # Ось y
            graph.create_line(-3, i, 3, i, width=0.5, fill='grey')
            graph.create_text(12, i, text=str(-i / 50), fill="purple", font=("Helvetica", "7"))

        graph.create_text(14, -(self.system.GRAPH_FRAME_HEIGHT // 2) + 14, text='X(t)', fill="purple",
                          font=("Helvetica", "10"))
        graph.create_text(self.system.GRAPH_FRAME_WIDTH // 2 - 5, 10, text='t', fill="purple", font=("Helvetica", "10"))

    def draw_graph(self, graph):
        params = self.get_params_from_spinboxes()
        points = []
        time = -2.5
        while time <= 2.5:
            x = time
            y = float(params['amplitude']) * cos(self.pendulums.start_nu * x)
            points.append((x * 50, -y))
            time += 0.1
        graph.create_line(points, fill='blue')

    def graph_config(self, graph):
        graph.configure(scrollregion=(-(self.system.GRAPH_FRAME_WIDTH // 2), -(self.system.GRAPH_FRAME_HEIGHT // 2),
                                        self.system.GRAPH_FRAME_WIDTH // 2, self.system.GRAPH_FRAME_HEIGHT // 2))

    def _create_field_with_parameters(self):
        # base frame
        self.field_with_parameters = tk.LabelFrame(self, text="Параметры",
                                                   width=self.system.FIELD_WITH_PARAMETERS_WIDTH,
                                                   height=self.system.FIELD_WITH_PARAMETERS_HEIGHT)
        self.field_with_parameters.grid(row=1, column=3)
        self.field_with_parameters.grid_propagate(False)

        # buttons
        self.start_button = tk.Button(self.field_with_parameters, text='Старт', command=self.start_button_pressed)
        self.start_button.grid(row=len(spinboxes_to_create) + 1, column=0,
                               pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        self.stop_button = tk.Button(self.field_with_parameters, text='Стоп', command=self.stop_button_pressed)
        self.stop_button.grid(row=len(spinboxes_to_create) + 1, column=1,
                              pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        # create ComboboxList
        self.list_delta_label = tk.Label(self.field_with_parameters, text="Разность через:", anchor='w',
                             width=self.system.FIELD_WITH_PARAMETERS_LABEL_WIDTH)
        self.list_delta_label.grid(row=0, column=0, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        self.list_delta_text_var = tk.StringVar()
        self.list_delta_text_var.trace('w', callback=self.list_delta_changed)

        self.list_delta = ttk.Combobox(self.field_with_parameters, values=["частоту", "длину"], state='readonly',
                                       text="частоту", width=self.system.FIELD_WITH_PARAMETERS_SPINBOX_WIDTH,
                                       textvar=self.list_delta_text_var)
        self.list_delta.current(0)

        self.list_delta.grid(row=0, column=1, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

        # create Spinboxes
        self.spinboxes = dict()
        self.spinboxes_labels = dict()
        for index, item in enumerate(spinboxes_to_create):
            default_value = tk.DoubleVar()
            default_value.set(item['default_value'])

            label = tk.Label(self.field_with_parameters, text=item['label'], anchor='w',
                             width=self.system.FIELD_WITH_PARAMETERS_LABEL_WIDTH)
            label.grid(row=index + 1, column=0, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)

            spinbox = tk.Spinbox(self.field_with_parameters, from_=item['min_value'], to=item['max_value'],
                                 increment=item['step'], textvariable=default_value,
                                 width=self.system.FIELD_WITH_PARAMETERS_SPINBOX_WIDTH)
            spinbox.grid(row=index + 1, column=1, pady=self.system.FIELD_WITH_PARAMETERS_BUTTON_PADY)
            self.spinboxes.update({item['name']: spinbox})
            self.spinboxes_labels.update({item['name']: label})



    def _check_params_in_spinboxes(self):
        params_are_correct = None
        try:
            for spinbox_original in spinboxes_to_create:
                value = float(self.spinboxes[spinbox_original['name']].get())
                if value < spinbox_original['min_value'] or value > spinbox_original['max_value']:
                    raise ValueError

                params_are_correct = True

        except ValueError:
            self.show_error()
            params_are_correct = False

        finally:
            return params_are_correct

    def show_error(self):
        mb.showwarning("Warning", "Проверьте параметры ввода")

    def get_params_from_spinboxes(self):
        params = dict()

        for name, spinbox in self.spinboxes.items():
            params.update({name: spinbox.get()})

        if self.list_delta.get() == 'частоту':
            params.update({"delta_type_nu": 1})
        else:
            params.update({"delta_type_nu": 0})

        params['amplitude'] = float(params['amplitude']) * 50

        return params

    def set_params_to_spinboxes(self, params):
        for name, value in params.items():
            if name == 'delta_type_nu':  # слегка костыль
                continue
            self.spinboxes[name].delete(0, len(self.spinboxes[name].get()))
            self.spinboxes[name].insert(0, value)

        self.pendulums.time = float(self.spinboxes['time'].get())

        self.list_delta.current(1)
        if params['delta_type_nu']:
            self.list_delta.current(0)

        # ДЛЯ ЖЕНИ! ВАЖНО! Теперь эта функция не устанавливает параметры маятников !!!

    def start_button_pressed(self):
        params_are_correct = self._check_params_in_spinboxes()

        if params_are_correct:
            params = self.get_params_from_spinboxes()
            self.pendulums.set_params(params)
            self._create_graph()

        else:
            self.stop_button_pressed()

    def stop_button_pressed(self):
        self.pendulums.stop_loop()

        # update time in spinbox
        self.spinboxes['time'].delete(0, len(self.spinboxes['time'].get()))
        self.spinboxes['time'].insert(0, round(self.pendulums.time, 3))

    def list_delta_changed(self, index, value, op):
        if self.spinboxes_labels is None:
            return

        if self.list_delta.get() == "частоту":
            self.pendulums.delta_type_nu = 1
            self.spinboxes_labels['delta_nu'].config(text="Разность частот")
        else:
            self.pendulums.delta_type_nu = 0
            self.spinboxes_labels['delta_nu'].config(text="Разность длин")


    # EVERYTHING BELOW BELONGS TO EVGENIY KONIAEV
    # it has NOT been modified (almost) during the last BIG update
    # that's why some bugs may be discovered

    def _create_experiments_frame(self):
        self.history = tk.LabelFrame(self, text='Эксперименты', width=250, height=250)
        self.history.grid(row=0, column=3)

        self.history_window_field = tk.Frame(self.history)

        self.history_window_field_title = tk.Label(self.history_window_field, text='Имя эксперимента', bg='#00bdff',
                                                   fg="#ffffff")
        self.history_window_field_enum = tk.Frame(self.history_window_field, bg='#ffffff')

        self.history_canvas = tk.Canvas(self.history_window_field_enum, bg="#ffffff")
        self.history_canvas_scroll_y = tk.Scrollbar(self.history_window_field_enum, orient=tk.VERTICAL,
                                                    command=self.history_canvas.yview)
        self.history_canvas_enum = tk.Frame(self.history_canvas, bg="#ffffff")

        self.history_canvas_enum.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(
                scrollregion=self.history_canvas.bbox("all")
            )
        )

        self.history_canvas.create_window((0, 0), window=self.history_canvas_enum, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_canvas_scroll_y.set)

        # Эксперименты - кнопки
        self.history_buttons_field = tk.Frame(self.history_window_field)

        self.button_new_experiment = tk.Button(self.history_buttons_field, text="Создать новый \nэксперимент",
                                               font=("Tahoma", 8), command=self.open_window_create_file)
        self.button_delete_current_experiment = tk.Button(self.history_buttons_field,
                                                          text="Удалить текущий \nэксперимент",
                                                          font=("Tahoma", 8), command=self.delete_current_file_event)

        # Выгружаем список экспериментов в окно
        if not os.path.exists("./experiments"):
            os.mkdir('./experiments')

        self.amount_rows_in_experiments = 0
        self.list_of_enums = []
        for file in glob.glob("./experiments/*.txt"):
            self.add_experiment_to_list(file[14:len(file) - 4])

        # переключение на стартовый эксперимент
        if len(self.list_of_enums) == 0:
            self.create_new_experiment_file('Новый эксперимент')

        self.current_experiment_name = self.list_of_enums[0].winfo_children()[0].cget("text")
        self.switch_to_experiment(self.current_experiment_name)

        # эксперименты - расположение в окне
        self.history.grid(row=0, column=3, columnspan=1)
        self.history.grid_propagate(False)
        self.history.columnconfigure(0, weight=1)
        self.history.rowconfigure(0, weight=1)

        self.history_window_field.grid(row=0, column=0, columnspan=1, sticky="nsew")
        self.history_window_field.columnconfigure(0, weight=1)
        self.history_window_field.rowconfigure(1, weight=1)

        self.history_window_field_title.grid(row=0, column=0, sticky="ew")
        self.history_window_field_enum.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.history_window_field_enum.rowconfigure(0, weight=1)
        self.history_window_field_enum.columnconfigure(0, weight=1)

        self.history_canvas.grid(row=0, column=0, columnspan=1, sticky="nsew")
        self.history_canvas.columnconfigure(0, weight=1)
        self.history_canvas_scroll_y.grid(row=0, column=1, sticky="ns")

        self.history_buttons_field.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.history_buttons_field.columnconfigure(0, weight=1)
        self.history_buttons_field.columnconfigure(1, weight=1)

        self.button_new_experiment.grid(column=0, sticky="w", padx=10)
        self.button_delete_current_experiment.grid(column=1, row=0, sticky="e", padx=10)

    def open_window_create_file(self):  # рабоатет заебись
        global newWindow
        global entry_name_file
        newWindow = tk.Toplevel(self)
        newWindow.title('Имя нового эксперимента')
        newWindow.resizable(False, False)
        newWindow.lift()
        newWindow.attributes("-topmost", True)
        newWindow.after(1, lambda: newWindow.focus_force())

        input_area = tk.Frame(newWindow)
        label_name_file = tk.Label(input_area, text='Имя эксперимента:', font=("Tahoma", 12))
        entry_name_file = tk.Entry(input_area, width=20, font=("Tahoma", 12))

        buttons_area = tk.Frame(newWindow)
        button_create = tk.Button(buttons_area, text="Создать",
                                  font=("Tahoma", 10), command=self.create_new_file_event)
        button_cancel = tk.Button(buttons_area, text="Закрыть",
                                  font=("Tahoma", 10), command=lambda: newWindow.destroy())

        input_area.pack(side="top", fill="both", ipadx=5, ipady=7)

        label_name_file.pack(side="left")
        entry_name_file.pack(side="left")

        buttons_area.pack(side="top", fill="both")

        button_create.pack(side="left", padx=40, pady=5, ipady=2, ipadx=4)
        button_cancel.pack(side="right", padx=40, pady=5, ipady=2, ipadx=4)

    def delete_current_file_event(self):  # работает заебись
        self.delete_file(self.current_experiment_name)
        self.remove_experiment_from_list(self.current_experiment_name)

        if len(self.list_of_enums) == 0:
            self.create_new_experiment_file('Новый эксперимент')

        self.current_experiment_name = self.list_of_enums[0].winfo_children()[0].cget("text")
        self.switch_to_experiment(self.current_experiment_name)

    def add_experiment_to_list(self, name_experiment):  # работает заебись
        self.list_of_enums.append(tk.Frame(self.history_canvas_enum, bg="#fff"))
        new_label = tk.Label(self.list_of_enums[self.amount_rows_in_experiments],
                             text=name_experiment, bg="#ffffff")
        self.list_of_enums[self.amount_rows_in_experiments].grid(row=self.amount_rows_in_experiments, column=0,
                                                                 columnspan=1, sticky="we")
        new_label.bind("<Button-1>", self.click_on_experiment)
        new_label.bind("<Enter>", self.hovered_event)
        new_label.bind("<Leave>", self.unhovered_event)
        new_label.grid(row=0, column=0)
        self.amount_rows_in_experiments += 1

    def click_on_experiment(self, event):  # работает заебись
        name_file_to_switch = event.widget.cget("text")

        self.spinboxes['time'].delete(0, len(self.spinboxes['time'].get()))
        self.spinboxes['time'].insert(0, round(self.pendulums.time, 2))

        par_of_cur_experiment = self.get_params_from_spinboxes()
        self.write_params_to_file(par_of_cur_experiment, self.current_experiment_name, './experiments/')

        self.current_experiment_name = name_file_to_switch
        self.switch_to_experiment(self.current_experiment_name)

    def unhovered_event(self, event):  # работает заебись
        event.widget.configure(fg="#000000")

    def hovered_event(self, event):  # работает заебись
        event.widget.configure(fg="#00bdff")

    def switch_to_experiment(self, name_file):  # работает заебись
        self.history_window_field_title.configure(text=('"' + name_file + '"'))

        # START: ADD by Yaroslav
        params_from_last_file = self.read_params_from_file(name_file)
        self.set_params_to_spinboxes(params_from_last_file)
        params_from_last_file['amplitude'] *= 50
        self.pendulums.set_params(params_from_last_file)
        self._create_graph()
        # STOP: ADD by Yaroslav

        self.pendulums.stop_loop()

    def read_params_from_file(self, name_file):  # работает заебись
        cur_file = open("./experiments/" + name_file + ".txt", "r")

        cur_value_params = cur_file.readline().split()

        par_of_getting_experiment = {
            'amplitude': 0,
            'number_of_pendulums': 0,
            'size': 0,
            'delta_nu': 0,
            'length': 0,
            'time': 0,
            'delta_type_nu': 1
        }

        for i in range(0, len(cur_value_params), 2):
            if cur_value_params[i] == 'delta_nu' or cur_value_params[i] == 'time' or cur_value_params[i] == 'amplitude':
                par_of_getting_experiment[cur_value_params[i]] = float(cur_value_params[i + 1])
            else:
                par_of_getting_experiment[cur_value_params[i]] = int(cur_value_params[i + 1])

        cur_file.close()

        return par_of_getting_experiment

    def write_params_to_file(self, params, name_file, path):  # работает заебись
        cur_file = open(path + name_file + ".txt", "w")

        for value in params:
            cur_value = params[value]
            if value == 'amplitude':
                cur_value /= 50
            cur_file.write(value + " " + str(cur_value) + " ")

        cur_file.close()

    def delete_file(self, name_file):
        if os.path.exists("./experiments/" + name_file + ".txt"):
            os.remove("./experiments/" + name_file + ".txt")

    def remove_experiment_from_list(self, name_experiment):  # работает заебись
        for i in range(len(self.list_of_enums)):
            if self.list_of_enums[i].winfo_children()[0].cget("text") == name_experiment:
                for j in range(i + 1, len(self.list_of_enums)):
                    self.list_of_enums[j].grid(row=j - 1, column=0)
                self.list_of_enums[i].destroy()
                del self.list_of_enums[i]
                self.amount_rows_in_experiments -= 1
                break

    def create_new_experiment_file(self, file_name):  # работает заебись

        default_params = {
            'amplitude': spinboxes_to_create[0]['default_value'] * 50,
            'number_of_pendulums': 5,
            'size': 10,
            'delta_nu': 0.1,
            'length': 4,
            'time': 0,
            'delta_type_nu': 1
        }

        self.write_params_to_file(default_params, file_name, './experiments/')
        self.add_experiment_to_list(file_name)

    def create_new_file_event(self):  # работает заебись
        self.spinboxes['time'].delete(0, len(self.spinboxes['time'].get()))
        self.spinboxes['time'].insert(0, round(self.pendulums.time, 2))

        par_of_cur_experiment = self.get_params_from_spinboxes()
        self.write_params_to_file(par_of_cur_experiment, self.current_experiment_name, './experiments/')

        self.current_experiment_name = entry_name_file.get()

        self.create_new_experiment_file(self.current_experiment_name)
        self.switch_to_experiment(self.current_experiment_name)

        newWindow.destroy()

    def open_file(self):
        path = fd.askopenfile()

        if path is None:
            return


        path_str = path.name

        tmp = path_str.split('/')
        name = tmp[len(tmp) - 1].split('.')[0]

        par_of_cur_experiment = self.get_params_from_spinboxes()
        self.write_params_to_file(par_of_cur_experiment, self.current_experiment_name, './experiments/')

        self.current_experiment_name = name

        if tmp[len(tmp) - 2] != 'experiments':
            self.write_params_to_file(par_of_cur_experiment, self.current_experiment_name, './experiments/')

        if tmp[len(tmp) - 2] != 'experiments':
            self.add_experiment_to_list(name)

        self.switch_to_experiment(name)

    def save_file_as(self):
        path = fd.asksaveasfilename(
            filetypes=(("TXT files", "*.txt"),
                       ("HTML files", "*.html;*.htm"),
                       ("All files", "*.*"))
        )

        if path == "":
            print("file empty")
            return

        print(path)
        tmp = path.split('/')
        name = tmp[len(tmp) - 1].split('.')[0]
        print(name)

        words = path.split('/')
        path_str = ""

        for i in range(0, len(words) - 1):
            path_str += words[i] + "/"

        print(path_str)

        params_of_cur_experiment = self.get_params_from_spinboxes()
        self.write_params_to_file(params_of_cur_experiment, self.current_experiment_name, './experiments/')

        have_that_file = False
        list_of_files = os.listdir("./experiments/")

        for somefile in list_of_files:
            f = somefile.split('.')[len(somefile.split('.')) - 2]
            if name == f:
                have_that_file = True

        if have_that_file:
            return

        self.current_experiment_name = name

        self.write_params_to_file(params_of_cur_experiment, name, path_str)

        if words[len(words) - 2] != 'experiments':
            self.write_params_to_file(params_of_cur_experiment, name, './experiments/')

        self.add_experiment_to_list(name)
        self.switch_to_experiment(name)

    def save_file(self):
        params_of_cur_experiment = self.get_params_from_spinboxes()
        self.write_params_to_file(params_of_cur_experiment, self.current_experiment_name, './experiments/')

    def show_authors(self):
        mb.showinfo('Авторы', 'Байрамгалин Ярослав\n'
                              'Коняев Евгений\n'
                              'Минаев Дмитрий\n'
                              'Пирязев Андрей\n'
                              'Винокуршин Валерий\n'
                              'Дыхал Полина\n\n'
                              'МГТУ им. Н.Э. Баумана\n'
                              'Группа ИУ7-23Б'
                    )

    def show_help(self):
        info = ''
        for spinbox in spinboxes_to_create:
            info += ' '.join((f"{spinbox['label']}\n", f"Минимальное значение: {str(spinbox['min_value'])}\n",
                              f"Максимальное значение: {str(spinbox['max_value'])}\n"))
            info += '\n'
        print(info)
        mb.showinfo('Справка', info)
