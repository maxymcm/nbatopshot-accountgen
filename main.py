import imaplib, email, requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import os



num = int(input("Number of accounts: "))

if not os.path.exists("credentials.txt"):
    file = open('credentials.txt', 'w+')
    file.write("email=\npassword=")
    file.close()
    exit()
if not os.path.exists("accounts.txt"):
    open('accounts.txt', 'w+').close()

file = open('credentials.txt', 'r')
data = file.readlines()
file.close()
data = [i.replace('\n','') for i in data]
data = [i.split('=') for i in data]

user = data[0][1]
password = data[1][1]
imap_url = 'imap.gmail.com'
print(user,password)


def newEmail(email): 
    splitEmail = [char for char in email.split('@')[0]]
    first = str(email.split('@')[0])
    num = random.randint(1, len(first)-2)
    for i in range(num):
        index = random.randint(0, len(splitEmail)-2)
        if '.' in splitEmail[index] or splitEmail[index] == splitEmail[-1]:
            if splitEmail[index] == splitEmail[-1]:
                continue
            while True:
                index = random.randint(0, len(splitEmail)-2)
                if '.' in splitEmail[index]:
                    continue
                else:
                    if splitEmail[index] == splitEmail[-1]:
                        continue
                    else:
                        splitEmail[index] = splitEmail[index] + '.'
                        break
        else:
            splitEmail[index] = splitEmail[index] + '.'
    email_ = ''
    for i in splitEmail:
        email_ += i
    email_ += '@' + email.split('@')[1]
    return email_



def verify():
    def get_body(msg): 
        if msg.is_multipart(): 
            return get_body(msg.get_payload(0)) 
        else: 
            return msg.get_payload(None, True) 
      
    def search(key, value, con):  
        result, data = con.search(None, key, '"{}"'.format(value)) 
        return data 
      
    def get_emails(result_bytes): 
        msgs = []
        for num in result_bytes[0].split(): 
            typ, data = con.fetch(num, '(RFC822)') 
            msgs.append(data) 
  
        return msgs 
    con = imaplib.IMAP4_SSL(imap_url)  
    con.login(user, password)  
    con.select('Inbox')  
    msgs = get_emails(search('FROM', 'no-reply@meetdapper.com', con)) 

    for msg in msgs[::-1]:  
        for sent in msg: 
            if type(sent) is tuple:  
      
                content = str(sent[1], 'utf-8')  
                data = str(content) 
      
                try:  
                    indexstart = data.find("ltr") 
                    data2 = data[indexstart + 5: len(data)] 
                    indexend = data2.find("</div>") 

                    data = data2[0: indexend].split('( ')
                    data.pop(0)
                    data[0] = data[0].split(' )')
                    data = data[0][0] 
                    requests.get(data)
      
                except UnicodeEncodeError as e: 
                    pass



for i in range(num):
    newEmail_ = newEmail(user)
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    driver.get("https://www.nbatopshot.com/")
    driver.find_element_by_xpath("//a[@data-testid='SignUpButton']").click()
    time.sleep(2)
    driver.find_elements_by_xpath("//input")[0].send_keys(newEmail_)
    driver.find_elements_by_xpath("//input")[1].send_keys(password)
    driver.find_element_by_xpath("//button[@id='login']").click()
    time.sleep(10)

    try:
        driver.find_element_by_xpath("//button[@class='ButtonBase__StyledButton-sc-1qgxh2e-0 gjCpfL Button__StyledButton-ig3kkl-1 cFRquA']").click()
    except:
        driver.quit()
        continue
    
    time.sleep(2)

    driver.execute_script('document.getElementsByClassName("intercom-app")[0].style.display="none";')
    driver.find_element_by_xpath("//button[@class='ButtonBase__StyledButton-sc-1qgxh2e-0 gjCpfL Button__StyledButton-ig3kkl-1 dQJcuA']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='Text-sc-179eaht-0 Actions__StyledSkipButton-sc-14iorui-2 jHRZYo hKJntT']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='Text-sc-179eaht-0 Actions__StyledSkipButton-sc-14iorui-2 jHRZYo hKJntT']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='Text-sc-179eaht-0 Actions__StyledSkipButton-sc-14iorui-2 jHRZYo hKJntT']").click()
    time.sleep(2)
    driver.find_element_by_xpath("//button[@class='ButtonBase__StyledButton-sc-1qgxh2e-0 gjCpfL Button__StyledButton-ig3kkl-1 dQJcuA']").click()
    verify()
    driver.quit()
    file = open('accounts.txt', 'a')
    file.write('{}:{}\n'.format(newEmail_, password))
    file.close()


