class networking():
  
  @staticmethod
  def ping(ip): #type:ignore
    import os
    return os.system(f'ping {ip}') #type:ignore

  @staticmethod
  def get_public_ip(): #type:ignore
    import public_ip as ip #type:ignore
    return ip.get()

  @staticmethod
  def get_private_ip_address(): #type:ignore
    import socket
    return socket.gethostbyname(socket.gethostname())

  @staticmethod
  def stop_wifi_network(): #type:ignore
    import subprocess
    try:
        # Stop the hosted network
        subprocess.run(['netsh', 'wlan', 'stop', 'hostednetwork'], check=True)
    except subprocess.CalledProcessError as ex:
      raise ex
    except Exception as e:
      raise e

  @staticmethod
  def start_wifi_network(): #type:ignore
    import subprocess
    import atexit
    #type:ignore
    try:
      # Start the hosted network
      subprocess.run(['netsh', 'wlan', 'start', 'hostednetwork'], check=True)
    except Exception as e:
      raise e
    else:
      atexit.register(networking.stop_wifi_network)

  @staticmethod
  def create_wifi_network(ssid, password, auto_start=True):
    import os 
    import subprocess
    import atexit
    #type:ignore
    try:
        # Create the hosted network
        subprocess.run(['netsh', 'wlan', 'set', 'hostednetwork', 'mode=allow', 'ssid=' + ssid, 'key=' + password], check=True) #type:ignore
    except subprocess.CalledProcessError as e:
        raise e
    except Exception as ex:
      raise ex
    else:
      if auto_start:
        networking.start_wifi_network()
      

  