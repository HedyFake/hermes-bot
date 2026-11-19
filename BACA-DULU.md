# Paket pindahan HdyBot → Hermes Agent

Isi paket ini diambil dari `bot-wa-main.zip`. Idenya: **Hermes jadi otaknya** (model, memori, pengingat, penghubung WhatsApp), sedangkan yang kamu bawa dari bot lama adalah **data, aturan, dan fitur** dalam bentuk skill.

## Pasang cepat
```bash
bash pasang.sh          # menyalin skill, database, dan persona ke ~/.hermes
```
Lalu di Hermes: mulai sesi baru (`/reset`) dan coba "jadwal besok" atau "hitung GCS E4 V5 M6".
Untuk menghubungkan WhatsApp, ikuti `hermes gateway setup` dan `hermes gateway start` (Hermes menautkan WA-nya sendiri; scan QR baru).

> Jujur soal pengujian: skrip Python dan pemasang sudah kujalankan dan lulus uji di sini. Hermes sendiri **belum** kujalankan, jadi pemuatan skill dan penyambungan WhatsApp di mesinmu belum teruji. Formatnya mengikuti dokumentasi Hermes (`~/.hermes/skills/<kategori>/<nama>/SKILL.md`).

## Isi paket
| Folder/berkas | Isi |
|---|---|
| `skills/hdybot/` | 8 skill: kelas, kalkulator, tugas-catatan, hiburan (**siap pakai, ada skrip**), akademik-keperawatan, lms-drive, admin-grup, katalog-perintah (**aturan + peta**) |
| `skills/hdybot/hdybot-katalog-perintah/references/` | **145 perintah, 307 alias, 8 halaman menu** (`commands.md`, `commands.json`) lengkap dengan peta ke skill |
| `database/hdybot.sqlite` | database siap pakai: 7 matkul, 15 sesi jadwal, 27 dosen, 32 relasi dosen–matkul, istirahat, 7 referensi SHJ + tabel kosong tugas/catatan/anggota/xp/pengingat |
| `database/csv/` | tabel yang sama dalam CSV |
| `database/postgres/` | `schema.prisma` (34 model, 3 enum), 5 migrasi, `schema-gabungan.sql`, seed, backup/restore |
| `database/AMBIL-DATA-LIVE-DARI-VPS.md` | **data yang tidak ada di zip** dan cara mengambilnya |
| `SOUL.md` | persona + aturan dasar untuk Hermes |
| `env.hermes.contoh` | variabel yang dipakai (tanpa nilai rahasia) |
| `docs-asli/`, `legacy-source/` | dokumen dan seluruh kode lama sebagai bahan porting |

## Apa yang diganti Hermes, apa yang dipindah
**Diganti Hermes (tidak perlu dibawa):** router model NVIDIA/OpenAI, adapter WhatsApp (wwebjs/baileys), dispatcher AI, worker pengingat, status/log/backup.
**Dipindah:** data kelas, kalkulator keperawatan, tugas/catatan, bank hiburan, aturan akademik, aturan keamanan, katalog perintah.
**Belum terpindah (perlu porting, 57 perintah):** LMS SHJ dan Google Drive (butuh kredensial milikmu), media (stiker, efek gambar, QR, OCR, TTS), sesi game grup + XP + leaderboard, pipeline klasifikasi grup → antrean review → kirim pengumuman. Kodenya lengkap di `legacy-source/`; opsi paling praktis: bungkus jadi server MCP (Hermes mendukung MCP) atau tulis ulang jadi skrip di skill terkait.

## ⚠️ Keamanan: baca sebelum jalan
1. **`.env` di zipmu berisi `NVIDIA_API_KEY` asli dan `DATABASE_URL`/`REDIS_URL`.** Aku tidak menyalinnya ke paket ini. Karena berkas itu sudah ikut terunggah, **anggap kunci itu bocor: buat kunci baru dan cabut yang lama.** Pastikan `.env` tidak ikut ke GitHub.
2. **Password admin = `hedyfake`**, tertulis sebagai nilai bawaan di `src/config/env.ts` dan di tes. Siapa pun yang punya kodenya tahu. Jangan pakai password itu lagi di tempat lain.
3. **Hermes adalah agen serbaguna yang punya tool terminal dan file.** Bot lama sengaja sempit (hanya perintah tertentu); Hermes tidak. Jangan buka ke grup tanpa membatasi: pakai allowlist pengguna, matikan tool yang tidak perlu lewat `hermes tools`, dan sebaiknya jalankan di profil/server terpisah (`hermes profile create`), bukan di laptop berisi data pribadimu.
4. `bot-state.json` dan tabel Postgres memuat nama, nomor, dan isi chat teman sekelas. Jaga sebagai data pribadi.

## Catatan kualitas data
- Semua data jadwal berstatus *USER_PROVIDED_PENDING_CONFIRMATION*: ruang, tahun ajaran, penugasan dosen per sesi, dan pengurus kelas **masih kosong** di seed. Isi dulu agar jawaban Hermes tidak "belum diketahui" terus.
- `docs-asli/DATABASE_SCHEMA.md` sudah usang (mendata 25 model); yang benar adalah `schema.prisma` (34 model, termasuk tabel multimodal).
- Bank hiburan di bot lama kecil (5 kutipan umum, 5 fakta, 3 pantun, 9 soal logika, dst). Hermes bisa membuat soal baru, tetapi tandai bila itu buatan model.
