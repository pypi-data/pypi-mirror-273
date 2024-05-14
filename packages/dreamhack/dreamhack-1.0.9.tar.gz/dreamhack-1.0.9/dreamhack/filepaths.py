class filepaths():
  
  @staticmethod
  def get_current_directory(): #type:ignore
    import os
    return os.path.realpath(os.getcwd())

  @staticmethod
  def get_all_files_in_directory(directory): #type:ignore
    import os
    try:
      return os.listdir(directory) #type:ignore
    except PermissionError as pe:  
      return [], pe 
    except Exception as e:
      return [], e