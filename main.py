version___ = 'PLN Spider v1.0'
# Formerly known as Auto PLN 0.4
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from openpyxl.drawing.image import Image
from selenium import webdriver
from datetime import datetime
from openpyxl import load_workbook
from openpyxl import utils
from time import sleep
import os
import base64

load_dotenv()
find_this = os.environ
URL = find_this['URL']
USER = find_this['USER']
PASSWORD = find_this['PASSWORD']
EXCEL_PATH = find_this['EXCEL_PATH']
ROW_AWAL = find_this['ROW_AWAL']
ROW_AKHIR = find_this['ROW_AKHIR']
COL_ID = find_this['COL_ID']
COL_PHOTO = find_this['COL_PHOTO']
BANYAK_PERCOBAAN = find_this['BANYAK_PERCOBAAN'] # -- Berapa kali untuk mencoba mencari foto saat internet tidak stabil
# -- Setting Foto --
desired_width = find_this['desired_width']
desired_height = find_this['desired_height']

# Convert huruf menjadi angka untuk index pelanggan
col_id_num= utils.column_index_from_string(COL_ID)-1
col_photo_num = utils.column_index_from_string(COL_PHOTO)-1
def show_vers():
    created_by = find_this['creator']
    print(f'\x1b[1;96m>> Created by : {created_by}\n>> Github : https://github.com/PolyLvst\n\x1b[1;93m@ {version___}\x1b[0m\n')
# ------------- Selenium web driver ------------ #
def start_web_dv():
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    options.set_preference("general.useragent.override", user_agent)
    options.set_preference("network.trr.mode", 2)
    options.set_preference("network.trr.uri", "https://mozilla.cloudflare-dns.com/dns-query")
    driver = webdriver.Firefox(options=options)
    return driver

def input_login():
    input_login_user.send_keys(USER)
    input_login_password.send_keys(PASSWORD)
    button_login.click()

def click_sidebar():
    # Folder MONITORING DAN LAPORAN
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'x-widget-8_f-14')))
    sidebar_tusbung_parent = driver.find_element(By.ID,'x-widget-8_f-14')
    sidebar_tusbung = sidebar_tusbung_parent.find_element(By.CSS_SELECTOR,'img.GCMY5A5CFOB')
    sidebar_tusbung.click()
    # Document Info Pelaksanaan TUL
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'x-widget-8_m-19')))
    informasi_TUL_parent = sidebar_tusbung_parent.find_element(By.ID,'x-widget-8_m-19')
    informasi_TUL = informasi_TUL_parent.find_element(By.CSS_SELECTOR,'img.GCMY5A5CEOB')
    informasi_TUL.click()

def search_pelanggan(id_pelanggan):
    input_pelanggan = driver.find_element('id','x-widget-19-input')
    input_pelanggan.clear()
    input_pelanggan.send_keys(id_pelanggan)
    tombol_cari = driver.find_element('xpath','/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[1]/div/div[5]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[1]/img')
    tombol_cari.click()
    element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[4]/div[1]/div/table/tbody/tr/td[1]/div')))
    sleep(3)
    filter_tahun = driver.find_element('xpath','/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[4]/div[1]/div/table/tbody/tr/td[1]/div')
    attribut_filter = filter_tahun.get_attribute("class")
    if "GCMY5A5CEIC" in attribut_filter:
        pass
    else:
        sleep(2)
        filter_tahun.click()
        filter_tahun.click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'table.GCMY5A5CMIC')))
    table_element = driver.find_element(By.CSS_SELECTOR,'table.GCMY5A5CMIC')
    tahun_ = table_element.find_elements(By.TAG_NAME,'tr')
    tahun_terbaru = tahun_[0]
    actions.move_to_element(tahun_terbaru).click().perform()

