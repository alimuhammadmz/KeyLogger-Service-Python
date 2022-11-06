import smtplib, ssl
import configparser
from pynput import keyboard

"""
REPRESENTATION:
+ = pressed
- = released
"""

def generateAlert():
    config_file = configparser.ConfigParser()

    config_file.read("configurations.ini")  # READ CONFIG FILE
    SENDER = config_file["FTPSettings"]["senderEmail"]
    PASSWORD = config_file["FTPSettings"]["senderPassword"]
    RECIEVER = config_file["FTPSettings"]["receiverEmail"]
    SMTP_SERVER = config_file["FTPSettings"]["smtp_server"]
    TEXT = config_file["Content"]["mailContent"]
    TEXT = TEXT.replace('\\n', '\n')

    port = 465
    SUBJECT = "ALERT: Monitoring Exitted"

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, port, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIEVER, message)

def listenerExitted():
    print("Listener exited!")

def onKeyPress(key):
    try:
        print("+ '" + format(key.char) + "'")
    except:
        if AttributeError:
            print("+ FunctionKey")

def onKeyRelease(key):
    try:
        print("- '" + format(key.char) + "'")
    except:
        if (key == keyboard.Key.end):
            print("Exitted")
            generateAlert()

            return False
        if AttributeError:
            print("- FunctionKey")

with keyboard.Listener(
        on_press=onKeyPress,
        on_release=onKeyRelease) as listener:
    listener.join()


