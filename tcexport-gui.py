#
# tcexport-gui.py --
#   Convert TinyCards decks from a Duolingo "Drive-Thru portal" export file
#   into a flat CSV file suitable for import into Anki or another flashcard app
#
# author: Michael Portuesi
# date: 2020-06-30
#
from exporter import Exporter
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *

import os

import pathlib
from pathlib import Path

class TCExportApp(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.input_file_name = StringVar()
        self.input_file_name.set('')
        self.output_file_name = StringVar()
        self.output_file_name.set('')

        self.master=master
        self.pack(fill=BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.master.title("TinyCards Exporter")

        frame1= Frame(self)
        frame1.pack(fill=tk.X)
        # input file prompt
        self.input_label= tk.Label(frame1, text='Input file:', font=('helvetica', 12, 'bold'))
        self.input_label.pack(side=tk.LEFT, padx=10, pady=10)

        # button to summon file chooser for input file
        self.input_button= tk.Button(frame1, text='Choose...',command=self.choose_input_file)
        self.input_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # input file text field
        self.input_field= tk.Entry(self, textvariable=self.input_file_name)
        self.input_field.pack(fill=tk.X, padx=10)

        frame2 = Frame(self)
        frame2.pack(fill=tk.X)
        # output file prompt
        self.output_label= tk.Label(frame2, text='Output file:', font=('helvetica', 12, 'bold'))
        self.output_label.pack(side=tk.LEFT, padx=10, pady=10)

        # button to summon file chooser for output file
        self.output_button= tk.Button(frame2, text='Choose...',command=self.choose_output_file)
        self.output_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # output file text field
        self.output_field= tk.Entry(self, textvariable=self.output_file_name)
        self.output_field.pack(fill=tk.X, padx=10)

        # convert button, starts out disabled, is enabled when both input/output names are set
        self.convert_button= tk.Button(self, text='Convert',command=self.do_conversion, bg="SpringGreen3", state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        self.input_file_name.trace('w', self.entry_callback)
        self.output_file_name.trace('w', self.entry_callback)

    def choose_input_file(self):
        p = pathlib.Path(os.path.expanduser("~"))
        file_name = fd.askopenfilename(initialdir = p,
            title = "Select input file", filetypes = (("CSV files","*.csv"),("all files","*.*")))
        if not file_name: return

        self.input_file_name.set(file_name)

    def choose_output_file(self):
        p = pathlib.Path(os.path.expanduser("~"))
        file_name = fd.asksaveasfilename(initialdir = p,
            title = "Select output file", filetypes = (("CSV files","*.csv"),("all files","*.*")))
        if not file_name: return

        self.output_file_name.set(file_name)

    def entry_callback(self, *args):
        self.update_convert_button_availability()

    def update_convert_button_availability(self):
        if self.input_file_name.get() and self.output_file_name.get():
            self.convert_button.config(state = tk.NORMAL)
        else:
            self.convert_button.config(state = tk.DISABLED)

    def do_conversion(self):
        exporter = Exporter()
        decks = None
        try:
            exporter.verify_input_file(self.input_file_name.get())
        except Exception as ex:
            messagebox.showwarning("Invalid File", ex)
            raise

        try:
            decks = exporter.read_and_convert_decks(self.input_file_name.get())
        except Exception as ex:
            messagebox.showerror("Could not convert", "Error while reading CSV file.")
            raise

        try:
            exporter.output_decks(decks, self.output_file_name.get())
        except Exception as ex:
            messagebox.showerror("Could not convert", "Error while writing CSV file.")
            raise

        messagebox.showinfo("Success", f'{len(decks)} decks converted.')

def main():
    root = tk.Tk()
    app = TCExportApp(master=root)
    app.mainloop()

main()