def lihat_foto(id_pelanggan):
    img_button = driver.find_element('xpath','/html/body/div[2]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div/div/div[1]/div/div[3]/div/div[3]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[1]/img')
    img_button.click()
    # Wait for the image element to be visible
    trying = 1
    final_image_source = ''
    while True:
        print(f'--> ID : {id_pelanggan}, Percobaan ke : {trying}')
        if trying > BANYAK_PERCOBAAN:
            if trying >= BANYAK_PERCOBAAN+1:
                print('--> Bad connection [Exit]')
                exit()
            print('--> Bad connection [Trying one last time again]')
        try:
            element = WebDriverWait(driver,40).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]')))
        except TimeoutException as e:
            print(f"--> Timeout exception occurred: [Waiting] trying again")
            sleep(5)
            element = WebDriverWait(driver,40).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[5]/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]')))
        # Pojok kiri bawah
        img_div_parent = driver.find_element('xpath','/html/body/div[5]/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]')
        img_element_1 = img_div_parent.find_element(By.CSS_SELECTOR,'img.gwt-Image')
        # Pojok kanan bawah
        img_div_parent = driver.find_element('xpath','/html/body/div[5]/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[2]/div[2]/div[1]')
        img_element_2 = img_div_parent.find_element(By.CSS_SELECTOR,'img.gwt-Image')
        # Pojok kiri atas
        img_div_parent = driver.find_element('xpath','/html/body/div[5]/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[1]')
        img_element_3 = img_div_parent.find_element(By.CSS_SELECTOR,'img.gwt-Image')
        # Pojok kanan atas
        img_div_parent = driver.find_element('xpath','/html/body/div[5]/div[2]/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[1]')
        img_element_4 = img_div_parent.find_element(By.CSS_SELECTOR,'img.gwt-Image')

        wait_src = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        image_source_1 = img_element_1.get_attribute("src")
        image_source_2 = img_element_2.get_attribute("src")
        image_source_3 = img_element_3.get_attribute("src")
        image_source_4 = img_element_4.get_attribute("src")
        if image_source_1 and image_source_2 and image_source_3 and image_source_4:
            if check_photo(image_source_1) == True:
                print('--> Menggunakan foto pojok kiri bawah')
                final_image_source = image_source_1
                break
            elif check_photo(image_source_2) == True:
                print('--> Menggunakan foto pojok kanan bawah')
                final_image_source = image_source_2
                break
            elif check_photo(image_source_3) == True:
                print('--> Menggunakan foto pojok kiri atas')
                final_image_source = image_source_3
                break
            elif check_photo(image_source_4) == True:
                print('--> Menggunakan foto pojok kanan atas')
                final_image_source = image_source_4
                break
            else:
                print('--> Something went wrong')
                exit()
        else:
            sleep(5)
        trying+=1
        
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/div/div/div/div[2]")))
    tombol_close_parent = driver.find_element('xpath','/html/body/div[5]/div[1]/div/div/div/div[2]')
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.GCMY5A5CCP.GCMY5A5CIK.GCMY5A5CHEC")))
    wait_tombol = WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'GCMY5A5CJJ')))
    try:
        tombol_close = tombol_close_parent.find_element(By.CSS_SELECTOR,'div.GCMY5A5CCP.GCMY5A5CIK.GCMY5A5CHEC')
        tombol_close.click()
    except ElementClickInterceptedException as e:
        # Handle the exception when the click is not clickable
        print(f"--> Click action failed: [Waiting and trying again]")
        sleep(5)
        tombol_close = tombol_close_parent.find_element(By.CSS_SELECTOR,'div.GCMY5A5CCP.GCMY5A5CIK.GCMY5A5CHEC')
        tombol_close.click()
    return final_image_source

def check_photo(source):
    data_url = source
    # Extract the base64-encoded image data from the Data URL
    image_data = data_url.split(",")[1]
    if image_data == base64_foto_tidak_tersedia:
        return False
    else:
        return True

def save_photo(source,cur_pos):
    data_url = source
    # Extract the base64-encoded image data from the Data URL
    image_data = data_url.split(",")[1]
    # Decode the base64 data into bytes
    image_bytes = base64.b64decode(image_data)
    image_format = data_url.split(";")[0].split(":")[1].split("/")[1]
    # Save the image to a file
    image_path = f"./TempImages/tempimage.{image_format}"
    with open(image_path, "wb") as file:
        file.write(image_bytes)

    img = Image(image_path)
    img.width = desired_width
    img.height = desired_height
    # add to worksheet and anchor next to cells
    worksheet.add_image(img, f'{COL_PHOTO}{cur_pos}')
    return 'True'

def check_folders():
    pass

# ------------------- MAIN PROGRAM ------------------
# Dapat juga berfungsi sebagai module
if __name__ == '__main__':
    show_vers()
    check_folders()
    driver = start_web_dv()
    actions = ActionChains(driver)
    driver.get(URL)
    element = WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.GCMY5A5CFN')))
    input_login_user = driver.find_element('id','x-widget-1-input')
    input_login_password = driver.find_element('id','x-widget-2-input')
    button_login = driver.find_element('xpath','/html/body/div[3]/div[2]/div[1]/div/div/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[1]/img')
    if input_login_user and input_login_password:
        input_login()
        click_sidebar()
        print('Logged in')
    else:
        print('Something went wrong ! [User input not found]')
        driver.quit()
        exit()

    excel_file_path = EXCEL_PATH
    nomer = 0
    base64_foto_tidak_tersedia = find_this['base_64_foto_tidak_tersedia']
    for row in range(ROW_AWAL,ROW_AKHIR):
        nomer+=1
        workbook = load_workbook(excel_file_path)
        worksheet = workbook.active
        id_pelanggan = worksheet[f'{COL_ID}{row}']
        str_pelanggan = id_pelanggan.value
        foto_cell=worksheet[f'{COL_PHOTO}{row}']
        if foto_cell.value == 'True':
            print(f'No.{nomer} Foto terdeteksi di excel [Skipping] . . . ID : {str_pelanggan}')
            continue
        search_pelanggan(str_pelanggan)
        current_time = datetime.now().time()
        # Extract hour, minute, and second components
        hour = current_time.hour
        minute = current_time.minute
        second = current_time.second
        print(f'No.{nomer} Mencari foto . . .')
        data_foto = lihat_foto(str_pelanggan)
        foto_cell.value = save_photo(data_foto,row)
        try:
            workbook.save(EXCEL_PATH)
            print("--> Workbook updated!")
            print(f'--> {hour}:{minute}:{second}')
            workbook.close()
        except Exception as e:
            print(f"An error occurred while saving the workbook: {e}")

    driver.quit()
    print('Webdriver flush\nExiting . . .')
    print('\x1b[1;92mAll done ...')
    show_vers()
    exit()
