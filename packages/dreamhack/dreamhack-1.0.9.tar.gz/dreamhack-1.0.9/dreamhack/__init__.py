from .encryption import encryption
from .windows import windows
from .colorcodes import colorcodes
from .zipfiles import zipfiles
from .logging import logging 
from .networking import networking
from .randoms import randoms
from .downloads import downloads
from .filepaths import filepaths
from .gui import gui
from .registry import RegistryEditor
from .registry import disable_regedit
from .registry import lock_all_drives
from .registry import disable_task_manager
from .registry import add_to_windows_startup

#type:ignore

import os
import sys
import subprocess

def get_current_directory():
  return os.getcwd()

def get_package_version():
  import pkg_resources
  try:
      return pkg_resources.get_distribution('dreamhack').version
  except pkg_resources.DistributionNotFound:
      return "Package not found"


def install(package):
  try:
    install_ = subprocess.check_call([sys.executable, "-m", "pip", "install", package])
  except Exception as e:
    raise e
  else:
    return package, install_

def taskkill(process_name):
  import platform
  if platform.platform() != 'Windows':
    subprocess.Popen(['killall',  '-KILL', process_name])
  else:
    subprocess.Popen(['taskkill', '/f', '/im', process_name])

def install_list_of_packages(package_list):
  for package in package_list:
    install(package)

def random_int_in_range(min, max):
  return randoms.random_number_in_range(min,max)

def list_directory(directory):
  return filepaths.get_all_files_in_directory(directory)
