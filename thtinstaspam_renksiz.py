# coding=utf-8
#!/usr/bin/env python3

""" 
Programı değiştirip bir yerde yayınlamadan önce lütfen
bu programın GPLv3 lisansı altında olduğunu unutmayınız.

Daha Fazla Bilgi:
https://tr.wikipedia.org/wiki/GNU_Genel_Kamu_Lisans%C4%B1
https://www.gnu.org/licenses/quick-guide-gplv3.html
"""

__author__ = "Hichigo TurkHackTeam"
__license__ = "GPLv3"
__version__ = "1.5.0"
__status__ = "Geliştiriliyor"
from random import choice
from multiprocessing import Process

try:
    from requests.sessions import Session
    from requests import get
except:
    print("'requests' Modülünüz eksik indirmek için 'pip3 install requests' komutunu kullanın!")

BANNER = """
  dBBBBBBP dBP dBP  dBBBBBBP    dBP dBBBBb.dBBBBP dBBBBBBP dBBBBBb       .dBBBBP dBBBBBb dBBBBBb     dBBBBBBb
                                       dBPBP                    BB       BP          dB'      BB      '   dB'
   dBP   dBBBBBP     dBP      dBP dBP dBP `BBBBb   dBP      dBP BB       `BBBBb  dBBBP'   dBP BB   dB'dB'dB' 
  dBP   dBP dBP     dBP      dBP dBP dBP     dBP  dBP      dBP  BB          dBP dBP      dBP  BB  dB'dB'dB'  
 dBP   dBP dBP     dBP      dBP dBP dBP dBBBBP'  dBP      dBBBBBBB     dBBBBP' dBP      dBBBBBBB dB'dB'dB'   
    Yapımcı: Hichigo THT   Sürüm: Renksiz
"""

USER_AGENTS = ["Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0",
"Mozilla/5.0 (Android 4.4; Tablet; rv:41.0) Gecko/41.0 Firefox/41.0",
"Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"]

USER_AGENT = choice(USER_AGENTS)

class Client:
    def __init__(self,username,password,proxy):
        self.ses = Session()
        self.loggedIn = False
        self.username = username
        self.password = password
        self.proxy = proxy
    
    def Login(self):
        if self.loggedIn == True:
            return None
        
        loginData = {
            "password":self.password,
            "username":self.username,
            "queryParams":"{}"
        }
        homePageResponse = self.ses.get("https://www.instagram.com/accounts/login/")
        loginHeaders = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip,deflate,br",
            "Accept-Language":"en-US,en;q=0.5",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "Host":"www.instagram.com",
            "Referer":"https://www.instagram.com/accounts/login/",
            "X-Requested-With":"XMLHttpRequest",
            "X-Instagram-AJAX":"1",
            "User-Agent":USER_AGENT,
            "X-CSRFToken":homePageResponse.cookies.get_dict()["csrftoken"],
        }
        "Hichigo Was Here THT"
        loginCookies = {
            "rur":"PRN",
            "csrftoken":homePageResponse.cookies.get_dict()["csrftoken"],
            "mcd":homePageResponse.cookies.get_dict()["mcd"],
            "mid":homePageResponse.cookies.get_dict()["mid"]
        }
        self.ses.headers.update(loginHeaders)
        self.ses.cookies.update(loginCookies)

        loginPostResponse = self.ses.post("https://www.instagram.com/accounts/login/ajax/",data=loginData)
    
        if loginPostResponse.status_code == 200 and loginPostResponse.json()["authenticated"] == True:
            self.loggedIn = True
            mainPageResponse = self.ses.get("https://www.instagram.com/")
            self.ses.cookies.update(mainPageResponse.cookies)
    
    def Spam(self,username,userid):
        if self.loggedIn == False:
            return None   

        link = "https://www.instagram.com/" + username + "/"
        profileGetResponse = self.ses.get(link)
        self.ses.cookies.update(profileGetResponse.cookies)
        spamHeaders = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip,deflate,br",
            "Accept-Language":"en-US,en;q=0.5",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "DNT":"1",
            "Host":"www.instagram.com",
            "X-Instagram-AJAX":"2",
            "X-Requested-With":"XMLHttpRequest",
            "Referer":link,
            "User-Agent":USER_AGENT,
            "X-CSRFToken":profileGetResponse.cookies.get_dict()["csrftoken"],
        }
        spamData = {
            "reason_id":"1",
            "source_name":"profile"
        }

        self.ses.headers.update(spamHeaders)

        spamPostResponse = self.ses.post("https://www.instagram.com/users/"+ userid +"/report/",data=spamData)
        if spamPostResponse.status_code == 200 and spamPostResponse.json()["description"] == "Your reports help keep our community free of spam.":
            self.ses.close()
            return True
        else:
            return False

def Success(username,shit):
    print("[" + username +"]"
    + " " + shit)

def Fail(username,shit):
    print("[" + username +"]"
    + " " + shit)

def Status(shit):
    print("[ THT Insta SPAM ]"
    + " " + shit)

def DoitAnakin(reportedGuy,reportedGuyID,username,password,proxy):
    try:
        insta = None
        if proxy != None:
            insta = Client(username,password,None)
        else:
            insta = Client(username,password,None)
        insta.Login()
        result = insta.Spam(reportedGuy,reportedGuyID)
        if insta.loggedIn == True and result == True:
            Success(username,"Başarıyla SPAM atıldı!")
        elif insta.loggedIn == True and result == False:
            Fail(username,"Giriş başarılı ama SPAM atılması başarısız!")
        elif insta.loggedIn == False:
            Fail(username,"Giriş başarısız!")
    except:
        Fail(username,"Giriş yapılırken hata oluştu!")

if __name__ == "__main__":
    userFile = open("kullanicilar.txt","r")

    USERS = []
    for user in userFile.readlines():
        if user.replace("\n","").replace("\r","\n") != "":
            USERS.append(user.replace("\n","").replace("\r","\n"))


    print(BANNER)
    Status(str(len(USERS)) + " Adet Kullanıcı Yüklendi!\n")
    reportedGuy = input( "SPAM'lanacak Kişinin Kullanıcı Adı: ")
    reportedGuyID = input( "SPAM'lanacak Kişinin User ID'si: ")
    print("")
    Status("Saldırı başlatılıyor!\n")

    for user in USERS:
        p = Process(target=DoitAnakin,args=(reportedGuy,reportedGuyID,user.split(" ")[0],user.split(" ")[1],None))
        p.start()
