# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace
# pylint: disable=bad-indentation
# pylint: disable=redefined-outer-name
# pylint: disable=no-self-argument


import argparse
import json
import os
import random
import sys

import colorama
import pyfiglet
import requests
from bs4 import BeautifulSoup as bs
from colorama import Fore

# color method
colorama.init(autoreset=True)
red = Fore.RED
blue = Fore.BLUE
cyan = Fore.CYAN
green = Fore.GREEN
yellow = Fore.YELLOW


# argument system
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="url of targeted website", required=True)
parser.add_argument(
    "-f",
    "--force",
    help="forced to look for sub domains without verifying the targeted domain",
    required=False,
)
parser.add_argument(
    "-r", "--remove", help="remove existing valid.txt file", required=False
)
parser.add_argument("-o", "--option", help="set option 1 / 2", required=False)
parser.add_argument("-m", "--method", help="set method http / https", required=True)
parser.add_argument("-fm", "--fast", help="fast print yes / no", required=True)
parser.add_argument(
    "-c", "--check", help="sub domain validation check (ex. -c yes / no)", required=True
)

args = parser.parse_args()

# main system
rapiddns = "https://rapiddns.io/subdomain/{}?full=1#valid"
crt_url = "https://crt.sh/?q={}&output=json"
all_subdomain = list()
subdomains = list()
subdomain = list()
valid_subdomain_list = list()
error_subdomain_list = list()


