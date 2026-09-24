# Tugas 2 (Pekan 2) — Perancangan Arsitektur untuk FoodGo
**Materi terkait:** Architectural Style (Service-Oriented Architecture, Publish-Subscribe)
## Studi Kasus
Melanjutkan Tugas 1, FoodGo membutuhkan sistem yang lebih **decoupled** agar tim kurir dan tim resto tidak saling mengganggu ketika salah satu modul diperbarui atau di-deploy ulang. Sebelumnya seluruh modul (pesanan, pembayaran, notifikasi kurir, dan katalog resto) berjalan sebagai satu aplikasi monolitik sehingga satu kali deploy menyebabkan semua modul ikut restart dan berpotensi menimbulkan downtime.
---
## Kelompok 9
| Nama | NIM | Kontribusi |
|---|---|---|
| Ni Putu Widya Auliya Pratama | 103072400052 | Justifikasi arsitektur & analisis coupling |
| Zafri Ahmad Fahriza | 103072400060 | Diagram & alur komunikasi |
| Abied Zilachuzzulfiq | 103072400083 | Trade-off & analisis |
---
