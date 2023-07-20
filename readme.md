
# PLN Spider
### Script ini adalah web scraper yang berfungsi untuk login, menavigasi, memfilter gambar, dan memasukkan nya ke excel.
 -- .env dibutuhkan untuk menjalankan script ini --

* The folder script need to be placed in user documents
- Document
    - PLN Spider
        - Document
            - target.xlsx
        - TempImages

- Jika website terlalu lama tidak muncul atau halaman login tidak muncul silahkan tekan CTRL R
- Anda dapat meminimize webdriver dan melakukan kegiatan lainnya
- Disarankan memiliki internet yang stabil, jika tidak anda dapat menaikkan BANYAK_PERCOBAAN
- Jangan membuka file excel yang masih dijalankan oleh program
- Jika ingin melanjutkan dari baris terakhir ubah lah ROW_AWAL ini dapat anda dapatkan dari row number di paling kiri pada excel

- .env -->
- URL = 'url'
- USER = 'user'
- PASSWORD = 'password'
- EXCEL_PATH = R'.\Document\target.xlsx'
- ROW_AWAL = 1
- ROW_AKHIR = 5
- COL_ID = 'A'
- COL_PHOTO = 'B'
- BANYAK_PERCOBAAN = 7 # -- Berapa kali untuk mencoba mencari foto saat internet tidak stabil
- creator = 'creator'
- -- Setting Foto --
- desired_width = 77
- desired_height = 61
- base_64_foto_tidak_tersedia = 'base 64 for the default image'

Ini adalah script pertama saya untuk freelance, client saya merupakan pegawai kantor PLN di bagian pemutusan dan penyambungan PLN