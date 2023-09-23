import os, threading, time, uuid, random, json, ctypes, string, sys, string, re, webbrowser

try:
    import requests
    import colorama
    import tls_client 
    import pystyle
    import datetime
except ModuleNotFoundError:
    os.system('pip install requests')
    os.system('pip install colorama')
    os.system('pip install tls_client')
    os.system('pip install pystyle')
    os.system('pip install datetime')

from colorama import *
from pystyle import *

red = Fore.RED
blue = Fore.BLUE
cyan = Fore.CYAN
yellow = Fore.YELLOW
lightcyan = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
orange = Fore.RED + Fore.YELLOW
green = Fore.GREEN
white = Fore.WHITE
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
reset = Fore.RESET

total = 0
application_created = 0
enabled_intent = 0
bot_tokens = 0
failed = 0
deleted = 0
joined = 0
with open('tokens.txt', 'r') as t:
    lines = t.readlines()
    tokens = sum(len(line.strip().split()) for line in lines)
    
ctypes.windll.kernel32.SetConsoleTitleW(f"『 Discord.Bot 』 By ~Z3R003~ / Tokens: {tokens}")

def get_time():
    date = datetime.datetime.now()
    current_time = date.strftime('%H:%M:%S')
    return current_time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def bot_generator_title():
    global total, application_created, enabled_intent, bot_tokens,failed,deleted
    ctypes.windll.kernel32.SetConsoleTitleW(f"『 Discord.Bot 』 By ~Z3R003~ / Tokens: {tokens} | Application Created : {application_created} ~ Intent Enabled : {enabled_intent} ~  Bot Tokens : {bot_tokens}")

def bot_deleter_title():
    global total, application_created, enabled_intent, bot_tokens,failed,deleted
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Discord.Bot 』 By ~Z3R003~ / Tokens: {tokens} | Application Deleted : {deleted} / Bot Deleted : {deleted}')

def bot_joiner_title():
    global total, application_created, enabled_intent, bot_tokens,failed,deleted, joined
    ctypes.windll.kernel32.SetConsoleTitleW(f'『 Discord.Bot 』 By ~Z3R003~ / Tokens: {tokens} | Bots Joined : {joined}')    

def load_proxies():
    with open('proxies.txt','r') as p:
        proxies = p.read().splitlines()
    return proxies

def name_gen():
    name = ''.join(random.choices(string.ascii_letters + string.digits, k =10))
    return name

def check_useproxies():
    session = tls_client.Session(
        client_identifier="chrome_113",
        random_tls_extension_order=True
    )
    with open('config.json','r') as d:
        data = json.load(d)
        check_proxies = data['use_proxies']
    if check_proxies == 'y' or check_proxies == 'yes' or check_proxies == 'Y' or check_proxies == 'YES':
        proxies = load_proxies()
        proxy = random.choice(proxies)
        session.proxies = {
                'http':f'http://{proxy}',
                'https':f'https://{proxy}'
            }
    else:
        pass
    return session

def bot_deleter(session,token):
    global total, application_created, enable_intent, bot_tokens, failed, deleted
    session = check_useproxies()
    output_lock = threading.Lock()
    session.headers = {
        'authorization': token
    }
    while True:
        while True:
            try:
                get_ids = session.get('https://discord.com/api/v9/applications?with_team_applications=true')
                break
            except:
                continue
        if get_ids.status_code == 200:
            all_ids = get_ids.json()
            for i in all_ids:
                id = i['id']
                while True:
                    try:
                        delete_bot = session.post(f'https://discord.com/api/v9/applications/{id}/delete')
                        break
                    except:
                        continue
                if delete_bot.status_code == 204:
                    with output_lock:
                        deleted +=1
                        time_rn = get_time()
                        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {green}Bot Deleted{gray} | ", end="")
                        sys.stdout.flush()
                        Write.Print(f"{id}\n", Colors.blue_to_cyan, interval=0.000)
                        bot_deleter_title()
                else:
                    with output_lock:
                        time_rn = get_time()
                        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}+{gray}) {green}Unknown Error{gray} | ", end="")
                        sys.stdout.flush()
                        Write.Print(f"{id}\n", Colors.blue_to_cyan, interval=0.000)
        elif get_ids.status_code == 401 and 'Unauthorized' in get_ids.text:
            with output_lock:
                time_rn = get_time()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {red}Invalid Token{gray} | ", end="")
                sys.stdout.flush()
                Write.Print(f"{token}\n", Colors.blue_to_cyan, interval=0.000)
                break
