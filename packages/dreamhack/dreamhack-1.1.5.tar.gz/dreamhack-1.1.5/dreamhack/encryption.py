class encryption():
  @staticmethod
  def generate_salt(size=16):
    import secrets
    return secrets.token_bytes(size)#type:ignore

  @staticmethod
  def derive_key(salt, password):
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)#type:ignore
    return kdf.derive(password.encode())

  @staticmethod
  def load_salt(custom_salt_filename = None):
    if custom_salt_filename is None:
      custom_salt_filename = "salt.salt"
    return open(custom_salt_filename, "rb").read()#type:ignore
    
  @staticmethod
  def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True, custom_salt_filename = 'salt.salt'):
    import base64
    salt = ""
    if load_existing_salt:
        salt = encryption.load_salt(custom_salt_filename=custom_salt_filename)#type:ignore
    elif save_salt:
        salt = encryption.generate_salt(salt_size)#type:ignore
        with open(custom_salt_filename, "wb") as salt_file:
            salt_file.write(salt)
    if salt is not None:
      derived_key = encryption.derive_key(salt, password) #type:ignore
      encode = base64.urlsafe_b64encode(derived_key)
      return encode
    else: 
      return -1 

  @staticmethod
  def encrypt(filename, key):
    from cryptography.fernet import Fernet
    f = Fernet(key)
    try:
      with open(filename, "rb") as file: 
          file_data = file.read()
      encrypted_data = f.encrypt(file_data)
      with open(filename, "wb") as file:
          file.write(encrypted_data)
          file.close()
    except PermissionError as pe:
      return -1, f"Permission Denied to file {filename}.", pe
    except Exception as e:
      return -2, e
    else:  
      return 1

  @staticmethod
  def encrypt_folder(directory, key, folders_to_exclude = []):
    import os
    from .filepaths import filepaths as fp
    #type:ignore
    if folders_to_exclude is not None and directory in folders_to_exclude:
      return
    dirlist = fp.get_all_files_in_directory(directory)
    for file in dirlist:
      file = os.path.join(str(directory), str(file))
      if os.path.isfile(file):
        encryption.encrypt(file, key)
      else:
        encryption.encrypt_folder(file, key)

  @staticmethod
  def encrypt_folders_in_list(directory_list, key, whitelist=[]):
    for folder in directory_list:#type:ignore
      if folder in whitelist:
        pass
      else:
        encryption.encrypt_folder(folder, key, folders_to_exclude=whitelist)