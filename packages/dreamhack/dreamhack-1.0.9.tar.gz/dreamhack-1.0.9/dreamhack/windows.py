class windows():

  @staticmethod
  def run_as_admin():
    import pyuac
    if not pyuac.isUserAdmin():
      pyuac.runAsAdmin()

  @staticmethod
  def block_mouse_input(on): #type:ignore
    import ctypes
    try:
      ctypes.windll.user32.BlockInput(on) #type:ignore
    except Exception as e:
      return -1, e
    else:
      return 1, on

  @staticmethod
  def block_keyboard_key(key): #type:ignore
    import keyboard #type:ignore
    try:
      keyboard.block_key(key) #type:ignore
    except Exception:
      raise Exception('Invalid Keyboard Key.') #type:ignore
    else:
      return key

  
  @staticmethod
  def unblock_keyboard_key(key): #type:ignore
    import keyboard #type:ignore
    try:
      keyboard.unblock_key(key) #type:ignore
    except Exception:
      raise Exception('Invalid Keyboard Key.') #type:ignore
    else:
      return key

  @staticmethod
  def disable_all_keyboard_keys(): #type:ignore
    keys_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#"
    for key in keys_list:
      windows.block_keyboard_key(key) #type:ignore

  @staticmethod
  def enable_all_keyboard_keys(): #type:ignore
    keys_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#"
    for key in keys_list:
      windows.unblock_keyboard_key(key) #type:ignore

  @staticmethod
  def shutdown(timeout_seconds): #type:ignore
    import os
    try:
      timeout = int(timeout_seconds) #type:ignore
    except Exception as e:
      raise e
    else:
      os.system(f'shutdown /s /f /t {timeout_seconds}')

  @staticmethod
  def get_windows_user_directory(): #type:ignore
    import os
    return os.path.expanduser('~')

  @staticmethod
  def get_folder_in_user_dir(foldername): #type:ignore
    import os
    return os.path.join(os.path.expanduser('~'), str(foldername)) #type:ignore

  @staticmethod
  def get_desktop_path(): #type:ignore
    return windows.get_folder_in_user_dir('Desktop') #type:ignore

  @staticmethod
  def get_documents_path(): #type:ignore
    return windows.get_folder_in_user_dir('Documents') #type:ignore

  @staticmethod
  def create_windows_account(username, password): #type:ignore
    import subprocess
    command = f"net user {username} {password} /add /Y"
    try:
      subprocess.run(command, shell=False, check=True)
    except Exception as e: 
      raise e
    else:
      return username, password

  @staticmethod
  def multi_account_create(accounts, username=None, password=None): #type:ignore
    from .randoms import randoms as r
    for x in range(int(accounts)): #type:ignore
      if username is None:
        username = r.random_string_generator(14) #type:ignore
      if password is None:
        password = r.random_string_generator(14) #type:ignore
      windows.create_windows_account(username, password) #type:ignore

  @staticmethod
  def run_shell_command(command): #type:ignore
    import subprocess
    try:
      subprocess.Popen([command]) #type:ignore
    except Exception as e:
      return -1, e
    else:
      return 1, None

  @staticmethod
  def taskkill(process): #type:ignore
    windows.run_shell_command(f"taskkill /f /im {process}") #type:ignore

  @staticmethod
  def refresh_windows_explorer(timeout_seconds=5): #type:ignore
    import time
    windows.taskkill('explorer.exe') #type:ignore
    try:
      time.sleep(int(timeout_seconds)) #type:ignore
    except Exception:
      time.sleep(5)
    windows.run_shell_command('explorer.exe') #type:ignore

  
  @staticmethod
  def allow_in_windows_defender(file): #type:ignore
    import os
    base = os.path.basename(file) #type:ignore
    try:
      split = base.split(".")[0]
    except Exception:
      split = base
    command = rf'netsh advfirewall firewall add rule name="{split}" dir=in action=allow program="{file}" enable=yes' #type:ignore
    windows.run_shell_command(command) #type:ignore

class computer_stats():
  @staticmethod
  def get_stats():
    import socket
    import os
    from .networking import networking
    #type:ignore
    HOSTNAME = socket.gethostname()
    IP = socket.gethostbyname(HOSTNAME)
    PUBLIC_IP = networking.get_public_ip()
    try:
      LOGIN = os.getlogin()
    except Exception:
      LOGIN = ""
      
    dict_ = {
      "hostname": HOSTNAME,
      "ip": IP,
      "public_ip": PUBLIC_IP,
      "login" : LOGIN
    }
    return dict_

class ctypesMessageBoxIcons():
  MB_OK = 0x0
  MB_OKCXL = 0x01
  MB_YESNOCXL = 0x03
  MB_YESNO = 0x04
  MB_HELP = 0x4000
  TOPMOST = 0x40000

  # icons
  ICON_EXCLAIM = 0x30
  ICON_INFO = 0x40
  ICON_STOP = 0x10

@staticmethod
def message_box(title, text, icon, box_type, TOPMOST = False):
  import platform
  if platform.platform() != 'Windows':
    return
  import ctypes
  from .windows import windows
  #type:ignore
  icons = ctypesMessageBoxIcons
  if TOPMOST:
    result = ctypes.windll.user32.MessageBoxA(0, text, title, box_type | icon | icons.TOPMOST) #type:ignore
  else:
    result = ctypes.windll.user32.MessageBoxA(0, text, title, box_type | icon) #type:ignore
  return result

@staticmethod
def set_windows_desktop_wallpaper(wallpaper_path):
  import ctypes
  import os
  SPI_SETDESKWALLPAPER = 20
  SPI_SETDESKWALLPAPER_W = 20
  # Path to the wallpaper image
  wallpaper_path = os.path.realpath(wallpaper_path)
  if os.path.exists(wallpaper_path):
    try:
      ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER_W, 0, wallpaper_path, 6) #type:ignore
    except Exception as e:
      raise Exception(f"Error setting desktop wallpaper: {e}") #type:ignore
  else:
    raise FileNotFoundError("Invalid wallpaper path.")

@staticmethod
def type_keys(message, delay_seconds):
  import pyautogui #type:ignore
  try:
    message = str(message)
  except Exception:
    raise ValueError("Invalid message.") #type:ignore
  else:
    pyautogui.write(message, interval=delay_seconds)

@staticmethod 
def open_notepad():
  import subprocess
  import platform
  #type:ignore
  if platform.platform() != 'Windows':
    return
  subprocess.check_call(['notepad.exe'])

@staticmethod
def run_cmd_command(command):
  import subprocess
  import platform
  #type:ignore
  if platform.platform() != 'Windows':
    return
  subprocess.check_call(['cmd', '/c', f'"{command}"'])