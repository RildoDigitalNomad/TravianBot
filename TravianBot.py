from tkinter import *
from tkinter import messagebox
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading
from queue import Queue

class TravianBot:
    def __init__(self):
        self.villageLst = []
        self.root = Tk()
        self.app = MainWindow(self.root)
        self.label_text = StringVar()
        self.loading_screen = LoadingScreen(self.root, self.label_text)
    def getLoguinConf(self):
        loginGui = Tk()
        loginGui.title("Login Config")
        loginGui.geometry("350x200")
        header = Frame(loginGui)  # bg = 'green')
        content = Frame(loginGui)  # bg = 'red')
        footer = Frame(loginGui)  # bg = 'green')

        loginGui.columnconfigure(0, weight=1)

        loginGui.rowconfigure(0, weight=1)
        loginGui.rowconfigure(1, weight=8)
        loginGui.rowconfigure(2, weight=1)

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

        loginEntryVar = StringVar()
        tkLoginEntry = Entry(content, width=30, textvariable=loginEntryVar).grid(row=0, column=1, sticky=W)
        strPassword = StringVar()
        tkPassword = Entry(content, width=30, textvariable=strPassword, show="*").grid(row=1, column=1, sticky=W)
        saveBtn = Button(footer, text="Save", fg="green",
                         command=lambda: self.saveLogin(loginEntryVar.get(), strPassword.get(), loginGui)).grid(row=0,
                                                                                                                column=0)
        loginGui.mainloop()

    def startApplication(self):

        if self.hasConfigMain():
            result_queue = Queue()
            worker_thread = threading.Thread(target=self.startTravianBoot, args=(result_queue,))
            worker_thread.start()
            self.root.withdraw()
            self.get_queue(result_queue)
        else:
            self.app.callLoginWindow()
        self.root.mainloop()
    def hasConfigMain(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.has_section('main')

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

        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

        lblVillages = Label(content, text='Villages ').grid(row=2, column=0)
        picklist = Listbox(content, selectmode=SINGLE)
        picklist.grid(row=3, column=0)
        selected_option = StringVar()
        selected_option.set('A ver')
        dropdown = OptionMenu(content, selected_option, "Option 1", "Option 2", "Option 3", "Option 4").grid(row=3, column=1)
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        for item in items:
            picklist.insert(END, item)
        picklist.bind("<<ListboxSelect>>", lambda event: self.on_select(event, picklist))

        btnLoginConfig = Button(content, text="Login Settings", fg="black", command=self.init_LoginGuiT).grid(row=0, column=0)
        btnConfig = Button(content, text="Village Settings", fg="black", command=self.init_ConfigGui).grid(row=0, column=1)
        btnStart = Button(footer, text="Start", fg="black", command=self.startTravianBoot).grid(row=0, column=0)

        root.mainloop()

    def on_select(self, event, picklist):
        selected_index = picklist.curselection()[0]
        # Use the index to retrieve the selected item
        selected_item = picklist.get(selected_index)
        print("Selected item:", selected_item)

    def update_label(self, string_var, str):

        def update():
            string_var.set(str)

        self.root.after(0, update)

    def get_queue(self, queue):
        keepRun = True
        if not queue.empty():
            villages = queue.get()
            self.root.after(1000, lambda: self.update_gui_after_queue(villages))
            keepRun = False
        if keepRun:
            self.root.after(2000, lambda: self.get_queue(queue))

    def update_gui_after_queue(self, villages):
        self.villageLst = villages
        self.loading_screen.close()
        self.app.initMainGui(self.villageLst)
        self.app.deiconify()
    def startTravianBoot(self, queue) :
        self.update_label(self.label_text, "Starting Bot")
        villages = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(options=chrome_options)
        self.update_label(self.label_text, "Opening Travian web page")
        browser.get('https://es2.kingdoms.com/#/page:village/window:welcomeScreen')
        self.update_label(self.label_text, "Finished to load home page")
        self.update_label(self.label_text, "Trying to get Reject Cockie")
        rejectCockie = None
        rejAttemp = 0
        while rejectCockie == None:
            if rejAttemp > 2:
                browser.refresh()
            try:
                rejectCockie = WebDriverWait(browser, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/div[1]/div[2]/span[1]/a')))
                rejectCockie.click()
            except Exception as e:
                rejAttemp+= 1
                print('Error trying to get reject Cockie ...')
                print('Attempt: ' + str(rejAttemp))
                print(e)

        self.update_label(self.label_text, "Found Cockie, clicked on reject")
        self.update_label(self.label_text, "Now, get Username text entry")

        mailTxt = None
        mailAtt = 0
        while mailTxt == None:
            if mailAtt == 2:
                browser.refresh()
            try:
                iframe = WebDriverWait(browser, 20).until(EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[5]/div/table/tbody/tr/td/div/div/iframe')))

                browser.switch_to.frame(iframe)

                title = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//html/head/title')))

                iframe2 = WebDriverWait(title, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/iframe')))
                browser.switch_to.frame(iframe2)
                mailTxt = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[1]/input')))
            except Exception as e:
                mailAtt += 1
                print('rapaaai')
                print('O Login quebraria aqui ...')
                print(e)
        self.update_label(self.label_text, "Got Username text entry")
        self.update_label(self.label_text, "Now getting password text entry")

        passwordTxt = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[2]/input')))
        loginBtn = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[3]/input')))

        self.update_label(self.label_text, "Everything fine, now input username and password")

        config = configparser.ConfigParser()
        config.read('config.ini')
        mailTxt.send_keys(config['main']['username'])
        passwordTxt.send_keys(config['main']['password'])
        loginBtn.click()
        self.update_label(self.label_text, "Login clicked")
        self.update_label(self.label_text, "Now click to enter world game")

        browser.switch_to.default_content()
        continuePlayBtn = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//html/body/div[2]/div/div[4]/div[2]/div/div[2]/div/div[3]/div[3]/div/div/button')))
        continuePlayBtn.click()
        self.update_label(self.label_text, "Mundo de jogo clicado")

        er = True
        erAtt = 0
        while er:
            if erAtt == 2:
                browser.refresh()
                erAtt = 0
            try:
                villagesOverView = WebDriverWait(browser, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/header/div[3]/div/div[2]/a[3]/i')))
                villagesOverView.click()
                er = False
            except Exception as e:
                erAtt += 1
                print('Esperando cargar pagina para entrar ao village overview:: ' + str(erAtt))


        self.update_label(self.label_text, "Agora abrir a tabela com as aldeias")

        table = WebDriverWait(browser, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//html/body/div[3]/window[2]/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/table/tbody')))
        #
        trs = WebDriverWait(table, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        for row in trs:
            tds = WebDriverWait(row, 25).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
            aT = ''
            while aT == '':
                try:
                    a = WebDriverWait(tds[0], 25).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    aT = a.text
                except Exception as e:
                    print('quebraria aqui a leitura do a')
            villages.append(aT)
        print(villages)
        queue.put(villages)

    def init_LoginGuiT(self):
        self.new_window = Toplevel(self.master)
        self.app = LoginWindow(self.new_window)
    def init_LoginGui(self):
        print('Login gui')
        loginGui = Toplevel()
        loginGui.title("Login Config")
        loginGui.geometry("350x200")
        header = Frame(loginGui)  # bg = 'green')
        content = Frame(loginGui)  # bg = 'red')
        footer = Frame(loginGui)  # bg = 'green')

        loginGui.columnconfigure(0, weight=1)

        loginGui.rowconfigure(0, weight=1)
        loginGui.rowconfigure(1, weight=8)
        loginGui.rowconfigure(2, weight=1)

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

        loginEntryVar = StringVar()
        tkLoginEntry = Entry(content, width=30, textvariable=loginEntryVar).grid(row=0, column=1, sticky=W)
        strPassword = StringVar()
        tkPassword = Entry(content, width=30, textvariable=strPassword, show="*").grid(row=1, column=1, sticky=W)
        saveBtn = Button(footer, text="Save", fg="green", command=lambda: self.saveLogin(loginEntryVar.get(), strPassword.get(), loginGui)).grid(row=0, column=0)

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
        saveBtn = Button(footer, text="Save", fg="green", command=self.saveConfig).grid(row=0, column=0)

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

    def saveLogin(self, loginEntryVar, strPassword, loginGui):
        config = configparser.ConfigParser()
        with open('config.ini', 'w') as f:
            config.add_section('main')
            config.set('main', 'username', str(loginEntryVar))
            config.set('main', 'password', str(strPassword))
            config.write(f)

        loginGui.withdraw()
        messagebox.showinfo('Message title', 'Preferences saved as expected!')

        loginGui.destroy()

    def saveConfig(self):
        config = configparser.ConfigParser()
        selectedCheckboxStr = ''
        for index, checkbox in enumerate(self.checkbox_vars):
            if checkbox.get() == 1:
                selectedCheckboxStr = self.confiGUI.nametowidget(str(self.checkboxes[index])).cget("text")
        with open('config.ini', 'w') as f:
            config.add_section('main')
            config.set('main', 'username', str(self.loginEntryVar.get()))
            config.set('main', 'password', str(self.strPassword.get()))
            config.set('main', 'resource_preference', str(selectedCheckboxStr))
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


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Main Window")

    def withdraw(self):
        self.master.withdraw()

    def deiconify(self):
        self.master.deiconify()
    def callLoginWindow(self):
        self.master.withdraw()
        self.new_window = Toplevel(self.master)
        self.app2 = LoginWindow(self.new_window, self.handle_login_save)


    def handle_login_save(self, toplevel, result):
        if result:
            messagebox.showinfo('Message title', 'Preferences saved as expected!')
            toplevel.destroy()
            self.initMainGui()
            self.master.deiconify()
    def initMainGui(self, villages):
        self.master.title("TravianBot")
        self.master.geometry("300x300")
        self.master.resizable(0, 0)
        self.master.pack_propagate(0)
        header = Frame(self.master)
        content = Frame(self.master)
        footer = Frame(self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=6)
        self.master.rowconfigure(2, weight=2)
        self.master.rowconfigure(3, weight=1)

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

        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

        lblVillages = Label(content, text='Villages ').grid(row=2, column=0)
        picklist = Listbox(content, selectmode=SINGLE)
        picklist.grid(row=3, column=0)
        selected_option = StringVar()
        selected_option.set('A ver')
        dropdown = OptionMenu(content, selected_option, "Option 1", "Option 2", "Option 3", "Option 4").grid(row=3,
                                                                                                             column=1)
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        for item in villages:
            picklist.insert(END, item)
        picklist.bind("<<ListboxSelect>>", lambda event: self.on_select(event, picklist))

        btnLoginConfig = Button(content, text="Login Settings", fg="black", command=self.callLoginWindow).grid(row=0, column=0)
        btnConfig = Button(content, text="Village Settings", fg="black").grid(row=0, column=1)
        btnStart = Button(footer, text="Start", fg="black").grid(row=0, column=0)

class LoadingScreen:
    def __init__(self, master, text):
        self.master = master
        self.loading_window = Toplevel(self.master)
        self.loading_window.title("Loading")
        self.loading_window.geometry("200x100")

        self.label = Label(self.loading_window, textvariable=text)
        self.label.pack(pady=20)
    def close(self):
        self.loading_window.destroy()
class LoginWindow:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback
        self.master.title("Login")
        self.master.title("Login Config")
        self.master.geometry("350x200")
        header = Frame(self.master)  # bg = 'green')
        content = Frame(self.master)  # bg = 'red')
        footer = Frame(self.master)  # bg = 'green')

        self.master.columnconfigure(0, weight=1)

        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=8)
        self.master.rowconfigure(2, weight=1)

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

        loginEntryVar = StringVar()
        tkLoginEntry = Entry(content, width=30, textvariable=loginEntryVar).grid(row=0, column=1, sticky=W)
        strPassword = StringVar()
        tkPassword = Entry(content, width=30, textvariable=strPassword, show="*").grid(row=1, column=1, sticky=W)
        saveBtn = Button(footer, text="Save", fg="green",
                         command=lambda: self.save_action(loginEntryVar.get(), strPassword.get())).grid(row=0,
                                                                                                                column=0)
    def save_action(self, loginEntryVar, strPassword):
        success = self.save_data(loginEntryVar, strPassword)
        self.callback(self.master, success)
    def save_data(self, login, password):
        try:
            config = configparser.ConfigParser()
            with open('config.ini', 'w') as f:
                config.add_section('main')
                config.set('main', 'username', str(login))
                config.set('main', 'password', str(password))
                config.write(f)
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

        return config.has_section('main')
def main():
    app = TravianBot().startApplication()

if __name__ == "__main__":
    main()