# -*- coding: utf-8 -*-

from tkinter import *
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import threading
import datetime
import time
import sys

now = datetime.datetime.now()

options = webdriver.ChromeOptions()
# # 창 숨기는 옵션 추가
#options.add_argument("headless")

chromedriver = "chromedriver.exe"
# driver 실행
driver = webdriver.Chrome(chromedriver, options=options)

action = ActionChains(driver)
url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"
root = Tk()
root.title("빠른댓글 매크로")

root.geometry("500x305") #가로 * 세로
root.resizable(False, False) #화면크기 조정 (가능 ,불가능 , True, False)

frame_login = LabelFrame(root, text="로그인")
frame_login.place(x=20,y=15)

frame_id = Label(frame_login)
frame_id.pack()
id = Label(frame_id, text = "  아이디  ")
txt1 = Entry(frame_id, width=21)
id.pack(side="left")
txt1.pack(side="left")

frame_pw = Label(frame_login)
frame_pw.pack()
pw = Label(frame_pw, text = "패스워드 ")
txt2 = Entry(frame_pw, width=21)
pw.pack(side="left")
txt2.pack(side="left")

frame_ad = LabelFrame(root, text="주소")
frame_ad.place(x=20,y=90)
txt3 = Text(frame_ad, width=30, height=4)
txt3.pack()

frame_re = LabelFrame(root, text = "댓글내용")
frame_re.place(x=20,y=175)
txt4 = Text(frame_re, width=30, height=7)
txt4.pack()

frame_pl = LabelFrame(root, text = "Log")
frame_pl.place(x=250, y=15)
frame=Frame(frame_pl)
frame.pack()
scrollbar=Scrollbar(frame)
scrollbar.pack(side="right", fill = "y")
txt5 = Listbox(frame, selectmode = "single", width=30, height=12, yscrollcommand = scrollbar.set)
txt5.pack()
scrollbar.config(command=txt5.yview)

class Thread1(threading.Thread):
    def run(self) -> None:
        try:
            driver.get(url)
            id = txt1.get()
            pw = txt2.get()
            txt5.insert(END,datetime.datetime.now(), '로그인을 시도합니다.')
            txt5.see(END)
            driver.execute_script("document.getElementsByName('id')[0].value=\'"+ id + "\'")
            driver.execute_script("document.getElementsByName('pw')[0].value=\'"+ pw + "\'")
            driver.find_element_by_css_selector(".btn_login").click()
            time.sleep(0.5)

            txt5.see(END)
            naver=txt3.get("1.0", END)
            txt5.insert(END,datetime.datetime.now(),' 로그인 성공.')
            driver.get(naver)
            time.sleep(1)

            num = driver.find_elements_by_class_name("gm-tcol-c.total")[0].get_attribute('textContent')
            num = num.replace(',', '')
            num = int(num)
            print(num)
            while True:
                driver.refresh()
                time.sleep(0.4)
                num1 = driver.find_elements_by_class_name("gm-tcol-c.total")[0].get_attribute('textContent')
                num1 = num1.replace(',', '')
                num1 = int(num1)
                txt5.insert(END,datetime.datetime.now(),' 검색 중 입니다.')
                txt5.see(END)

                global stop_threads 
                if stop_threads:
                    txt5.insert(END,datetime.datetime.now(),' 중지되었습니다.')
                    break            
                if num < num1:
                    retxt = txt4.get("1.0", END)
                    driver.switch_to.frame("cafe_main")
                    time.sleep(0.35)
                    driver.find_elements_by_class_name("article")[3].click()
                    time.sleep(0.4)
                    driver.switch_to.window(driver.window_handles[0])
                    driver.switch_to.frame("cafe_main")
                    time.sleep(0.35)
                    driver.find_element_by_css_selector(".comment_inbox_text").send_keys(retxt)
                    driver.find_element_by_css_selector(".button.btn_register").click()
                    txt5.insert(END,datetime.datetime.now(),' 작성완료.')
                    txt5.see(END)
                    break
        except:
            txt5.insert(END,datetime.datetime.now(),' 오류발생.')
            txt5.see(END)
    
class Thread2(threading.Thread):
    def run(self) -> None:
        root.update() 
        time.sleep(0.1)

T1 = Thread1()
T2 = Thread2()
T2.daemon=False
T2.start()
stop_threads=False
def change():
    T1.start()
    

def cancle():
    global stop_threads
    stop_threads = True
    return stop_threads




btn1 = Button(root, padx = 10, pady = 5, text="실행", command=change)
btn1.place(x=310, y=250)

btn2 = Button(root, padx = 10, pady = 5, text="중지", command=cancle)
btn2.place(x=370, y=250)

root.mainloop()