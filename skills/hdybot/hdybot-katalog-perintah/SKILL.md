---
name: hdybot-katalog-perintah
description: Peta lengkap perintah bertitik HdyBot lama (.jadwal, .tugas, .ask, .lms, dst) ke skill Hermes yang menanganinya. Pakai saat pengguna mengetik perintah berawalan titik atau bertanya "menu"/"bisa apa saja".
version: 1.0.0
---

# Katalog perintah HdyBot

Pengguna kelas terbiasa dengan perintah berawalan `.` (contoh `.jadwal besok`, `.tugas`, `.ask ...`). Perlakukan itu sebagai **permintaan biasa**: cari perintahnya di `references/commands.json`, lalu jalankan skill yang tertera.

- `references/commands.md`: 8 halaman menu asli + tabel perintah → skill → strategi.
- `references/commands.json`: data mesin (145 perintah kanonik, 307 alias, 51 khusus admin) dengan kolom `skill`, `strategi`, `catatan`, `contoh_sintaks`.

## Cara memakai
1. Pesan diawali `.` → ambil kata pertama sebagai alias, cari di `commands.json` (`aliases`).
2. `strategi = skrip` → jalankan skrip skill terkait. `hermes-native` → kerjakan sendiri dengan aturan di SKILL terkait. `perlu-port` → jelaskan jujur bahwa fitur itu belum dipasang. `diganti-hermes` → arahkan ke fungsi Hermes yang setara.
3. Perintah **khusus admin** (`akses` memuat "Admin") hanya dilayani untuk owner/admin di chat pribadi.
4. `.menu` / `.help` → tampilkan halaman dari `halaman_menu`, **hanya fitur yang benar-benar terpasang** (strategi bukan `perlu-port`) untuk pengguna biasa.
5. Perintah tak dikenal: jangan mengarang; tawarkan padanan terdekat.

## Menu ringkas untuk pengguna
📚 Info kelas · 🕒 Jadwal & tugas · 🧠 Belajar & materi · 🎮 Permainan · 🎨 Media · 🛠️ Utilitas · 🎓 LMS SHJ · 🔐 Administrasi (hanya admin)