class main_system:
    def method_check():
        if args.method == "http":
            method = "http"
        elif args.method == "https":
            method = "https"
        return method

    def url_check():
        c_method = main_system.method_check()
        url = str(args.url)
        if args.force:
            print(yellow + "[-] Forced to look for sub domains")
        else:
            try:
                good_url = f"{c_method}://{url}"
                response = requests.get(good_url, timeout=20)
                print(green + "[*] Target is valid")
            except:
                print(red + "[*] Target is invalid")
                exit()

    def get_data_by_rapiddns(data):
        web = str(args.url)
        req = requests.get(rapiddns.format(web), timeout=20)
        soup = bs(req.text, "html.parser")
        if data == "subdomain_num":
            total_subdomain = soup.find("div", {"class": "d-flex align-items-left"})
            for total_subdomain_div in total_subdomain.find_all("div"):
                for total_subdomain_div_span in total_subdomain_div.find_all("span"):
                    return total_subdomain_div_span

        if data == "web_url":
            return web

    def rapiddns_subdomain_collection_purify():
        print(yellow + "[*] Starting to find subdomain in rapid dns")
        if args.fast == "yes":
            if main_system.get_data_by_rapiddns("subdomain_num").text == "0":
                pass
            else:
                print(
                    red
                    + " [-] "
                    + green
                    + "Total sub domain find in rapid dns: "
                    + str(main_system.get_data_by_rapiddns("subdomain_num").text)
                )
        web = str(args.url)
        req = requests.get(rapiddns.format(web), timeout=20)
        soup = bs(req.text, "html.parser")
        total_subdomain_num = main_system.get_data_by_rapiddns("subdomain_num")
        table_data = soup.find("table", {"id": "table"})
        for table_data_tbody in table_data.find_all("tbody"):
            i = int(total_subdomain_num.text)
            ii = 0
            while ii < i:
                subdomain_data = table_data_tbody.find_all("tr")[ii]
                for subdomain_data_td in subdomain_data.find_all("td")[0]:
                    ii += 1
                    all_subdomain.append(subdomain_data_td)
                    if args.fast == "yes":
                        print(red + " [ 111 ] " + yellow + subdomain_data_td)

        print(green + "[+] done")

    def crtsh():
        print(yellow + "[*] starting to find subdomain in crtsh")
        domain = main_system.get_data_by_rapiddns("web_url")
        try:
            response = requests.get(crt_url.format(domain), timeout=20)
            if response.ok:
                content = response.content.decode("UTF-8")
                jsondata = json.loads(content)
                for i in range(len(jsondata)):
                    name_value = jsondata[i]["name_value"]
                    if name_value.find("\n"):
                        subname_value = name_value.split("\n")
                        for subname_value in subname_value:
                            if subname_value.find("*"):
                                if subname_value not in subdomains:
                                    subdomains.append(subname_value)
                                    all_subdomain.append(subname_value)
                                    if args.fast == "yes":
                                        print(
                                            red + " [ 111 ] " + yellow + subname_value
                                        )
            if args.fast == "yes":
                print(
                    red
                    + " [-] "
                    + green
                    + "Total sub domain find in crtsh: "
                    + str(len(subdomains))
                )
            print(green + "[+] done")
        except:
            print("Something went wrong in crt sub domain finder")

    def valid_subdomain():
        if args.check == "yes":
            print(yellow + "[*] printing valid sub domains")
            f = open("result.txt", "r", encoding="UTF-8")
            for line in f:
                subdomain.append(line.strip())
                i = len(subdomain)
            ii = 0
            while ii < i:
                single_subdomain = subdomain[ii]
                ii += 1
                try:
                    response = requests.get(f"https://{single_subdomain}", timeout=20)
                    valid_subdomain_list.append(single_subdomain)
                    print(green + " [ 200 ] " + yellow + single_subdomain)
                except:
                    error_subdomain_list.append(single_subdomain)
            print(
                green
                + "[*] Total valid sub domain found: "
                + str(len(valid_subdomain_list))
            )
            # i = len(valid_subdomain_list)
            # ii = 0
            # while ii < i:
            #     single_subdomain = valid_subdomain_list[ii]
            #     ii += 1
            #     print(green + " [ 200 ] " + yellow + single_subdomain)
            print(green + "[+] done")
        elif args.fast == "no":
            print(red + "[-] sub domains are unverified")
            all_subdomain_s = list(set(all_subdomain))
            i = len(all_subdomain_s)
            print(green + "[*] Total sub domain found: " + str(i))
            ii = 0
            while ii < i:
                unverified_single_subdomain = all_subdomain_s[ii]
                ii += 1
                print(red + " [ 000 ] " + yellow + unverified_single_subdomain)
            print(green + "[+] done")

    def file_check():
        if args.remove:
            if os.path.exists("./result.txt"):
                os.remove("./result.txt")
                f_r = open("./result.txt", "w", encoding="utf-8")
                return f_r
            else:
                f_r = open("./result.txt", "w", encoding="utf-8")
                return f_r

    def file_check_1():
        if args.remove:
            if os.path.exists("./valid.txt"):
                os.remove("./valid.txt")
                f = open("./valid.txt", "w", encoding="utf-8")
                return f
            else:
                f = open("./valid.txt", "w", encoding="utf-8")
                return f

    def file_check_2():
        if args.remove:
            if os.path.exists("./invalid.txt"):
                os.remove("./invalid.txt")
                f_in = open("./invalid.txt", "w", encoding="utf-8")
                return f_in
            else:
                f_in = open("./invalid.txt", "w", encoding="utf-8")
                return f_in

    def write_file_1():
        file_name = main_system.file_check()
        all_subdomain_s = list(set(all_subdomain))
        i = int(len(all_subdomain_s))
        ii = int(0)
        while ii < i:
            single_data = str(all_subdomain_s[ii])
            file_name.write(f"{single_data}\n")
            ii += 1

    def write_file_2():
        file_name_2 = main_system.file_check_2()
        error_subdomain_list_s = list(set(error_subdomain_list))
        i = int(len(error_subdomain_list_s))
        ii = int(0)
        while ii < i:
            invalid_single_data = str(error_subdomain_list_s[ii])
            file_name_2.write(f"{invalid_single_data}\n")
            ii += 1

    def write_file_3():
        file_name_3 = main_system.file_check_1()
        valid_subdomain_list_s = list(set(valid_subdomain_list))
        i = int(len(valid_subdomain_list_s))
        ii = int(0)
        while ii < i:
            valid_single_data = str(valid_subdomain_list_s[ii])
            file_name_3.write(f"{valid_single_data}\n")
            ii += 1

    def banner():
        # banner system
        banner_style = [
            "3-d",
            "3x5",
            "5lineoblique",
            "acrobatic",
            "alligator",
            "alligator2",
            "alphabet",
            "avatar",
            "banner",
            "banner3-D",
            "banner3",
            "banner4",
            "barbwire",
            "basic",
            "bell",
            "big",
            "bigchief",
            "block",
            "broadway",
            "bubble",
            "bulbhead",
            "calgphy2",
            "caligraphy",
            "catwalk",
            "chunky",
            "coinstak",
            "colossal",
            "computer",
            "contessa",
            "contrast",
            "cosmic",
            "cosmike",
            "crawford",
            "cricket",
            "cyberlarge",
            "cybermedium",
            "cybersmall",
            "decimal",
            "diamond",
            "digital",
            "doh",
            "doom",
            "dotmatrix",
            "double",
            "drpepper",
            "dwhistled",
            "eftichess",
            "eftifont",
            "eftipiti",
            "eftirobot",
            "eftitalic",
            "eftiwall",
            "eftiwater",
            "epic",
            "fender",
            "fourtops",
            "fraktur",
            "fuzzy",
            "goofy",
            "gothic",
            "graceful",
            "gradient",
            "graffiti",
            "hex",
            "hollywood",
            "invita",
            "isometric1",
            "isometric2",
            "isometric3",
            "isometric4",
            "italic",
            "ivrit",
            "jazmine",
            "katakana",
            "kban",
            "l4me",
            "larry3d",
            "lcd",
            "lean",
            "letters",
            "linux",
            "lockergnome",
            "madrid",
            "marquee",
            "maxfour",
            "mike",
            "mini",
            "mirror",
            "mnemonic",
            "nancyj-fancy",
            "nancyj-underlined",
            "nancyj",
            "nipples",
            "nvscript",
            "o8",
            "octal",
            "ogre",
            "script",
            "shadow",
            "slant",
            "small",
            "smscript",
            "smshadow",
            "smslant",
            "standard",
            "term",
        ]

        random_banner_style = random.choice(banner_style)
        banner = pyfiglet.figlet_format("submix", font=random_banner_style)
        print(cyan + banner)
        print(yellow + "[*************] " + "created by Solaiman" + " [*************]")
        print(green + "[*] Target: " + main_system.get_data_by_rapiddns("web_url"))

    def main_text():
        main_system.banner()
        main_system.url_check()
        print(yellow + "[*] looking for sub domains....")
        if args.option == str(1) and args.check == "no":
            if int(main_system.get_data_by_rapiddns("subdomain_num").text) == 0:
                pass
            else:
                main_system.rapiddns_subdomain_collection_purify()
        elif args.option == str(2) and args.check == "no":
            main_system.crtsh()
        elif args.option == str(1) and args.check == "yes":
            if int(main_system.get_data_by_rapiddns("subdomain_num").text) == 0:
                pass
            else:
                main_system.rapiddns_subdomain_collection_purify()
                main_system.write_file_1()
                main_system.valid_subdomain()
                main_system.write_file_2()
                main_system.write_file_3()
        elif args.option == str(2) and args.check == "yes":
            main_system.crtsh()
            main_system.write_file_1()
            main_system.valid_subdomain()
            main_system.write_file_2()
            main_system.write_file_3()
        else:
            if int(main_system.get_data_by_rapiddns("subdomain_num").text) == 0:
                pass
            else:
                main_system.rapiddns_subdomain_collection_purify()
            main_system.crtsh()
            main_system.write_file_1()
            main_system.valid_subdomain()
            main_system.write_file_2()
            main_system.write_file_3()


try:
    main_system.main_text()
except KeyboardInterrupt:
    print(red + "Quitting now")
    print(green + "Thanks for using me....")
# except:
#     print(red + "[-] Something went wrong")
#     print(yellow + "[?] Please try again with a new terminal window")
