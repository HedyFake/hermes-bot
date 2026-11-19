---
name: hdybot-kalkulator
description: Kalkulator keperawatan dan utilitas (IMT/BMI, GCS, tetesan infus, balance cairan, IP/IPK, kalkulator aman, konversi satuan). Pakai untuk setiap perhitungan agar angka akhir pasti benar.
version: 1.0.0
---

# Kalkulator keperawatan & utilitas

Angka akhir **selalu dihitung oleh skrip**, bukan ditebak model.

```bash
python3 ~/.hermes/skills/hdybot/hdybot-kalkulator/scripts/hitung.py imt 65 170
python3 ~/.hermes/skills/hdybot/hdybot-kalkulator/scripts/hitung.py gcs E4 V5 M6
python3 ~/.hermes/skills/hdybot/hdybot-kalkulator/scripts/hitung.py tetesan 500 6 20     # ml, jam, faktor tetes (opsional)
python3 ~/.hermes/skills/hdybot/hdybot-kalkulator/scripts/hitung.py balance 1650 1400    # masuk, keluar (mL)
python3 ~/.hermes/skills/hdybot/hdybot-kalkulator/scripts/hitung.py ipk "4:4.0,3:3.5"    # sks:bobot
python3 ~/.hermes/skills/hdybot/hdybot-kalkulator/scripts/hitung.py calc "(120*3)/4+10"
python3 ~/.hermes/skills/hdybot/hdybot-kalkulator/scripts/hitung.py konversi 38 c f
```

## Aturan
- Hasil untuk **belajar**, bukan diagnosis atau instruksi dosis pada pasien nyata. Katakan itu pada soal klinis.
- Faktor tetes diambil dari kemasan set infus; jangan menebaknya. Tanpa faktor, hanya mL/jam yang dihitung.
- GCS: bila komponen tidak dapat diuji, total tidak dihitung.
- Kurs mata uang tidak ada di skrip: cari lewat web dan sebut sumber serta waktunya.
- Belum ada di bot lama (jangan berpura-pura ada): BSA, dosis obat, kalori.
