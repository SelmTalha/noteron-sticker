#!/usr/bin/env python3 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets , uic
from PyQt5.QtWidgets import *
import sys,os

#Tasarımsal olarak ana mainin sola sabit kalması ve açılan not pencerelerinin hareketli olması fikri şahsıma aittir :) Tercihen bu durumu değiştirmek için 
# Mouse Event and Title Bar Move # içerisindeki fonksiyonları NotDefteri sınıfı içerisine alınız. Ve başlangıç konumunu değiştirdiğim NotDefteri sınıfı __init__ fonksiyonundaki
#self.move(100,200) satırını siliniz.
aktif=False
class NotDefteri(QMainWindow):
    def __init__(self):
        super(NotDefteri,self).__init__()
        uic.loadUi('notdefterim.ui',self)
        self.liste_goster()
        self.icons()
        self.move(100,200)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.secret_button.clicked.connect(self.showMinimized)
        self.listWidget.itemDoubleClicked.connect(self.not_goster)
        self.close_button.clicked.connect(sys.exit)
        self.not_ekle.clicked.connect(self.not_olustur)
        self.not_kaldir_button.clicked.connect(self.not_silme)
        self.secret_not.clicked.connect(self.gizli_notlari_goster)

    def icons(self):
        self.icon1 = QIcon()
        self.icon1.addPixmap(QPixmap("icons/secret.png"), QIcon.Normal, QIcon.Off)
        self.secret_not.setIcon(self.icon1)
        self.secret_not.setIconSize(QSize(18, 18))
        self.icon2=QIcon()
        self.icon2.addPixmap(QPixmap("icons/no_secret.png"), QIcon.Normal, QIcon.Off)

    def gizli_notlari_goster(self):
        file=open(".sifre.txt","r")
        sifre_listesi=[]
        for i in file:
            sifre_listesi.append(i)
        #Şifre ile fazla uğraşmak istemedim o yüzden otomatik şifre taini yapmadım.Manuel olarak yeni şifreler ekleyebilirsiniz .Gerek varsa :)
        #sifre_yeni=sifre_listesi[index] sondaki [:-1] ifadesinin sebebi listelerin sonunda \n olmasından kaynaklıydı sorun olurmu bilmiyorum ama yinede böyle yapmak istedim.
        #[:-1] ifadesinin önemi sadece liste sonu haricindekilere uygulanmalı son şifrenin bulunduğu indekste zaten \n bulunmuyor.
        sifre_1=sifre_listesi[0][:-1]
        sifre_2=sifre_listesi[1][:-1]
        sifre_3=sifre_listesi[2][:-1]
        sifre_4=sifre_listesi[3][:-1]
        sifre_5=sifre_listesi[4]
        global aktif
        if aktif==False:
            sifre, okPressed = QInputDialog.getText(self, "Admin Girişi","Gizli Dosyaları Sadece admin görebilir.\nAdmin Şifresini giriniz:", QLineEdit.Password, "********")
            if okPressed and (sifre == sifre_1 or sifre== sifre_2 or sifre==sifre_3 or sifre == sifre_4 or sifre == sifre_5):
                aktif=True
                self.listWidget.clear()
                self.gizli_liste()
                self.secret_not.setIcon(self.icon2)
                self.secret_not.setToolTip("Gizli Notları Kapat")
                self.frame.setStyleSheet("border-radius:25px;\n"
                "background-color: rgb(85, 87, 83);\n"
                "")
                self.label.setStyleSheet("color: rgb(238, 238, 236);\n"
                "")
                self.listWidget.setStyleSheet( "background-color: rgb(46, 52, 54);\n"
                "border-radius:5px;\n"
                "color: rgb(211, 215, 207);")
            elif okPressed and (sifre!="yalova26" or sifre !="sherlockholmes221" or sifre !="admin22126"):
                QMessageBox.warning(self, "Giriş Hatası", "Şifreyi hatalı girdiniz !")
            else:
                pass
        else:
            self.frame.setStyleSheet("border-radius:25px;\n"
            "background-color: rgb(114, 159, 207);\n"
            "")
            self.listWidget.setStyleSheet("background-color: rgb(52, 101, 164);\n"
            "border-radius:5px;\n"
            "color: rgb(211, 215, 207);")
            self.label.setStyleSheet("color: rgb(0, 0, 0);\n"
            "")
            self.listWidget.clear()
            self.liste_goster()
            self.secret_not.setIcon(self.icon1)
            aktif=False
            self.secret_not.setToolTip("Gizli Notları Göster")

    def gizli_liste(self):
        #Bu fonksiyonda os modülü ile dosya dizinini değiştirip dizindekileri listeleyip pyqt5 e yönlendirme ve daha sonrasında kod komutu main.py dizinine geri dönme işlemi yapıldı.
        a=os.getcwd()
        b=a+"/.gizli"
        os.chdir(b)
        c=os.listdir()
        for i in c: 
            self.listWidget.addItem(i[:-4]) 
        os.chdir(a)

    def not_silme(self):
        global aktif
        row=self.listWidget.currentRow()
        item=self.listWidget.item(row)
        if item is None:
            return
        reply=QMessageBox.warning(self, "Not Silme", "Bu işlem geri alınamaz.\nNotu silmek istediğinize emin misiniz ?",QMessageBox.Close|QMessageBox.Ok)
        if reply==QMessageBox.Ok:
            item=self.listWidget.takeItem(row)
            notadi=item.text()
            if aktif==False:
                os.remove(".notlar/{}.txt".format(notadi))
                del item
            else:
                os.remove(".gizli/{}.txt".format(notadi))
                del item
        else:
            pass
    
    def liste_goster(self):
        a=os.getcwd()
        b=a+"/.notlar"
        os.chdir(b)
        c=os.listdir()
        for i in c: 
            self.listWidget.addItem(i[:-4]) 
        os.chdir(a)

    def not_goster(self,item):
        pop=Not_Gosterici(item.text(),self)
        pop.show()

    def not_olustur(self):
        text, okPressed = QInputDialog.getText(self, "Not Oluşturma","Not için Başlık Giriniz:", QLineEdit.Normal, "Selolololoy")
        if okPressed and text != '':
            pop=Not_Gosterici(text,self)
            pop.show()
        else:
            pass
        self.listWidget.addItem(text)
        
