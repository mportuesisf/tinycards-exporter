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
from tkinter import *

import os

import pathlib
from pathlib import Path

class TCExportApp(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.input_file_name = ""
        self.output_file_name = ""

        self.master=master
        self.pack()
        self.create_widgets()

    # XXX fix layout
    def create_widgets(self):
        # input file prompt
        self.input_label= tk.Label(self, text='Input file:', font=('helvetica', 12, 'bold'))
        self.input_label.pack(side="top")

        # input file text field
        self.input_field= tk.Entry(self, textvariable=self.input_file_name)
        self.input_field.pack(side="top")

        # input file button to summon file chooser
        self.input_button= tk.Button(text='Choose Input File...',command=self.choose_input_file)
        self.input_button.pack(side="top")

        # output file prompt
        self.output_label= tk.Label(self, text='Output file:', font=('helvetica', 12, 'bold'))
        self.output_label.pack(side="bottom")

        # output file text field
        self.output_field= tk.Entry(self, textvariable=self.output_file_name)
        self.output_field.pack(side="bottom")

        # output file button to summon file chooser
        self.output_button= tk.Button(text='Choose Output File...',command=self.choose_output_file)
        self.output_button.pack(side="bottom")

        # convert button, starts out disabled, is enabled when both input/output names are set
        self.convert_button= tk.Button(text='Convert',command=self.do_conversion)
        self.convert_button.pack(side="bottom")

    def choose_input_file(self):
        p = pathlib.Path(os.path.expanduser("~"))
        self.input_file_name = fd.askopenfilename(initialdir = p,
            title = "Select input file", filetypes = (("CSV files","*.csv"),("all files","*.*")))
        if not self.input_file_name: return

        self.input_field.delete(0, END)
        self.input_field.insert(0, self.input_file_name)
        self.update_convert_button_availability()

    def choose_output_file(self):
        p = pathlib.Path(os.path.expanduser("~"))
        self.output_file_name = fd.asksaveasfilename(initialdir = p,
            title = "Select output file", filetypes = (("CSV files","*.csv"),("all files","*.*")))
        if not self.output_file_name: return

        self.output_field.delete(0, END)
        self.output_field.insert(0, self.output_file_name)
        self.update_convert_button_availability()

    # XXX also handle typeins to the text field, update_convert_button_availability

    def update_convert_button_availability(self):
        # XXX if both input and output are set, then enable the convert button, otherwise disable
        pass

    def do_conversion(self):
        exporter = Exporter()
        decks = None
        try:
            print(f'verifying: {self.input_file_name}')
            exporter.verify_input_file(self.input_file_name)
        except Exception as ex:
            print(ex)

        try:
            print(f'reading: {self.input_file_name}')
            decks = exporter.read_and_convert_decks(self.input_file_name)
        except Exception:
            print ("Error while reading CSV file:")

        try:
            print(f'writing: {self.output_file_name}')
            exporter.output_decks(decks, self.output_file_name)
        except Exception:
            print ("Error while writing CSV file:")

        print("DONE")

def main():
    root = tk.Tk()
    app = TCExportApp(master=root)
    app.mainloop()

main()