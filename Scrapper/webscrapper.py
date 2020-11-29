from selenium import webdriver
import time
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

item = ""
amazonitem = False
bestbuyitem = False
neweggitem = False
microcenteritem = False
bhitem = False

def getItemName():
    return input("What Graphics Card are you looking for?: ")

# Needs work!!!
def amazon(item, dept):
    inStock = []
    url = "https://www.amazon.com"
    browser = webdriver.Chrome()
    browser.get(url)
    searchbar = browser.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    searchbar.send_keys(item)
    searchicon = browser.find_element_by_xpath('//*[@id="nav-search-submit-text"]/input').click()
    minprice = browser.find_element_by_xpath('//*[@id="low-price"]')
    minprice.send_keys('499')
    maxprice = browser.find_element_by_xpath('//*[@id="high-price"]')
    maxprice.send_keys('600')
    go = browser.find_element_by_xpath('//*[@id="a-autoid-1"]/span/input').click()
    deptSelect = browser.find_element_by_partial_link_text(dept).click()
    products = browser.find_elements_by_class_name('sg-col-4-of-12')
    for items in products:
        if(item in items.text and "$" in items.text):
            inStock.append(items.text)
        else:
            inStock.append("Sold Out")
    browser.close()
    return inStock

def bestbuy(item):
    inStock = []
    url = "https://www.bestbuy.com/"
    browser = webdriver.Chrome()
    browser.get(url)
    searchbar = browser.find_element_by_xpath('//*[@id="gh-search-input"]')
    searchbar.send_keys(item)
    searchIcon = browser.find_element_by_xpath('//*[@id="header-block"]/div[2]/div[1]/div/div[2]/div/div[1]/div/div/form/button[2]').click()
    products = browser.find_elements_by_class_name('sku-item')
    for items in products:
        if("Sold Out" in items.text):
            inStock.append("Sold Out")
        elif("Add to Cart" in items.text or "Get it today" in items.text):
            inStock.append(items.text)
    browser.close()
    return inStock

def newegg(item, dept):
    inStock = []
    url = "https://www.newegg.com/"
    browser = webdriver.Chrome()
    browser.get(url)
    searchbar = browser.find_element_by_xpath('//*[@id="app"]/header/div[1]/div[3]/div[1]/form/div/div[1]/input')
    searchbar.send_keys(item)
    searchIcon = browser.find_element_by_xpath('//*[@id="app"]/header/div[1]/div[3]/div[1]/form/div/div[2]/button').click()
    deptSelect = browser.find_element_by_link_text(dept).click()
    products = browser.find_elements_by_class_name('item-cell')
    for items in products:
        if("VIDEO CARD" in items.text or "COMPONENTS" in items.text):
            continue
        elif("OUT OF STOCK" in items.text):
            inStock.append("Sold Out")
        elif("ADD TO CART" in items.text or "VIEW DETAILS" in items.text):
            inStock.append(items.text)
    browser.close()
    return inStock

def microcenter(item, dept):
    inStock = []
    url = "https://www.microcenter.com/"
    browser = webdriver.Chrome()
    browser.get(url)
    searchbar = browser.find_element_by_xpath('//*[@id="search-query"]')
    searchbar.send_keys(item)
    searchIcon = browser.find_element_by_xpath('//*[@id="searchForm"]/input[4]').click()
    currURL = browser.current_url
    currURL = currURL + '&myStore=false'
    browser.get(currURL)
    selectDept = browser.find_element_by_partial_link_text(dept).click()
    time.sleep(5)
    products = browser.find_elements_by_class_name('product_wrapper')
    for items in products:
        if("UNAVAILABLE ONLINE" in items.text):
            inStock.append("Sold Out")
        elif("ADD TO CART" in items.text or "IN STOCK" in items.text):
            inStock.append(items.text)
    browser.close()
    return(inStock)

def bhphotovideo(item, dept):
    inStock = []
    url = 'https://www.bhphotovideo.com/'
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(15)
    searchbar = browser.find_element_by_xpath('//*[@id="top-search-input"]')
    searchbar.send_keys(item)
    searchIcon = browser.find_element_by_xpath('//*[@id="header"]/section[2]/div[1]/form/p/button').click()
    selectDept = browser.find_element_by_partial_link_text(dept).click()
    time.sleep(5)
    products = browser.find_elements_by_class_name('product_19pae40ejOyj6V7StHfjYz ')
    for items in products:
        if("Notify When Available" in items.text):
            inStock.append("Sold Out")
        elif("Add to Cart" in items.text):
            inStock.append(items.text)
    browser.close()
    return(inStock)

def sendText(whereInStock):
    sender_email = "your.email@gmail.com" # Enter gmail username
    receiver_email = "phonenumber@cell.provider" # Enter your email to recieve notifications or your phone at you provider email forwarder find out what it is here: https://www.textsendr.com/emailsms.php
    password = "gmail password" # Enter gmail password make sure to allow insecure apps
    message = MIMEMultipart("alternative")
    message["Subject"] =  itemName + " Update!"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hello,
    Your item might be available at: """ + whereInStock + """
    Head over there and check it out!
    Good Luck!
    """

    html = """\
    <html>
      <body>
        <p>Hello,<br>
           Your item might be available at: """ + whereInStock + """"<br>
           Head over there and check it out! 
           Good Luck!
        </p>
      </body>
    </html>
    """
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
       )

if __name__ == "__main__":
    itemName = getItemName()
    while True:
        startTime = time.time()
        amazonStock = amazon(itemName, "Computer Graphics Cards")
        bestbuyStock = bestbuy(itemName)
        neweggStock = newegg(itemName, "Desktop Graphics Cards")
        microcenterStock = microcenter(itemName, "Computer Parts")
        bhStock = bhphotovideo(itemName, "Graphic Display Cards")
        for item in amazonStock:
            if ("Sold Out" != item) and (not amazonitem):
                amazonitem = True
        for item in bestbuyStock:
            if ("Sold Out" != item) and (not bestbuyitem):
                bestbuyitem = True
        for item in neweggStock:
            if ("Sold Out" != item) and (not neweggitem):
                neweggitem = True
        for item in microcenterStock:
            if ("Sold Out" != item) and (not microcenterStock):
                microcenteritem = True
        for item in bhStock:
            if ("Sold Out" != item) and (not bhStock):
                bhitem = True
        endTime = time.time()
        totalTime = (endTime - startTime)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if (amazonitem):
            sendText("Amazon")
            print("Check Amazon!")
        if (bestbuyitem):
            sendText("BestBuy")
            print("Check Best Buy!")
        if (neweggitem):
            sendText("Newegg")
            print("Check Newegg!")
        if (microcenteritem):
            sendText("Micro Center")
            print("Check Micro Center!")
        if (bhitem):
            sendText("B&H Photo and Video")
            print("Check B&H Photo and Video!")
        if (not amazonitem and not bestbuyitem and not neweggitem and not microcenteritem and not bhitem):
            print(dt_string + " - Sorry Item is Unavailable! Took " + str(round(totalTime, 2)) + " seconds!")
        amazonitem = False
        bestbuyitem = False
        neweggitem = False
        microcenteritem = False
        bhitem = False
        time.sleep(1800)