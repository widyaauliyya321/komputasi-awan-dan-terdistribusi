# Tugas 6 (Pekan 6) — Penamaan & Resolusi Lokasi

**Materi terkait:** Flat Naming, Structured Naming (DNS), Distributed Hash Table (DHT)/Chord.

## Studi Kasus

Pelanggan FoodGo kesulitan menemukan alamat IP server kurir yang **dinamis** (kurir berpindah lokasi/jaringan, IP-nya sering berubah). FoodGo butuh cara memetakan **ID Kurir** (identitas tetap) ke **alamat IP terkininya** tanpa server pusat tunggal yang jadi bottleneck/single point of failure.

## Tugas Kelompok

Implementasikan **simulasi Chord DHT** sederhana (single-process, tidak perlu jaringan sungguhan — cukup simulasi struktur data & algoritma di satu program Python) yang memetakan ID Kurir ke alamat IP mereka.

Konsep yang harus terlihat jalan dalam simulasi kalian:
1. **Consistent hashing**: ID Kurir dan ID Node di-hash ke ruang angka yang sama (mis. 0–255 untuk kesederhanaan, `m=8` bit).
2. **Ring topology**: node-node diurutkan melingkar berdasarkan hasil hash-nya.
3. **Lookup**: fungsi `lookup(kurir_id)` yang menemukan node mana yang bertanggung jawab menyimpan mapping ID Kurir tersebut → alamat IP-nya (aturan Chord: node dengan ID hash **terkecil yang lebih besar atau sama dengan** hash key, disebut *successor*).
4. **Perubahan topologi**: simulasikan minimal satu node baru bergabung (`join`) atau satu node keluar (`leave`), tunjukkan bagaimana mapping berpindah tanggung jawab ke node lain.

Skeleton disediakan di `src/chord_simulation.py` dengan fungsi hashing dan struktur ring sudah ada — bagian `lookup()`, `join()`, dan `leave()` sengaja dikosongkan.

### Cara Menjalankan

```bash
python3 src/chord_simulation.py
```

## Tugas Analisis (`README.md`)

1. Jelaskan **kenapa DHT/Chord** lebih cocok untuk kasus ini dibanding **flat naming sederhana** (mis. tabel pusat ID→IP) atau **DNS konvensional** — kaitkan dengan sifat "IP kurir sering berubah" dan kebutuhan tanpa titik gagal tunggal.

DHT (Distributed Hash Table) dengan algoritma Chord lebih cocok digunakan pada kasus FoodGo karena dapat menyimpan dan mencari mapping antara ID Kurir dengan alamat IP secara terdistribusi. Hal ini penting karena alamat IP kurir dapat berubah sewaktu-waktu ketika kurir berpindah lokasi atau jaringan, sedangkan ID kurir tetap sama sebagai identitasnya.

Jika menggunakan *flat naming* sederhana berupa tabel pusat ID Kurir ke alamat IP, seluruh data harus dikelola melalui satu server pusat. Cara ini kurang efektif karena server pusat dapat menjadi bottleneck ketika banyak permintaan pencarian dilakukan secara bersamaan. Selain itu, apabila server pusat mengalami gangguan, proses pencarian alamat IP kurir juga dapat terganggu (*single point of failure*).

Sementara itu, DNS konvensional menggunakan sistem penamaan hierarkis untuk menerjemahkan nama domain menjadi alamat IP. DNS sebenarnya sudah terdistribusi, tetapi mekanisme caching dan TTL dapat menyebabkan perubahan alamat IP tidak langsung diketahui oleh semua pengguna. Hal ini menjadi tantangan ketika FoodGo membutuhkan pembaruan dan pencarian alamat IP kurir yang sering berubah.

Dengan menggunakan DHT/Chord, data dibagi ke beberapa node berdasarkan hasil *hashing*. Setiap node bertanggung jawab atas bagian data tertentu, sehingga tidak semua permintaan harus ditangani oleh satu server pusat. Chord juga menggunakan konsep *consistent hashing* untuk menentukan node yang bertanggung jawab atas suatu data. Ketika ada node yang bergabung atau keluar, pembagian tanggung jawab data dapat disesuaikan tanpa harus mengatur ulang seluruh data.

Oleh karena itu, DHT/Chord lebih sesuai untuk FoodGo karena mendukung penyimpanan data secara terdistribusi, mengurangi ketergantungan pada satu server pusat, serta mempermudah pencarian alamat IP terbaru berdasarkan ID kurir yang tetap.

3. Gambarkan (boleh pakai Mermaid, lihat Tugas 2) ring topology dari simulasi kalian, tandai node mana yang bertanggung jawab atas ID Kurir mana.
4. Jelaskan apa yang terjadi pada mapping saat sebuah node **keluar** dari ring (siapa yang mengambil alih tanggung jawabnya) — dukung dengan output program.

## Struktur Submission

```
tugas-06-penamaan-dht/
├── README.md      # Analisis + diagram ring
├── JURNAL.md
├── src/
│   └── chord_simulation.py
└── bukti/          # Output program (screenshot/log) untuk skenario join & leave
```

## Rubrik Penilaian (Tugas 6)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi lookup/join/leave benar | 35% | Consistent hashing & successor lookup sesuai aturan Chord |
| Bukti perubahan topologi (join/leave) | 25% | Output menunjukkan mapping berpindah dengan benar |
| Analisis kenapa DHT vs flat naming/DNS | 25% | Argumen spesifik ke kasus IP kurir dinamis, bukan definisi umum |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistent hashing/Chord ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/chord_simulation.py` (`find_successor`, `join`, `leave`, dst). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menelusuri manual (langkah demi langkah) bagaimana `lookup()` menemukan successor untuk salah satu ID Kurir contoh yang dipakai di `chord_simulation.py` — bukan cuma menempelkan output program.
