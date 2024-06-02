#Bu kod Mert Bülbül (220502006) ve Can Şafak Çakır (220502002) tarafından hazırlanmıştır

import tkinter as tk
from tkinter import simpledialog, messagebox
import random
class MantikDevreSimulatoru:
    def __init__(self, ana_pencere):
        self.ana_pencere = ana_pencere
        self.ana_pencere.title("Mantık Devre Simülatörü")
        self.bilesenler = []
        self.baglanti_modu = False
        self.secili_bilesen = None

        self.arayuz_olustur()

    def arayuz_olustur(self):

        ana_cerceve = tk.Frame(self.ana_pencere, padx=10, pady=10)
        ana_cerceve.pack(fill=tk.BOTH, expand=True)


        araclar_cercevesi = tk.LabelFrame(ana_cerceve, text="Araçlar", padx=10, pady=10)
        araclar_cercevesi.pack(side=tk.LEFT, fill=tk.Y)


        kapilar_cercevesi = tk.LabelFrame(araclar_cercevesi, text="Mantık Kapıları", padx=10, pady=10)
        kapilar_cercevesi.pack(fill=tk.X, pady=5)
        self.arac_dugmesi_ekle(kapilar_cercevesi, "NOT Kapısı", self.not_kapisi_ekle, {"etiket": "NOT Kapısı", "giris_sayisi": 1})
        self.arac_dugmesi_ekle(kapilar_cercevesi, "Buffer", self.buffer_ekle, {"etiket": "Buffer", "giris_sayisi": 1})
        self.arac_dugmesi_ekle(kapilar_cercevesi, "AND Kapısı", self.and_kapisi_ekle, {"etiket": "AND Kapısı", "giris_sayisi": 2})
        self.arac_dugmesi_ekle(kapilar_cercevesi, "OR Kapısı", self.or_kapisi_ekle, {"etiket": "OR Kapısı", "giris_sayisi": 2})
        self.arac_dugmesi_ekle(kapilar_cercevesi, "NAND Kapısı", self.nand_kapisi_ekle, {"etiket": "NAND Kapısı", "giris_sayisi": 2})
        self.arac_dugmesi_ekle(kapilar_cercevesi, "NOR Kapısı", self.nor_kapisi_ekle, {"etiket": "NOR Kapısı", "giris_sayisi": 2})
        self.arac_dugmesi_ekle(kapilar_cercevesi, "XOR Kapısı", self.xor_kapisi_ekle, {"etiket": "XOR Kapısı", "giris_sayisi": 2})
        self.arac_dugmesi_ekle(kapilar_cercevesi, "XNOR Kapısı", self.xnor_kapisi_ekle, {"etiket": "XNOR Kapısı", "giris_sayisi": 2})


        giris_cikis_cercevesi = tk.LabelFrame(araclar_cercevesi, text="Giriş Çıkış Elemanları", padx=10, pady=10)
        giris_cikis_cercevesi.pack(fill=tk.X, pady=5)
        self.arac_dugmesi_ekle(giris_cikis_cercevesi, "Giriş Kutusu", self.giris_kutusu_ekle, {"etiket": "Giriş Kutusu", "renk": "green"})
        self.arac_dugmesi_ekle(giris_cikis_cercevesi, "Çıkış Kutusu", self.cikis_kutusu_ekle, {"etiket": "Çıkış Kutusu", "renk": "red"})
        self.arac_dugmesi_ekle(giris_cikis_cercevesi, "LED", self.led_ekle, {"etiket": "LED", "renk": "red"})


        baglanti_cercevesi = tk.LabelFrame(araclar_cercevesi, text="Bağlantı Elemanları", padx=10, pady=10)
        baglanti_cercevesi.pack(fill=tk.X, pady=5)
        self.arac_dugmesi_ekle(baglanti_cercevesi, "Çizgi Çizme", self.baglanti_modu_aktif, {"etiket": "Çizgi Çizme", "renk": "black"})


        kontrol_tuslari_cercevesi = tk.LabelFrame(ana_cerceve, text="Kontrol Tuşları", padx=10, pady=10)
        kontrol_tuslari_cercevesi.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        self.kontrol_dugmesi_ekle(kontrol_tuslari_cercevesi, "Çalıştır", self.simulasyonu_calistir)
        self.kontrol_dugmesi_ekle(kontrol_tuslari_cercevesi, "Reset", self.simulasyonu_sifirla)
        self.kontrol_dugmesi_ekle(kontrol_tuslari_cercevesi, "Durdur", self.simulasyonu_durdur)


        tasarim_cercevesi = tk.Frame(ana_cerceve, bg="white", padx=10, pady=10)
        tasarim_cercevesi.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tasarim_alani = tk.Canvas(tasarim_cercevesi, bg="white")
        self.tasarim_alani.pack(fill=tk.BOTH, expand=True)

    def arac_dugmesi_ekle(self, cerceve, metin, komut, ozellikler):
        dugme = tk.Button(cerceve, text=metin, command=lambda: komut(ozellikler))
        dugme.pack(fill=tk.X, pady=2)

    def kontrol_dugmesi_ekle(self, cerceve, metin, komut):
        dugme = tk.Button(cerceve, text=metin, command=komut)
        dugme.pack(fill=tk.X, pady=2)

    def bilesen_ekle(self, bilesen):
        self.bilesenler.append(bilesen)
        self.tasarim_alani.tag_bind(bilesen.ogeci, "<Button-3>", lambda event, b=bilesen: self.ozellikleri_goster(b))
        self.tasarim_alani.tag_bind(bilesen.ogeci, "<Button-1>", lambda event, b=bilesen: self.baglanti_belirle(b))

    def not_kapisi_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.not_kapisi, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def buffer_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.buffer, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def and_kapisi_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.and_kapisi, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def or_kapisi_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.or_kapisi, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def nand_kapisi_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.nand_kapisi, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def nor_kapisi_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.nor_kapisi, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def xor_kapisi_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.xor_kapisi, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def xnor_kapisi_ekle(self, ozellikler):
        bilesen = MantikKapi(self.tasarim_alani, **ozellikler, fonksiyon=self.xnor_kapisi, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def giris_kutusu_ekle(self, ozellikler):
        bilesen = GirisKutusu(self.tasarim_alani, **ozellikler, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def cikis_kutusu_ekle(self, ozellikler):
        bilesen = CikisKutusu(self.tasarim_alani, **ozellikler, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def led_ekle(self, ozellikler):
        bilesen = LED(self.tasarim_alani, **ozellikler, koordinat=self.yeni_bilesen_koordinat())
        self.bilesen_ekle(bilesen)

    def yeni_bilesen_koordinat(self):
        x = random.randint(50, 450)
        y = random.randint(50, 450)
        return (x, y)

    def baglanti_modu_aktif(self, ozellikler):
        self.baglanti_modu = not self.baglanti_modu
        if self.baglanti_modu:
            messagebox.showinfo("Bağlantı Modu", "Bağlantı modu aktif!")
        else:
            self.secili_bilesen = None
            messagebox.showinfo("Bağlantı Modu", "Bağlantı modu kapalı!")

    def baglanti_belirle(self, bilesen):
        if self.baglanti_modu:
            if not self.secili_bilesen:
                self.secili_bilesen = bilesen
            else:
                self.secili_bilesen.baglanti_ekle(bilesen)
                self.secili_bilesen = None

    def ozellikleri_goster(self, bilesen):
        yeni_deger = simpledialog.askstring("Özellikleri Değiştir", "Yeni değer:")
        if yeni_deger is not None:
            bilesen.deger = yeni_deger
            if isinstance(bilesen, LED):
                if bilesen.deger == "1":
                    bilesen.led_rengi = "red"
                else:
                    bilesen.led_rengi = "grey"
                bilesen.calistir()

        else:
            self.tasarim_alani.itemconfig(bilesen.ogeci, text=f"{bilesen.etiket}\n{yeni_deger}")

    def simulasyonu_calistir(self):
        for bilesen in self.bilesenler:
            bilesen.calistir()

    def simulasyonu_sifirla(self):
        self.tasarim_alani.delete("all")
        self.bilesenler = []

    def simulasyonu_durdur(self):
        messagebox.showinfo("Simülasyon Durduruldu", "Simülasyon durduruldu!")

    def not_kapisi(self, degerler):
        return [not degerler[0]]

    def buffer(self, degerler):
        return [degerler[0]]

    def and_kapisi(self, degerler):
        return [all(degerler)]

    def or_kapisi(self, degerler):
        return [any(degerler)]

    def nand_kapisi(self, degerler):
        return [not all(degerler)]

    def nor_kapisi(self, degerler):
        return [not any(degerler)]

    def xor_kapisi(self, degerler):
        return [degerler[0] != degerler[1]]

    def xnor_kapisi(self, degerler):
        return [degerler[0] == degerler[1]]

class Bilesen:
    def __init__(self, canvas, etiket, koordinat, renk="black"):
        self.canvas = canvas
        self.etiket = etiket
        self.koordinat = koordinat
        self.renk = renk
        self.baglantilar = []
        self.deger = 0
        self.ogeci = None
        self.ogec_olustur()

    def ogec_olustur(self):
        x, y = self.koordinat
        self.ogeci = self.canvas.create_rectangle(x-30, y-15, x+30, y+15, fill=self.renk, outline="black")
        self.text = self.canvas.create_text(x, y, text=self.etiket, fill="white")


    def baglanti_ekle(self, bilesen):
        self.baglantilar.append(bilesen)
        x1, y1 = self.koordinat
        x2, y2 = bilesen.koordinat
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST)

    def calistir(self):
        for bilesen in self.baglantilar:
            bilesen.deger = self.deger

class MantikKapi(Bilesen):
    def __init__(self, canvas, etiket, koordinat, fonksiyon, giris_sayisi):
        super().__init__(canvas, etiket, koordinat)
        self.fonksiyon = fonksiyon
        self.giris_sayisi = giris_sayisi
        self.girisler = []

    def calistir(self):
        self.girisler = [baglanti.deger for baglanti in self.baglantilar[:self.giris_sayisi]]
        self.deger = self.fonksiyon(self.girisler)[0]
        super().calistir()

class GirisKutusu(Bilesen):
    def __init__(self, canvas, etiket, koordinat, renk="green"):
        super().__init__(canvas, etiket, koordinat, renk)

    def ogec_olustur(self):
        x, y = self.koordinat
        self.ogeci = self.canvas.create_rectangle(x-30, y-15, x+30, y+15, fill=self.renk, outline="black")
        self.text = self.canvas.create_text(x, y, text=self.etiket, fill="white")


class CikisKutusu(Bilesen):
    def __init__(self, canvas, etiket, koordinat, renk="red"):
        super().__init__(canvas, etiket, koordinat, renk)

    def ogec_olustur(self):
        x, y = self.koordinat
        self.ogeci = self.canvas.create_rectangle(x-30, y-15, x+30, y+15, fill=self.renk, outline="black")
        self.text = self.canvas.create_text(x, y, text=self.etiket, fill="white")


class LED(Bilesen):
    def __init__(self, canvas, etiket, koordinat, renk="red"):
        super().__init__(canvas, etiket, koordinat, renk)
        self.led_kapali_rengi = "red"
        self.led_acik_rengi = "green"

    def calistir(self):
        if self.deger == "1":
            self.canvas.itemconfig(self.ogeci, fill=self.led_acik_rengi)
        else:
            self.canvas.itemconfig(self.ogeci, fill=self.led_kapali_rengi)




if __name__ == "__main__":
    root = tk.Tk()
    app = MantikDevreSimulatoru(root)
    root.mainloop()
