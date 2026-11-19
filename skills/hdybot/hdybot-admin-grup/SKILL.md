---
name: hdybot-admin-grup
description: Kontrol admin/owner dan kecerdasan grup (klasifikasi pesan grup, antrean review, persetujuan lalu kirim pengumuman, emergency stop, allowlist grup). Pakai saat owner mengelola grup, menyetujui pengumuman, atau meminta ringkasan pesan grup.
version: 1.0.0
---

# Admin & kecerdasan grup

**Status: sebagian diganti Hermes, sebagian perlu port.** Kode asli: `legacy-source/src/admin/` dan `legacy-source/src/ai/classification/group-intelligence.ts`, `legacy-source/src/whatsapp/outbound/gate.ts`.

## Peran akses (bot lama)
`owner` > `admin` > `officer` (ketua/sekretaris/bendahara) > `member` > `anonymous`. Perintah admin hanya di **chat pribadi owner/admin**, dengan password (`ADMIN_REQUIRE_PASSWORD`) dan batas percobaan. Di Hermes, ganti dengan allowlist pengguna Hermes + aturan di bawah. **Jangan** menyimpan password admin di memori atau skill.

## Aturan pengiriman (wajib)
1. Pesan keluar ke grup hanya ke grup yang ada di allowlist dan tidak dijeda.
2. Pengumuman: **draf → tampilkan ke owner → persetujuan eksplisit → kirim**. Tindakan sensitif memakai konfirmasi sekali pakai; tanpa konfirmasi, jangan kirim.
3. **Emergency stop** (`.admin pause`): hentikan semua pengiriman keluar ke grup sampai owner mencabutnya (`.admin resume`).
4. Idempotensi: jangan mengirim ulang pesan yang sama (kunci per pengumuman).
5. Mode `DRY_RUN` untuk uji: tampilkan apa yang akan dikirim tanpa mengirim.

## Klasifikasi pesan grup
Prioritas: `URGENT | IMPORTANT | NORMAL | LOW | REVIEW`. Kualitas: `baik | netral | buruk`. Signifikansi: `inti_penting | biasa | tidak_penting`.
Kategori konten: `schedule_change, assignment, deadline, exam, announcement, material, meeting, lecturer, administrative, social, other`.
- Jangan menandai URGENT hanya karena tanda seru, huruf kapital, atau kata "penting". Harus ada dampak akademik konkret dan tenggat/urgensi jelas.
- Ekstrak hanya fakta yang eksplisit (jenis kejadian, matkul, tanggal ISO atau null, jam, dosen mentah, ruang, tenggat, tindakan, audiens, sumber pesan).
- Tanggal relatif ("besok") diresolusi dari **waktu pesan + Asia/Jakarta**, bukan ditebak; tampilkan hasilnya ke admin.
- Pesan yang meragukan masuk antrean **review** (`.pending`, `.approve <id>`, `.reject <id> <alasan>`), tidak langsung disebarkan.
- Tampilkan sumber dan status verifikasi saat menjelaskan info dari percakapan grup.

## Ringkasan grup (pisahkan bagian)
Keputusan/Informasi · Tugas & Deadline · Perubahan Jadwal · Hal Belum Pasti · Tindak Lanjut. Gabungkan duplikat, jangan hapus koreksi penting, sertakan sumber grup dan waktu pesan.

## Privasi
Simpan teks mentah pesan seperlunya (bot lama: retensi 7 hari, `MESSAGE_RAW_RETENTION_DAYS`). Skor XP hanya untuk yang opt-in. Jangan menampilkan nomor telepon utuh (bot lama memakai masking).

## Diganti oleh Hermes
`.status/.health/.system/.runtime/.logs/.errors/.backup/.db status/.whatsapp status` → gunakan `hermes doctor`, `hermes status`, dan log Hermes.
