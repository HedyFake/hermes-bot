# Data live yang TIDAK ada di zip

Zip yang kamu kirim hanya berisi kode dan data awal (seed). Data yang terkumpul saat bot berjalan ada di VPS-mu. Ambil dengan cara berikut **sebelum** bot lama dimatikan.

| Data | Lokasi di VPS | Isinya | Cara ambil |
|---|---|---|---|
| PostgreSQL | database di `DATABASE_URL` | jadwal yang sudah diedit admin, pengingat, pengumuman, antrean review, klasifikasi pesan, akun LMS (terenkripsi), log audit, pemakaian model | `pg_dump -Fc -f hdybot.dump "$DATABASE_URL"` (atau `scripts/backup.sh` bawaan) |
| State lokal JSON | `data/runtime/bot-state.json` | **tugas, catatan, daftar anggota, pengurus, kontak dosen, skor/XP, sesi game, AFK** | salin file-nya langsung |
| Sesi WhatsApp | folder `WHATSAPP_AUTH_DIR` (default `./whatsapp-auth`) | sesi perangkat WA | **jangan dipindah ke Hermes**; Hermes menautkan WA sendiri (scan QR baru). Menjalankan dua klien pada satu sesi akan saling mengeluarkan. |
| Kunci enkripsi LMS | `LMS_ENCRYPTION_KEY` di `.env` | kunci pembuka kredensial LMS | tanpa kunci ini akun LMS harus dihubungkan ulang |

## Mengimpor ke SQLite Hermes
`bot-state.json` berisi tugas/catatan/anggota. Setelah kamu menyalinnya ke komputer ini, minta Hermes: *"impor data dari bot-state.json ke hdybot.sqlite (tabel tugas, catatan, anggota, xp)"*. Skema tabel kerja sudah disiapkan di `hdybot.sqlite`.

## Mengimpor Postgres (opsional)
Bila ingin memakai tabel Postgres asli: `createdb hdybot && psql hdybot < postgres/schema-gabungan.sql` lalu `pg_restore -d hdybot hdybot.dump`. Untuk kelas sebesar ini SQLite sudah cukup; Postgres hanya perlu bila mau membuka lagi kode lama.

## Catatan privasi
`bot-state.json`, `AuditLog`, `InboxMessage` memuat nama, nomor, dan isi chat teman sekelasmu. Perlakukan sebagai data pribadi: jangan unggah ke tempat umum dan hapus yang tidak perlu.
