import matplotlib.pyplot as plt
import sqlite3


baglantı= sqlite3.Connection("kullanıcılar.db")
cursor= baglantı.cursor()

def verilerial():
    cursor.execute("SELECT* FROM adaylar")
    data=cursor.fetchall()
    for i in data:
        print(i)

def tabloyu():
    cursor.execute("DELETE FROM adaylar")
    baglantı.commit()
    baglantı.close()

def veriekle(id, ad, soyad, numara, deneyim_yılı, en_iyi2dil, yaş, maaş_beklentisi, uzmanlık_alanı,
             matematik_bilgisi_puanı, sql_bilgisi_puanı, yaşadığı_şehir, çalıştığı_firma_sayısı, bir_adet_yönetilmiş_proje):
    veri= "INSERT INTO adaylar VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(veri,(id, ad,soyad, numara, deneyim_yılı, en_iyi2dil, yaş, maaş_beklentisi, uzmanlık_alanı,
                         matematik_bilgisi_puanı, sql_bilgisi_puanı, yaşadığı_şehir, çalıştığı_firma_sayısı, bir_adet_yönetilmiş_proje))
    baglantı.commit()

def tekfiltremaas(maaş_beklentisi):
    veri1 = "SELECT * FROM adaylar WHERE maaş_beklentisi = ?"
    cursor.execute(veri1, (maaş_beklentisi,))
    listeye_at= cursor.fetchall()
    print(listeye_at)
    baglantı.commit()

def tekfiltresehir(yaşadığı_şehir):
    veri1 = "SELECT * FROM adaylar WHERE yaşadığı_şehir = ?"
    cursor.execute(veri1, (yaşadığı_şehir,))
    listeye_at1= cursor.fetchall()
    print(listeye_at1)
    baglantı.commit()

def tekfiltredeneyimyılı(deneyim_yılı):
    veri1 = "SELECT * FROM adaylar WHERE deneyim_yılı = ?"
    cursor.execute(veri1, (deneyim_yılı,))
    listeye_at2= cursor.fetchall()
    print(listeye_at2)
    baglantı.commit()

def sadedegel2():
    cursor.execute(
        "SELECT * FROM adaylar WHERE (yaşadığı_şehir='Ankara' OR yaşadığı_şehir='İstanbul')"
        " AND sql_bilgisi_puanı>=3 AND matematik_bilgisi_puanı>=2 AND deneyim_yılı>11 AND "
        "deneyim_yılı>3 AND en_iyi2dil='python ve sql' AND uzmanlık_alanı LIKE '%senior%' AND uzmanlık_alanı LIKE '%veri bilimci%'"
        "AND çalıştığı_firma_sayısı>4 AND çalıştığı_firma_sayısı<10 AND yaş<50 AND yaş>40 "
        "AND matematik_bilgisi_puanı>4 AND sql_bilgisi_puanı>4 "
        "AND bir_adet_yönetilmiş_proje LIKE '%yapay zeka%' AND maaş_beklentisi<=35000 "
        "AND yaş>42 AND bir_adet_yönetilmiş_proje LIKE '%yapay zeka ve analizi%'")

    data3=cursor.fetchall()
    for i in data3:
        print(i)
    baglantı.commit()

def puanhesapla4(id):
    veri1 = "SELECT * FROM adaylar WHERE id = ?"
    cursor.execute(veri1, (id,))
    aday_bilgileri = cursor.fetchall()

    if len(aday_bilgileri) > 0:
        adi = aday_bilgileri[0][1]
        soyadi = aday_bilgileri[0][2]
        sql_bilgisi_puanı = aday_bilgileri[0][10]
        matematik_bilgisi_puanı = aday_bilgileri[0][9]
        deneyim_yılı = aday_bilgileri[0][4]


        sql_puanı = sql_bilgisi_puanı * 3
        matematik_puanı = matematik_bilgisi_puanı * 2
        deneyim_puanı = deneyim_yılı * 3
        adayın_puanı = matematik_puanı + sql_puanı + deneyim_puanı
        cursor.execute("UPDATE adaylar SET puan = ? WHERE id = ?", (adayın_puanı, id))

        print('kullanıcının id: ', id)
        print('Adı:', adi)
        print('Soyadı:', soyadi)
        print('SQL ilk Puanı:', sql_bilgisi_puanı)
        print('Matematik ilk Puanı:', matematik_bilgisi_puanı)
        print('adayın son sql puanı:', sql_puanı)
        print('adayın son matematik puanı:', matematik_puanı)
        print('Toplam Puanı:', adayın_puanı)
        print('Tüm Bilgiler:', aday_bilgileri)

    else:
        print("Bu id'ye sahip bir aday bulunamadı.")
    baglantı.commit()

def grafik_puan_dagılımı():
    veri1 = "SELECT puan FROM adaylar"
    cursor.execute(veri1)
    uygunluk_puanlari = cursor.fetchall()

    puanlar = [puan[0] for puan in uygunluk_puanlari]
    plt.hist(puanlar, bins=10, edgecolor='black')

    plt.title('Uygunluk Puanları Dağılımı')
    plt.xlabel('Puan')
    plt.ylabel('Kişi Sayısı')

    plt.show()

def enyuksek_puana_oran():
    veri1 = "SELECT puan FROM adaylar"
    cursor.execute(veri1)
    uygunluk_puanlari = cursor.fetchall()

    puanlar = [puan[0] for puan in uygunluk_puanlari]
    en_yuksek_puan = max(puanlar)

    oranlar = [puan / en_yuksek_puan for puan in puanlar]
    plt.hist(oranlar, bins=10, edgecolor='black')

    plt.title('En Yüksek Puanlı Adaya Oranlar')
    plt.xlabel('Oran')
    plt.ylabel('Kişi Sayısı')

    plt.show()

def en_uygunun_verimliligi():
    veri1 = "SELECT puan FROM adaylar"
    cursor.execute(veri1)
    uygunluk_puanlari = cursor.fetchall()
    puanlar = [puan[0] for puan in uygunluk_puanlari]
    en_yuksek_puan = max(puanlar)

    ihtimaller = [puan / en_yuksek_puan for puan in puanlar]
    plt.hist(ihtimaller, bins=10, edgecolor='black')

    plt.title('En Uygun Adayın Seçilme İhtimalleri')
    plt.xlabel('Seçilme İhtimali')
    plt.ylabel('Kişi Sayısı')
    plt.show()



#sadedegel2()

#veriekle()
#verilerial()
#tekfiltremaas()

#tekfiltresehir('Ankara')
#tekfiltredeneyimyılı()
#puanhesapla4(10)
#rafik_puan_dagılımı()
#enyuksek_puana_oran()
#en_uygunun_verimliligi()




baglantı.close()




