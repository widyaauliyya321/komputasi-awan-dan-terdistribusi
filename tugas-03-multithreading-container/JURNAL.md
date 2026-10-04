# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat:

Program dijalankan 5 kali dengan 100 pesanan dan 10 thread (mode 'USE_LOCK=0') dan mendapatkan hasil sebagai berikut:

  | Run | Hasil | Seharusnya |
  |-----|-------|------------|
  | 1   | 59    | 100        |
  | 2   | 64    | 100        |
  | 3   | 65    | 100        |
  | 4   | 61    | 100        |
  | 5   | 65    | 100        |

  Hasilnya selalu dibawah 100 dan berbeda tiap run (tidak deterministik)

- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri):

Semua thread dalam satu proses berbagi address space yang sama sehingga 10 thread mengakses satu variabel `processed_count` yang sama. Berbeda dengan proses terpisah yang punya salinan memori masing-masing, thread tidak dilindungi oleh OS/hardware dari perubahan yang dilakukan thread lain (trade-off thread).

Menambah counter bukan merupakan operasi atomik, melainkan tiga langkah: (1) baca nilai, (2) tambah 1, (3) tulis kembali (read-modify-write). Karena penjadwalan
thread bisa berpindah kapan saja (context switch), thread lain dapat menyela di antara langkah baca dan tulis. Di program ini kami menggunakan jeda `time.sleep(0.0001)` di antara baca dan tulis supaya penyelaan ini sering terjadi, dan hasilnya hanya 59-65 dari 100.

## Percobaan dengan Lock

- Hasil `processed_count` setelah perbaikan:

Program dijalankan 5 kali dengan 100 pesanan dan 10 thread (mode `USE_LOCK=1`).

  | Run | Hasil | Seharusnya | 
  |-----|-------|------------|
  | 1   | 100   | 100        | 
  | 2   | 100   | 100        | 
  | 3   | 100   | 100        | 
  | 4   | 100   | 100        | 
  | 5   | 100   | 100        | 

Hasilnya selalu tepat 100 dan konsisten di setiap run (deterministik), berbeda dengan percobaan tanpa lock yang hanya menghasilkan 59-65.

- Perbaikan yang dilakukan:

Dibuat satu objek `lock = threading.Lock()` di tingkat modul, sehingga seluruh thread memakai lock yang sama. Lalu seluruh tiga langkah (baca, jeda, tulis) dibungkus dengan `with lock:`. Jeda `time.sleep(0.0001)` juga sengaja dipertahankan di dalam blok lock, dengan nilai yang sama seperti percobaan tanpa lock. Jadi perbedaan hasil memang berasal dari lock, bukan dari perubahan lain.

- Kenapa lock memperbaikinya:

Lock menjamin mutual exclusion: hanya satu thread yang boleh berada didalam bagian kritis (critical section) pada satu waktu. Thread lain yang ingin masuk harus menunggu sampai lock dilepas. Sehingga, thread kedua baru boleh membaca `processed_count` setelah thread pertama selesai menulis hasilnya, sehingga tidak ada lagi dua thread yang membaca nilai lama yang sama dan tidak ada update yang hilang.

Seluruh langkah baca-jeda-tulis harus berada di dalam lock. Jika hanya langkah tulis yang dikunci, thread lain tetap bisa membaca nilai lama sebelum update selesai, sehingga race condition tetap terjadi.


## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
