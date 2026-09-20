# Template Landing Page RodaLinks

Versi terbaru: tiga layanan, CTA WhatsApp +6285110539167, dan optimasi SEO area Kota serta Kabupaten Bogor.

## Isi file

- `index.html`: halaman utama struktur landing page.
- `style.css`: tata letak dan desain visual (CSS terpisah).
- `script.js`: skrip interaktif (JavaScript terpisah untuk tahun dan menu navigasi mobile).
- `rodalinks-concept.webp`: gambar utama yang telah dioptimalkan.
- `rodalinks-concept.png`: salinan gambar sumber.
- `robots.txt` dan `sitemap.xml`: pengaturan dasar penelusuran mesin pencari.
- `404.html`: halaman untuk alamat yang tidak ditemukan.

## Membuka di komputer

1. Ekstrak ZIP ke satu folder.
2. Buka `index.html` di browser untuk melihat halaman.
3. Untuk preview dengan seluruh URL aset berfungsi, gunakan server lokal. Jika memakai XAMPP, letakkan isi folder di `htdocs/rodalinks/`, lalu buka `http://localhost/rodalinks/` saat Apache aktif. Preload gambar memakai path root; gambar latar tetap menggunakan path relatif.

Template ini berupa HTML, CSS, dan JavaScript statis. Tidak membutuhkan npm, database, atau proses build. Font Google dan tautan WhatsApp membutuhkan koneksi internet. CSS, JavaScript, dan aset gambar utama sudah disertakan.

## Memasang pada hosting sendiri

1. Unggah file website ke folder publik hosting, misalnya `public_html`, dengan `index.html` berada di root domain.
2. Sebelum digunakan dengan domain baru, ganti SEMUA kemunculan `https://rodalinks-bogor.irw-aplika.chatgpt.site` menjadi domain HTTPS milikmu dalam `index.html`, `sitemap.xml`, dan `robots.txt`. Ini mencakup canonical, Open Graph, serta URL dan ID pada JSON-LD.
3. Sesuaikan tanggal `lastmod` di sitemap dengan perubahan konten berikutnya.
4. Pastikan hosting menampilkan `404.html` dengan status HTTP 404 untuk URL yang tidak ada. Cara pengaturannya mengikuti penyedia hosting.
5. Pastikan halaman dapat dibuka tanpa login bila ingin diindeks Google. Setelah domain aktif, verifikasi kepemilikan melalui Google Search Console dan kirim sitemap domain tersebut. Paket ini belum berisi token verifikasi Search Console.

## Mengedit

- Buka `index.html` di editor teks seperti VS Code.
- Cari teks yang ingin diubah. Tema warna berada pada deklarasi `:root`.
- Untuk mengubah nomor WhatsApp, ganti semua `6285110539167` pada tautan dan sesuaikan nomor tampilan serta `telephone` pada JSON-LD.
- Jaga informasi tiga layanan dan area layanan tetap konsisten antara teks halaman dan data JSON-LD.

Paket ini tidak menyertakan kredensial, data pelanggan, atau konfigurasi akun hosting. Pengunduhan ini tidak mengubah akses situs yang sudah diterbitkan.
