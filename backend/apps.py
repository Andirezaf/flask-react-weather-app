from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests

app = Flask(__name__)
CORS(app)  # Aktifkan CORS untuk semua rute

# Koneksi ke database
db = mysql.connector.connect(
    host="127.0.0.1",  # Ganti dengan IP database jika tidak di localhost
    user="root",  # Ganti dengan username database Anda
    password="password",  # Ganti dengan password database Anda
    database="weather_app"  # Ganti dengan nama database Anda
)

API_KEY = "e5ba1ff54fd2e602f6badd07043a3342"  # API Key dari OpenWeatherMap

@app.route('/api/lokasi', methods=['POST'])
def add_lokasi():
    data = request.json # Ambil data dari permintaan JSON
    nama_kota = data.get("nama_kota")  # Ambil nama kota
    kode_negara = data.get("kode_negara")  # Ambil kode negara
    cursor = db.cursor()  # Buat cursor untuk eksekusi query
    cursor.execute("INSERT INTO lokasi (nama_kota, kode_negara) VALUES (%s,%s)", (nama_kota, kode_negara))  # Masukkan nama kota ke database
    db.commit()  # Simpan perubahan ke database
    return {
      "message":"Sukses menambah lokasi"
    }, 201

@app.route('/api/lokasi', methods=['GET'])
def get_lokasi():
  cursor = db.cursor(dictionary=True)
  query = "SELECT * FROM lokasi"
  cursor.execute(query)
  result = cursor.fetchall()
  cursor.close()
  return {
    "data":result
  }, 200

@app.route('/api/lokasi/<int:id>', methods=['PUT'])
def update_lokasi(id: int):
  data = request.json
  cursor =  db.cursor()
  query = "UPDATE lokasi SET nama_kota = %s, kode_negara = %s WHERE id = %s"
  values =(data["nama_kota"], data["kode_negara"], id)
  cursor.execute(query, values)
  db.commit()
  cursor.close()
  return {
    "message":"Data berhasil di update"
  }, 200

@app.route('/api/cuaca/<nama_kota>')
def get_cuaca_kota(nama_kota: str):
  api_url = f"http://api.openweathermap.org/data/2.5/weather?q={nama_kota}&units=metric&appid={API_KEY}"
  response = requests.get(api_url).json()
  if response.get('cod') == 200:
    return {
      "lokasi":nama_kota,
      "temperatur":response["main"]["temp"],
      "kecepatan_angin":response["wind"]["speed"],
      "deskripsi":response["weather"][0]["description"]
    }, 200
  else:
    return {
      "message":"Data tidak ditemukan"
    }, 404
if __name__=='__main__':
  app.run('0.0.0.0', port=5055, debug=True)
