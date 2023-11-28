import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from interface import *


uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_QMainWindow()
ui.setupUi(pencere)
pencere.show()

#Veritabanı 

import sqlite3

baglanti = sqlite3.connect("musteri.db")
islem = baglanti.cursor()
baglanti.commit()

table = islem.execute("create table if not exists musteri (musteriAdi text, plaka text, telno int, marka text, hizmetturu text )")
baglanti.commit()
#  FONKSİYONLAR
def musteri_ekle():
    musteriAdi = ui.line_name.text()
    plaka = ui.linePlaka.text()
    telNo = ui.lineNo.text()
    marka = ui.combobx_marka.currentText()
    hizmetturu = ui.combobx_hizmet.currentText()



    try:
        ekle ="insert into musteri (musteriAdi,plaka,marka,telno,hizmetturu) values(?,?,?,?,?)"
        islem.execute(ekle,(musteriAdi,plaka,telNo,marka,hizmetturu))
        baglanti.commit()
        ui.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı..." , 5000 )
        kayit_listele()

    except Exception as error:
        ui.statusbar.showMessage("Kayıt Eklenemedi..=== "+str(error ))

def kayit_listele():
    ui.tableListe.clear()
    ui.tableListe.setHorizontalHeaderLabels(["MÜŞTERİ İSMİ", "TEL NO", "PLAKA", "HİZMET TÜRÜ", "MARKA"])
    ui.tableListe.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    sorgu = "select * from musteri"
    islem.execute(sorgu)

    for indexsatir, kayitNumarasi  in enumerate(islem):
        for indexsutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tableListe.setItem(indexsatir,indexsutun,QTableWidgetItem(str(kayitSutun)))

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere,"Silme Onayı","Silme İşlemini Onaylıyor musunuz ?",QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tableListe.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "delete from musteri where musteriAdi = ?"

        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla silindi...")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken hata Çıktı.."+str(error))
    else:
        ui.statusbar.showMessage("Kayıt Silme İşlemi İptal Edildi...")
       

def kategoriye_gore():
    listelenecek_kategori = ui.linePlaka_2.currentText()
    sorgu = "select * from musteri where plaka = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tableListe.clear()
    for indexsatir, kayitNumarasi  in enumerate(islem):
        for indexsutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tableListe.setItem(indexsatir,indexsutun,QTableWidgetItem(str(kayitSutun)))


# def kayit_guncelle():
#     message_guncelle = QMessageBox.question("Bu Kaydı Güncellemek İstediğinize Emin misiniz ? ",QMessageBox.Yes | QMessageBox.No)   
#     if message_guncelle ==  QMessageBox.Yes :
#         try:
#             musteri_adi = ui.line_name.text()
#             marka = ui.combobx_marka.currentText()
#             plaka = ui.linePlaka.text()
#             tel_no = ui.lineNo.text()
#             hizmet = ui.combobx_hizmet.currentText()



#buton işlemleri 
ui.button_ekle.clicked.connect(musteri_ekle)
ui.pushButton_5.clicked.connect(kayit_listele)
ui.button_sil.clicked.connect(kayit_sil)
ui.pushButton_6.clicked.connect(kategoriye_gore)
sys.exit(uygulama.exec_())




