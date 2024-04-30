from tkinter import *
from tkinter import messagebox
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import threading
from queue import Queue
import time
from datetime import datetime, timedelta
import schedule
import math
import pandas as pd
import re
import json

class TravianBot:
    def __init__(self):
        self.villageLst = []
        self.root = Tk()
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        self.mainDriver = webdriver.Chrome(options=chrome_options)
        self.app = MainWindow(self.root, self.mainDriver)
        self.label_text = StringVar()
        self.loading_screen = LoadingScreen(self.root, self.label_text, self.mainDriver)
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

    def initFarmList(self):
        print("Initing farm list")
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        er = True
        erAtt = 0
        while er:
            if erAtt == 2:
                self.mainDriver.refresh()
                erAtt = 0
            try:
                villagesOverView = WebDriverWait(self.mainDriver, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/header/div[3]/div/div[2]/a[3]/i')))
                villagesOverView.click()
                er = False
            except Exception as e:
                erAtt += 1
                print('Esperando cargar pagina para entrar ao village overview:: ' + str(erAtt))
        table = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH,
             '//html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/table/tbody')))
            # /html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/table/tbody
        trs = WebDriverWait(table, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        villageLink = None
        for row in trs:
            tds = WebDriverWait(row, 25).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
            villageName = ''
            while villageName == '':
                try:
                    a = WebDriverWait(tds[0], 25).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    villageName = a.text
                    if villageName == 'Sampa':
                        villageLink = a
                        print('encontrou a aldeia Sampa! Kraio')
                except Exception as e:
                    print('quebraria aqui a leitura do village name')
        villageLink.click()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        new_url = 'https://com1n.kingdoms.com/#/page:village/villId:537804822/location:32/window:building/cp:1'
        #https://com1n.kingdoms.com/#/page:village/villId:537804822/location:32/window:building/cp:1/tab:FarmList
        self.mainDriver.execute_script(f"window.location.href = '{new_url}'")
        farmListTab = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH,
             '//html/body/div[3]/window/div/div/div[4]/div/nav/a[3]/div/span/span')))
        farmListTab.click()
        farmList = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH,
             '//html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/table/tbody/tr[1]/td[1]/div/input')))
        farmList.click()
        startRaid = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH,
             '//html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div[3]/button[2]/div/i[1]')))
        time.sleep(5)
        startRaid.click()
    def startApplication(self):

        if self.hasConfigMain():
            #v1 = Village('Santos', 100, 100, 100, 100)
            #v2 = Village('Itapema', 100, 100, 100, 100)
            #self.villageLst.append(v1)
            #self.villageLst.append(v2)
            #self.villageLst = ['Santos', 'Itapema']
            self.app.initMainGui(self.villageLst)
            result_queue = Queue()
            worker_thread = threading.Thread(target=self.startTravianBoot, args=(result_queue,))
            worker_thread.start()
            self.root.withdraw()
            self.get_queue(result_queue)
            #self.testScheduleFastBuild()
            #current_time = time.time()
                #execution_time = time.mktime((2024, 4, 3, 15, 35, 0, 0, 0, 0))
            #time_difference = execution_time - current_time
            #if time_difference > 0:
            #    timer = threading.Timer(time_difference, self.testScanMap)
            #    timer.start()
        else:
            self.app.callLoginWindow()
        self.root.mainloop()

    def testScanMap(self):
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        er = True
        while er:
            print('test')
            try:
                print('antes de dar pau')
                overView = WebDriverWait(self.mainDriver, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/header/div[5]/div/nav/a[3]')))
                print('achou o overview? como?')
                print(overView)
                overView.click()  # open map
                er = False
            except OSError as e:
                print('oxiiiiiii')
                print(e)
                print(e.errno)
                print(e.strerror)
                time.sleep(10)
            # error_code = e.errno
            # print("Error code:", error_code)
            # self.browser.quit()

        script = """
        			window.mouseData = {};

        			document.addEventListener("mousemove", function(event) {
        				// Store the mouse coordinates in the global variable
        				window.mouseData = { x: event.clientX, y: event.clientY };
        			});
        		"""
        self.browser.execute_script(script)

        # canvas = driver.find_element_by_css_selector("canvas")
        x = 150
        y = 150
        asc = ActionChains(self.browser)
        asc.send_keys(Keys.ESCAPE).perform()
        canvas = WebDriverWait(self.browser, 40).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[5]/canvas')))
        time.sleep(10)
        action = ActionChains(self.browser)
        action.move_to_element(canvas).perform()
        mouse_data = self.browser.execute_script("return window.mouseData;")
        print(mouse_data)
        try:
            coo = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[1]')))
            print(coo.text)
            away = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[2]')))
            print(away.text)
        except Exception as e:
            print('nao achou nome de vila')

        print('+ 10 seg de sleep')
        time.sleep(10)
        action.move_by_offset(-30, -30).perform()
        mouse_data = self.browser.execute_script("return window.mouseData;")
        print(mouse_data)
        try:
            coo2 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[1]')))
            print(coo2.text)
            away2 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[2]')))
            print(away2.text)
        except Exception as e:
            print('nao achou nome de vila')

        print('passou')
        time.sleep(10)
        action.move_by_offset(40, 40).perform()
        mouse_data = self.browser.execute_script("return window.mouseData;")
        print(mouse_data)
        try:
            coo3 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[1]')))
            print(coo3.text)
            away3 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[2]')))
            print(away3.text)
        except Exception as e:
            print('nao achou nome de vila')

        print('passou again')
        print('mentira que é só isso')
        time.sleep(10)
        action.move_by_offset(50, 50).perform()
        try:
            coo4 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[1]')))
            print(coo4.text)
            away4 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[2]')))
            print(away4.text)
        except Exception as e:
            print('nao achou nome de vila')
        print('tem que vir agora, 24 11')
        time.sleep(10)
        action.move_by_offset(60, 60).perform()
        try:
            coo4 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[1]')))
            print(coo4.text)
            away4 = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[3]/div[2]/div[3]/div/div[3]/div[1]/span[2]')))
            print(away4.text)
        except Exception as e:
            print('nao achou nome de vila')

        print('iniciando o test do doble click e arraste')
        action.click_and_hold().perform()
        action.move_by_offset(160, 160).perform()
        action.release().perform()

    def testScheduleFastBuild(self):
        print('Starting the test to fast buid')
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        er = True
        erAtt = 0
        while er:
            if erAtt == 2:
                self.mainDriver.refresh()
                erAtt = 0
            try:
                villagesOverView = WebDriverWait(self.mainDriver, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/header/div[3]/div/div[2]/a[3]/i')))
                villagesOverView.click()
                er = False
            except Exception as e:
                erAtt += 1
                print('Esperando cargar pagina para entrar ao village overview:: ' + str(erAtt))
        table = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH,
             '//html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/table/tbody')))
        # /html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/table/tbody
        trs = WebDriverWait(table, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        villageLink = None
        for row in trs:
            tds = WebDriverWait(row, 25).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
            villageName = ''
            while villageName == '':
                try:
                    a = WebDriverWait(tds[0], 25).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    villageName = a.text
                    if villageName == 'Cubatão':
                        villageLink = a
                        print('encontrou a aldeia Sampa! Kraio')
                except Exception as e:
                    print('quebraria aqui a leitura do village name')
        villageLink.click()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        try:
            # try to get the html element
            # slot element - /html/body/div[3]/div[2]/div[4]/div/div[1]/div[2]/div[1]
            freeSlot = WebDriverWait(self.mainDriver, 60).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[4]/div/div[1]/div[1]/div")))

            actions = ActionChains(self.mainDriver)
            actions.move_to_element(freeSlot).perform()
        except OSError as e:
            error_code = e.errno
            print("Error code:", error_code)
            print('Erro tentando ler o segundo slot')
        #/html/body/div[3]/div[2]/div[4]/div/div[2]/div/div/div[2]/div[2]/div[2]/span
        remaningTime = WebDriverWait(self.mainDriver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//html/body/div[3]/div[2]/div[4]/div/div[2]/div/div/div[2]/div[2]/div[2]/span")))
        print(remaningTime.text)
        newRemaningTime = remaningTime.text.split(':')
        duration_to_add = timedelta(hours=int(newRemaningTime[0]), minutes= (int(newRemaningTime[1] ) - 5), seconds=int(newRemaningTime[2])+ 5)
        current_datetime = datetime.now()
        new_datetime = current_datetime + duration_to_add
        print(new_datetime)

        timestamp = new_datetime.timestamp()
        current_time = time.time()

        time_difference = timestamp - current_time
        if time_difference > 0:
            timer = threading.Timer(time_difference, self.testBuildJob)
            timer.start()

    def testBuildJob(self):
        print('start o job mesmo')
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(self.mainDriver).send_keys(Keys.ESCAPE).perform()
        try:
            # try to get the html element
            # slot element - /html/body/div[3]/div[2]/div[4]/div/div[1]/div[2]/div[1]
            slot = WebDriverWait(self.mainDriver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//html/body/div[3]/div[2]/div[4]/div/div[2]/div/div/div[2]/div[3]/button")))

            actions = ActionChains(self.mainDriver)
            actions.move_to_element(slot).perform()
            slot.click()
        except OSError as e:
            error_code = e.errno
            print("Error code:", error_code)
            print('Erro tentando ler o segundo slot')
        #botao - /html/body/div[3]/div[2]/div[4]/div/div[2]/div/div/div[2]/div[3]/button
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
        self.update_label(self.label_text, "Opening Travian web page")
        self.mainDriver.get('https://es2.kingdoms.com/#/page:village/window:welcomeScreen')
        self.update_label(self.label_text, "Finished to load home page")
        self.update_label(self.label_text, "Trying to get Reject Cockie")
        rejectCockie = None
        rejAttemp = 0
        while rejectCockie == None:
            if rejAttemp == 2:
                self.mainDriver.refresh()
                rejAttemp = 0
            try:
                rejectCockie = WebDriverWait(self.mainDriver, 20).until(
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
                self.mainDriver.refresh()
            try:
                iframe = WebDriverWait(self.mainDriver, 20).until(EC.presence_of_element_located(
                    (By.XPATH, '//html/body/div[5]/div/table/tbody/tr/td/div/div/iframe')))

                self.mainDriver.switch_to.frame(iframe)

                title = WebDriverWait(self.mainDriver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//html/head/title')))

                iframe2 = WebDriverWait(title, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/iframe')))
                self.mainDriver.switch_to.frame(iframe2)
                mailTxt = WebDriverWait(self.mainDriver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[1]/input')))
            except Exception as e:
                mailAtt += 1
                print('rapaaai')
                print('O Login quebraria aqui ...')
                print(e)
        self.update_label(self.label_text, "Got Username text entry")
        self.update_label(self.label_text, "Now getting password text entry")

        passwordTxt = WebDriverWait(self.mainDriver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[2]/input')))
        loginBtn = WebDriverWait(self.mainDriver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//html/body/div[1]/form/div[3]/input')))

        self.update_label(self.label_text, "Everything fine, now input username and password")

        config = configparser.ConfigParser()
        config.read('config.ini')
        mailTxt.send_keys(config['main']['username'])
        passwordTxt.send_keys(config['main']['password'])
        loginBtn.click()
        self.update_label(self.label_text, "Login clicked")
        self.update_label(self.label_text, "Now click to enter world game")

        self.mainDriver.switch_to.default_content()
        continueErr = True
        continueAtmp = 0
        try:
            while continueErr:
                if continueAtmp == 10:
                    self.mainDriver.refresh()
                    continueErr = 0
                continuePlayBtn = WebDriverWait(self.mainDriver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//html/body/div[2]/div/div[4]/div[2]/div/div[2]/div/div[3]/div[3]/div/div/button')))
                continuePlayBtn.click()
                self.update_label(self.label_text, "Mundo de jogo clicado")
                continueErr = False
        except Exception as e:
            continueAtmp += 1
            print('Erro ao tentar clicar no Botão Continue Playing:: ' + str(continueAtmp))
            time.sleep(3)

        er = True
        erAtt = 0
        while er:
            if erAtt == 10:
                self.mainDriver.refresh()
                erAtt = 0
            try:
                villagesOverView = WebDriverWait(self.mainDriver, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/header/div[3]/div/div[2]/a[3]/i')))
                villagesOverView.click()
                er = False
            except Exception as e:
                erAtt += 1
                print('Esperando cargar pagina para entrar ao village overview:: ' + str(erAtt))
                time.sleep(3)


        self.update_label(self.label_text, "Agora abrir a tabela com as aldeias")

        resourcesA = WebDriverWait(self.mainDriver, 120).until(
                    EC.presence_of_element_located((By.XPATH, '//html/body/div[3]/window/div/div/div[4]/div/nav/a[2]')))
        resourcesA.click()
        table = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div[2]/div/table/tbody')))
                        #/html/body/div[3]/window[2]/div/div/div[4]/div/div/div[1]/div/div/div/div/div/div/table
                        #/html/body/div[3]/window/div/div/div[4]/div/div/div[1]/div/div/div/div/div[2]/div/table/tbody

        trs = WebDriverWait(table, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        for row in trs:
            tds = WebDriverWait(row, 25).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
            villageName = ''
            villageWood = ''
            villageClay = ''
            villageIron = ''
            villageCroop = ''
            while villageName == '':
                try:
                    a = WebDriverWait(tds[0], 25).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    villageName = a.text
                except Exception as e:
                    print('quebraria aqui a leitura do village name')
            #read village wood
            while villageWood == '':
                try:
                    villageWood = tds[1].text
                except Exception as e:
                    print('quebraria aqui a leitura do village wood')
            # read village Clay
            while villageClay == '':
                try:
                    villageClay = tds[2].text
                except Exception as e:
                    print('quebraria aqui a leitura do village clay')
            # read village Iron
            while villageIron == '':
                try:
                    villageIron = tds[3].text
                except Exception as e:
                    print('quebraria aqui a leitura do village iron')
            # read village Croop
            while villageCroop == '':
                try:
                    villageCroop = tds[4].text
                except Exception as e:
                    print('quebraria aqui a leitura do village croop')
            villages.append(Village(villageName, villageWood, villageClay, villageIron, villageCroop))

        resourcesTab = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH, '//html/body/div[3]/window[2]/div/div/div[4]/div/nav/a[2]/div/span/span')))
        resourcesTab.click()

        resourcesTable = WebDriverWait(self.mainDriver, 15).until(EC.presence_of_element_located(
            (By.XPATH,
             '//html/body/div[3]/window[2]/div/div/div[4]/div/div/div[1]/div/div/div/div/div[2]/div/table/tbody')))
        resourcesTrs = WebDriverWait(resourcesTable, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        for row in resourcesTrs:
            tds = WebDriverWait(row, 25).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'td')))
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
    def __init__(self, master, mainDriver):
        self.master = master
        self.master.title("Main Window")
        self.mainDriver = mainDriver
    def quit_application(self):
        self.master.quit()
        self.mainDriver.quit()
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
        self.master.geometry("400x400")
        self.master.resizable(0, 0)
        self.master.pack_propagate(0)
        header = Frame(self.master, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        content = Frame(self.master)
        contentR = Frame(content, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        contentL = Frame(content, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        footer = Frame(self.master, highlightbackground="black", highlightcolor="black", highlightthickness=1)

        self.master.columnconfigure(0, weight=10)
        self.master.rowconfigure(0, weight=2)
        self.master.rowconfigure(1, weight=6)
        self.master.rowconfigure(2, weight=2)


        header.grid(row=0, column=0, sticky='news')
        header.columnconfigure(0, weight=10)
        header.rowconfigure(0, weight=2)

        content.grid(row=1, sticky='news')
        content.columnconfigure(0, weight=5)
        content.columnconfigure(1, weight=5)
        content.rowconfigure(0, weight=10)

        contentL.grid(row=0, column=0, sticky='news')
        contentL.rowconfigure(0, weight=2)
        contentL.rowconfigure(1, weight=8)
        contentL.columnconfigure(0, weight=0)

        contentR.grid(row=0, column=1, sticky='news')
        contentR.columnconfigure(0, weight=5)
        contentR.rowconfigure(0, weight=2)
        contentR.rowconfigure(1, weight=2)
        contentR.rowconfigure(2, weight=2)
        contentR.rowconfigure(3, weight=2)

        #content.rowconfigure(2, weight=2)
        #content.rowconfigure(3, weight=2)
        #content.rowconfigure(4, weight=2)

        footer.grid(row=2, sticky='news')
        footer.columnconfigure(0, weight=3)
        footer.rowconfigure(0, weight=1)

        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]

        lblVillages = Label(contentL, text='Villages')
        lblVillages.grid(row=0, column=0, padx=0, pady=0)
        #print(lblVillages.winfo_width())
        #print(lblVillages.winfo_height())

        picklist = Listbox(contentL, selectmode=SINGLE)
        picklist.grid(row=1, column=0)
        lblWood = Label(contentR, text='Wood: ').grid(row=0, column=0)
        self.lblWoodValue = Label(contentR, text='')
        self.lblWoodValue.grid(row=0, column=1)
        ######## ----- dropdown
        #selected_option = StringVar()
        #selected_option.set('A ver')
        #dropdown = OptionMenu(content, selected_option, "Option 1", "Option 2", "Option 3", "Option 4").grid(row=3,
         #                                                                                                    column=1)
        ###########

        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        for item in villages:
            #print(item)
            #print(item.name)
            #print(item.croop)
            picklist.insert(END, item.name)
        picklist.bind("<<ListboxSelect>>", lambda event: self.on_select(event, picklist, villages))

        #btnLoginConfig = Button(header, text="Login Settings", fg="black", command=self.callLoginWindow).grid(row=0, column=0)
        #btnConfig = Button(header, text="Village Settings", fg="black").grid(row=0, column=1)
        #btnStart = Button(footer, text="Start", fg="black").grid(row=0, column=0)
        btnQuit = Button(footer, text="Quit", fg="black", command=self.quit_application).grid(row=0, column=0)
        btnFunc = Button(footer, text="Func", fg="black", command=self.getFunc).grid(row=0, column=1)

    def getFunc(self):
        print('Initing')
        error_flag = False  # Initialize error flag
        attmp = 0
        while True:
            try:
                if attmp == 5:
                    break
                with open('IA.py', 'r') as file:
                    code = file.read()
                    globals()['error_flag'] = error_flag
                    exec(code, globals(), locals())  # Execute code in the current locals() namespace
                    locals()['fun'](self.mainDriver, self.master)
                    break
            except OSError as e:
                print('Deu arro no getFunc da main principal')
                print(e)
                print(e.errno)
                print(e.strerror)
                error_flag = True  # Set error flag to True
                attmp += 1



    def on_select(self, event, picklist, villages):
        selected_index = picklist.curselection()[0]
        self.lblWoodValue.config(text = villages[selected_index].wood)

class LoadingScreen:
    def __init__(self, master, text, mainDriver):
        self.master = master
        self.mainDriver = mainDriver
        self.loading_window = Toplevel(self.master)
        self.loading_window.title("Loading")
        self.loading_window.geometry("200x100")

        self.label = Label(self.loading_window, textvariable=text)
        self.label.pack(pady=20)
        btnQuit = Button(self.loading_window, text="Quit", fg="black", command=self.quit_application)
        btnQuit.pack()
    def close(self):
        self.loading_window.destroy()

    def quit_application(self):
        self.loading_window.destroy()
        self.master.quit()
        self.mainDriver.quit()
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

class Village:
    def __init__(self, name, wood, clay, iron, croop ):
        self.name = name
        self.wood = wood
        self.clay = clay
        self.iron = iron
        self.croop = croop


def main():
    app = TravianBot().startApplication()

if __name__ == "__main__":
    main()