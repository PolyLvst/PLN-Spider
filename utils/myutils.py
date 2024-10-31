import logging
from selenium.webdriver.firefox.options import Options
import os
from selenium import webdriver

os.makedirs("logs", exist_ok=True)
os.makedirs("DataSnaphots", exist_ok=True)
os.makedirs("Document", exist_ok=True)
os.makedirs("TempImages", exist_ok=True)
os.makedirs("TempImages/rumah", exist_ok=True)
os.makedirs("TempImages/meteran", exist_ok=True)

class MyLoggerUtils:
    def __init__(self,log_file_path: str = "./logs/MyLoggerUtils.log") -> None:
        self.log_file_path = log_file_path

    def Log_write(self,text,stat='info'):
        """Available params ->>\ndebug,info,warning,error,critical"""
        text = str(text)
        log_filename = self.log_file_path
        logging.basicConfig(filename=log_filename, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        # Set the logging level for the selenium logger to WARNING
        logging.getLogger('selenium').setLevel(logging.WARNING)
        # Set the logging level for the webdriver logger to WARNING
        logging.getLogger('webdriver').setLevel(logging.WARNING)
        # Set the logging level, to prevent unwanted message showing in log file
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        print(text)
        text = text.replace('\n',' ')
        # Map the level string to a logging level constant
        level_map = {'debug': logging.DEBUG,
                    'info': logging.INFO,
                    'warning': logging.WARNING,
                    'error': logging.ERROR,
                    'critical': logging.CRITICAL}
        log_level = level_map.get(stat.lower(), logging.INFO)
        logging.log(log_level,text)

class WebScraperUtils:
    # ------------- Selenium web driver ------------ #
    def start_web_dv(profile="default"):
        options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        options.set_preference("general.useragent.override", user_agent)
        options.set_preference("network.trr.mode", 2)
        options.set_preference("network.trr.uri", "https://mozilla.cloudflare-dns.com/dns-query")
        profile_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'Profiles')
        # List all directories in the Profiles folder
        if profile:
            profiles = [d for d in os.listdir(profile_path) if os.path.isdir(os.path.join(profile_path, d))]
            path_prof = None 
            for path_p in profiles:
                if profile in path_p:
                    path_prof = os.path.join(profile_path, path_p)
                    break
            if path_prof:
                print(f"-- Using {profile} profile")
                options.add_argument("-profile")
                options.add_argument(path_prof)
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        return driver