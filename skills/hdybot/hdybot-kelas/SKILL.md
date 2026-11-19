---
name: hdybot-kelas
description: Info kelas Nursing Class A Semester 5A (jadwal kuliah, mata kuliah, SKS, dosen, pengurus, referensi SHJ, hitung mundur, bagi kelompok). Pakai saat ditanya jadwal, matkul, dosen, kuliah berikutnya.
version: 1.0.0
---

# Kelas Nursing Class A · Semester 5A

Data ada di SQLite `$HDYBOT_DB` (default `~/.hermes/hdybot/hdybot.sqlite`). Jangan menjawab jadwal dari ingatan: selalu jalankan skrip.

## Kapan dipakai
Pertanyaan seperti "jadwal hari ini/besok/senin", "kuliah berikutnya", "matkul apa saja", "dosen gerontik", "bagi kelompok".

## Perintah
```bash
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py jadwal            # hari ini (WIB)
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py jadwal besok|senin|minggu
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py next
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py matkul
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py dosen [kode/nama matkul]
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py kelas | pengurus | referensi
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py hitungmundur 2026-12-20
python3 ~/.hermes/skills/hdybot/hdybot-kelas/scripts/kelas.py kelompok 3 Ani,Budi,Cici,Dedi
```

## Aturan (diwarisi dari bot lama)
- Zona waktu **Asia/Jakarta**. Jadwal berulang mingguan, Senin–Jumat.
- Jangan mengarang dosen, ruang, tanggal, tenggat, atau aturan kampus. Ruang dan penugasan dosen per sesi **belum terkonfirmasi** (kolom kosong = belum diketahui, katakan begitu).
- SKS adalah atribut matkul (7 matkul, 22 SKS unik); jangan dijumlah per sesi.
- Nama dosen dengan variasi penulisan tidak digabung otomatis.
- Semua data berstatus `USER_PROVIDED_PENDING_CONFIRMATION`: sebut itu bila relevan.
- Mengubah jadwal (tambah/ubah/hapus) hanya atas permintaan pemilik/admin dan setelah konfirmasi eksplisit; tulis langsung ke tabel `jadwal` lalu tunjukkan hasilnya.
