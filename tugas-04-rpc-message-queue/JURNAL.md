# Jurnal Proses — Tugas 4

## Jalur yang dipilih
Kelompok kami memilih kedua jalur tersebut karena ingin tahu bagaimana implementasi dan dapat memahami perbedaan komunikasi sinkron menggunakan RPC serta komunikasi asinkron menggunakan Massage Queue (MQ). Pada studi kasus FoodGo terdapat dua jenis kebutuhan komunikasi antar komponen, yaitu komunikasi yang membutuhkan respons secara langsung (sinkron) dan komunikasi yang tidak membutuhkan respons secara langsung (asinkron). Dengan mengimplementasikan keduanya, kami dapat menyesuaikan pola komunikasi proses yang dijalankan serta membandingkan kelebihan dan kekurangan masing-masing pendekatan.

RPC dipilih untuk komunikasi antara modul Pesanan dan Pembayaran karena terdapat proses yang membutuhkan hasil secara langsung, seperti pengecekan saldo dan proses pembayaran. Pada implementasinya, client bertindak sebagai modul Pesanan dan server sebagai modul Pembayaran. Client memanggil fungsi cek_saldo() dan proses_pembayaran(), kemudian menunggu response dari server sebelum melanjutkan proses.
RPC sesuai untuk komunikasi request-response karena hasilnya dibutuhkan secara langsung. Namun, client memiliki ketergantungan terhadap server. Jika server Pembayaran tidak tersedia, client tidak dapat memperoleh response.

Sementara MQ dipilih untuk komunikasi antara modul Pembayaran dan Kurir/Notifikasi karena pengiriman notifikasi tidak perlu menunggu modul Kurir siap. Modul Pembayaran cukup mengirim pesan ke RabbitMQ, kemudian pesan akan disimpan di dalam queue sampai modul Kurir siap memprosesnya.
Dengan cara ini, modul Pembayaran tetap bisa berjalan meskipun consumer sedang sibuk atau tidak aktif. Pengujian juga menunjukkan bahwa saat consumer dimatikan, 3 pesan tetap tersimpan di queue dan baru diproses setelah consumer dijalankan kembali. Jadi, MQ cocok untuk proses seperti notifikasi pembayaran yang sifatnya asinkron dan tidak membutuhkan response secara langsung.

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
