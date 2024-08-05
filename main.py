from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import keyboard
import openpyxl
from openpyxl import load_workbook
from datetime import datetime
from JobDataExcelManager import JobDataExcelManager
from PromptEngineer import PromptEngineer
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
title = ["Platsbanken - Sök lediga jobb - Arbetsförmedlingen", ""]
driver.get("https://arbetsformedlingen.se/platsbanken/")
print(driver.title)
driver.implicitly_wait(10)
yrke = ["svetsare", "automationsingenjör", "Plåtslagare","Truckförare","Valsare","Bockare","Industrirörmontör","Montör","Underhållsmekaniker","Servicetekniker"]
yrkeIndex = 7
search_input_element = driver.find_element("css selector", "#search_input")
search_input_element.send_keys(yrke[yrkeIndex])
search_input_element.send_keys(Keys.RETURN)
#################################################################################
# Get the current month and year
current_month_year = datetime.now().strftime("%Y_%m")

# Construct the file name with the current month and year
file_name = f"job_data_{current_month_year}.xlsx"

# Create an instance of the JobDataExcelManager class
excel_manager = JobDataExcelManager(file_name)
my_Prompt_engineer = PromptEngineer()

###################################################################################
def GetAntalAnnoser():
    try:
        #element = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CSS_SELECTOR,'h2[aria-label='))
        Annonser_element = driver.find_element("xpath","/html/body/div[1]/div[2]/div[7]/div/div/main/div[3]/div/div/div[2]/div/div/div/div/div[2]/div[1]/pb-root/div/pb-page-search/div[2]/pb-feature-tabs/div[2]/pb-section-search-result/div/section/div/div/div/pb-section-search-metadata/div/pb-feature-search-result-number/h2/strong")
        Jobb_element = driver.find_element("xpath","/html/body/div[1]/div[2]/div[7]/div/div/main/div[3]/div/div/div[2]/div/div/div/div/div[2]/div[1]/pb-root/div/pb-page-search/div[2]/pb-feature-tabs/div[2]/pb-section-search-result/div/section/div/div/div/pb-section-search-metadata/div/pb-feature-search-result-number/h2/span")
        # Get the text from the element
        print(f"Yrke vald {yrke[yrkeIndex]}")
        text = [Annonser_element.text,Jobb_element.text]
        for i in range(len(text)):
            match = re.search(r'\b(\d+)\b', text[i])
            temptext = ["Annonser","Jobb"]
            # Check if a match is found
            if match:
                extracted_value = int(match.group(1))
                print(f"Antal {temptext[i]}: {extracted_value}")
            else:
                print(f"No integer value found in the input string {i + 1}.")

    finally:
        time.sleep(3)


def GenerateChatGPTPrompt(företag_name,arbetsroll):
    print("Prompt Generated")


