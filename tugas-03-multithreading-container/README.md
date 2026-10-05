# Tugas 3 (Pekan 3) — Efisiensi Proses & Kontainer

**Materi terkait:** Threading, Virtualization, Containers.

## Studi Kasus

Server FoodGo boros sumber daya karena setiap permintaan pesanan masuk diproses sebagai **proses baru yang berat** (mis. `fork()` proses OS penuh per request). Saat 100 pesanan masuk bersamaan, server kehabisan memori karena tiap proses membawa overhead-nya sendiri.

## Tugas Kelompok

1. Implementasikan **simulasi pesanan masuk** di Python (`src/order_simulator.py`) yang memproses banyak pesanan **secara konkuren memakai multithreading** (bukan multiprocessing, bukan sekuensial biasa).
2. Program harus mensimulasikan **race condition yang sengaja dibuat lalu diperbaiki** — buktikan pemahaman kalian tentang `Lock`/sinkronisasi dengan cara:
   - Jalankan dulu versi TANPA lock, tunjukkan hasil counter yang salah (screenshot/log).
   - Perbaiki dengan `threading.Lock()`, tunjukkan hasil counter yang benar.
   - Tulis perbandingan ini di `JURNAL.md`.
3. Paketkan program ke dalam **Docker container** (`Dockerfile` disediakan skeleton-nya, lengkapi bagian yang kosong).
4. Jalankan container di laptop, buktikan program tetap berjalan benar di dalam container (screenshot/video di `bukti/`).

## Skeleton yang Disediakan

- `src/order_simulator.py` — kerangka program dengan `# TODO` di bagian logika inti (worker function, penggunaan lock, agregasi hasil). **Kalian wajib mengisi bagian TODO sendiri** — ini bagian penilaian utama.
- `requirements.txt` — kosong/minimal (program ini sengaja hanya pakai standard library Python, tidak perlu dependency eksternal).
- `Dockerfile` — kerangka dengan beberapa baris `# TODO`, lengkapi agar image bisa di-build dan dijalankan.

## Cara Menjalankan (Setelah Skeleton Dilengkapi)

Tanpa Docker (langsung di laptop, untuk debugging cepat):
```bash
cd tugas-03-multithreading-container
python3 src/order_simulator.py
```

Dengan Docker (wajib untuk submission akhir):
```bash
cd tugas-03-multithreading-container
docker build -t foodgo-order-sim .
docker run --rm foodgo-order-sim
```

## Struktur Submission

```
tugas-03-multithreading-container/
├── README.md          # Analisis: race condition, perbaikan, kenapa threading (bukan multiprocessing/proses OS)
├── JURNAL.md           # Log sebelum/sesudah lock, error yang ditemui saat build Docker
├── Dockerfile
├── requirements.txt
├── src/
│   └── order_simulator.py
└── bukti/              # Screenshot/video: hasil counter salah (tanpa lock), hasil benar (dengan lock), container jalan
```


## Analisis

### 1. Kenapa threading, bukan multiprocessing atau fork() per request

Multithreading dipilih karena karakteristik proses pada FoodGo lebih banyak
menangani pekerjaan yang dapat berjalan secara konkuren, seperti menerima dan
memproses banyak pesanan dalam waktu yang hampir bersamaan. Dengan threading,
beberapa pekerjaan ditangani oleh thread dalam satu proses sehingga
penggunaan resource relatif lebih ringan dibandingkan membuat banyak proses
terpisah.

Pada studi kasus FoodGo, beban server meningkat ketika terjadi lonjakan
pesanan, sehingga aplikasi menjadi lambat, beberapa request mengalami
timeout, bahkan server dapat crash. Jika setiap pesanan ditangani dengan
proses baru (`fork()`), kebutuhan memori dan overhead pembuatan proses
semakin besar (100 pesanan berarti 100 proses, masing-masing membawa process
context dan salinan memori sendiri), sehingga memperparah server yang sudah
berbeban tinggi.

Sebaliknya, multithreading memungkinkan beberapa pesanan diproses secara
konkuren dalam satu proses karena thread berbagi address space, sehingga
lebih murah dibuat dan di-switch. Program ini memakai 10 thread pekerja untuk
100 pesanan. Pendekatan ini sesuai untuk simulasi server FoodGo yang harus
menangani banyak request bersamaan tanpa membuat proses baru per pesanan.

Konsekuensinya, beberapa thread dapat mengakses data bersama secara
bersamaan. Pada multiprocessing tidak ada race condition karena memori
terpisah, tetapi memori jauh lebih besar dan hasil harus digabung lewat
komunikasi antar-proses. Karena itu pada simulasi digunakan
`threading.Lock()` untuk melindungi `processed_count`. Thread juga cocok
karena pekerjaan pesanan banyak menunggu (I/O). Untuk pekerjaan yang murni
menghitung di CPU, GIL membatasi thread sehingga multiprocessing lebih
cocok.

### 2. Race condition

Tanpa lock, 10 thread memperbarui satu variabel bersama (`processed_count`)
tanpa sinkronisasi. Hasilnya hanya 59-65 di laptop dan 74-75 di Docker,
padahal seharusnya 100, dan angkanya berbeda tiap run.

Penyebabnya, menambah counter adalah tiga langkah: baca, tambah 1, tulis
kembali. Thread lain bisa menyela di antara baca dan tulis. Contohnya,
thread A dan B sama-sama membaca 7 lalu menulis 8, padahal seharusnya 9.
Satu update hilang (lost update).

Jeda `time.sleep(0.0001)` sengaja ditambahkan di antara baca dan tulis untuk
memperlebar celah itu. Tanpa jeda, bug jarang muncul tetapi kodenya tetap
tidak aman. Perbedaan angka antara laptop dan Docker menunjukkan bahwa
penjadwalan thread tidak deterministik.

### 3. Perbaikan dengan Lock

Seluruh blok baca-jeda-tulis dibungkus `with lock:` dengan satu objek
`threading.Lock()` yang dipakai semua thread. Lock menjamin mutual exclusion:
hanya satu thread di bagian kritis pada satu waktu, thread lain menunggu
giliran. Hasilnya selalu 100, di laptop maupun di Docker. Seluruh langkah
harus berada di dalam lock, karena jika hanya langkah tulis yang dikunci,
thread lain tetap bisa membaca nilai lama.

Harganya adalah waktu tunggu, tetapi hanya pada bagian kritis. Simulasi kerja
tiap pesanan berada di luar lock sehingga tetap berjalan bersamaan.

### 4. Peran container

Di dalam Docker, program tetap satu proses dengan 10 thread, sehingga race
condition tanpa lock tetap muncul (74-75) dan lock tetap memperbaikinya (100).
Container tidak mengubah perilaku thread. Ia hanya mengisolasi program lewat
namespaces, union file system, dan cgroups, serta berbagi kernel dengan host
sehingga lebih ringan daripada VM.

### Kesimpulan

1. Multithreading dipilih untuk FoodGo karena pesanan dapat diproses
   konkuren dalam satu proses, jauh lebih hemat memori daripada `fork()` per
   request.
2. Berbagi memori menimbulkan race condition: tanpa lock counter salah dan
   tidak konsisten (59-65 di laptop, 74-75 di Docker).
3. `threading.Lock()` memperbaikinya, hasil selalu tepat 100, dan karena
   hanya bagian kritis yang bergiliran, program tetap konkuren.
4. Docker membungkus program agar berjalan dengan perilaku yang sama di mesin
   mana pun, tanpa mengubah cara kerja thread di dalamnya.
