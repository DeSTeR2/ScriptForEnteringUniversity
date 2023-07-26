from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import yagmail
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("ok")
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
print("ok")

driver =  webdriver.Chrome(options=chrome_options)
url = "https://cabinet.edbo.gov.ua/login"
print("ok")
login = LOGIN # changed for privacy
password= PASSWORD # changed for privacy

EMAIL_ADDRESS = EMAIL # changed for privacy
EMAIL_PASSWORD = CODE # changed for privacy


links = [
    'https://vstup.osvita.ua/y2023/r27/41/1190610/',
    'https://vstup.osvita.ua/y2023/r27/41/1206075/',
    'https://vstup.osvita.ua/y2023/r14/97/1213428/',
    'https://vstup.osvita.ua/y2023/r14/282/1204296/'
]

def sendEmail(text):
    yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
    head = 'Оновлена інформація про вступ.'
    yag.send(TO_EMAIL, head, text) # changed for privacy

def operateWithEl(input, place, proposition, spec, index):
    allInfo = ''
    allInfo=allInfo + '\n' +"<b>Статус заявки в кабінеті --------------------------- </b>"+input.text
    allInfo=allInfo + '\n' +"<b>Назва універу ------------------------------------------ </b>"+place.get_attribute("textContent")
    allInfo=allInfo + '\n' +"<b>Спеціальність ----------------------------------------- </b>" + spec.get_attribute("textContent")
    allInfo=allInfo + '\n' +"<b>Навчальна програма -------------------------------- </b>"+proposition.get_attribute("textContent")

    nDriver = webdriver.Chrome(options=chrome_options)
    nDriver.get(url=links[index])
    time.sleep(1)
    elem = nDriver.find_element(By.XPATH, '//span[text()="Завантажити ще..."]')
    nDriver.execute_script("arguments[0].click();", elem)
    elem = None
    while elem == None:
        try:
            elem = nDriver.find_element(By.XPATH, '//td[text()="Власенко З. С."]')
        except NoSuchElementException:
            pass

    elem = nDriver.find_element(By.CLASS_NAME, 'rwd-table')

    elem = elem.find_element(By.TAG_NAME, "tbody")
    elem = elem.find_elements(By.TAG_NAME, "td")

    for i in range(0, len(elem)):
        el = elem[i]
        if (el.text == "Власенко З. С."):
            i = i - 1
            allInfo=allInfo + '\n' +"<b>Номер в загальному списку абітурєнтів ---- </b>"+elem[i].text
            allInfo=allInfo + '\n' +"<b>Статус заявки на сайті vstup.osvita.ua ------- </b>"+elem[i + 2].text
            break
    print(allInfo)
    return allInfo

def getNewText(start,pos,rep):
    new=list(start)
    new[pos]=rep
    ans = ''
    ans=''.join(new)
    return ans

try:
    driver.get(url=url)
    input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')

    input.send_keys(login)

    input = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')

    input.send_keys(password)

    input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[2]/div[3]/button")))
    input.click()
    print("clicked")
    input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Подані заяви на вступ')))
    input.click()
    print("logged")
    xpath= '//*[@id="content"]/div/div[3]/div[2]/main/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div[4]/div/p'
    placeXpath='//*[@id="content"]/div/div[3]/div[2]/main/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div[6]/div/p'
    propositionXpath='//*[@id="content"]/div/div[3]/div[2]/main/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div[8]/div/p'
    specXpath='//*[@id="content"]/div/div[3]/div[2]/main/div/div[1]/div[3]/div[2]/div/div/div/div[1]/div[11]/div/p'
    nums= '1234'

    pos = 83
    time.sleep(2)
    sendToEm = ''

    XPATH = []
    PLACE= []
    PROP=[]
    SPEC=[]
    for i in range(0,4):
        xpath=getNewText(xpath,pos,nums[i])
        placeXpath=getNewText(placeXpath,pos,nums[i])
        propositionXpath=getNewText(propositionXpath,pos,nums[i])
        specXpath=getNewText(specXpath,pos,nums[i])

        sendToEm+=operateWithEl(driver.find_element(By.XPATH, xpath), driver.find_element(By.XPATH, placeXpath), driver.find_element(By.XPATH, propositionXpath),driver.find_element(By.XPATH, specXpath),i)
        sendToEm+='\n'
    #print(XPATH)
    sendEmail(sendToEm)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


