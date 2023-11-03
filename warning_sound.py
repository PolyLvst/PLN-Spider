from playsound import playsound
import threading
from datetime import datetime
import msvcrt
import os

def play_warning_sound():
    playsound(soft_sound)
    playsound(medium_sound)
    while True:
        playsound(security_alarm_sound)
        for _ in range(0,5):
            playsound(warning_sound)
        playsound(warning_bouncy2_sound)
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

print(f"Program failed [{datetime.now()}] ... ")
print("Something went wrong happen ... ")
print("Press SPACE to stop ... ")
print("Press ESC to stop ... ")
print("########### SPACE/ESC -> STOP ###########")
while True:
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b' ' or key == b'\x1b':  # Check if the spacebar is pressed
            print(f"Stopping warning alarm at [{datetime.now()}].")
            # exit_event.set()
            sound_thread.join(timeout=0.2)
            exit(0)