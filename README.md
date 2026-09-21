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