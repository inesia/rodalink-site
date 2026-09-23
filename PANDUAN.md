# Template Landing Page Roda.asia

Versi terbaru: tiga layanan, CTA WhatsApp +6285110539167, dan optimasi SEO area Kota serta Kabupaten Bogor.

## Isi file

- `index.html`: halaman utama struktur landing page.
- `dana-syariah.html`: halaman khusus layanan pembiayaan Dana Syariah Gadai BPKB Motor & Mobil (lengkap dengan kalkulator simulasi).
- `produk.html`: halaman utama katalog motor Yamaha (28 model & 65 varian, filter & pencarian).
- `produk/`: folder berisi 28 halaman statis detail spesifikasi dan varian motor Yamaha.
- `produk.css`: stylesheet khusus katalog motor dan halaman detail produk.
- `produk.js`: skrip interaktif filter kategori, pencarian, sort, dan pemilihan varian motor.
- `data/`: database produk format JSON (`produk.json`) dan spreadsheet (`produk.csv`).
- `build_produk.py`: skrip Python generator statis untuk me-regenerasi katalog dari `data/produk.json`.
- `style.css`: tata letak dan desain visual (CSS terpisah).
- `script.js`: skrip interaktif (JavaScript terpisah untuk tahun, menu mobile, dan PWA).
- `images/logo-rodalink.png`: logo resmi Roda.asia.
- `images/favicon/`: paket lengkap favicon multi-resolusi (ico, png, apple-icon).
- `images/rodalinks-concept.webp`: gambar hero utama yang telah dioptimalkan.
- `images/produk/`: gambar format WebP untuk seluruh 28 model motor Yamaha.
- `images/service-sales-motor.jpg`: ilustrasi Yamaha NMAX untuk layanan pembelian motor.
- `images/service-bpkb-motor.jpg`: ilustrasi dokumen BPKB dan dana tunai motor.
- `images/service-bpkb-mobil.jpg`: ilustrasi dokumen BPKB dan dana tunai mobil.
- `robots.txt` dan `sitemap.xml`: pengaturan dasar penelusuran mesin pencari.
- `404.html`: halaman untuk alamat yang tidak ditemukan.
- `.htaccess`: konfigurasi web server Apache / XAMPP (rule clean URL disiapkan untuk diaktifkan nanti).
- `_redirects`: konfigurasi Netlify (rule clean URL disiapkan untuk diaktifkan nanti).
- `manifest.webmanifest`: file manifest PWA agar website dapat di-install layaknya aplikasi native di HP/Desktop.
- `sw.js`: Service Worker untuk kapabilitas PWA (offline caching dan installable web app).

## Membuka di komputer

1. Ekstrak ZIP ke satu folder.
2. Buka `index.html` di browser untuk melihat halaman.
3. Untuk preview dengan seluruh URL aset berfungsi, gunakan server lokal. Jika memakai XAMPP, letakkan isi folder di `htdocs/rodalinks/`, lalu buka `http://localhost/rodalinks/` saat Apache aktif. Preload gambar memakai path root; gambar latar tetap menggunakan path relatif.

Template ini berupa HTML, CSS, dan JavaScript statis. Tidak membutuhkan npm, database, atau proses build. Font Google dan tautan WhatsApp membutuhkan koneksi internet. CSS, JavaScript, dan aset gambar utama sudah disertakan.

## Memasang pada hosting sendiri

1. Unggah file website ke folder publik hosting, misalnya `public_html`, dengan `index.html` berada di root domain.
2. Sebelum digunakan dengan domain baru, ganti SEMUA kemunculan `https://roda.asia` menjadi domain HTTPS milikmu dalam `index.html`, `sitemap.xml`, dan `robots.txt`. Ini mencakup canonical, Open Graph, serta URL dan ID pada JSON-LD.
3. Sesuaikan tanggal `lastmod` di sitemap dengan perubahan konten berikutnya.
4. Pastikan hosting menampilkan `404.html` dengan status HTTP 404 untuk URL yang tidak ada. Cara pengaturannya mengikuti penyedia hosting.
5. Pastikan halaman dapat dibuka tanpa login bila ingin diindeks Google. Setelah domain aktif, verifikasi kepemilikan melalui Google Search Console dan kirim sitemap domain tersebut. Paket ini belum berisi token verifikasi Search Console.

## Mengedit

- Buka `index.html` di editor teks seperti VS Code.
- Cari teks yang ingin diubah. Tema warna berada pada deklarasi `:root`.
- Untuk mengubah nomor WhatsApp, ganti semua `6285110539167` pada tautan dan sesuaikan nomor tampilan serta `telephone` pada JSON-LD.
- Jaga informasi tiga layanan dan area layanan tetap konsisten antara teks halaman dan data JSON-LD.

Paket ini tidak menyertakan kredensial, data pelanggan, atau konfigurasi akun hosting. Pengunduhan ini tidak mengubah akses situs yang sudah diterbitkan.
