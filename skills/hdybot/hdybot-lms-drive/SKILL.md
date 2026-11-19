---
name: hdybot-lms-drive
description: Integrasi LMS STIKES Husada Jombang (lms.shj.ac.id) dan Google Drive materi kelas. Pakai untuk dashboard LMS, materi, tugas, kuis, dan katalog/unduh dokumen Drive. Butuh kredensial milik pengguna, belum bisa jalan tanpa porting.
version: 1.0.0
---

# LMS SHJ & Google Drive

**Status: perlu port.** Kode aslinya ada di `legacy-source/src/modules/lms/` (client, parser, katalog, service) dan `legacy-source/src/modules/materials/drive.ts`. Skill ini mendokumentasikan perilaku dan batas keamanannya supaya Hermes (atau kamu) bisa menulis ulang sebagai skrip atau server MCP.

## LMS: perilaku bot lama
- Penghubungan akun **per nomor WhatsApp pengirim**, diverifikasi NIM lewat dashboard kampus. Perintah: `.lms <nama> hubungkan <password>` (hanya di DM), `hubungkan-nim <NIM> <password>`.
- Setelah terhubung: `dashboard`, `matkul [kata]`, `detail`, `dosen`, `materi [list|terbaru|baru|cari|detail|kirim <ID>]`, `tugas [pending|terbaru|selesai|cari|detail|deadline]`, `kuis [aktif|terbaru|detail]`, `sync [status|pause|resume|history]`, `notif on|off`, `ai on|off`, `ask/summarize/flashcard/quiz belajar`, `logout`.
- Sinkronisasi berkala (default 45 menit, 30 menit–1 hari), maksimal 2 akun per putaran, crawler maksimal 30 halaman per putaran dengan jeda.
- Hanya HTTPS pada origin `lms.shj.ac.id`; CAPTCHA/OTP harus interaksi resmi.

## Aturan keamanan (wajib dipertahankan)
1. Password dan sesi **tidak pernah** ditulis ke memori Hermes, log, atau chat grup. Bot lama menyimpannya terenkripsi (AES-256-GCM, terikat nomor+NIM) dengan kunci `LMS_ENCRYPTION_KEY`; simpan kunci itu bersama backup, atau akun harus dihubungkan ulang.
2. Login, kredensial, dan data LMS hanya lewat **DM** pemilik akun. Dari grup, hasil dikirim ke DM pengirim.
3. Kutipan materi LMS dikirim ke model AI **hanya bila pemilik memberi izin** (`ai on`), dan materi LMS tidak disisipkan di jawaban grup.
4. Membuka/mengunduh materi bisa mengubah status baca di LMS; beri tahu pengguna.
5. Minta pengguna menghapus pesan yang berisi password setelah login.

## Google Drive
- Folder materi dibaca dengan **akun layanan** (`GOOGLE_APPLICATION_CREDENTIALS`), ID folder di `GOOGLE_DRIVE_FOLDER_ID`.
- Hanya chat yang diizinkan pemilik (`GOOGLE_DRIVE_ALLOWED_CHATS`) boleh menerima isi folder; periksa izin unduh, ukuran, dan MIME setiap kali.
- Perintah: `.materi`, `.carimateri <kata>`, `.drive status|sync|files|search`, `.download <id>`, `.tanyadokumen <id> <tanya>`, `.ringkasdokumen <id>`.
- Ekstraksi teks PDF memakai poppler dan OCR memakai tesseract (`legacy-source/src/modules/materials/extract.ts`).

## Jalur porting yang disarankan
Jadikan server MCP kecil (Node, memakai `legacy-source/src/modules/lms` apa adanya) lalu daftarkan di konfigurasi MCP Hermes, atau tulis ulang jadi skrip Python di folder `scripts/` skill ini. Untuk Drive, pustaka Google resmi sudah cukup.
