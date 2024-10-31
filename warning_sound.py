import logging
from playsound import playsound
import threading
from datetime import datetime
import msvcrt
import json
import os

if os.path.exists("./DataSnapshots/loglastrunpath.json"):
    with open("./DataSnapshots/loglastrunpath.json","r") as f:
        log_file_path = json.load(f)["log_path"]
else:
    now__ = datetime.now()
    now_time = now__.strftime('%d-%m-%Y_%H-%M-%S')
    log_file_path = './logs/PLN-Spider-'+now_time+'.log'

def Log_write(text,stat='info'):
    """Available params ->>\ndebug,info,warning,error,critical"""
    text = str(text)
    log_filename = log_file_path
    # We want to append to existing logs for this warning
    # So we use file mode a for append
    logging.basicConfig(filename=log_filename, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
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

def play_warning_sound():
    # playsound(soft_sound)
    # playsound(medium_sound)
    while True:
        for _ in range(0,5):
            playsound(warning_sound)
        playsound(warning_bouncy2_sound)
        playsound(security_alarm_sound)
        # playsound(warning_bouncy_sound)
        playsound(honk_alarm_sound)
        # playsound(alarm_sound)

curdir = os.getcwd().replace("\practice","")
soft_sound = os.path.join(curdir,R"assets\sounds\soft-alarm.mp3")
medium_sound = os.path.join(curdir,R"assets\sounds\medium-alarm.mp3")
security_alarm_sound = os.path.join(curdir,R"assets\sounds\security-alarm.mp3")

warning_bouncy2_sound = os.path.join(curdir,R"assets\sounds\warning-bouncy-2.mp3")
warning_sound = os.path.join(curdir,R"assets\sounds\warning-sound.mp3")
# warning_bouncy_sound = os.path.join(curdir,R"assets\sounds\warning-bouncy.mp3")

# alarm_sound = os.path.join(curdir,R"assets\sounds\alarm.mp3")
honk_alarm_sound = os.path.join(curdir,R"assets\sounds\honk-alarm-repeat.mp3")

sound_thread = threading.Thread(target=play_warning_sound,daemon=True)
sound_thread.start()

Log_write(f"Program failed [{datetime.now()}] ... ")
Log_write("Something went wrong happen ... ")
Log_write("Press SPACE to stop ... ")
Log_write("Press ESC to stop ... ")
Log_write("########### SPACE/ESC -> STOP ###########")
while True:
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b' ' or key == b'\x1b':  # Check if the spacebar is pressed
            Log_write(f"Stopping warning alarm at [{datetime.now()}].")
            # exit_event.set()
            sound_thread.join(timeout=0.2)
            exit(0)