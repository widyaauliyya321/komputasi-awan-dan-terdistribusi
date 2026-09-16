# Tugas 1 — Analisis Pitfall FoodGo

## Studi Kasus: FoodGo

Startup **FoodGo** (aplikasi pesan-antar makanan) mengalami kegagalan sistem saat pesanan melonjak (misalnya jam makan siang atau saat promo besar). Gejala yang dilaporkan tim engineering FoodGo:

- Aplikasi jadi sangat lambat, beberapa permintaan *timeout*.
- Server backend kadang *crash* total dan perlu di-restart manual.
- Tim menemukan bahwa kode mereka menulis asumsi seperti `# network is always reliable, no need for retry` dan tidak ada *timeout* sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).
- Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.

Ini merupakan gejala klasik dari **kesalahan asumsi tentang jaringan dan skala** yang terkenal di literatur sebagai *Fallacies of Distributed Computing* (Peter Deutsch et al.), ditambah masalah desain terkait skalabilitas.


## Tugas Kelompok

1. **Identifikasi minimal 3 pitfall utama** yang dialami FoodGo dari daftar *Fallacies of Distributed Computing* (referensi: "the network is reliable", "latency is zero", "bandwidth is infinite", "the network is secure", "topology doesn't change", "there is one administrator", "transport cost is zero", "the network is homogeneous") **DAN/ATAU** masalah desain sistem terdistribusi lain yang relevan (mis. *single point of failure* karena arsitektur monolitik).
2. Untuk **tiap pitfall**, tulis:
   - Kutipan/paraphrase bagian skenario yang menunjukkan pitfall ini terjadi.
   - Penjelasan **kenapa** asumsi ini keliru dalam sistem terdistribusi nyata.
   - Dampak konkret ke FoodGo (mis. "karena tidak ada timeout, satu service pembayaran yang lambat membuat seluruh thread modul pesanan tertahan, akhirnya server kehabisan resource").
3. Usulkan **solusi desain awal** (tingkat konsep, bukan kode) untuk tiap pitfall — misalnya: timeout + retry dengan backoff untuk asumsi jaringan reliabel, circuit breaker, pemisahan modul jadi service terpisah, dsb.
4. Diskusikan **satu trade-off** dari solusi yang diusulkan (solusi tidak gratis — misalnya retry bisa memperparah beban saat *cascading failure*).
   
**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| [nama 1] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 2] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: [The Network is Reliable] — ditulis oleh Ni Putu Widya Auliya Pratama]

**Bukti di skenario:** Tim menemukan bahwa kode mereka menulis asumsi seperti `# network is always reliable, no need for retry` dan tidak ada *timeout* sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).

**Kenapa ini keliru:** Dalam sistem terdistribusi, layanan pesan antar dilakukan melalui jaringan yang tidak selalu berjalan dengan baik. Request dapat mengalami keterlambatan, gagal terkirim, koneksi terputus, atau layanan yang dituju tidak memberikan respons. Oleh karena itu, sistem tidak boleh berasumsi bahwa setiap proses pertukaran data selalu berhasil.

**Dampak ke FoodGo:** Ketika terjadi gangguan jaringan atau modul pembayaran tidak memberikan respons, modul pesanan akan terus menunggu. jika kondisi ini terjadi pada banyak pesanan secara bersamaan, maka akan semakin banyak request yang tertahan dan menggunakan resource server. Sehingga aplikasi menjadi lambat, beberapa permintaan mengalami timeout, dan jika dalam kondisi trafik tinggi server dapat mengalami overload hingga crash.

**Solusi desain awal:** FoodGo dapat menerapkan timeout agar modul pesanan tidak menunggu terus menerus. Selain itu, dapat menggunakan retry dengan exponential backoff untuk mencoba kembali request yang gagal secara terbatas. Circuit breaker juga dapat digunakan untuk menghentikan sementara request ke layanan yang sedang bermasalah sehingga kegagalan tidak menyebar ke layanan yang lain.

**Trade-off:** Penerapan retry dapat menambah jumlah request ke layanan tujuan. Sehingga jika layanan tersebut sebenarnya sedang overload, retry yang terlalu banyak dapat menambah beban dan memperparah kegagalan. Karena itu, retry perlu dibatasi dengan jumlah percobaan dan jeda (backoff) yang sesuai.

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
