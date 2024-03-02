from tkinter import *
from tkinter import messagebox
import configparser
class TravianBot:

    def __init__(self):
        self.villageLst = []

    def initMainGui(self):
        root = Tk()
        root.title("TravianBot")
        root.geometry("300x300")
        root.resizable(0, 0)
        root.pack_propagate(0)
        header = Frame(root)
        content = Frame(root)
        footer = Frame(root)


        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=6)
        root.rowconfigure(2, weight=2)
        root.rowconfigure(3, weight=1)

        header.grid(row=0, sticky='news')
        header.columnconfigure(0, weight=3)
        header.rowconfigure(0, weight=1)

        content.grid(row=1, sticky='news')
        content.columnconfigure(0, weight=5)
        content.columnconfigure(1, weight=5)
        content.rowconfigure(0, weight=2)
        content.rowconfigure(1, weight=2)
        content.rowconfigure(2, weight=2)
        content.rowconfigure(3, weight=2)
        content.rowconfigure(4, weight=2)

        footer.grid(row=3, sticky='news')
        footer.columnconfigure(0, weight=3)
        footer.rowconfigure(0, weight=1)

        btnConfig = Button(content, text="Configurar", fg="black", command=self.init_ConfigGui).grid(row=0, column=1)

        btnStart = Button(footer, text="Start", fg="black", command=self.startTravianBoot).grid(row=0, column=0)

        root.mainloop()

    def startTravianBoot(self):
        print('aqui em teoria a magica começa')
    def init_ConfigGui(self):
        print('Config GUI')
        self.confiGUI = Toplevel()
        self.confiGUI.title("TK Config")
        self.confiGUI.geometry("350x200")
        header = Frame(self.confiGUI)  # bg = 'green')
        content = Frame(self.confiGUI)  # bg = 'red')
        footer = Frame(self.confiGUI)  # bg = 'green')

        self.confiGUI.columnconfigure(0, weight=1)

        self.confiGUI.rowconfigure(0, weight=1)
        self.confiGUI.rowconfigure(1, weight=8)
        self.confiGUI.rowconfigure(2, weight=1)

        header.grid(row=0, sticky='news')
        header.columnconfigure(0, weight=3)
        header.rowconfigure(0, weight=1)

        content.grid(row=1, sticky='news')
        content.columnconfigure(0, weight=5)
        content.columnconfigure(1, weight=5)
        content.rowconfigure(0, weight=2)
        content.rowconfigure(1, weight=2)
        content.rowconfigure(2, weight=2)
        content.rowconfigure(3, weight=2)
        content.rowconfigure(4, weight=2)

        footer.grid(row=2, sticky='news')
        footer.columnconfigure(0, weight=3)
        footer.rowconfigure(0, weight=1)

        lblTitle = Label(header, text='Preferences', font=("Helvetica", 16)).grid(row=0, column=0)

        lblTime = Label(content, text='Login: ').grid(row=0, column=0)
        lblPassword = Label(content, text='Password: ').grid(row=1, column=0)



        self.loginEntryVar = StringVar()
        tkLoginEntry = Entry(content, width=30, textvariable=self.loginEntryVar).grid(row=0, column=1, sticky=W)
        self.strPassword = StringVar()
        tkPassword = Entry(content, width=25, textvariable=self.strPassword, show="*").grid(row=1, column=1, sticky=W)
        #self.button = Button(footer, text="Get Entry Value", command=self.get_entry_value)
        button1 = Button(footer, text="Save", fg="green", command=self.saveConfig).grid(row=0, column=0)

        self.checkbox_vars = []
        test_option = ['WoodCutter', 'ClayPit', 'IronMine', 'CroopLand']
        self.checkboxes = []

        for i in range(4):
            var = IntVar()
            self.checkbox_vars.append(var)
            checkbox = Checkbutton(content, text=test_option[i], variable=var,
                                   command=lambda i=i: self.checkbox_changed(i))
            self.checkboxes.append(checkbox)
            checkbox.grid(row=2 + i, column=1, sticky=W)

    def saveConfig(self):
        config = configparser.ConfigParser()
        with open('config.ini', 'w') as f:
            config.add_section('main')
            config.set('main', 'username', str(self.loginEntryVar.get()))
            config.set('main', 'password', str(self.strPassword.get()))
            config.write(f)

        self.confiGUI.withdraw()
        messagebox.showinfo('Message title', 'Preferences saved as expected!')

        self.confiGUI.destroy()

    def get_entry_value(self):
        entry_value = self.strPassword.get()
        print("Entry value:", entry_value)

    def checkbox_changed(self, checkbox_index):
        for i, checkbox in enumerate(self.checkboxes):
            if i != checkbox_index:
                checkbox.deselect()

def main():
    app = TravianBot().initMainGui()

if __name__ == "__main__":
    main()