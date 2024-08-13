version___ = 'PLN Spider ACMT v1.0'
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl.drawing.image import Image
from datetime import datetime
from openpyxl import load_workbook
import json
import os
from time import time
from time import sleep
import requests
from utils import myutils

load_dotenv(verbose=True)
find_this = os.environ
URL = find_this['WEB_URL']
USER = find_this['USER_ACMT']
PASSWORD = find_this['PW_ACMT']
EXCEL_PATH = find_this['EXCEL_PATH_acmt']
ROW_AWAL = int(find_this['ROW_START_acmt'])
ROW_AKHIR = int(find_this['ROW_END_acmt'])
COL_ID = find_this['ID_COL_acmt']
COL_PHOTO = find_this['PHOTO_COL_acmt']
# -- Berapa kali untuk mencoba mencari foto saat internet tidak stabil
BANYAK_PERCOBAAN = int(find_this['BANYAK_PERCOBAAN'])
# -- Setting Foto --
desired_width = int(find_this['img_width_acmt'])
desired_height = int(find_this['img_height_acmt'])

# Sleep timer
sleep_retry_foto = 2

now__ = datetime.now()
now_time = now__.strftime('%d-%m-%Y_%H-%M-%S')
log_file_path = './logs/PLN-Spider-ACMT'+now_time+'.log'

class ExceptionTryRefreshing(Exception):
    pass

