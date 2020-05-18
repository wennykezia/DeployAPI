# API Documentation
API ini dibuat dengan sumber database chinook.db sebagai salah satu dari empat cases dalam Capstone Project. API untuk mengirimkan data kepada user. Proses wrangling dilakukan sesuai endpoint-endpoint yang dimaksud. Base url dari aplikasi ini adalah https://capstone-deployapi-wenny.herokuapp.com/

___
## Open Endpoints : 

**Top Tracks - Artist** : 
> `/artistsales', methods=['GET']`    

Menampilkan data berupa tracks yang tersusun berdasarkan artis/penyanyi dengan total penjualan tertinggi di seluruh negara.
Contoh : https://capstone-deployapi-wenny.herokuapp.com/artistsales

**Top Track - Country** : 

> `/countrysales', methods=['GET']`  

Menampilkan data berupa daftar negara dari angka penjualan tertinggi, serta top track di masing-masing negara tersebut. 
Contoh : https://capstone-deployapi-wenny.herokuapp.com/countrysales

**Sales Amount in Period - Country** : 

> `'/trans/get/<country>', methods=['GET']`  

Menampilkan total nilai penjualan bulanan di tiap kota pada masing-masing negara. User dapat mencari informasi penjualan berdasarkan kota dan negara yang terdaftar dalam database. 
Contoh : https://capstone-deployapi-wenny.herokuapp.com/trans/get/USA