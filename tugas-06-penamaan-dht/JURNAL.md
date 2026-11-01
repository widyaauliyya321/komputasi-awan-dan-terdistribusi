# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): ...
Pada versi awal, fungsi find_successor() hanya mencari node yang memiliki ID lebih besar atau sama dengan key_hash, lalu memilih ID terkecil dari kandidat yang ditemukan. Masalah muncul ketika hash key lebih besar dari seluruh ID node yang ada. Misalnya, hash 217 pada ring yang berisi node 40, 102, 136, dan 177 tidak memiliki kandidat successor, sehingga fungsi mengembalikan None. Jika kondisi ini terjadi saat kurir didaftarkan, sistem tidak dapat menentukan node yang bertanggung jawab dan proses lookup() juga gagal menemukan kurir tersebut. Kesalahan ini awalnya tidak terlihat karena tiga kurir yang digunakan dalam pengujian memiliki hash 28, 50, dan 132, yang semuanya masih berada di bawah ID node terbesar, yaitu 177. Bug baru diketahui setelah fungsi diuji menggunakan hash di ujung ring. Bukti pengujian terdapat pada bukti/bug_tanpa_wraparound.txt.

- Cara memperbaikinya: ...
Perbaikan dilakukan dengan menambahkan mekanisme wrap-around sesuai sifat ring Chord yang melingkar. Jika tidak ditemukan node dengan ID lebih besar atau sama dengan key_hash, pencarian akan kembali ke node dengan ID terkecil di dalam ring. Dengan begitu, find_successor(217) akan mengembalikan ID 40, yaitu node-bandung-1. Selain itu, ditambahkan pengecekan untuk memastikan ring tidak dalam keadaan kosong, serta pengujian wrap-around pada fungsi main() agar mekanisme tersebut dapat dibuktikan melalui output program.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: ...
- Hasil sebelum & sesudah node keluar: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
