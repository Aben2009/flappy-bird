# Flappy Bird (Python & Pygame)

Salah satu program pertama saya waktu belajar coding: versi sederhana Flappy Bird.
Semua grafis (burung, pipa, tanah) digambar langsung lewat kode, tanpa file gambar atau suara.

> Dibuat saat belajar Python di kelas coding. 

## Cara main

Terbangkan burung melewati celah pipa tanpa menabrak pipa atau tanah.
Setiap pipa yang berhasil dilewati = +1 skor.

| Tombol | Fungsi |
|---|---|
| `Spasi` / klik kiri mouse | Terbang (flap), mulai game, main lagi |
| `R` | Restart |
| `Esc` | Keluar |

## Fitur

- Layar mulai dengan animasi burung naik-turun
- Skor dan high score (selama game terbuka)
- Pipa dengan posisi celah acak
- Gravitasi, batas kecepatan jatuh, dan deteksi tabrakan

## Cara menjalankan

pip install -r requirements.txt
python flappy.py


Butuh Python 3 dan Pygame.

## Yang saya pelajari

- Game loop: update posisi dan gambar ulang 60 kali per detik
- Fisika sederhana: gravitasi dan lompatan
- Deteksi tabrakan pakai `pygame.Rect`
- State game (start, playing, game over)
- Membuat rintangan acak dengan `random`

## Ide pengembangan

- Simpan high score ke file supaya tidak hilang saat game ditutup
- Pakai variabel `rotation` agar burung miring saat naik/turun
- Buat font sekali di awal, bukan setiap frame (lebih hemat)
- Tambah suara, awan bergerak, dan tingkat kesulitan yang naik seiring skor
