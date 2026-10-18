# Tugas 5 (Pekan 5) — Koordinasi & Konsensus

**Materi terkait:** Physical/Logical Clock, Election Algorithm (Bully/Raft).

## Studi Kasus

Terjadi konflik urutan waktu pada pesanan FoodGo (dua server mencatat urutan pesanan berbeda karena jam tidak sinkron), dan sistem membutuhkan satu **"Node Leader"** untuk mengelola antrean pesanan pusat agar tidak terjadi konflik pemrosesan ganda.

## Tugas Kelompok

Implementasikan simulasi **Bully Algorithm** untuk memilih leader di antara **5 node virtual** yang berjalan sebagai 5 proses Python terpisah di laptop yang sama (tiap node = satu proses di port berbeda, komunikasi lewat TCP socket di `localhost`).

Skeleton yang disediakan (`src/node.py`) sudah menangani bagian **infrastruktur jaringan** (membuka socket, menerima & mengirim pesan antar node) — bagian **algoritma Bully sendiri sengaja dikosongkan** (`# TODO`), karena itu inti pembelajaran tugas ini.

### Aturan Bully Algorithm yang harus diimplementasikan

1. Node yang mendeteksi leader tidak merespons (atau saat start pertama kali) mengirim pesan `ELECTION` ke semua node dengan ID **lebih besar** darinya.
2. Jika ada node ber-ID lebih besar yang merespons `OK`, node yang memulai election **berhenti mencalonkan diri** dan menunggu pesan `COORDINATOR`.
3. Jika **tidak ada** node ber-ID lebih besar yang merespons dalam batas waktu tertentu, node tersebut menjadi leader dan mem-broadcast `COORDINATOR` ke semua node lain.
4. Semua node mencatat siapa leader saat ini.

### Cara Menjalankan

Buka 5 terminal terpisah (satu per node):
```bash
python3 src/node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
python3 src/node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
python3 src/node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
python3 src/node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
python3 src/node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
```

### Skenario Wajib Diuji & Dicatat

1. **Start normal**: nyalakan node 1–5 hampir bersamaan, catat siapa yang terpilih jadi leader (harusnya node ber-ID tertinggi, yaitu node 5).
2. **Leader mati**: matikan (Ctrl+C) proses node leader (node 5), amati node lain mendeteksi leader hilang dan memicu election baru. Catat leader baru yang terpilih (harusnya node 4).
3. Simpan log terminal (screenshot atau `> log_nodeX.txt` redirect) dari kedua skenario ke folder `bukti/`.

## Struktur Submission

```
tugas-05-koordinasi-konsensus/
├── README.md      # Analisis: kenapa perlu leader, kenapa Bully (vs Raft), hasil 2 skenario
├── JURNAL.md
├── src/
│   └── node.py
└── bukti/          # Log/screenshot skenario start normal & leader mati
```

## Deskripsi Sistem dan Implementasi

FoodGo merupakan sistem pemesanan makanan berbasis sistem terdistribusi yang menggunakan lima node untuk mengelola layanan. Untuk menjaga koordinasi antar-node, sistem menerapkan **Bully Algorithm** guna memilih leader berdasarkan ID node tertinggi yang masih aktif. Pada pengujian, Node 5 menjadi leader awal, kemudian Node 4 mengambil alih ketika Node 5 mengalami kegagalan.

Komunikasi antar-node menggunakan **TCP Socket** melalui `localhost` dengan port yang berbeda pada setiap node.

| Node | Port |
|------|------|
| Node 1 | 5001 |
| Node 2 | 5002 |
| Node 3 | 5003 |
| Node 4 | 5004 |
| Node 5 | 5005 |

Pesan yang digunakan dalam komunikasi meliputi `ELECTION` (memulai pemilihan), `OK` (konfirmasi node aktif), `COORDINATOR` (mengumumkan leader baru), dan `PING` (memeriksa status leader).

## Analisis
### 1. Mengapa Sistem Memerlukan Leader?
Leader diperlukan untuk mengoordinasikan proses agar seluruh node memiliki acuan yang sama. Leader membantu mengurangi konflik dalam pengelolaan antrean pesanan. Namun, mekanisme tambahan tetap diperlukan untuk menjamin konsistensi data dan mencegah pesanan diproses lebih dari satu kali.

### 2. Mengapa Menggunakan Bully Algorithm Dibandingkan Raft?
Bully Algorithm dipilih karena sederhana dan mudah diterapkan. Leader ditentukan berdasarkan ID tertinggi dari node aktif. Dibandingkan Raft, Bully lebih mudah dipahami, tetapi tidak menyediakan mekanisme replikasi log untuk menjaga konsistensi data.

### 3. Hasil Pengujian
- **Skenario 1:** Berdasarkan catatan pengujian dalam `JURNAL.md`, kelima node berhasil dijalankan dan Node 5 dengan port 5005 terpilih sebagai leader karena memiliki ID tertinggi. Setelah terpilih, Node 5 mengirimkan pesan `COORDINATOR` kepada node lainnya untuk mengumumkan kepemimpinannya. Hasil ini menunjukkan bahwa proses pemilihan leader pada kondisi awal tercatat berjalan sesuai dengan mekanisme Bully Algorithm.

- **Skenario 2:** Pada skenario kedua, Node 5 dihentikan untuk menyimulasikan kegagalan leader. Node lainnya kemudian mendeteksi bahwa leader tidak aktif dan memulai proses pemilihan ulang. Berdasarkan catatan dalam `JURNAL.md`, Node 4 terpilih sebagai leader baru dengan waktu deteksi sekitar 10 detik. Node 4 selanjutnya mengirimkan pesan `COORDINATOR` kepada Node 1, Node 2, dan Node 3 untuk mengumumkan kepemimpinannya.

   Hasil tersebut menunjukkan bahwa mekanisme pemilihan ulang dapat membantu sistem menentukan leader pengganti ketika leader sebelumnya mengalami kegagalan. Namun, waktu deteksi dan keberhasilan pemilihan ulang tetap perlu diverifikasi melalui pengujian langsung..

## Rubrik Penilaian (Tugas 5)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi Bully Algorithm benar | 35% | Election, OK, COORDINATOR message bekerja sesuai aturan algoritma |
| Bukti skenario leader mati → re-election | 30% | Log jelas menunjukkan leader baru terpilih otomatis |
| Analisis (kenapa perlu leader, trade-off Bully vs Raft) | 20% | Dikaitkan ke masalah urutan pesanan di skenario FoodGo |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI tentang gambaran umum algoritma election; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/node.py` (logika `on_message`, `start_election`, `declare_leader`, `monitor_leader`). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan kenapa Bully Algorithm selalu memilih node ber-ID tertinggi yang masih hidup, dan apa kelemahannya dibanding algoritma lain (mis. jumlah pesan yang dikirim saat election, single point of failure sebelum leader baru terpilih) — bukan sekadar definisi generik.