def bot_generator(session,token,name,intent):
    global total, application_created, enabled_intent, bot_tokens, failed, deleted
    session = check_useproxies()
    #name = name_gen()
    output_lock = threading.Lock()
    session.headers = {
        'authorization': token
    }
    if name == '' or name == 'n' or name == 'no':
        payload = {
            'name':'Z3R003 On TOP'
        }
    else:
        payload = {
            'name':name
        }
    while True:
        while True:
            try:
                application_creator = session.post('https://discord.com/api/v9/applications', json=payload)
                break
            except:
                continue
        if application_creator.status_code == 201:            
            id = application_creator.json()['id']
            with output_lock:
                application_created += 1
                time_rn = get_time()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({yellow}*{gray}) {yellow}Application Created{gray} | ", end="")
                sys.stdout.flush()
                Write.Print(f"{id}\n", Colors.blue_to_cyan, interval=0.000)
                bot_generator_title()
            if intent == 'y' or intent == 'yes':
                intent_payload  ={
                    "bot_public": True,
                    "bot_require_code_grant": False,
                    "flags": "557056"
                }
                while True:
                    try:
                        enable_intent = session.patch(f'https://discord.com/api/v9/applications/{id}', json=intent_payload)
                        break
                    except:
                        continue
                if enable_intent.status_code == 200:
                    with output_lock:
                        enabled_intent += 1
                        time_rn = get_time()
                        print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({pink}/{gray}) {pink}Intent Enabled{gray} | ", end="")
                        sys.stdout.flush()
                        Write.Print(f"{id}\n", Colors.blue_to_cyan, interval=0.000)
                        bot_generator_title()
            while True:
                try:
                    get_token = session.post(f'https://discord.com/api/v9/applications/{id}/bot/reset')
                    break
                except:
                    continue
            if get_token.status_code == 200:
                bot_token = get_token.json()['token']
                with output_lock:
                    bot_tokens +=1
                    time_rn = get_time()
                    print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({green}+{gray}) {green}Token Generated{gray} | ", end="")
                    sys.stdout.flush()
                    Write.Print(f"{bot_token}\n", Colors.blue_to_cyan, interval=0.000)
                    bot_generator_title()
                    open('bot_tokens.txt','a').write(f'{bot_token}\n')
                    open('oauth2_links.txt','a').write(f'https://discord.com/api/oauth2/authorize?client_id={id}&permissions=8&scope=bot\n')
        elif application_creator.status_code == 401 and 'Unauthorized' in application_creator.text:
            with output_lock:
                time_rn = get_time()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {red}Invalid Token{gray} | ", end="")
                sys.stdout.flush()
                Write.Print(f"{token}\n", Colors.blue_to_cyan, interval=0.000)
                break
        else:
            with output_lock:
                time_rn = get_time()
                print(f"{reset}[ {cyan}{time_rn}{reset} ] {gray}({red}-{gray}) {red}Ratelimit{gray}")
                break
