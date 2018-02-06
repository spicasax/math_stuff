# See StackOverflow for how to switch pages:
# http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter


import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox

from fractions import Fraction

LARGE_FONT = ("Verdana", 16)


class FractionCompareApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Fraction Compare Quiz")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, CheckPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Enter Fractions To Compare and Select Comparator:", font=LARGE_FONT)
        self.label.grid(row=0, column=0, columnspan=4, sticky=tk.W)

        num1 = tk.Label(self, text="Numerator:", justify=tk.RIGHT)
        num2 = tk.Label(self, text="Denominator:", justify=tk.RIGHT)
        num1.grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)
        num2.grid(row=3, column=0, sticky=tk.E, padx=10, pady=10)

        self.e1 = ttk.Entry(self)
        self.e2 = ttk.Entry(self)
        self.e1.grid(row=1, column=1, padx=10, pady=10)
        self.e2.grid(row=3, column=1, padx=10, pady=10)

        self.button1 = ttk.Button(self, text="<")
        self.button1.config(command=lambda button=self.button1: self.check_answer(button))
        self.button1.grid(row=1, column=2)

        self.button2 = ttk.Button(self, text="=")
        self.button2.config(command=lambda button=self.button2: self.check_answer(button))
        self.button2.grid(row=2, column=2)

        self.button3 = ttk.Button(self, text=">")
        self.button3.config(command=lambda button=self.button3: self.check_answer(button))
        self.button3.grid(row=3, column=2)

        num3 = tk.Label(self, text="Numerator:", justify=tk.RIGHT)
        num4 = tk.Label(self, text="Denominator:", justify=tk.RIGHT)
        num3.grid(row=1, column=3, sticky=tk.E, padx=10, pady=10)
        num4.grid(row=3, column=3, sticky=tk.E, padx=10, pady=10)

        self.e3 = ttk.Entry(self)
        self.e4 = ttk.Entry(self)
        self.e3.grid(row=1, column=4, padx=10, pady=10)
        self.e4.grid(row=3, column=4, padx=10, pady=10)

    def check_answer(self, button):
        self.controller.compare = "Equal"
        if button == self.button1:
            self.controller.compare = "<"
        elif button == self.button2:
            self.controller.compare = "="
        else:
            self.controller.compare = ">"
        self.controller.numerator1 = self.e1.get()
        self.controller.denominator1 = self.e2.get()
        self.controller.numerator2 = self.e3.get()
        self.controller.denominator2 = self.e4.get()

        self.controller.frames[CheckPage].correct_label()
        self.controller.show_frame(CheckPage)


class CheckPage(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller

        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Page One", font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

    def correct_label(self):
        # check we have numbers
        try:
            _num1 = int(self.controller.numerator1)
            _den1 = int(self.controller.denominator1)
            _num2 = int(self.controller.numerator2)
            _den2 = int(self.controller.denominator2)
        except:
            msgbox.showinfo("Error", "Please enter numbers only.")
            answer = "Incorrect"
            self.label.config(text=answer)
            return

        # check we don't divide by zero
        if (_den1 == 0) | (_den2 == 0):
            msgbox.showinfo("Error", "Do not divide by zero.")
            answer = "Incorrect"
            self.label.config(text=answer)
            return

        _compare = self.controller.compare

        if _compare == '>':
            compare = Fraction(_num1,_den1) > Fraction(_num2,_den2)
        elif _compare == '=':
            compare = Fraction(_num1, _den1) == Fraction(_num2, _den2)
        else:
            compare = Fraction(_num1, _den1) < Fraction(_num2, _den2)

        if compare:
            answer = "Correct"
        else:
            answer = "Incorrect"
        self.label.config(text=answer)
        return

if __name__ == "__main__":
    app = FractionCompareApp()
    app.mainloop()