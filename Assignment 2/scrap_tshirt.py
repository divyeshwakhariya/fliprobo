#Importing libraries
import requests
from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import shutil
from random import choice
from string import ascii_uppercase

#Defining parameters
ScrapUrl = "https://www.flipkart.com/clothing-and-accessories/topwear/tshirt/men-tshirt/pr?sid=clo,ash,ank,edy&otracker=categorytree&otracker=nmenu_sub_Men_0_T-Shirts"

#Adding chrome driver
ChromeDriver = webdriver.Chrome("chrome/chromedriver.exe")
ChromeDriver.get(ScrapUrl)
Content = ChromeDriver.page_source
Soup = BeautifulSoup(Content, "html.parser")

#Initiate data storage
ImageInfo = []
ImageReq = 100
ImageCount = 0

#looping multiple pages
for PageVisits in range(1,10):

    ShirtDiv = Soup.find_all('div', class_='IIdQZO _1SSAGr')

    #Loop through each Container
    for Container in ShirtDiv:

        #Checking for the image count
        if(ImageCount < ImageReq):
            
            image_tag = Container.findChildren('img')
            ImageInfo.append((image_tag[0]["src"], image_tag[0]["alt"]))
            ImageCount = ImageCount+1

        else:
            break

    if(ImageCount < ImageReq):

        #Getting number of buttons i.e. Next and Previous
        ButtonCount  = len(ChromeDriver.find_elements_by_xpath("//a[@class='_3fVaIS']"))

        #If there are two button with same class, it will click on Next button and if only single button it will click on Next only
        if ButtonCount > 1:
            SubmitButton = ChromeDriver.find_elements_by_xpath("//a[@class='_3fVaIS']")[1]
            SubmitButton.click()
        else:
            SubmitButton = ChromeDriver.find_elements_by_xpath("//a[@class='_3fVaIS']")[0]
            SubmitButton.click()
    else:
        break

    #Initializing sleep of 2 second
    sleep(2)

#Creating download function to download images            
def DownloadImage(Image):
    Response = requests.get(Image[0], stream=True)
    ImageName  = ''.join(choice(ascii_uppercase) for i in range(15))
    
    file = open("D:/DATASCIENCE/TshirtShirt/training/tshirts/{}.jpg".format(ImageName), 'wb')
    Response.raw.decode_content = True
    shutil.copyfileobj(Response.raw, file)
    del Response

for i in range(0, len(ImageInfo)):
    DownloadImage(ImageInfo[i])
