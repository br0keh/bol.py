# -*- coding: utf-8 -*-


import requests
import random

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


def parse_error(body):
    try:
        x = str(body).split('<!-- ')[1]
        errorMessage = x.split(' -->')[0]
        return "API RESPONSE: "+errorMessage
    except:
        return "Unknow error."


def login(email, password):
    if not email.endswith('bol.com.br'):
        return print("[x] %s %s -> Email provider not supported." % (email, password))

    userAgent = random.choice(USER_AGENT_LIST)

    loginPageReq = requests.get(
        'https://email.bol.uol.com.br/login', headers={'user-agent': userAgent})
    loginPageCookies = loginPageReq.cookies.get_dict()

    loginPayload = "skin=bol-default&dest=WEBMAIL&deviceId=&user=%s&pass=%s" % (
        email, password)
    loginRequest = requests.post(
        'https://visitante.acesso.uol.com.br/login.html', data=loginPayload, headers=LOGIN_REQUEST_HEADERS, cookies=loginPageCookies)

    if 'openApp(dna.uid);' in loginRequest.text:
        print("[-] %s %s -> Logged in successfully.")
        pass
    elif 'throwErrorStatus(' in loginRequest.text:
        print("[!] %s %s -> %s" % (email, password,
                                   parse_error(loginRequest.text)))
        pass
    else:
        print("[!] %s %s -> Request error." % (email, password))
    pass


def main():
    login("test@bol.com.br", "test")
    pass


main()
