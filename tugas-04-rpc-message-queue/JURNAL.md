# Jurnal Proses — Tugas 4

## Jalur yang dipilih
Kelompok kami memilih kedua jalur tersebut karena ingin tahu bagaimana implementasi dan dapat memahami perbedaan komunikasi sinkron menggunakan RPC serta komunikasi asinkron menggunakan Massage Queue (MQ). Pada studi kasus FoodGo terdapat dua jenis kebutuhan komunikasi antar komponen, yaitu komunikasi yang membutuhkan respons secara langsung (sinkron) dan komunikasi yang tidak membutuhkan respons secara langsung (asinkron). Dengan mengimplementasikan keduanya, kami dapat menyesuaikan pola komunikasi proses yang dijalankan serta membandingkan kelebihan dan kekurangan masing-masing pendekatan.

RPC dipilih untuk komunikasi antara modul Pesanan dan Pembayaran karena terdapat proses yang membutuhkan hasil secara langsung, seperti pengecekan saldo dan proses pembayaran. Pada implementasinya, client bertindak sebagai modul Pesanan dan server sebagai modul Pembayaran. Client memanggil fungsi cek_saldo() dan proses_pembayaran(), kemudian menunggu response dari server sebelum melanjutkan proses.
RPC sesuai untuk komunikasi request-response karena hasilnya dibutuhkan secara langsung. Namun, client memiliki ketergantungan terhadap server. Jika server Pembayaran tidak tersedia, client tidak dapat memperoleh response.

Sementara MQ dipilih untuk komunikasi antara modul Pembayaran dan Kurir/Notifikasi karena pengiriman notifikasi tidak perlu menunggu modul Kurir siap. Modul Pembayaran cukup mengirim pesan ke RabbitMQ, kemudian pesan akan disimpan di dalam queue sampai modul Kurir siap memprosesnya.
Dengan cara ini, modul Pembayaran tetap bisa berjalan meskipun consumer sedang sibuk atau tidak aktif. Pengujian juga menunjukkan bahwa saat consumer dimatikan, 3 pesan tetap tersimpan di queue dan baru diproses setelah consumer dijalankan kembali. Jadi, MQ cocok untuk proses seperti notifikasi pembayaran yang sifatnya asinkron dan tidak membutuhkan response secara langsung.

## Kendala teknis

1. Setup RabbitMQ menggunakan Docker:
   
Pada setup awal, Docker kami belum dapat digunakan karena Docker Desktop belum berjalan sehingga container RabbitMQ tidak dapat dijalankan. Setelah Docker Desktop dijalankan, RabbitMQ berhasil dijalankan menggunakan Docker Compose.

2. Proses download image RabbitMQ:
   
Saat menjalankan docker compose up -d, proses pengunduhan image rabbitmq:3-management sempat mengalami error unexpected EOF karena buruknya sinyal kami. Perintah kemudian dijalankan kembali hingga image berhasil diunduh dan container RabbitMQ berhasil dibuat dan dijalankan.

3. Library Python pika:
   
Library pika perlu dipasang pada virtual environment karena digunakan oleh publisher dan consumer RabbitMQ. Untuk pika kami menggunakan pika==1.3.2 sesuai requirements.txt.

4. Pemilihan Python interpreter di VS Code:
   
Pada awalnya VS Code menggunakan Python yang berbeda sehingga library pika tidak terdeteksi. Setelah interpreter diarahkan ke Python pada virtual environment mq\venv, library dapat digunakan dengan baik.

## Uji "pesan tidak hilang" (khusus Jalur B)

## 1. Langkah uji
  1. RabbitMQ dijalankan menggunakan Docker Compose.
  2. Consumer dijalankan terlebih dahulu untuk memastikan koneksi ke RabbitMQ berhasil.
  3. Consumer kemudian dihentikan menggunakan Ctrl + C.
  4. Publisher dijalankan ketika consumer dalam keadaan mati.
  5. Publisher berhasil mengirim 3 pesan ke queue pembayaran_berhasil.
  6. RabbitMQ Management Dashboard dibuka untuk melihat kondisi queue.
  7. Terlihat terdapat 3 pesan Ready di queue.
  8. Consumer kemudian dijalankan kembali.
  9. Consumer mengambil dan memproses ketiga pesan tersebut.
  10. Setelah semua pesan berhasil diproses dan di-acknowledge, jumlah pesan Ready kembali menjadi 0.

## 2. Hasil yang diamati
Hasil pengujian menunjukkan bahwa pesan tidak hilang ketika consumer tidak aktif. Ketika publisher mengirimkan tiga pesan, sementara consumer dimatikan, RabbitMQ menyimpan ketiga pesan tersebut di queue pembayaran_berhasil. Dashboard menunjukkan jumlah Ready = 3.
Setelah consumer dinyalakan kembali, ketiga pesan berhasil diterima dan diproses. Setelah proses selesai, jumlah pesan Ready menjadi 0.
Hal ini membuktikan bahwa Message Queue memberikan mekanisme komunikasi asinkron, karena publisher dapat mengirim pesan tanpa harus menunggu consumer aktif pada saat yang sama. Pesan dapat menunggu di RabbitMQ sampai consumer tersedia untuk memprosesnya.

## 3. Hasil Pengujian RPC
Pada pengujian RPC, server dijalankan pada port 8000, kemudian client dijalankan di terminal lain.

    Memanggil cek_saldo('user1') ... menunggu respons sinkron
    
    Hasil cek saldo: 50000
    
    Waktu tempuh: 2.1339 detik
    
    Memanggil proses_pembayaran('user1', 20000) ...
    
    Hasil pembayaran: {'status': 'sukses', 'saldo_akhir': 30000}

Hasil tersebut menunjukkan bahwa client berhasil mendapatkan saldo awal 50000 dan melakukan pembayaran 20000, sehingga saldo akhir menjadi 30000. Client juga menunggu response dari server, sehingga komunikasi berjalan secara sinkron.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 06-10-2026 | ChatGPT | Meminta penjelasan mengenai tahapan pengerjaan Tugas 4 yang mencakup implementasi RPC dan Message Queue pada studi kasus FoodGo. | Memberikan gambaran tahapan implementasi serta aspek yang perlu diuji. | Kelompok menggunakan informasi tersebut sebagai panduan, kemudian melakukan implementasi dan pengujian secara mandiri sesuai template tugas. |
| 06-10-2026 | ChatGPT | Meminta bantuan untuk mengidentifikasi penyebab kendala pada setup Docker, RabbitMQ, dan library Python pika. | Memberikan beberapa kemungkinan penyebab error dan langkah troubleshooting. | Kelompok mencoba solusi yang diberikan secara langsung dan memverifikasi hasilnya melalui terminal serta RabbitMQ Dashboard. |
| 06-10-2026 | ChatGPT | Menentukan metode pengujian yang sesuai untuk komunikasi RPC dan Message Queue pada Tugas 4. | Menjelaskan langkah pengujian RPC client-server dan pengujian Message Queue saat consumer tidak aktif. | Kelompok melakukan pengujian secara mandiri dan mencatat hasil aktual sebagai bukti. |
