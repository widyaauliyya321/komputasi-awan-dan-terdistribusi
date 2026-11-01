# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): 
Pada implementasi awal, fungsi find_successor() hanya mencari node yang memiliki ID lebih besar atau sama dengan key_hash, lalu memilih ID terkecil dari kandidat yang ditemukan. Masalah muncul ketika hash key lebih besar dari seluruh ID node yang ada. Misalnya, hash 217 pada ring yang berisi node 40, 102, 136, dan 177 tidak memiliki kandidat successor, sehingga fungsi mengembalikan None. Jika kondisi ini terjadi saat kurir didaftarkan, sistem tidak dapat menentukan node yang bertanggung jawab dan proses lookup() juga gagal menemukan kurir tersebut. Kesalahan ini awalnya tidak terlihat karena tiga kurir yang digunakan dalam pengujian memiliki hash 28, 50, dan 132, yang semuanya masih berada di bawah ID node terbesar, yaitu 177. Bug baru diketahui setelah fungsi diuji menggunakan hash di ujung ring. 

- Cara memperbaikinya: 
Perbaikan dilakukan dengan menambahkan mekanisme wrap-around sesuai sifat ring Chord yang melingkar. Jika tidak ditemukan node dengan ID lebih besar atau sama dengan key_hash, pencarian akan kembali ke node dengan ID terkecil di dalam ring. Dengan begitu, find_successor(217) akan mengembalikan ID 40, yaitu node-bandung-1. Selain itu, ditambahkan pengecekan untuk memastikan ring tidak dalam keadaan kosong, serta pengujian wrap-around pada fungsi main() agar mekanisme tersebut dapat dibuktikan melalui output program.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: 
Sebelum node baru bergabung, ring terdiri dari empat node dengan ID 40, 102, 136, dan 177. Mapping kurir-002 dengan hash 28 disimpan pada node-bandung-1, kurir-001 dengan hash 50 pada node-jakarta-2, dan kurir-003 dengan hash 132 pada node-surabaya-1.
Setelah node-medan-1 dengan ID 123 bergabung, node tersebut mengambil alih sebagian rentang tanggung jawab yang sebelumnya dimiliki node-surabaya-1. Namun, tidak ada mapping kurir yang berpindah karena tidak terdapat kurir dengan hash pada rentang 103–123. Hasil lookup("kurir-001") juga tetap menunjukkan IP 192.168.1.10. Hal ini sesuai dengan konsep Chord, yaitu node baru hanya mengambil alih key yang berada di antara predecessor dan ID node tersebut.

- Hasil sebelum & sesudah node keluar: 
Ketika node-jakarta-1 dengan ID 177 keluar dari ring, node tersebut tidak menyimpan mapping kurir apa pun. Oleh karena itu, tidak ada data yang perlu dipindahkan ke node lain dan hasil lookup("kurir-001") serta lookup("kurir-002") tetap menunjukkan IP yang sama. Meskipun tidak ada mapping yang berpindah, tanggung jawab atas rentang 137–177 beralih ke node dengan ID terkecil, yaitu node-bandung-1, sesuai mekanisme wrap-around. Perilaku tersebut juga diuji secara langsung melalui fungsi find_successor().

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 30 Oktober 2026 | ChatGPT | Membantu menganalisis kode chord_simulation.py dan memperbaiki implementasi fungsi yang masih belum lengkap. | AI memberikan saran mengenai pencarian successor, mekanisme wrap-around, dan perpindahan tanggung jawab mapping kurir. | Kode diperiksa dan disesuaikan kembali dengan kebutuhan simulasi. Pengujian dilakukan menggunakan beberapa ID kurir dan node untuk memastikan hasil lookup sesuai. |
| 31 Oktober 2026 | ChatGPT | Membantu memeriksa kode terakhir dan menjelaskan kesalahan yang ditemukan pada fungsi find_successor(). | AI menjelaskan bahwa pencarian successor perlu menangani kondisi ketika hash key lebih besar daripada seluruh ID node yang ada. | Penjelasan digunakan untuk menyusun bagian kesalahan pertama dan cara memperbaikinya pada jurnal. Contoh hash 217 digunakan untuk menjelaskan bug wrap-around. |
| 31 Oktober 2026 | ChatGPT | Membantu menyusun penjelasan hasil simulasi join dan leave agar lebih mudah dipahami. | AI memberikan penjelasan mengenai perubahan tanggung jawab node ketika node baru bergabung atau node lama keluar dari ring. | Hasil simulasi disusun kembali menggunakan bahasa sendiri dengan mencantumkan ID node, hash kurir, dan hasil lookup sebelum serta sesudah perubahan topologi. |
| 31 Oktober 2026 | ChatGPT | Membantu menyusun skenario pengujian untuk membuktikan perpindahan tanggung jawab mapping kurir saat node bergabung dan keluar dari ring. | AI menyarankan pengujian menggunakan hash kurir yang berada pada rentang tanggung jawab node baru agar perpindahan data dapat terlihat pada output program. | Saran digunakan untuk memahami pemilihan skenario pengujian. Hasilnya disesuaikan dengan ID node dan hash kurir pada simulasi, kemudian dijadikan dasar untuk menjelaskan hasil join dan leave dalam jurnal. |
