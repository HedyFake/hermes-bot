---
name: hdybot-tugas-catatan
description: Tugas dan deadline kuliah, catatan kelas, pengingat, draf pengumuman. Pakai saat pengguna menambah/melihat/menyelesaikan tugas, menyimpan catatan, atau minta diingatkan.
version: 1.0.0
---

# Tugas, catatan, pengingat

Data di tabel `tugas` dan `catatan` pada `$HDYBOT_DB`.

```bash
python3 ~/.hermes/skills/hdybot/hdybot-tugas-catatan/scripts/tugas.py add "Metpen|Bab 1|2026-11-20|PDF"
python3 ~/.hermes/skills/hdybot/hdybot-tugas-catatan/scripts/tugas.py list [semua]
python3 ~/.hermes/skills/hdybot/hdybot-tugas-catatan/scripts/tugas.py done 1
python3 ~/.hermes/skills/hdybot/hdybot-tugas-catatan/scripts/tugas.py del 1
python3 ~/.hermes/skills/hdybot/hdybot-tugas-catatan/scripts/tugas.py note-add "Judul|Isi"
python3 ~/.hermes/skills/hdybot/hdybot-tugas-catatan/scripts/tugas.py note-list
```

## Pengingat
Bot lama memakai worker sendiri (offset H-1, jam, dst). Di Hermes, **pakai fitur cron/penjadwalan Hermes** dengan pengiriman ke chat WhatsApp tujuan: untuk tiap tugas yang punya tenggat, buat pengingat (usulan bawaan bot lama: H-3, H-1, dan pagi hari-H, zona Asia/Jakarta). Jangan membuat pengingat ke grup tanpa izin admin.

## Pengumuman ke grup
Bot lama: draf → antrean review → persetujuan pemilik → kirim (one-time nonce). Pertahankan alurnya: **tulis draf, tampilkan ke pemilik, kirim hanya setelah pemilik menyetujui secara eksplisit.**

## Aturan
- Tanggal format YYYY-MM-DD; tenggat lewat ditandai ⚠️.
- Hanya pembuat atau admin yang boleh menghapus tugas/catatan orang lain.