def main():
    global total, application_created, enable_intent, bot_tokens, failed, deleted, joined
    with open('config.json','r') as d:
        data = json.load(d)
        bot_username = data['bot_username'] 
        threads_num = data['threads']
    Write.Print('''
                    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗    ██████╗  ██████╗ ████████╗
                    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗   ██╔══██╗██╔═══██╗╚══██╔══╝
                    ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║   ██████╔╝██║   ██║   ██║   
                    ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║   ██╔══██╗██║   ██║   ██║   
                    ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝██╗██████╔╝╚██████╔╝   ██║   
                    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═════╝  ╚═════╝    ╚═╝                               
════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════                  
                                  ╔════════════════════════════════════════════════╗
                                  ║ By ~Z3R003  github.com/Z3R003 | .gg/jfCpNdxKk  ║
                                  ║════════════════════════════════════════════════║   
                                  ║ [01] Bot Generator     ║  [02] Bot Deleter     ║   
                                  ║ [03] Bot Joiner        ║  [04] Coming Soon...  ║
                                  ╚════════════════════════╩═══════════════════════╝
                                                    Z3R003 ON TOP
                
                   '''                                    
    , Colors.blue_to_cyan, interval=0.000)
    choice = input(f""" {blue}
┌──{cyan}(Discord@Bot){blue} ~ [{cyan}Ϟ{blue}]
└─> """)
    session = check_useproxies()
    threads = []
    if choice == '1' or choice == '01':
        use_intent = input(f'{cyan}[{blue}?{cyan}] Generate Bots with intent enabled? (y,n) > ')
        print('\n')
        with open('tokens.txt','r')as t:
            tokens = t.read().splitlines()
        start_time1 = time.time()
        for token in tokens:
            for _ in range(threads_num):
                t = threading.Thread(target=bot_generator, args=(session, token,bot_username,use_intent))
                t.start()
                threads.append(t)
        update_title_threads = threading.Thread(target=bot_generator_title)
        update_title_threads.start()
        threads.append(update_title_threads)
        for thread in threads:
            thread.join()
        current_time = time.time()
        elapsed_time = current_time - start_time1
        elapsed_hours = int((elapsed_time % 86400) // 3600)
        elapsed_minutes = int((elapsed_time % 3600) // 60)
        elapsed_seconds = int(elapsed_time % 60)
        print('\n')
        print(f'\n{white}[{blue}!{white}]{green} finished! {cyan}Generated {red}{bot_tokens} {cyan}bots in {red}{elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s')
        input(f'{reset}\nEnter to go back!')
        clear_screen()
        main()     
    elif choice == '2' or choice == '02':
        with open('tokens.txt','r')as t:
            tokens = t.read().splitlines()
        start_time2 = time.time()
        for token in tokens:
            for _ in range(threads_num):
                t = threading.Thread(target=bot_deleter, args=(session, token))
                t.start()
                threads.append(t)
        update_title_threads = threading.Thread(target=bot_deleter_title)
        update_title_threads.start()
        threads.append(update_title_threads)
        for thread in threads:
            thread.join()
        current_time = time.time()
        elapsed_time = current_time - start_time2
        elapsed_hours = int((elapsed_time % 86400) // 3600)
        elapsed_minutes = int((elapsed_time % 3600) // 60)
        elapsed_seconds = int(elapsed_time % 60)
        print('\n')
        print(f'\n{white}[{blue}!{white}]{green} finished! {cyan}Deleted {red}{deleted} {cyan}bots in {red}{elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s')
        input(f'{reset}\nEnter to go back!')
        clear_screen()
        main()
    elif choice == '3' or choice == '03':
        file = input(f'{cyan}[{blue}?{cyan}] .txt file (oauth2_links.txt) > ')
        with open(file,'r') as f:
           oauth2links = f.read().splitlines()
        start_time3 = time.time()
        print('\n')
        for oauth2link in oauth2links:
            webbrowser.open_new(oauth2link)
            joined +=1
        update_title_threads = threading.Thread(target=bot_joiner_title)
        update_title_threads.start()
        threads.append(update_title_threads)
        current_time = time.time()
        elapsed_time = current_time - start_time3
        elapsed_hours = int((elapsed_time % 86400) // 3600)
        elapsed_minutes = int((elapsed_time % 3600) // 60)
        elapsed_seconds = int(elapsed_time % 60)
        print(f'\n{white}[{blue}!{white}]{green} finished! {cyan}Joined {red}{bot_tokens} {cyan}bots {cyan}in {red}{elapsed_hours}h {elapsed_minutes}m {elapsed_seconds}s')
        input(f'{reset}\nEnter to go back!')
        clear_screen()
        main()
    else:
        clear_screen()
        print(f'{cyan}[{red}!{cyan}]{red} Invalid choice', end=' ')
        [print('.', end='', flush=True) or time.sleep(0.7) for _ in range(3)]
        clear_screen()
        main()
if __name__ == '__main__':
    main()