class ACMT:
    def __init__(self,driver):
        self.created_by = find_this['creator']
        self.MyLoggerUtils = myutils.MyLoggerUtils(log_file_path=log_file_path)
        self.driver = driver
        self.snapshots_folder = './DataSnapshots'
        self.temp_folder = "./TempImages/"
        self.cache_img = f"{self.snapshots_folder}/cache_img.json"
        self.ids_path = f"{self.snapshots_folder}/cached_ids.json"
        self.checkpoint_path = f'{self.snapshots_folder}/checkpoint.json'
        self.last_logout_time = 1
        with open(f"{self.snapshots_folder}/loglastrunpath.json","w") as f:
            json.dump({"log_path":log_file_path},f)

    def Log_write(self,text,stat='info'):
        return self.MyLoggerUtils.Log_write(text,stat=stat)
    
    def __repr__(self) -> str:
        return f'\x1b[1;96m>> Created by : {self.created_by}\n>> Github : https://github.com/PolyLvst\n\x1b[1;93m@ {version___}\x1b[0m'

    def input_login(self,user,passw,btn):
        user.click()
        user.send_keys(USER)
        passw.click()
        passw.send_keys(PASSWORD)
        input_captcha = self.driver.find_element('id',"x-auto-3-input")
        input_captcha.click()
        captcha = input("Input the captcha shown : ")
        input_captcha.send_keys(captcha)
        btn.click()

    def logout_akun(self):
        current_time = time()
        elapsed_time = current_time - self.last_logout_time
        self.Log_write(f"Time since last logout : {elapsed_time}s")
        if elapsed_time <= 30:
            self.Log_write("Logout cooldown ... [30s]","warning")
            for i in range(30,0,-1):
                sleep(1)
                if i%2 == 0:
                    print(f"\r[{i}] (-_-) zzZ ",end="")
                elif i%3 == 0:
                    print(f"\r[{i}] (^-^) Zzz ",end="")
                else:
                    print(f"\r[{i}] (-_-) zZz ",end="")
            print(f"\r[0] (UWU) Logging out ",end="")
            print("\n")
        try:
            element = WebDriverWait(self.driver,45).until(EC.presence_of_element_located((By.XPATH,"//div[@class='GCNLWM1ON'][contains(.,'Logout')]")))
            tombol_logout = self.driver.find_element(By.XPATH,"//div[@class='GCNLWM1ON'][contains(.,'Logout')]")
            tombol_logout.click()
            self.Log_write("Logged out ... ")
        except Exception:
            self.Log_write("Logout button not found","error")
            exit(1)

    def click_sidebar(self):
        try:
            # Overlay loading
            overlay = self.driver.find_element(By.CLASS_NAME, "GCNLWM1NBC")
            WebDriverWait(self.driver, 40).until(EC.invisibility_of_element_located((By.CLASS_NAME, "GCNLWM1NBC")))
        except Exception:
            self.Log_write("Great no overlay .. ")
        try:
            # Folder KCT info Baca KCT
            element = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//span[@class='GCNLWM1OLB'][contains(.,'Info Baca KCT')]")))
            informasi_TUL = self.driver.find_element(By.XPATH,"//span[@class='GCNLWM1OLB'][contains(.,'Info Baca KCT')]")
            informasi_TUL.click()
        except Exception:
            self.Log_write("Something went wrong [Sidebar not detected]")
            # exit(1)
            raise ExceptionTryRefreshing

    def search_pelanggan(self,id_pelanggan):
        try:
            input_pelanggan = self.driver.find_element('id',"x-auto-38-input")
            input_pelanggan.clear()
            input_pelanggan.send_keys(id_pelanggan)
        except Exception:
            self.Log_write("Input pelanggan not found","error")
            raise ExceptionTryRefreshing
        try:
            sleep(sleep_retry_foto)
            # tombol_cari = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/form/div/div[2]/div[1]/div/div/div[1]/div/div/div/div[2]/div[1]/div/div/div[1]/div/div[1]/fieldset/div/div/div/div[2]/div/table/tbody/tr[2]/td[2]/div/div/table/tbody/tr/td[1]')))
            tombol_cari = self.driver.find_element('xpath',"//div[@class='GCNLWM1ON'][contains(.,'Cari')]")
            tombol_cari.click()
        except Exception:
            try:
                element = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='GCNLWM1ON'][contains(.,'OK')]")))
                tombol_error_google = self.driver.find_element('xpath',"//div[@class='GCNLWM1ON'][contains(.,'OK')]")
                tombol_error_google.click()
                self.Log_write("Google gwt error closed","warning")
            except Exception:
                self.Log_write("Something wrong happens [search_pelanggan]","error")
            # //div[@class='GCNLWM1FQ'][contains(.,'Problem detected : com.google.gwt.user.client.rpc.StatusCodeException: 0')]
            # //div[@class='GCNLWM1ON'][contains(.,'OK')]
            # exit(1)
            raise ExceptionTryRefreshing

    def lihat_foto(self,id_pelanggan,nomer):
        try:
            actions = ActionChains(self.driver)
            foto_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,"//img[contains(@class,'gwt-Image')]")))
            foto = self.driver.find_element(By.XPATH,"//img[contains(@class,'gwt-Image')]")
            self.driver.execute_script("arguments[0].scrollIntoView();", foto)
            actions.move_to_element(foto).perform()
        except Exception:
            self.Log_write(f'--> ID : {id_pelanggan}')
            self.Log_write("--> Foto tidak tersedia","warning")
            return False
        trying = 1
        final_image_source = ''
        while True:
            self.Log_write(f'--> ID : {id_pelanggan}, Percobaan ke : {trying}')
            # will exit after +1 trying
            if trying > BANYAK_PERCOBAAN:
                # if trying >= BANYAK_PERCOBAAN+1:
                self.Log_write('--> Bad connection [Logout & Exit]','error')
                raise ExceptionTryRefreshing

            # Foto bawah
            img_element_1 = self.driver.find_element('xpath',"//img[contains(@class,'gwt-Image')]")
            image_source_1 = img_element_1.get_attribute("src")
            try:
                response = requests.get(image_source_1,timeout=3)
                if response.ok:
                    final_image_source = response
                    break
                else:
                    final_image_source = False
                    break
            except Exception:
                trying+=1
                self.search_pelanggan(id_pelanggan)
        return final_image_source

    def checkpoint(self,row,no,id_pel):
        checkpoint = self.checkpoint_path
        data = {}
        # with open(checkpoint,'r') as f:
        #     data = json.load(f)
        data.update({'row_awal':ROW_AWAL,'checkpoint':{'no':no,'row_checkpoint':row,'id':id_pel}})
        with open(checkpoint,'w') as f:
            json.dump(data,f)
            self.Log_write('Updated checkpoint ..')

    def ask_checkpoint(self):
        data = {}
        nomer = 1
        row_checkpoint = ROW_AWAL
        checkpoint = self.checkpoint_path
        folder_snapshots = self.snapshots_folder
        if not os.path.exists(folder_snapshots):
            os.mkdir(folder_snapshots)
        self.clean_old_files(folder_snapshots)
        if os.path.exists(checkpoint):
            self.Log_write('--> Checkpoint found, using value from checkpoint')
            with open(checkpoint,'r') as f:
                try:
                    data:dict = json.load(f)
                except Exception:
                    self.Log_write('No value detected, fallback default')
                    return nomer,row_checkpoint
            check_idx:dict = data['checkpoint']
            nomer = check_idx.get('no')
            row_checkpoint = check_idx.get('row_checkpoint')
            return nomer,row_checkpoint
        else:
            data = {'row_awal':ROW_AWAL,'checkpoint':{'no':1,'row_checkpoint':ROW_AWAL,'id':'first time run'}}
            with open(checkpoint,'w') as f:
                json.dump(data,f)
            self.Log_write('Init checkpoint ..')
            return nomer,row_checkpoint

    def get_cached_ids(self):
        ids_path = self.ids_path
        data = {}
        if os.path.exists(ids_path):
            self.Log_write("Using cached ids ..")
            with open(ids_path,"r") as f:
                data = json.load(f)
            return data
        workbook = load_workbook(EXCEL_PATH)
        worksheet = workbook.active
        end_row = ROW_AKHIR+1
        for row in range(ROW_AWAL,end_row):
            id_pelanggan = worksheet[f'{COL_ID}{row}']
            str_pelanggan = id_pelanggan.value
            data[f"no-{str_pelanggan}"] = {"str_pelanggan":str_pelanggan,
                                        "status_value":"Init_state"}
        with open(ids_path,"w") as f:
            json.dump(data,f)
        self.Log_write("Init cached ids ..")
        workbook.close()
        return data

    def update_cache_ids(self,no_id,status_given):
        "no_id = no-1"
        ids_path = self.ids_path
        data = {}
        if os.path.exists(ids_path):
            with open(ids_path,"r") as f:
                data = json.load(f)
            data[no_id]["status_value"] = status_given
            with open(ids_path,"w") as f:
                json.dump(data,f)
            self.Log_write("Status value updated ..")
        else:
            self.Log_write("Something wrong happens [cached_ids not found]","error")
            exit(1)

    def download_photo(self,source,cur_pos,status_value):
        cache_img = self.cache_img
        temp_folder = self.temp_folder
        response = source
        if source == False:
            image_path = "Tidak tersedia"
        else:
            image_name = f"image_{cur_pos}.jpg"  # You can change the file name logic as needed
            image_path = os.path.join(temp_folder, image_name)
            with open(image_path, "wb") as f:
                f.write(response.content)
        data = {}
        if os.path.exists(cache_img):
            with open(cache_img,"r") as f:
                data = json.load(f)
        with open(cache_img,"w") as f:
            data[cur_pos] = {"img":image_path,
                            "status_value":status_value}
            json.dump(data,f)
        self.Log_write("--> Cache img updated ..")

    def save_photo(self):
        self.Log_write("Saving photos from cache ..")
        cache_img = self.cache_img
        data = {}
        if os.path.exists(cache_img):
            with open(cache_img,"r") as f:
                data = json.load(f)
        else:
            self.Log_write("Something wrong [no cache img found]","error")
            exit(1)
        workbook = load_workbook(EXCEL_PATH)
        worksheet = workbook.active
        starts_row = ROW_AWAL
        for customer_id in data:
            self.Log_write(f"--> Saving {customer_id} ..")
            cur_pos = starts_row
            foto_cell=worksheet[f'{COL_PHOTO}{cur_pos}']
            image_path = data[customer_id]["img"]
            status_value = data[customer_id]["status_value"]
            if status_value == "False":
                pass
            else:
                img = Image(image_path)
                img.width = desired_width
                img.height = desired_height
                # add to worksheet and anchor next to cells
                worksheet.add_image(img, f'{COL_PHOTO}{cur_pos}')
            foto_cell.value = status_value
            starts_row += 1
        workbook.save(EXCEL_PATH)
        self.Log_write("--> Workbook updated!")
        workbook.close()

    def delete_temp(self):
        folder = self.temp_folder
        for file_img in os.listdir(folder):
            print(f"deleting -> {file_img}")
            os.remove(f"{folder}/{file_img}")
    
    def clean_old_files(path_to):
        max_age_seconds = 3 * 24 * 60 * 60
        old_files = []
        for file_path in os.listdir(path_to):
            file_path = os.path.join(path_to,file_path)
            file_stat = os.stat(file_path)
            current_time = time()
            # Calculate the age of the file in seconds
            file_age_seconds = current_time - file_stat.st_mtime
            # Compare the age with the maximum allowed age
            if file_age_seconds > max_age_seconds:
                # File is older than 3 days
                old_files.append(file_path)
        if not old_files:
            return
        print(f"Old files found in {path_to} ..")
        print("Use p for delete on prompt")
        cond = input(f"Delete all old files in ? {path_to} [y/n/p] ").lower()
        if cond == "n":
            print("No files deleted ..")
            return
        if cond != "y" and cond != "p":
            print("Invalid choice")
            exit(0)
        for file in old_files:
            # prompt mode if cond not "y"
            if cond != "y":
                inp = input(f"Delete {file} ? [y/n] ").lower()
                if inp == "n":
                    print(f"Skipping {file} ..")
                    continue
            # if cond == "y" then go delete all file without prompt
            os.remove(file)
            print(f"{file} has been deleted as it's more than 3 days old.","warning")

