#FurkanFilikci
import tkinter as tk
import random
from tkinter import messagebox

class YilanOyunu:
    def __init__(self, ana_pencere):
        self.ana_pencere = ana_pencere
        self.ana_pencere.title("Yılan Oyunu")
        self.canvas = tk.Canvas(ana_pencere, width=600, height=400, bg="black")
        self.canvas.pack()

        # Yılan özellikleri
        self.yilan_karakteri = "X"
        self.yilan = [[100, 100], [90, 100], [80, 100]]
        self.yon = "Sağ"
        self.siradaki_yon = "Sağ"  # Aynı anda birden fazla yöne geçişi önlemek için

        # Yiyecek özellikleri
        self.yiyecek_karakteri = "*"
        self.yiyecek = self.yeni_yiyecek()

        # Skor ve En yüksek skor
        self.skor = 0
        self.en_yuksek_skor = self.en_yuksek_skoru_yukle()

        # Duraklatma durumu
        self.paused = False
        self.after_id = None  # Oyun döngüsünün kontrolü için

        # Tuş bağlamaları
        self.ana_pencere.bind("<Up>", lambda e: self.yon_degistir("Yukarı"))
        self.ana_pencere.bind("<Down>", lambda e: self.yon_degistir("Aşağı"))
        self.ana_pencere.bind("<Left>", lambda e: self.yon_degistir("Sol"))
        self.ana_pencere.bind("<Right>", lambda e: self.yon_degistir("Sağ"))
        self.ana_pencere.bind("<space>", lambda e: self.toggle_pause())

        # Oyun döngüsü
        self.delay = 150
        self.game_loop()

        # Düğmeleri oluştur
        self.create_buttons()

    def yeni_yiyecek(self):
        while True:
            x = random.randint(1, 58) * 10
            y = random.randint(1, 38) * 10
            if [x, y] not in self.yilan:
                return [x, y]

    def en_yuksek_skoru_yukle(self):
        try:
            with open(".yilan_en_yuksek_skor.txt", "r") as dosya:
                return int(dosya.read())
        except FileNotFoundError:
            return 0

    def en_yuksek_skoru_kaydet(self):
        with open(".yilan_en_yuksek_skor.txt", "w") as dosya:
            dosya.write(str(self.en_yuksek_skor))

    def game_loop(self):
        if not self.paused:
            self.yon = self.siradaki_yon
            self.move_snake()
            self.check_collision()
            self.draw_canvas()

        self.after_id = self.ana_pencere.after(self.delay, self.game_loop)

    def move_snake(self):
        bas_x, bas_y = self.yilan[0]

        if self.yon == "Yukarı":
            bas_y -= 10
        elif self.yon == "Aşağı":
            bas_y += 10
        elif self.yon == "Sol":
            bas_x -= 10
        elif self.yon == "Sağ":
            bas_x += 10

        bas_x = bas_x % 600  # Yatayda sarılma
        bas_y = bas_y % 400  # Dikeyde sarılma

        self.yilan.insert(0, [bas_x, bas_y])

    def check_collision(self):
        bas_x, bas_y = self.yilan[0]

        if bas_x == self.yiyecek[0] and bas_y == self.yiyecek[1]:
            self.skor += 1
            self.yiyecek = self.yeni_yiyecek()
            if self.skor > self.en_yuksek_skor:
                self.en_yuksek_skor = self.skor
                self.en_yuksek_skoru_kaydet()

        else:
            self.yilan.pop()

        for bolum in self.yilan[1:]:
            if bas_x == bolum[0] and bas_y == bolum[1]:
                self.oyun_sonu()

    def yon_degistir(self, yon):
        zit_yonlar = {"Yukarı": "Aşağı", "Aşağı": "Yukarı", "Sol": "Sağ", "Sağ": "Sol"}
        if not self.paused and yon != zit_yonlar[self.yon]:
            self.siradaki_yon = yon

    def draw_canvas(self):
        self.canvas.delete("all")

        self.canvas.create_text(70, 10, text="Skor: " + str(self.skor), fill="white", anchor="nw")
        self.canvas.create_text(250, 10, text="Yılan Oyunu", fill="white", anchor="nw")
        self.canvas.create_text(470, 10, text="En Yüksek Skor: " + str(self.en_yuksek_skor), fill="white", anchor="nw")

        # Yılanı Çiz
        for bolum in self.yilan:
            x, y = bolum
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green", outline="black")

        # Yiyeceği Çiz
        yiyecek_x, yiyecek_y = self.yiyecek
        self.canvas.create_text(yiyecek_x + 5, yiyecek_y + 5, text=self.yiyecek_karakteri, fill="red")

        # Duraklama Ekranını Çiz
        if self.paused:
            self.canvas.create_rectangle(0, 0, 600, 400, fill="gray", stipple="gray12")
            self.canvas.create_text(300, 200, text="Duraklatıldı", fill="white", font=("Helvetica", 30), justify="center")

    def oyun_sonu(self):
        self.en_yuksek_skoru_kaydet()
        mesaj = f"Oyun Bitti!\nSkorunuz: {self.skor}\nEn Yüksek Skor: {self.en_yuksek_skor}\nTekrar oynamak ister misiniz?"
        cevap = messagebox.askyesno("Oyun Bitti", mesaj)
        if cevap:
            self.oyunu_yeniden_baslat()
        else:
            self.ana_pencere.quit()

    def oyunu_yeniden_baslat(self):
        self.yilan = [[100, 100], [90, 100], [80, 100]]
        self.yon = "Sağ"
        self.siradaki_yon = "Sağ"
        self.skor = 0
        self.yiyecek = self.yeni_yiyecek()
        self.paused = False
        self.game_loop()

    def toggle_pause(self):
        self.paused = not self.paused

        if not self.paused:
            self.game_loop()
        else:
            self.ana_pencere.after_cancel(self.after_id)

    def create_buttons(self):
        self.pause_button = tk.Button(self.ana_pencere, text="Duraklat", command=self.toggle_pause)
        self.pause_button.pack(side="left", padx=5)

        self.restart_button = tk.Button(self.ana_pencere, text="Yeniden Başlat", command=self.oyunu_yeniden_baslat)
        self.restart_button.pack(side="left", padx=5)

        self.quit_button = tk.Button(self.ana_pencere, text="Çıkış", command=self.ana_pencere.quit)
        self.quit_button.pack(side="right", padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    oyun = YilanOyunu(root)
    root.mainloop()