class Not_Gosterici(QMainWindow):
    def __init__(self,name,parent):
        super(Not_Gosterici,self).__init__(parent)
        uic.loadUi('notyapragi.ui',self)
        self.item_name=name
        self.icerikgoster()
        self.not_basligi.setText(name)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.secret_button2.clicked.connect(self.showMinimized)
        self.close_button2.clicked.connect(self.kaydetvekapat)
        self.setWindowIcon(QIcon("icons/icon.png"))

    def icerikgoster(self):
        global aktif
        if aktif==False:
            try:
                with open(".notlar/{}.txt".format(self.item_name),"r") as f:
                    self.plainTextEdit.setPlainText(f.read())
            except Exception as ex: 
                print("Hata oluştu !",ex)
        else:
            try:
                with open(".gizli/{}.txt".format(self.item_name),"r") as f:
                    self.plainTextEdit.setPlainText(f.read())
            except Exception as ex: 
                print("Hata oluştu !",ex)

    def kaydetvekapat(self):
        global aktif
        if aktif==False:
            mytext = self.plainTextEdit.toPlainText()
            with open(".notlar/{}.txt".format(self.item_name),"w+") as f:
                f.write(mytext)
            self.close()
        else:
            mytext = self.plainTextEdit.toPlainText()
            with open(".gizli/{}.txt".format(self.item_name),"w+") as f:
                f.write(mytext)
            self.close()
    #############################################################################################
    # Mouse Event and Title Bar Move
    #############################################################################################

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    #############################################################################################

def main():
    app = QApplication(sys.argv) 
    be=NotDefteri()
    be.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()