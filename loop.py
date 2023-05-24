#import all needed libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

#chrome as main webdriver, also set to not close after opening (detach)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

#create 7 empty lists where data will be stored
name = []
temp = []
weath = []
humi = []
press = []
vis = []
uv = []

#open website, bypass cookies
driver.get("https://weather.com/en-GB/weather/today/l/UKXX0085:1:UK")
time.sleep(2)
btn_rej = driver.find_element(By.CLASS_NAME, "truste-button3").click()
time.sleep(2)

#ask user to choose in which unit show temperature
unit = input("Would you like to see temperature in °C or °F: ")

#click button to change temperature
btn_unit = driver.find_element(By.CLASS_NAME, "LanguageSelector--LanguageSelectorStatus--2KFS4").click()

#make functions to set temperature to °C or °F
def c():
    btn_c = driver.find_element(By.ID, "UnitSelectorTabs-tab_1").click()

def f():
    btn_f = driver.find_element(By.ID, "UnitSelectorTabs-tab_0").click()

#call function based on user input
if unit.lower() == "c":
    c()
elif unit.lower() == "f":
    f()
else:
    print("Enter C/c or F/f")
    driver.quit()
    exit()
    
#loop, so you can check temperature of more cities
while True:
    city = input("Enter City name you would like to know current weather details (or 'q' to quit): ")
    if city.lower() == "q":
        driver.quit()
        break
    
    #enter sub-website with given city name
    time.sleep(1)
    search_field = driver.find_element(By.CSS_SELECTOR, ".SearchInput--InputField--1UoCv.Search--inputClass--1FEhl")
    time.sleep(1)
    search_field.send_keys(city)
    time.sleep(2)
    try:
        btn_loc = driver.find_element(By.ID, "LocationSearch_listbox-0").click()
    except:
        print("Wrong city name")
        driver.quit()
        break

    time.sleep(2)

    #find all data based on css/class...
    name.append(driver.find_element(By.CLASS_NAME, "CurrentConditions--location--1YWj_").text)
    temp.append(driver.find_element(By.CLASS_NAME, "CurrentConditions--tempValue--MHmYY").text)
    weath.append(driver.find_element(By.CLASS_NAME, "CurrentConditions--phraseValue--mZC_p").text)
    humi.append(driver.find_element(By.CSS_SELECTOR, 'span[data-testid="PercentageValue"]').text)
    press.append(driver.find_element(By.CSS_SELECTOR, 'span[data-testid="PressureValue"].Pressure--pressureWrapper--3SCLm.undefined').text.split(" ")[0])
    vis.append(driver.find_element(By.CSS_SELECTOR, 'span[data-testid="VisibilityValue"]').text.split(" ")[0])
    uv.append(driver.find_element(By.CSS_SELECTOR, 'span[data-testid="UVIndexValue"]').text.split(" ")[0])

#create dataset with all gathered infos
dataset = {
    "City": name,
    "Temperature": temp,
    "Climate": weath,
    "Humidity": humi,
    "Pressure (mb)": press,
    "Visibility (km)": vis,
    "UV Index (10)": uv
}

#turn dataset into csv..
df = pd.DataFrame(dataset)
df.to_csv("weather.csv", index=True, encoding='utf-8-sig')