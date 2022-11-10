from email.mime.multipart import MIMEMultipart
import cv2 # GORUNTU ISLEME ILE ILGILI FONKSIYONLARI KULLANMAK ICIN
import smtplib # YANGIN DURUMU TESPIT EDILIRSE MAIL GONDERMEK ICIN
import time

# mail gondermek icin bir fonksiyon kullandik
def send_mail(): # mail gönderme fonksiyonu // cihaz yangini gerekli miktarda tespit ettiğinde ilgili birime mail atacak
    msg=MIMEMultipart() # mesaj icerigi olusturmak icin
    msg['Subject'] = " Yangin Durumu Tespit Edildi ! " # mailin icerigi
    mail = smtplib.SMTP("smtp-mail.outlook.com",587) # smtp protokolü
    mail.ehlo()
    mail.starttls()
    mail.login("zakiryldz11@hotmail.com","yildiz-zakir112526") # maili gonderen kisinin mail bilgileri (gmail uzerinden gizlilik iznı vermek gerekebilir)
    mail.sendmail("zakiryldz11@hotmail.com", "yildizzakir0@gmail.com",msg.as_string())
    mail.quit()
    print("E-mail gönderildi, lütfen e-posta kutunuzu kontrol ediniz")

# bu kisimda videodaki yangin durumlarini goruntu isleme ile tespit edebiliyor
# vid=cv2.VideoCapture(0) idafesini yazsaydik goruntuyu kameradan alacaktik
parametreGoruntu=cv2.VideoCapture("Watch_ Massive forest fire in Turkey; choppers fill buckets at sea to douse flames; over 7 dead.mp4") # videodan tespit etmek için
yangin_cascade=cv2.CascadeClassifier("FireAndSmoke_Cascade.xml") # yanginla ilgili dataset dosyası
tespitSayisi=0 # bu tespit edilen yangin sayisi belli bir degerin ustunde tespit yapabilirse mail gonderir


while True:
    ret,kare=parametreGoruntu.read() # videodaki her bir goruntu frame adli degiskene kaydedilir ve her iterasyonda bu goruntu degisir
    kare=cv2.resize(kare,(480,360)) # goruntuyu yeniden boyutlandirarak daha kolay islem yapmayı saglar
    gray=cv2.cvtColor(kare,cv2.COLOR_BGR2GRAY) # rgb ren uzayindan bgr ve gri renk uzayına çeviriyoruz nesnenin daha kolay tespit edilebilmesi için cihazın öğrendiği bilgi ile parametredeki veriyi karşılaştırır
    yangin=yangin_cascade.detectMultiScale(gray,7,10) 
# Verilen görüntüde, basamaklı için eğitilmiş nesneleri içermesi muhtemel dikdörtgen bölgeler bulur ve bu bölgeleri bir dikdörtgen dizisi olarak döndürür. İşlev, görüntüyü farklı ölçeklerde birkaç kez tarar. Her seferinde görüntüdeki çakışan bölgeleri dikkate alır.

    for(x,y,w,h) in yangin: # tespit edilen bolge etrafina bir dikdortgen cizer
        cv2.rectangle(kare,(x,y),(x+w,y+h),(0,0,255),2) # tepit edilen bölgenin etrafına bir çerçeve ekler
        font1=cv2.FONT_HERSHEY_PLAIN
        cv2.putText(kare,"Fire and smoke",(x,y),font1,1,(0,255,0)) # tespit edilen bolgenin ustune "fire and smoke yazar"
        tespitSayisi+=1  # yangin tespit edilirse tespit sayisini tut
        print("Ates Ve Duman Tespit Edildi ! ",tespitSayisi)
        #time.sleep(0.05)
    if tespitSayisi >=10000: # 100 kez yangin durumu tespit edilirse mail gonderecek
        send_mail() # MAIL GONDER
        break # UYGULAMAYI SONLARDIR
    else:
        print("Ates ya da Duman Tespit Edilemedi !")
        #time.sleep(0.05)
    cv2.imshow("Yangin Tespiti",kare) # goruntuyu ekrana verir

    if cv2.waitKey(20)&0xFF==ord("q"): # UYGULAMA CALISIYORKEN  q  TUSUNA BASTIGINIZDA UYGULAMAYI KAPATIR
        break

parametreGoruntu.release() # GORUNTUYU EKRANA VER
cv2.destroyAllWindows() # UYGULAMA SONLANINCA TUM ACIK PENCERELERI KAPATIR