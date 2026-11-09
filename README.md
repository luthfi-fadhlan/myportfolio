Nama : Luthfi

NPM : 2506617203

Kelas : PBP F

Created : 01/09/2026

### Tugas 1

1. Ya, saya menggunakan elemen 'section'. Pada kasus ini untuk membuat bagian baru, yaitu 'Projects'. Dalam pembuatan suatu website statis, 'section' ini membantu menandakan seksi baru di website dan sering disertakan dengan elemen 'header'. Elemen semantik seperti ini mendeskripsikan peran dari konten di dalamnya.
2. Awalnya saat aspect ratio dipersempitkan, grid proyek yang saya buat kacau. Jadi, saya tambahkan ke bagian @media spesifikasi grid-container agar bisa adapt dengan ukuran layar yang lebih sempit/ada pada mobile device.
3. Saya merasa sangat sulit untuk membuat perubahan pada elemen dan konten karena pada website static ini semuanya di-hard-code. Untuk kedepannya saya mau fitur di mana kita bisa bikin suatu template elemen yang kemudian bisa dimasukkan saat kita perlukan (seperti menambahkan tombol social links tanpa harus hard-code elemen baru, tinggal pake template aja)

Tidak Menggunakan AI.

First I searched online how to make a "grid" that I can put my projects in. I found one from w3schools (https://www.w3schools.com/css/tryit.asp?filename=trycss_template1_grid) and modified it, discarding the footer but keeping everything else. I also changed the colors to match the previous section.

For every part of this projects section, I made a new class and css style to go with it.

I made a new div to put contents inside of the grid boxes. Inside these divs I put the project title, image, and short paragraph explaining the project. I adjusted the padding, margins, and max-width of most of the content to make sure they looked neat.

The hardest part was figuring out how to size the images correctly. I ended up putting them all at a fixed size (width: 200px) even though I wanted them all to be the same size (in both height and width, like having the same frame in canva) and be aligned with each other.

There are other minor problems I faced; for all of them, I searched google with the "-AI" tag to disable the Google AI Overview and tried finding a solution in the results. I also did not use any chatbots or LLMs.

### Tugas 2

1. saat user klik tombol untuk halaman (misalnya experiences di web saya), request ke api akan dikirim. urls.py (di main) akan tangkap request tersebut dan route nya ke halaman yang sesuai. views.py lalu ngirim request lagi untuk render halaman dari templates. models.py berfungsi sebagai perantara front-end dengan database. Ia menentukan apa saja objek dan fields yang direturn ke front-end untuk di-display.
2. karena prinsip DRY. Kalau di hard-code langsung di template bakal memakan banyak waktu dan susah untuk diubah massal. Dengan menggunakan model dan database, kita hanya perlu mendefinisikan sekali dan bisa tambah/delete data yang setipe berkali-kali.
3. makemigrations hanya melihat kode yang kita tulis dan menulis kode SQL yang sesuai untuk mengubah model database (jika ada perubahan). migrate lah yang mengaplikasikan perubahan tersebut (membuat atau mengubah tabelnya)

## Tugas 3

1. Kita pakai ModelForm dari Django agar forms yang kita buat dapat dipastikan sesuai dengan model data yang ada di database kita. Lebih gampang juga buat diupdate jika kita ada perubahan dalam pemodelan data nanti, daripada mengubahnya satu per satu pada suatu forms html manual. Kita butuh masukkan baris csrf token untuk mengizinkan user mengubah data lewat forms yang kita buat.
2. JSON cenderung lebih singkat karena tidak memiliki closing tag seperti xml. JSON juga turunan dari JavaScript (JavaScript Object Notation), bahasa yang menjadi "glue" dari segala hal mengenai web-programming.
3. Alur: Request HTTP ke /api/xyz/ -> get_xyz_json via urls.py -> Xyz.objects.all() mengembalikan QuerySet yang isinya objek-objek Python Xyz -> QuerySet diserialize menjadi string JSON -> String JSON dikembalikan dengan content_type="application/json". Kita menggunkan serialization untuk mengubah QuerySet (objek Python) menjadi JSON yang dapat dikembalikan. Hal tersebut disebabkan HTTP tidak dapat mengembalikan objek Python secara mentah.

## Tugas 5

1. Debouncing adalah metode untuk delay pengiriman request ke server hingga jeda waktu tertentu tanpa suatu event baru. Selama pengguna masih mengetik, timer dibatalkan dan dimulai ulang. Metode ini penting untuk fitur pencarian berbasis AJAX agar browser tidak mengirim request untuk setiap karakter yang diketik, sehingga mengurangi beban server secara signifikan.
2. Await adalah cara untuk menunggu suatu fungsi asinkron menyelesaikan eksekusinya (Promise selesai) sebelum lanjut ke baris kode berikutnya. Jika tidak menggunakan await saat memanggil fetch(), kode berikutnya akan langsung dieksekusi sebelum data diterima, sehingga variabel yang seharusnya berisi data JSON malah berisi Promise yang masih pending.
3. XSS merupakan cara bagi penyerang untuk menyisipkan kode JavaScript ke dalam website kita yang kemudian dapat digunakan untuk melakukan hal-hal berbahaya. AJAX lebih rentan karena saat data disisipkan ke innerHTML via JavaScript, tidak ada escaping otomatis, sehingga karakter seperti '<' dan '>' dibaca sebagai tag HTML. Berbeda dengan template Django yang melakukan auto-escaping pada setiap {{ variabel }}.

## Tugas 6

1. REST adalah arsitektur API yang punya aturan lebih dari sekadar "kembalikan JSON". API harus stateless (server tidak simpan state client), pakai HTTP method sesuai fungsinya (GET baca, POST buat, PUT/PATCH ubah, DELETE hapus), dan URL merepresentasikan resource. Mengembalikan JSON saja belum RESTful kalau misalnya semua operasi pakai POST, atau URL-nya `/getUser?action=delete`. PUT dipakai saat kita kirim seluruh data objek untuk mengganti sepenuhnya (misalnya update semua field Education sekaligus). PATCH dipakai saat kita hanya kirim field yang berubah (misalnya hanya ubah `year_ended` tanpa kirim ulang `institution` dan `field_of_study`).
2. Serializer di DRF berperan sebagai lapisan konversi dua arah: dari model Python ke JSON (untuk response) dan dari JSON ke data tervalidasi (untuk request). Keuntungannya dibanding rakit dictionary manual di `JsonResponse` seperti Tugas 5 adalah validasi otomatis lewat `validate_<field>`, field readonly seperti `star_count` dan `is_starred` bisa didefinisikan sekali, dan kalau model berubah cukup update serializer saja, tidak perlu ubah satu per satu di setiap view.
3. Autentikasi adalah proses memverifikasi siapa user-nya (login/session), sedangkan otorisasi adalah proses memutuskan apa yang boleh dilakukan user tersebut (permission class). Hak akses harus diperiksa di server karena menyembunyikan tombol di template hanya mengubah tampilan. Request tetap bisa dikirim langsung lewat curl atau Postman tanpa melalui UI sama sekali. Kalau server tidak periksa, siapapun bisa kirim DELETE request meski tombolnya tidak tampil.
4. `SessionAuthentication` mengidentifikasi user lewat session cookie yang otomatis dikirim browser di setiap request. Karena browser mengirim cookie secara otomatis, situs lain bisa membuat form tersembunyi yang mengirim request ke API kita atas nama user yang sedang login, inilah serangan CSRF. Token CSRF membuktikan bahwa request benar-benar berasal dari halaman kita. `force_authenticate` di test langsung menyuntikkan user ke request tanpa melalui mekanisme session dan CSRF sama sekali, jadi tidak bisa membuktikan bahwa perlindungan CSRF berjalan. Hanya `.login()` dengan `enforce_csrf_checks=True` yang bisa membuktikannya.