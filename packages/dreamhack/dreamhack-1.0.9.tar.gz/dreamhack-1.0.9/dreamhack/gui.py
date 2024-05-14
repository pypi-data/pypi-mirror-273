from tkinter import NONE


class gui():
  @staticmethod
  def get_tkinter_root(): #type:ignore
    import tkinter
    return tkinter.Tk()

  @staticmethod
  def tk_geometry(root, width, height): #type:ignore
    try:
      return root.geometry(f'{width}x{height}') #type:ignore
    except Exception:
      raise Exception('Invalid Root.') #type:ignore

# ----------------------------------CUSTOMTKINTER---------------------------------------

  class CTkappearancemodes():
    SYSTEM = 'system'
    LIGHT = 'light'
    DARK = 'dark'

  class CTKMessageBoxIcons:
    CHECKMARK = 'check'
    ERROR = 'cancel'
    QUESTION = 'question'
    INFO = 'info'

  @staticmethod
  def set_ctk_appearance_mode(mode):
    import customtkinter as ctk
    ctk.set_appearance_mode(mode)

  
  @staticmethod
  def get_customtkinter_root(): #type:ignore
    import customtkinter #type:ignore
    return customtkinter.CTk()

  @staticmethod
  def ctk_geometry(root, width, height): #type:ignore
    try:
      return root.geometry(f'{width}x{height}') #type:ignore
    except Exception:
      raise Exception('Invalid Root.') #type:ignore

  @staticmethod
  def ctk_message_box(title, message_text, icon=CTKMessageBoxIcons.INFO, option_1 = None, option_2 = None, option_3 = None): #type:ignore
    from CTkMessagebox import CTkMessagebox
    if icon == gui.CTKMessageBoxIcons.INFO:
      if option_1 is None and option_2 is None and option_3 is None:
        return CTkMessagebox(title=title, message=message_text)
      elif option_1 is not None and option_2 is None and option_3 is None:
        return CTkMessagebox(title=title, message=message_text, option_1=option_1)
      elif option_1 is not None and option_2 is not None and option_3 is None:
        return CTkMessagebox(title=title, message=message_text, option_1=option_1, option_2 = option_2) #type:ignore
      elif option_1 is not None and option_2 is not None and option_3 is not None:
        return CTkMessagebox(title=title, message=message_text, option_1 = option_1, option_2 = option_2, option_3 = option_3) #type:ignore
      elif option_1 is None and option_2 is not None and option_3 is not None:
        return CTkMessagebox(title=title, message=message_text, option_2 = option_2, option_3 = option_3) #type:ignore
      elif option_1 is None and option_2 is None and option_3 is not None:
        return CTkMessagebox(title=title, message=message_text, option_3 = option_3)
      else:
        return CTkMessagebox(title=title, message=message_text)
    else:
      #------------------------------ICON----------------------------------------
      if option_1 is None and option_2 is None and option_3 is None:
        return CTkMessagebox(title=title, message=message_text, icon=icon)
      elif option_1 is not None and option_2 is None and option_3 is None:
        return CTkMessagebox(title=title, message=message_text, option_1=option_1, icon=icon)
      elif option_1 is not None and option_2 is not None and option_3 is None:
        return CTkMessagebox(title=title, message=message_text, option_1=option_1, option_2 = option_2, icon=icon) #type:ignore
      elif option_1 is not None and option_2 is not None and option_3 is not None:
        return CTkMessagebox(title=title, message=message_text, option_1 = option_1, option_2 = option_2, option_3 = option_3, icon=icon) #type:ignore
      elif option_1 is None and option_2 is not None and option_3 is not None:
        return CTkMessagebox(title=title, message=message_text, option_2 = option_2, option_3 = option_3, icon=icon) #type:ignore
      elif option_1 is None and option_2 is None and option_3 is not None:
        return CTkMessagebox(title=title, message=message_text, option_3 = option_3, icon=icon)
      else:
        return CTkMessagebox(title=title, message=message_text, icon=icon)