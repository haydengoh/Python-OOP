import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


class GDCGUI_GRID:
    def __init__(self):
        self._win = tk.Tk()
        self._win.resizable(False, False)
        self._win.title("GDC - HAYDEN")
        self._win.geometry("350x260")
        self.create_widgets()

        self._win.mainloop()

    def create_widgets(self):
        dataFrame = ttk.Frame(self._win)
        dataFrame.grid(column=0, row=0, padx=8, pady=4)

        # Swing Speed - .Label
        ss_lbl = ttk.Label(dataFrame, text="Swing Speed:")
        ss_lbl.grid(column=0, row=0, sticky='W')
        # Swing Speed - .Entry
        self._ss = tk.StringVar()  # store input
        self._ss_Ety = ttk.Entry(dataFrame,
                                 width=6,
                                 textvariable=self._ss)
        self._ss_Ety.grid(column=1, row=0)
        # Swing Speed - .Radiobutton
        self._spdValue = tk.IntVar()  # store input
        self._spdValue.set(0)
        self._mph_rdbtn = ttk.Radiobutton(dataFrame,
                                          text='mph',
                                          variable=self._spdValue,
                                          value=0)
        self._kph_rdbtn = ttk.Radiobutton(dataFrame,
                                          text='kph',
                                          variable=self._spdValue,
                                          value=1)
        self._mph_rdbtn.grid(column=3, row=0)
        self._kph_rdbtn.grid(column=4, row=0)
        self._ss_Ety.focus()

        # Club Length - .Label
        cLength_lbl = ttk.Label(dataFrame, text="Club Length:")
        cLength_lbl.grid(column=0, row=1, sticky='W')
        # Club Length - .Entry
        self._cLength = tk.StringVar()  # store input
        self._cLength_Ety = ttk.Entry(dataFrame,
                                      width=6,
                                      textvariable=self._cLength)
        self._cLength_Ety.grid(column=1, row=1)
        # Club Length - .Radiobutton
        self._lengthValue = tk.IntVar()  # store input
        self._lengthValue.set(0)
        self._inch_rdbtn = ttk.Radiobutton(dataFrame,
                                           text='inch',
                                           variable=self._lengthValue,
                                           value=0)
        self._cm_rdbtn = ttk.Radiobutton(dataFrame,
                                         text='cm',
                                         variable=self._lengthValue,
                                         value=1)
        self._inch_rdbtn.grid(column=3, row=1)
        self._cm_rdbtn.grid(column=4, row=1)

        # Club Loft - .Label
        cLoft_lbl = ttk.Label(dataFrame, text="Club Loft(degree):")
        cLoft_lbl.grid(column=0, row=2, sticky='W')
        # Swing Speed - .Entry
        self._cLoft = tk.StringVar()  # store input
        self._cLoft_Ety = ttk.Entry(dataFrame,
                                    width=6,
                                    textvariable=self._cLoft)
        self._cLoft_Ety.grid(column=1, row=2)

        # ================ Button ================
        actionFrame = ttk.Frame(dataFrame)
        actionFrame.grid(column=0, row=3, padx=8, pady=4, columnspan=3)
        # “Calculate” (enabled)
        self._calc_btn = ttk.Button(actionFrame,
                                    text="Calculate",
                                    command=self.calculate)
        self._calc_btn.grid(column=0, row=0, padx=4, pady=4)
        # “Clear” (disabled)
        self._clear_btn = ttk.Button(actionFrame,
                                     text="Clear",
                                     command=self.clear)
        self._clear_btn.grid(column=1, row=0, padx=4, pady=4)
        self._clear_btn.config(state=tk.DISABLED)

        # ================ ScrolledText ================
        outputFrame = ttk.Frame(self._win)
        outputFrame.grid(column=0, row=1, columnspan=2)
        # Scrolled Text (disabled)
        self._scrol_stxt = scrolledtext.ScrolledText(outputFrame,
                                                     width=50,
                                                     height=9,
                                                     wrap=tk.WORD)
        self._scrol_stxt.grid(column=0, row=0, sticky='WE')
        self._scrol_stxt.config(state=tk.DISABLED)

    def calculate(self):
        self._scrol_stxt.config(state=tk.NORMAL)
        try:
            length = float(self._cLength.get())
            loft = float(self._cLoft.get())
            swingSpeed = float(self._ss.get())

            """
            Ensure swing speed is a positive number.
            Ensure length must be within 30 to 48 inches.
            Ensure loft must be within 8 to 64 degrees.
            """
            if (swingSpeed < 0) or (length < 30) or (length > 48) or (loft < 8) or (loft > 64):
                raise Exception

            if self._spdValue.get() == 1:
                swingSpeed = swingSpeed * 0.621371

            if self._lengthValue.get() == 1:
                length = length * 0.393701

            # length (inches), SwingSpeed (mph)
            distance = (280 - abs(length-48)*10 -
                        abs(loft-10)*1.25) * swingSpeed/96
            self._scrol_stxt.insert(
                'end', "Estimated Distance: {} yards\n".format(round(distance)))
        except Exception as e:
            # self._scrol_stxt.insert('end', str(e) + "\n")
            self._scrol_stxt.insert(
                'end', 'Error(s) in input values\nPlease <clear> and try again\n')
        finally:
            # making sure the last line is visiable
            self._scrol_stxt.see('end')
            # diable the scrolled text
            self._scrol_stxt.config(state=tk.DISABLED)
            # enable clear button
            self._clear_btn.config(state=tk.NORMAL)

            # clear the 3 text fields
            self._ss.set("")
            self._cLength.set("")
            self._cLoft.set("")

            # focus
            self._ss_Ety.focus()

    def clear(self):
        # enable ScrolledText
        self._scrol_stxt.config(state=tk.NORMAL)

        # clear the 3 text fields
        self._ss.set("")
        self._cLength.set("")
        self._cLoft.set("")

        # focus
        self._ss_Ety.focus()

        # clear the ScrolledText
        self._scrol_stxt.delete(1.0, tk.END)

        # default selection of the radiobuttons to “mph” and “inch”
        self._spdValue.set(0)
        self._lengthValue.set(0)

        # disable the “Clear” button
        self._clear_btn.config(state=tk.DISABLED)

        # disable ScrolledText
        self._scrol_stxt.config(state=tk.DISABLED)


GDCGUI_GRID()