def GetAndSetInfoAnnosPage():
    driver.current_url
    print(driver.current_url)
    ################################################### jobb title
    try:

        title_element = driver.find_element(By.XPATH,'//h1[contains(@data-read-assistance-title,"")]')

        # Extract the text of the title
        title_text = title_element.text

        # Print the extracted title
        print("Jobb Title:", title_text)
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("Jobb Title: Element not found. Exiting GetAndSetInfoAnnosPage function.")
        return 1
    ################################################### företag namn
    try:
        # pb-company-name
        # Locate the <div> element using its attribute values
        div_element = driver.find_element(By.CSS_SELECTOR,"#pb-company-name")
        #driver.find_element(By.XPATH, '//*[@id="pb-company-name"]')

        # Extract the text content of the <div> element
        företag_name = div_element.text

        # Print the extracted text content
        print("Företags namn:", företag_name)
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("Företags namn: Element not found. Exiting GetAndSetInfoAnnosPage function.")
        return 1
    ############################################################# arbetsroll
    try:
        # Locate the <h3> element using its attribute values
        arbetsroll_element = driver.find_element(By.XPATH, '//*[@id="pb-job-role"]')

        # Extract the text content of the <h3> element
        arbetsroll = arbetsroll_element.text

        # Print the extracted text content
        print("Arbetsroll:", arbetsroll)
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("Arbetsroll: Element not found. Exiting GetAndSetInfoAnnosPage function.")
        return 1
    ################################################# kommun
    try:
        # Locate the <h3> element using its attribute values
        h3_element = driver.find_element(By.XPATH, '//*[@id="pb-job-location"]')

        # Extract the text content of the <h3> element
        text_content = h3_element.text

        # Split the text content by ':', and get the second part (after the colon)
        Kommun = text_content.split(':')[-1].strip()

        # Print the extracted location
        print("Kommun:", Kommun)
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("Kommun: Element not found. Exiting GetAndSetInfoAnnosPage function.")
        return 1
    ################################################# annons id
    try:
        h2_element = driver.find_element(By.XPATH, '//pb-section-job-about//div//h2[1]')

        # Extract the text content of the <h2> element
        annons_id_text = h2_element.text

        # Extract the numeric part from the text (assuming it is always a number)
        annons_id = ''.join(filter(str.isdigit, annons_id_text))

        # Print the extracted value
        print("Annons-Id:", annons_id)
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("Annons-Id: Element not found. Exiting GetAndSetInfoAnnosPage function.")
        return 1
    ############################# kommun och län

    current_date = datetime.now().strftime('%Y-%m-%d')
    print(current_date)
    datum = current_date
    # Saving the workbook to a file
    data = [driver.current_url, title_text, företag_name, arbetsroll, Kommun, annons_id,datum]

    # Add the data to the sheet
    excel_manager.add_data(data)

    # Save the workbook to a file with the current month and year in the name
    excel_manager.save_workbook()
    my_Prompt_engineer.GeneratePrompt(företag_name,arbetsroll)

def find_element_with_relative_xpath(driver, parent_class, tag_name):
    xpath = f"//*[contains(@class, '{parent_class}')]//{tag_name}"
    element = driver.find_element(By.XPATH, xpath)
    return element


def get_text_from_job_main_content(url):
    try:
        # Navigera till sidan
        driver.get(url)

        # Hämta elementet med CSS-selektorn
        element = driver.find_element(By.CSS_SELECTOR,
                                      "#pb-root > pb-page-job > div > section > div > div.jobb-container.container > div:nth-child(2) > section > pb-section-job-main-content > div")

        # Hämta texten från elementet
        text = element.text
        return text
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("Element not found. get_text_from_job_main_content failed")
        return 1
def get_arbetsroll_from_job_main_content(url):
    try:
        # Locate the <h3> element using its attribute values
        arbetsroll_element = driver.find_element(By.XPATH, '//*[@id="pb-job-role"]')

        return arbetsroll_element.text
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("Arbetsroll: Element not found. Exiting GetAndSetInfoAnnosPage function.")
        return 1
def get_företags_namn_from_main_content(url):
    try:
        # pb-company-name
        # Locate the <div> element using its attribute values
        div_element = driver.find_element(By.CSS_SELECTOR, "#pb-company-name")
        # driver.find_element(By.XPATH, '//*[@id="pb-company-name"]')

        # Extract the text content of the <div> element
        företag_name = div_element.text

        return företag_name
    except NoSuchElementException:
        # Handle the case where the element is not found
        print("get Företags namn: Element not found. existing get_företags_namn_from_main_content")
        return 1

