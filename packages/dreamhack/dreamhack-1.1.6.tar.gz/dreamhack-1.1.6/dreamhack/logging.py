class logging():
  @staticmethod
  def create_log_file(log_path): #type:ignore
    from datetime import datetime
    now = datetime.now()
    yr = now.year
    mo = now.month
    dy = now.day
    hr = now.hour
    min = now.minute
    se = now.second
    try:
      with open(log_path, "w") as f: #type:ignore
        f.write(f"[{yr}_{mo}_{dy}_{hr}_{min}_{se}] \n \n")
        f.close()
    except FileExistsError:
      raise FileExistsError('Log file already exists.') #type:ignore
    except Exception as e:
      raise e

  @staticmethod
  def log(log_path, message, symbol='*'): #type:ignore
    from datetime import datetime
    now = datetime.now()
    yr = now.year
    mo = now.month
    dy = now.day
    hr = now.hour
    min = now.minute
    se = now.second  
    try:
      with open(log_path, 'a+') as f: #type:ignore
        f.write(f'[{symbol}] [{yr}_{mo}_{dy}_{hr}_{min}_{se}] : {message} \n')
        f.close()
    except FileNotFoundError:
        try:
          logging.create_log_file(log_path)
        except Exception:
          raise FileNotFoundError('Invalid Log Path.') #type:ignore
        else:
          logging.log(log_path, message)
    except Exception as e:
      raise Exception(f'Error creating log file: {e}') #type:ignore
      
  @staticmethod
  def error(log_path, message): #type:ignore
    logging.log(log_path, message, symbol='!')
    
  @staticmethod
  def warning(log_path, message): #type:ignore
    logging.log(log_path, message, symbol='#')