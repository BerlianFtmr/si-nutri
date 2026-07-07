from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.balita import BalitaInput
from models.kalkulator import evaluasi_gizi, evaluasi_tren

app = FastAPI(title="Kalkulator Stunting Permenkes 2020")

# WAJIB: Izinkan Frontend mengakses Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Mengizinkan semua perangkat (HP/Laptop) mengakses API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/evaluasi")
def api_evaluasi_gizi(data: BalitaInput):
    # 1. Hitung Status Gizi (Z-Score)
    hasil_gizi = evaluasi_gizi(data.umur_bulan, data.jenis_kelamin, data.berat_badan, data.tinggi_badan)
    
    # Jika ada error dari database
    if "error" in hasil_gizi:
        return hasil_gizi
        
    # 2. Hitung Tren Pertumbuhan (Increment)
    hasil_tren = evaluasi_tren(
        data.umur_bulan, 
        data.berat_badan, data.berat_badan_lalu, 
        data.tinggi_badan, data.tinggi_badan_lalu
    )
    
    # Gabungkan hasil untuk dikirim ke Frontend
    return {
        "status": "success",
        "biodata": {"umur": data.umur_bulan, "jk": data.jenis_kelamin},
        "gizi": hasil_gizi,
        "tren": hasil_tren
    }