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
   
**Kelompok:** Aul cantik

| Nama | NIM | Kontribusi |
|---|---|---|
| [Ni Putu Widya Auliya Pratama] | [103072400052] | [pitfall 1 The Network is Reliable] |
| [Zafri Ahmad Fahriza] | [103072400060] | [pitfall 2 The Latency is Zero] |
| [Abied Zilachuzzulfiq] | [103072400083] | [pitfall 3 Single Point of Failure] |

## Pitfall 1: [The Network is Reliable] — ditulis oleh Ni Putu Widya Auliya Pratama]

**Bukti di skenario:** Tim menemukan bahwa kode mereka menulis asumsi seperti `# network is always reliable, no need for retry` dan tidak ada *timeout* sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).

**Kenapa ini keliru:** Dalam sistem terdistribusi, layanan pesan antar dilakukan melalui jaringan yang tidak selalu berjalan dengan baik. Request dapat mengalami keterlambatan, gagal terkirim, koneksi terputus, atau layanan yang dituju tidak memberikan respons. Oleh karena itu, sistem tidak boleh berasumsi bahwa setiap proses pertukaran data selalu berhasil.

**Dampak ke FoodGo:** Ketika terjadi gangguan jaringan atau modul pembayaran tidak memberikan respons, modul pesanan akan terus menunggu. jika kondisi ini terjadi pada banyak pesanan secara bersamaan, maka akan semakin banyak request yang tertahan dan menggunakan resource server. Sehingga aplikasi menjadi lambat, beberapa permintaan mengalami timeout, dan jika dalam kondisi trafik tinggi server dapat mengalami overload hingga crash.

**Solusi desain awal:** FoodGo dapat menerapkan timeout agar modul pesanan tidak menunggu terus menerus. Selain itu, dapat menggunakan retry dengan exponential backoff untuk mencoba kembali request yang gagal secara terbatas. Circuit breaker juga dapat digunakan untuk menghentikan sementara request ke layanan yang sedang bermasalah sehingga kegagalan tidak menyebar ke layanan yang lain.

**Trade-off:** Penerapan retry dapat menambah jumlah request ke layanan tujuan. Sehingga jika layanan tersebut sebenarnya sedang overload, retry yang terlalu banyak dapat menambah beban dan memperparah kegagalan. Karena itu, retry perlu dibatasi dengan jumlah percobaan dan jeda (backoff) yang sesuai.

---

## Pitfall 2: [The Latency is Zero] — ditulis oleh [Zafri Ahmad Fahriza]

**Bukti di skenario:** Pada kasus FoodGo disebutkan bahwa “modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu.” Selain itu, ketika jumlah pengguna meningkat, aplikasi menjadi sangat lambat dan beberapa permintaan mengalami timeout. Hal ini menunjukkan bahwa sistem seolah-olah menganggap proses komunikasi antar modul dapat berlangsung dengan cepat dan tanpa adanya keterlambatan.

**Kenapa ini keliru:** Dalam sistem terdistribusi, komunikasi antar service tidak selalu berlangsung secara cepat. Setiap kali modul pesanan berkomunikasi dengan modul pembayaran, terdapat proses pengiriman request melalui jaringan, pemrosesan oleh service pembayaran, dan pengiriman kembali hasilnya. Waktu yang dibutuhkan bisa berubah-ubah, terutama ketika banyak pengguna mengakses sistem secara bersamaan.

**Dampak ke FoodGo:** Ketika sedang terjadi lonjakan pesanan, jumlah request yang masuk ke modul pembayaran juga ikut meningkat. Jika modul pembayaran mulai lambat, modul pesanan akan ikut menunggu lebih lama. Akibatnya, semakin banyak request yang tertahan dan resource server seperti thread dan koneksi akan terus digunakan. Jika kondisi tersebut berlangsung terus-menerus, performa FoodGo akan semakin menurun. Pengguna dapat mengalami aplikasi yang lambat, beberapa request mengalami timeout, dan pada kondisi yang lebih parah server dapat kehabisan resource hingga mengalami crash.

**Solusi desain awal:** FoodGo dapat memberikan timeout pada setiap komunikasi antar-service sehingga modul pesanan tidak menunggu respons pembayaran selamanya. Selain itu, FoodGo dapat menggunakan monitoring latency untuk melihat service mana yang mulai mengalami peningkatan waktu respons ketika trafik sedang tinggi.

**Trade-off:** Penggunaan asynchronous processing dapat membuat sistem lebih tahan terhadap proses yang lambat, tetapi arsitekturnya menjadi lebih kompleks. Hasil pembayaran juga mungkin tidak langsung diterima oleh modul pesanan, sehingga sistem perlu menangani status seperti pending, berhasil, atau gagal. Tim juga perlu memastikan bahwa proses yang tertunda tetap dapat dipantau dan tidak hilang.

---

## Pitfall 3: [Single Point of Failure] — ditulis oleh [Abied Ziachuzzulfiq]

**Bukti di skenario:** Pada kasus FoodGo, disebutkan bahwa satu server menangani semua modul seperti pesanan, pembayaran, dan notifikasi kurir dalam satu proses monolitik.

**Kenapa ini keliru:** Ketika semua modul bergantung pada satu server, beban yang terlalu tinggi pada satu bagian dapat memengaruhi bagian lainnya. Hal ini menjadi masalah terutama ketika trafik meningkat secara tiba-tiba, misalnya saat jam makan siang atau promo besar.

**Dampak ke FoodGo:** Server harus menangani banyak proses sekaligus sehingga resource yang tersedia semakin terbebani. Jika server sudah tidak mampu menangani beban tersebut, aplikasi menjadi lambat dan bahkan bisa crash. Karena semua modul berada di server yang sama, ketika server mengalami masalah, layanan pesanan, pembayaran, dan notifikasi kurir juga ikut terganggu.

**Solusi desain awal:** FoodGo dapat mulai memisahkan beberapa modul menjadi service yang berbeda, terutama modul yang memiliki beban tinggi seperti pembayaran dan pesanan. Dengan begitu, jika salah satu service mengalami masalah, service lainnya masih dapat berjalan.

**Trade-off:** Cara ini memang dapat mengurangi ketergantungan pada satu server, tetapi pengelolaan sistem menjadi lebih kompleks karena setiap service perlu dipantau dan komunikasi antar-service juga harus diperhatikan.

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
