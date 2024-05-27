# Import the required Modules 
import requests 
  
proxies = []
# Create a pool of proxies 
with open('proxies.txt', 'r') as file:
    # Lee todas las líneas del archivo y elimina los espacios en blanco al principio y al final de cada línea
    proxies = [line.strip() for line in file]
  
  
def get_active_proxies():
    return proxies
    """# Iterate the proxies and check if it is working. 
    active_proxies = []
    for proxy in proxies: 
        try: 
            # https://ipecho.net/plain returns the ip address 
            # of the current session if a GET request is sent. 
            page = requests.get('https://ipecho.net/plain', proxies={"http": proxy, "https": proxy}) 
            active_proxies.append(proxy)
            # Prints Proxy server IP address if proxy is alive. 
            print("Status OK, Output:", page.text) 
    
        except OSError as e: 
            # Proxy returns Connection error 
            print(e) 
    return active_proxies"""
