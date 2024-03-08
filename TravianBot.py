from tkinter import *
from tkinter import messagebox
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
class TravianBot:

    def __init__(self):
        self.villageLst = []

    def startApplication(self):

        if self.hasConfigMain():
            self.initMainGui()
        else:
            print('toca crear')
            self.initMainGui()
            self.init_LoginGui()
    def hasConfigMain(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if (config.has_section('main')):
            return True
        return False

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

        btnLoginConfig = Button(content, text="Login Settings", fg="black", command=self.init_LoginGui).grid(row=0, column=0)
        btnConfig = Button(content, text="Village Settings", fg="black", command=self.init_ConfigGui).grid(row=0, column=1)
        btnStart = Button(footer, text="Start", fg="black", command=self.startTravianBoot).grid(row=0, column=0)

        root.mainloop()

    def on_select(self, event, picklist):
        selected_index = picklist.curselection()[0]
        # Use the index to retrieve the selected item
        selected_item = picklist.get(selected_index)
        print("Selected item:", selected_item)

    def startTravianBoot(self):
        print('aqui em teoria a magica começa')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        browser = webdriver.Chrome(options=chrome_options)
        browser.get('https://es2.kingdoms.com/#/page:village/window:welcomeScreen')
        rejectCockie = WebDriverWait(browser, 120).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/div[1]/div[2]/span[1]/a')))
        rejectCockie.click()
        mailTxt = None
        while mailTxt == None:
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
                print('O Login quebraria aqui ...')
                print(e)

        passwordTxt = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[2]/input')))
        loginBtn = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[3]/input')))
        mailTxt.send_keys('nathanmvnunes@gmail.com')
        passwordTxt.send_keys('Dj!kstr@21travian2')
        loginBtn.click()

        browser.switch_to.default_content()
        continuePlayBtn = WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//html/body/div[2]/div/div[4]/div[2]/div/div[2]/div/div[3]/div[3]/div/div/button')))
        continuePlayBtn.click()

        #after opened
        er = True
        while er:
            try:
                villagesOverView = WebDriverWait(browser, 50).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/header/div[3]/div/div[2]/a[3]/i')))
                villagesOverView.click()
                er = False
            except Exception as e:
                print('erro tentando abrir o village overview')


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
            print(aT)

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

def main():
    app = TravianBot().startApplication()

if __name__ == "__main__":
    main()