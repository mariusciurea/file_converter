"""This is the file convertor application.
    It allows the user to browse for the input file and choose the output file type

    The output file type can be:
        - .csv
        - .txt
        - .xlsx

    It saves the data from the input file to the output file.
    The output file is automatically created at the same path of the input file
    by adding the chosen extension to the original one
"""
import os.path
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


__auther__ = 'Marius Ciurea'
__email__ = 'marius.ciurea@itschool.ro, ciurea.marius1@gmail.com'
__version__ = 1.0

__all__ = ['ConverterGUI', 'FileConversion']


class FileConversion:
    """Class FileConverter

        Instances of this class have an input file as argument
        This can be a text, a csv or an Excel file

        The user can choose the method to save the file in a different format
            Methods: text_to_csv
                     csv_to_text
                     csv_to_excel
                     excel_to_csv
                     excel_to_text
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1]

    def text_to_csv(self):
        pass

    def text_to_xlsx(self):
        pass

    def csv_to_txt(self):
        pass

    def csv_to_xlsx(self):
        df = pd.read_csv(self.file_path)
        df.to_excel(self.file_path.replace(self.extension, '.xlsx'), index=False)

    def xlsx_to_txt(self):
        df = pd.read_excel(self.file_path)
        df.to_csv(self.file_path.replace(self.extension, '.txt'), index=False)

    def xlsx_to_csv(self):
        df = pd.read_excel(self.file_path)
        df.to_csv(self.file_path.replace(self.extension, '.csv'), index=False)


def _get_method(obj: FileConversion, ext_pair):
    """Get the specific FileConversion method based on the input/output
        file extensions
    """

    file_type = {
        ('.txt', '.csv'): obj.text_to_csv,
        ('.csv', '.txt'): obj.csv_to_txt,
        ('.txt', '.xlsx'): obj.text_to_xlsx,
        ('.csv', '.xlsx'): obj.csv_to_xlsx,
        ('.xlsx', '.csv'): obj.xlsx_to_csv

    }
    return file_type[ext_pair]


class ConverterGUI(tk.Frame):
    """GUI that facilitates file conversion. Inherits from tkinter Frame class

        It has a button widget that allows the user to browse the files and pick up
        the one that wants to be converted

        It has a listbox widget that allows the user to choose one of the following
        file types: .csv, .txt, .xlsx in which the input file must be converted
    """
    def __init__(self, parent):
        """Initialize an instance

       master argument is the widget where the Frame object is located to
       """
        super().__init__()
        self['width'] = 500
        self['height'] = 300

        self.filename = None
        self.label_file_explorer = tk.Label(self, text='Choose file', width=10, height=2, fg='red')
        self.label_file_explorer.grid(row=0, column=0)

        self.label_file_type = tk.Label(self, text='File Type', width=10, height=2, fg='red')
        self.label_file_type.grid(row=0, column=1)

        self.button_explore = tk.Button(self, text='Browse Files', command=self._browse_files)
        self.button_explore.grid(row=1, column=0)

        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=1, column=1)
        self.listbox.insert(1, '.csv')
        self.listbox.insert(2, '.txt')
        self.listbox.insert(3, '.xlsx')

        self.button_convert = tk.Button(self, text='CONVERT', command=self._convert)
        self.button_convert.grid(row=2, column=1)

        self.grid(row=0, column=0)

    def _browse_files(self):
        """Opens a file dialog and gies the user the possibility to pick up a file
        Modifies the label text with the name of the chosen file
        """

        self.filename = filedialog.askopenfilename(initialdir='/', title='Select a file',
                                                   filetypes=(("Text files", '*.txt*'),
                                                              ("all files", '*.*')))
        self.label_file_explorer.configure(width=60, text=self.filename)

    def _convert(self):
        """Covert the input file in the chosen file type (.txt, .csv, .xlsx)

        An instance of Conversion class will be created and this will handle
        the conversion
        """
        selection = {
            0: '.csv',
            1: '.txt',
            2: '.xlsx'
        }
        selected_extension = selection.get(self.listbox.curselection()[0])
        file = FileConversion(self.filename)
        try:
            result = _get_method(file, (file.extension, selected_extension))
            result()
            # check if the file exists
            messagebox.showinfo(message='Conversion successfully done')

        except KeyError:
            print('Exception occurred!')


if __name__ == '__main__':
    root = tk.Tk()
    cvt = ConverterGUI(root)

    root.mainloop()