class SpiderACMT:
    def __init__(self):
        # use the name of your firefox profile
        self.driver = myutils.WebScraperUtils.start_web_dv(profile="default")
        self.acmt_crawler = ACMT(driver=self.driver)

    def run(self):
        while True:
            try:
                self.__main()
                self.__cleanup()
                exit()
            except Exception as e:
                self.acmt_crawler.Log_write(f"Got error : {e}")
                self.acmt_crawler.Log_write(f"\x1b[1;35m--> Relogin [Refreshing]\x1b[0m","warning")
                self.acmt_crawler.logout_akun()
                self.acmt_crawler.last_logout_time = time()
                continue

    def save_photo(self):
        self.acmt_crawler.save_photo()

    def delete_temp_photo(self):
        self.acmt_crawler.delete_temp()
    
    def test_run(self):
        print(f">> After testing done, you need to delete images in the {EXCEL_PATH} after test run")
        print(f">> Or the file might have duplicate image on top of other.")
        self.__main(stop_at_offset = 3)

    def delete_snapshots(self):
        folder_snapshots = self.acmt_crawler.snapshots_folder
        self.acmt_crawler.clean_old_files(folder_snapshots)

    def __main(self,stop_at_offset: int = 0):
        # Stop at offset 0 means it will stop at ROW_AKHIR if defined, it will stop at last checkpoint + stop_at_offset
        driver = self.driver
        acmt_crawler = self.acmt_crawler
        driver.get(URL)
        acmt_crawler.Log_write(str(acmt_crawler))
        # Overlay
        overlay = driver.find_element(By.CLASS_NAME, "blockOverlay")
        WebDriverWait(driver, 40).until(EC.invisibility_of_element_located((By.CLASS_NAME, "blockOverlay")))

        element = WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.ID, "x-auto-1-input")))
        input_login_user = driver.find_element('id',"x-auto-1-input")
        input_login_password = driver.find_element('id',"x-auto-2-input")
        button_login = driver.find_element('xpath',"//div[@class='GCNLWM1ON'][contains(.,'Login')]")
        if input_login_user and input_login_password:
            # sleep(5)
            acmt_crawler.input_login(input_login_user,input_login_password,button_login)
        else:
            acmt_crawler.Log_write('Something went wrong ! [User input not found]','error')
            driver.quit()
            exit(1)
        acmt_crawler.click_sidebar()
        acmt_crawler.Log_write('Logged in')
        nomer,row_checkpoint = acmt_crawler.ask_checkpoint()
        print(f">> Starting with id : {row_checkpoint}")
        cache_ids = acmt_crawler.get_cached_ids()
        if nomer == 1:
            splice_range = 0
        else:
            splice_range = nomer-1
        acmt_crawler.Log_write(f"\x1b[1;96m>> Total : {ROW_AKHIR-ROW_AWAL}\x1b[0m")
        # Convert the dictionary items to a list and slice it
        if stop_at_offset:
            items_list = list(cache_ids.items())[splice_range:splice_range+stop_at_offset]
        else:
            items_list = list(cache_ids.items())[splice_range:]
        # Gets the latest section of ids, from checkpoint to the end
        cache_ids = dict(items_list)
        for row in cache_ids:
            foto_status = cache_ids[row]["status_value"]
            str_pelanggan = cache_ids[row]["str_pelanggan"]
            if foto_status == 'True':
                acmt_crawler.Log_write(f'No.{nomer} Foto terdeteksi [Skipping] . . . ID : {str_pelanggan}')
                nomer+=1
                continue
            acmt_crawler.Log_write(f'No.{nomer} Mencari foto . . .')
            acmt_crawler.search_pelanggan(str_pelanggan)
            data_foto = acmt_crawler.lihat_foto(str_pelanggan,nomer)
            if data_foto == False:
                acmt_crawler.Log_write("--> Cache img updated [No image] ..")
                acmt_crawler.download_photo(data_foto,row,"False")
                acmt_crawler.update_cache_ids(row,"False")
            else:
                acmt_crawler.download_photo(data_foto,row,"True")
                acmt_crawler.update_cache_ids(row,"True")
            current_time = datetime.now().time()
            # Extract hour, minute, and second components
            hour = current_time.hour
            minute = current_time.minute
            second = current_time.second
            # Log_write("--> Workbook updated!")
            acmt_crawler.Log_write(f'--> {hour}:{minute}:{second}')
            acmt_crawler.checkpoint(row,nomer,str_pelanggan)
            acmt_crawler.Log_write(f"\x1b[1;96m>> Total left : {ROW_AKHIR-ROW_AWAL-nomer}\x1b[0m")
            nomer+=1
        acmt_crawler.save_photo()
        acmt_crawler.logout_akun()
        acmt_crawler.Log_write('Webdriver flush\nExiting . . .')
        driver.quit()
        acmt_crawler.Log_write('\x1b[1;92mAll done ...')
        acmt_crawler.Log_write(str(acmt_crawler))

    def __cleanup(self):
        acmt_crawler.Log_write('\x1b[1;92mCleaning up temp images ...')
        acmt_crawler = self.acmt_crawler
        acmt_crawler.delete_temp()

if __name__ == '__main__':
    main = SpiderACMT()
    # main.run()
    exit(1)
    # Uncomment to use individual functionality you need
    # main.save_photo()
    # main.delete_temp_photo()
    # main.test_run()