ordlista = [
    "Allvarlig", "Aktsam", "Alert", "Ambitiös", "Anpassningsbar", "Ansvarsfull",
    "Arbetsam", "Banbrytande", "Behärskad", "Beskyddande", "Bestämd", "Diplomatisk",
    "Disciplinerad", "Diskret", "Driven", "Dynamisk", "Effektiv", "Eftertänksam",
    "Ekonomisk", "Energisk", "Entusiastisk", "Envis", "Erfaren", "Exceptionell",
    "Expert", "Flexibel", "Följsam", "Försiktig", "Genomtänkt", "Glad", "Grundlig",
    "Human", "Ihärdig", "Impulsiv", "Initiativtagande", "Innovativ", "Insiktsfull",
    "Karismatisk", "Klarsynt", "Klok", "Kompetent", "Konsekvent", "Kreativ",
    "Kunnig", "Kvalitetsmedveten", "Kvicktänkt", "Känslig", "Lojal", "Lugn",
    "Lyhörd", "Lättsam", "Medmänsklig", "Metodisk", "Mjuk", "Modig", "Motiverad",
    "Mottaglig", "Målinriktad", "Mångsidig", "Noggrann", "Obeveklig", "Objektiv",
    "Omsorgsfull", "Ordningsam", "Organiserad", "Orädd", "Positiv", "Praktisk",
    "Pratsam", "Prestigelös", "Proffsig", "Punktlig", "Pålitlig", "Rationell",
    "Realistisk", "Resultatinriktad", "Rolig", "Rörlig", "Saklig", "Samarbetsvillig",
    "Serviceminded", "Skarp", "Smart", "Snabb", "Självgående", "Självständig",
    "Självsäker", "Stark", "Strukturerad", "Stresstålig", "Stödjande", "Trovärdig",
    "Taktisk", "Tuff", "Tålmodig", "Unik", "Uppriktig", "Uppskattande", "Uthållig",
    "Utåtriktad", "Vaksam", "Vaken", "Vältränad", "Äventyrlig", "Ödmjuk", "Öppen","tekniskt intresse","resultatinriktad"

]
matchande_nyckelord = []
def Identifiera_nyckelord(text,keywords):
    matchande_nyckelord = []  # Lista för att lagra matchande nyckelord

    for keyword in keywords:
        matches = re.finditer(keyword, text, flags=re.IGNORECASE)
        for match in matches:
            matchande_nyckelord.append(keyword)
            print(f"Keyword '{keyword}' found at position {match.start()}-{match.end()}")
    #for nyckelord in matchande_nyckelord:
    #print(f"skriv ett personligt brev baserad på egenskaper {matchande_nyckelord}")
    return matchande_nyckelord


GetAntalAnnoser()

while True:
        if keyboard.is_pressed('F8'):
            print("F8 is pressed!")
            GetAndSetInfoAnnosPage()
        if keyboard.is_pressed('F10'):
            print("F10 is pressed!")
            select = 2
            TempFöretagsNamn = get_företags_namn_from_main_content(driver.current_url)
            Temptext = get_text_from_job_main_content(driver.current_url)
            TempArbetsroll = get_arbetsroll_from_job_main_content(driver.current_url)
            #print(Temptext)
            matchande_nyckelord = Identifiera_nyckelord(Temptext,ordlista)
            #print(f"skriv ett personligt brev för arbetsrollen {TempArbetsroll} och att jag innehar dessa egenskaper {matchande_nyckelord}")
            #print(f"vad kan en {TempArbetsroll} göra och vilka uppgifter gör dom")
            #prompt till chatgpt
            if select == 1:
                print(f"Snälla hjälp mig att skriva ett riktat följebrev för rollen {TempFöretagsNamn} och rollen {TempArbetsroll} ,"
                  " som framhäver mitt intresse för att gå med i företaget och hur mina kunskaper och erfarenheter gör mig"
                  " till en stark kandidat. Här är några viktiga punkter om min bakgrund och motivation för att söka tjänsten:"
                  f" här är mitt personliga brev som beskriv mina Kvalifikationer: {my_Prompt_engineer.personligt_brev} , [ Skäl till intresse för företaget] "
                  "och [Exempel på kompetens och erfarenheter som ligger i linje med företagets värderingar].")
            if select == 2:
                print(f"hej detta är mitt personliga brev {my_Prompt_engineer.personligt_brev}. och här är jobbannosen texten {Temptext} för arbetsrollen {TempArbetsroll}."
                      f" och att jag innehar dessa egenskaper {matchande_nyckelord} baserat på denna infon kan du anpassa mitt personliga brev till annos texten ?")



time.sleep(15)
#driver.quit()