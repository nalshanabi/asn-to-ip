'''
THIS TOOL IS OPEN SOURCE AND FREE TO USE . NOT FOR SALE !!
DONT REMOVE THIS CREDIT IF YOU ARE A GOOD MANNERS PROGRAMMER

# Coded by : D K .
# Github : https://github.com/dkmpostor
# Created : Sat , 17 Sep 2022 09:57

'''

import os
import datetime
import requests
import ipranges
from colorama import init, Fore

init(autoreset=True)

def removeduplicate(path):

    lines = open(path, 'r').readlines()
    lines_set = set(lines)
    out  = open(path, 'w')
    for line in lines_set:
        out.write(line)


def asnToIP(asn):

    r = requests.get(f'https://api.bgpview.io/asn/{asn}/prefixes').json()
    data = r['data']['ipv4_prefixes']
    
    for i in range(0, int(len(data)) - 1):
        res = r['data']['ipv4_prefixes'][i]
        pre = res['ip'] + '/' + str(res['cidr'])
        iplist = ipranges.IP4Net(pre)
        for ip in iplist:
            yield ip

def main():

    # result name == date now
    fn = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # mass asn to ip
    asn = open(input('? Input .txt : '), 'r').read().splitlines()
    print("")
    for i in asn:
        # get length of result ip
        if len(list(asnToIP(i))) > 0:
            print(Fore.GREEN + f'[+] ASN : {i} -> {len(list(asnToIP(i)))} IP' + Fore.RESET)
        elif len(list(asnToIP(i))) == 0:
            print(Fore.RED + f'[+] ASN : {i} -> {len(list(asnToIP(i)))} IP' + Fore.RESET)

        # write to file
        if not os.path.exists('resultasn'):
            os.mkdir('resultasn')

        with open(f'resultasn/{fn}.txt', 'a', errors='ignore', encoding='utf-8') as f:
            for ip in asnToIP(i):
                f.write(str(ip) + '\n')
                
    # remove duplicate
    removeduplicate(f'resultasn/{fn}.txt')
    print(Fore.BLUE + f'\n[+] Remove Duplicate Done ! -> {len(open(f"resultasn/{fn}.txt", "r").readlines())} IP' + Fore.RESET)
                


if __name__ == '__main__':

    print('''
                    _          _       
                   | |        (_)      
   __ _ ___ _ __   | |_ ___    _ _ __  
  / _` / __| '_ \  | __/ _ \  | | '_ \ 
 | (_| \__ \ | | | | || (_) | | | |_) |
  \__,_|___/_| |_|  \__\___/  |_| .__/ 
                                | |    
    Update : 17-09-2022         |_|        
    ''')
    main()
