"""
Spam a scammer API with realistic data.
"""

import random
import requests
import threading
from time import perf_counter

URL_SCAMMER = "https://bb-va-seg-fior.000webhostapp.com/break.php"
THREADS = 100

def main():
    """
    Prepare threading to run the maximum ammount of functions that the processor will do. It's set
    to 100 threads, but it probably won't do 100 at the same time, it depends on computing power.
    """
    threads:list[threading.Thread] = []
    for n in range(1,THREADS):
        t = threading.Thread(target=threaded_loop, args=(n,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    
def threaded_loop(thread:int):
    """
    Make a POST every loop to the scammer API so it's database will contain false information.
    For use on other server, it will need modification.
    """
    global time_out
    global continue_loop
    global request_count
    time_out = 0
    continue_loop = True
    request_count = 0
    while continue_loop:
        nif:str = generate_nif()
        phone:int = generate_phone()
        password:str = generate_password()
        ids:float = float(random.uniform(0, 10000))
        url:str = URL_SCAMMER
        otp:int = int(random.randint(100000, 999999))
        try:
            r = requests.post(url, data={"numCliente" : nif, "tel" : phone, "pass" : password, "id" : ids})
            s = requests.post(url, data={"id" : ids, "otp" : otp})
            #if thread == 1:
                #print("====================================================================================================")
                #print("Response main:" + str(r.status_code) + " " + str(r.reason))
                #print("Response OTP:" + str(s.status_code) + " " + str(s.reason))
            if str(r.status_code) != "200" or str(s.status_code) != "200":
                time_out += 1
        except:
            print("Request failed.")
            time_out += 1
        request_count += 1
        if time_out >= 100:
            continue_loop = False
        if thread == 1:
            print("Generated data: " + str(nif) + ", " + str(phone) + ", " + str(password) + ", " + str(ids) + ", " + str(otp) + ".")
            print("Total requests: " + str(request_count) + ". Total errors: " + str(time_out) + ".")
            print("ScammerSmasher ETA: " + str(perf_counter()))
            print("")
    print("Loop ended.")

def get_nif_letter(nif:str):
    """
    Generate a character for a number corresponding to a national document of identity (Spanish 
    one). The character will be on uppercase or lowercase to make it more confusing and realistic.
    """
    dictionary_letters:dict[int,str] = {
        0:"T",
        1:"R",
        2:"W",
        3:"A",
        4:"G",
        5:"M",
        6:"Y",
        7:"F",
        8:"P",
        9:"D",
        10:"X",
        11:"B",
        12:"N",
        13:"J",
        14:"Z",
        15:"S",
        16:"Q",
        17:"V",
        18:"H",
        19:"L",
        20:"C",
        21:"K",
        22:"E"
    }
    letter:str = dictionary_letters[int(nif) % 23]
    if random.randint(0,1) == 0:
        letter = letter.lower()
    return letter

def generate_nif():
    """
    Generate a National Identifier on the Spanish format with a valid letter at the end.
    """
    index:int = 0
    nif:str = ""
    while index < 8:
        nif = nif + str(random.randint(1,9))
        index += 1
    nif = nif + get_nif_letter(nif)
    return nif

def generate_phone():
    """
    Generate a phone number starting on 6, 7 or 9, as all normal phone numbers will start in Spain.
    """
    index:int = 0
    phone_prefix:int = 0
    phone_generated:int
    random_number:int = random.randint(0,2)
    if random_number == 0:
        phone_prefix = 6
    elif random_number == 1:
        phone_prefix = 9
    else:
        phone_prefix = 7
    phone_generated = phone_prefix
    while index < 8:
        phone_generated = int(str(phone_generated) + str(random.randint(0,9)))
        index += 1
    return phone_generated

def generate_password():
    """
    Generate a password from the dictionary passwords.txt. It will append a number on front or back
    or even remove the word completly and just use the number like a pin.
    """
    random_password:str = random.choice(open('sm/passwords.txt').readlines()).rstrip()
    random_number:int = random.randint(0,3)
    if random_number == 0:
        random_password = random_password + str(random.randint(0,9999))
    elif random_number == 1:
        random_password = str(random.randint(0,9999)) + random_password
    elif random_number == 2:
        random_password = str(random.randint(1000,9999))
    return random_password


if __name__ == "__main__":
    main()