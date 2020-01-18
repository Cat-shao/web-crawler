# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 20:23:16 2020

@author: Cat-shao
"""
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

option = webdriver.ChromeOptions()
option.add_argument("user-data-dir=C:\\Users\\x1c\\AppData\\Local\\Google\\Chrome\\User Data")

driver = webdriver.Chrome(chrome_options=option)
driver.maximize_window()

driver.get("https://www.bilibili.com/blackboard/xianxing2020bnj.html?anchor=game")
sleep(5)
add_button=driver.find_elements_by_class_name("fzdysk")[17]
#ActionChains(driver).move_to_element(add_button).perform()
while 1:
    try:
        #ActionChains(driver).click(add_button).perform()
        add_button.click()
    except:
        if driver.page_source.find("天呐！你居然获得了稀有食材")!=-1:
            f1=driver.page_source.find("<div class=\"cnt\">")+17
            f2=driver.page_source.find("</div>",f1-1)
            print("发现稀有食材：%s"%driver.page_source[f1:f2])
            #ActionChains(driver).click(driver.find_element_by_xpath("//div[@class='close-button ibg']")).perform()
    
        if driver.page_source.find("你趁别人不注意往锅里加了个...")!=-1:
            f1=driver.page_source.find("<div class=\"cnt\">")+17
            f2=driver.page_source.find("</div>",f1-1)
            print("发现另类食材：%s"%driver.page_source[f1:f2])
            #ActionChains(driver).click(driver.find_element_by_xpath("//div[@class='close-button ibg']")).perform()
            
        if driver.page_source.find("class=\"thousand-thanks\"")!=-1:
            print("为拜年祭火锅宴做出了\n连续加菜1000次的贡献 获得称号")
            #ActionChains(driver).click(driver.find_element_by_xpath("//div[@class='close-button ibg']")).perform()
            
        driver.find_element_by_xpath("//div[@class='close-button ibg']").click()

    #sleep(0.01)
