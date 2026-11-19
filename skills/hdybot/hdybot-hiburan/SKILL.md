---
name: hdybot-hiburan
description: Hiburan dan kuis ringan kelas (kutipan, fakta, pantun, doa, truth/dare, dadu, suit, tebak kata, cak lontong, family100, soal logika, transformasi teks). Pakai saat grup minta game atau hiburan.
version: 1.0.0
---

# Hiburan & kuis kelas

Konten di `data/bank.json` (diekstrak dari source bot lama).

```bash
python3 ~/.hermes/skills/hdybot/hdybot-hiburan/scripts/hiburan.py quote [umum|islami|motivasi]
python3 ~/.hermes/skills/hdybot/hdybot-hiburan/scripts/hiburan.py fakta | pantun | doa | surah | truth | dare | dadu | koin
python3 ~/.hermes/skills/hdybot/hdybot-hiburan/scripts/hiburan.py suit batu
python3 ~/.hermes/skills/hdybot/hdybot-hiburan/scripts/hiburan.py soal tebakkata|caklontong|family100|asahotak|deretangka|...
python3 ~/.hermes/skills/hdybot/hdybot-hiburan/scripts/hiburan.py cek <kategori> <indeks> <jawaban>
python3 ~/.hermes/skills/hdybot/hdybot-hiburan/scripts/hiburan.py hilih "selamat pagi"
```

`soal` mengeluarkan penanda `[kategori#indeks]`; simpan penanda itu untuk memeriksa jawaban dengan `cek`.

## Yang belum dipindah (ada di bot lama)
Sesi game per chat (host, duel, riwayat), skor XP, leaderboard opt-in (`.privacy gamification on|off`), AFK, tantangan harian, jadwal sholat per kota. Tabel `xp` sudah ada di database; logika aslinya di `legacy-source/src/modules/fun/fun-utility-service.ts` dan `legacy-source/src/modules/academic/extended-modules.ts`.
Skor XP hanya dicatat bila pemain **opt-in**.

## Aturan
Hiburan aman dan ramah kampus; tolak permintaan yang menyinggung SARA atau pelecehan.
