from datetime import datetime
import os.path
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

class Instagram:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.fileName = self.username + "-Followers" + ".json"
        self.getUnFollowers()



    def signIn(self):
        self.browser.get("https://www.instagram.com/")
        time.sleep(3)

        #Email, kullanıcı adı, telefon numarası girebileceğimiz alanın adresi
        emailArea = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        #Bu adrese bilgileri yolluyoruz
        emailArea.send_keys(self.username)

        # Şifre girebileceğimiz alanın adresi
        passwordArea = self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
        #Şifre alanına bilgileri yolluyoruz.
        passwordArea.send_keys(self.password)

        #Giriş butonunun adresini alıyoruz
        enterButton = self.browser.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
        #Giriş butonuna tıklıyoruz.
        enterButton.click()
        time.sleep(5)

    def down(self):
        # Selenium ile Space tuşunu yollamak için tanımlama yapıyoruz
        action = webdriver.ActionChains(self.browser)

        #3 kere space tuşunu kullanıyoruz, sayfanın aşağı inmesine yardımcı oluyor
        for i in range(4):
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

        return True

    def followerList(self):
        self.signIn()


        # Profile gidiyoruz
        self.browser.get("https://www.instagram.com/" + self.username)
        time.sleep(2)

        # Takipçilerin görüntüleceği ekranı açmak için takipçi sayısı kutusu
        self.browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)

        # Takipçilerin görüntülendiği kutu
        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")

        # Ekranda gözüken kullanıcı sayısını saklıyoruz
        followerCount = len(dialog.find_elements_by_css_selector("li"))



        while True:
            # Dialog ekranını aktif ediyoruz
            dialog.click()

            #Sayfayı aşağı indirme fonksiyonu
            self.down()
            time.sleep(3)

            #Yüklenen yeni takipçi sayısını newCount değişkenine atıyoruz
            newCount = len(dialog.find_elements_by_css_selector("li"))

            #Eğer görüntülenen takipçi sayısı bir önceki sayıyla aynıysa artık yeni takipçi yüklenmiyordur. Farklıysa devam ediyoruz
            if followerCount != newCount:
                followerCount = newCount
                time.sleep(2)
            else:
                break

        #Tüm takipçilerin saklandığı değişken
        followers = dialog.find_elements_by_css_selector("li")

        #Takipçilerin linklerini saklayacağımız liste
        self.followersLink = []


        #Tüm takipçilerin profil adreslerini listeye ekliyoruz.
        for user in followers:
            userLink = user.find_element_by_css_selector("a").get_attribute("href")
            self.followersLink.append(userLink)

        #Listeyi geri dönderiyoruz
        return self.followersLink

    def getModifiedTime(self):
        time = os.path.getmtime(self.fileName)
        print("Takipçi Listesi En Son (Modified Time): "+datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')+ " Tarihinde Değiştirildi")


    #Takipçileri json dosyası olarak kaydeden fonksiyon
    def saveFollowers(self):
        followerList = self.followerList()
        with open(self.fileName, 'w') as json_dosya:
            json.dump(followerList, json_dosya)

    #Takipten çıkan kişileri yazdıran fonksiyon
    def getUnFollowers(self):


        #Eğer daha önceden oluşturulmuş bir liste mevcutsa çalışır
        if (os.path.isfile(self.fileName)):

            #Önceden kaydedilmiş takipçi listesini okuyoruz
            with open(self.fileName) as f:
                lastFollower = json.load(f)

                #Anlık olarak takipçi olanları listeye atıyoruz
                currentlyFollowers = self.followerList()

                #Listenin en son ne zaman güncellendiğini yazdırıyoruz.
                self.getModifiedTime()

                #Önceki takipçileri tek tek alıyoruz
                for i in lastFollower:

                    #Eğer önceden takip eden birisi şu an bulunan listede yoksa takipten çıkmış kabul ediyoruz.
                    if (i not in currentlyFollowers):
                        print(i + " unfollowed you..")

            #Sonradan kullanmak için güncel listeyi kaydediyoruz
            with open(self.fileName, 'w') as json_dosya:
                json.dump(currentlyFollowers, json_dosya)
                self.getModifiedTime()


        #Eğer takipçi listesi daha oluşturulmadıysa liste oluşturuyoruz
        else:
            print("Daha önce kaydedilmiş takipçi listesi bulunumadı, liste oluşturulacak..")
            print("Previously registered record list not found, list will be created..")
            self.saveFollowers()




Instagram()