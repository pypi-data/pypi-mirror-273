from customtkinter.windows.widgets.appearance_mode.appearance_mode_base_class import CTkAppearanceModeBaseClass


class downloads:
  @staticmethod
  def download_file_from_github(url, save_path): #type:ignore
    import ssl
    import urllib.request
    import shutil #type:ignore
    try:
      ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
      ssl_context.check_hostname = False
      ssl_context.verify_mode = ssl.CERT_NONE
      with urllib.request.urlopen(url, context=ssl_context) as response: #type:ignore
        with open(save_path, 'wb') as out_file:
          shutil.copyfileobj(response, out_file)
    except Exception as e:
      raise e
    else:
      return url, save_path

  @staticmethod
  def download_webpage_content(url, save_path): #type:ignore
    import requests
    try:
      cont = requests.get(url).text #type:ignore
    except Exception:
      raise Exception('Invalid URL.') #type:ignore
    else:
      try:
        with open(save_path, 'r+') as f:
          f.write(cont)
      except Exception as e:
        raise Exception(f'Error writing to file: {e}') #type:ignore
      else:
        return cont, save_path