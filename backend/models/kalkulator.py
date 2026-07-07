from models.storage import get_standar_gizi

standar_data = get_standar_gizi()

def hitung_zscore(nilai_aktual, standar_umur):
    """
    Rumus Z-Score: (Nilai Aktual - Nilai Median) / (Nilai Simpang Baku Rujukan)
    Simpang Baku = Median - (-1SD) jika Aktual < Median
    Simpang Baku = (+1SD) - Median jika Aktual > Median
    """
    median = standar_umur["median"]
    
    if nilai_aktual < median:
        sd_rujukan = median - standar_umur["-1SD"]
    else:
        sd_rujukan = standar_umur["1SD"] - median
        
    # Cegah pembagian dengan nol
    if sd_rujukan == 0:
        return 0
        
    return round((nilai_aktual - median) / sd_rujukan, 2)

def status_bbu(zscore):
    if zscore < -3.0: return "Berat Badan Sangat Kurang", "Rujuk ke faskes, berikan makanan padat gizi (F100/F75)."
    elif -3.0 <= zscore < -2.0: return "Berat Badan Kurang", "Tingkatkan asupan kalori dan protein hewani (telur, ikan, daging)."
    elif -2.0 <= zscore <= 1.0: return "Berat Badan Normal", "Pertahankan pola makan seimbang sesuai panduan Isi Piringku."
    else: return "Risiko Berat Badan Lebih", "Pantau asupan gula dan lemak, tingkatkan aktivitas fisik balita."

def status_tbu(zscore):
    if zscore < -3.0: return "Sangat Pendek (Severely Stunted)", "Segera rujuk ke dokter spesialis anak (Sp.A). Fokus intervensi protein hewani."
    elif -3.0 <= zscore < -2.0: return "Pendek (Stunted)", "Perbanyak protein hewani tiap makan, stimulasi pertumbuhan, perbaiki sanitasi."
    elif -2.0 <= zscore <= 3.0: return "Normal", "Lanjutkan pemberian gizi seimbang dan pantau tinggi setiap bulan."
    else: return "Tinggi", "Pertumbuhan linear sangat baik."

def evaluasi_gizi(umur, jk, bb, tb):
    data_jk = standar_data.get(jk, {})
    umur_str = str(umur)
    
    # Ambil standar sesuai umur
    std_bbu = data_jk.get("BBU", {}).get(umur_str)
    std_tbu = data_jk.get("TBU", {}).get(umur_str)
    
    if not std_bbu or not std_tbu:
        return {"error": "Data standar untuk umur tersebut belum tersedia di database."}
        
    z_bbu = hitung_zscore(bb, std_bbu)
    z_tbu = hitung_zscore(tb, std_tbu)
    
    status_bb, saran_bb = status_bbu(z_bbu)
    status_tb, saran_tb = status_tbu(z_tbu)
    
    return {
        "indikator": {
            "BB_U": {"z_score": z_bbu, "status": status_bb, "saran": saran_bb},
            "TB_U": {"z_score": z_tbu, "status": status_tb, "saran": saran_tb}
        },
        "saran_umum": "Pastikan balita mendapat ASI Eksklusif (jika < 6 bulan) dan MPASI adekuat (> 6 bulan). Patuhi jadwal imunisasi."
    }
# Standar Kenaikan Minimal (KBM) Permenkes 2020 (Contoh nilai standar umum)
# BB dalam Gram (g), TB dalam Centimeter (cm) berdasarkan kelompok umur
TABEL_INCREMENT = {
    "BB": {"1": 800, "2": 900, "3": 800, "4": 600, "5": 500, "6": 400, "7": 400, "8": 300, "9": 300, "10": 300, "11": 300, "12": 200},
    "TB": {"1": 4.0, "2": 3.5, "3": 3.0, "4": 2.5, "5": 2.0, "6": 2.0, "7": 1.5, "8": 1.5, "9": 1.5, "10": 1.2, "11": 1.2, "12": 1.0}
    # Catatan: Di atas 12 bulan, kenaikan melandai (BB ~200g/bulan, TB ~0.5cm/bulan)
}

def evaluasi_tren(umur, bb_sekarang, bb_lalu, tb_sekarang, tb_lalu):
    if bb_lalu is None or tb_lalu is None:
        return {"status": "Data Bulan Lalu Belum Ada", "pesan": "Tren baru bisa terlihat pada pengukuran bulan berikutnya."}
    
    # Hitung selisih dalam satuan yang sesuai
    kenaikan_bb_gram = round((bb_sekarang - bb_lalu) * 1000) # ubah ke gram
    kenaikan_tb_cm = round(tb_sekarang - tb_lalu, 1)
    
    umur_str = str(umur)
    # Ambil target minimal (jika umur > 12, pakai target default minimal anak batita)
    target_bb = TABEL_INCREMENT["BB"].get(umur_str, 200)
    target_tb = TABEL_INCREMENT["TB"].get(umur_str, 0.5)
    
    status_bb = "Naik Cukup (N)" if kenaikan_bb_gram >= target_bb else "Kenaikan Kurang (T)"
    status_tb = "Tumbuh Cukup" if kenaikan_tb_cm >= target_tb else "Pertumbuhan Lambat"
    
    return {
        "tren_berat_badan": {
            "kenaikan_aktual": f"{kenaikan_bb_gram} gram",
            "target_minimal": f"{target_bb} gram",
            "status": status_bb
        },
        "tren_tinggi_badan": {
            "kenaikan_aktual": f"{kenaikan_tb_cm} cm",
            "target_minimal": f"{target_tb} cm",
            "status": status_tb
        },
        "kesimpulan_tren": "Pertumbuhan Bagus!" if (kenaikan_bb_gram >= target_bb and kenaikan_tb_cm >= target_tb) else "Waspada, kejar ketertinggalan pertumbuhan bulan ini."
    }