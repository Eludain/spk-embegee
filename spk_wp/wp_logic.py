import db_config

def hitung_rekomendasi_wp_otomatis():
    """
    Menghitung Vektor S dan Vektor V untuk SELURUH menu yang ada di database.
    Hanya menu yang sudah diberi nilai gizi yang akan dihitung.
    """
    # 1. Tarik Data Master
    data_penilaian = db_config.ambil_semua_penilaian_lengkap()
    kriteria_list = db_config.ambil_semua_kriteria()

    # Jika kosong, hentikan proses
    if not data_penilaian or not kriteria_list:
        return []

    # 2. Perbaikan Bobot Kriteria (Normalisasi)
    total_bobot_awal = sum([float(k['bobot_awal']) for k in kriteria_list 
                            if k['tipe_kriteria'] == 'Benefit']) \
                    - sum([float(k['bobot_awal']) for k in kriteria_list 
                            if k['tipe_kriteria'] == 'Cost'])  # = 0.8
    
    # Menentukan Pangkat berdasarkan Benefit (positif) atau Cost (negatif)
    bobot_pangkat = {}
    for k in kriteria_list:
        kode = k['kode_kriteria'].lower() # Menjadi 'c1', 'c2', dst
        bobot_ternormalisasi = float(k['bobot_awal']) / total_bobot_awal
        
        if k['tipe_kriteria'] == 'Benefit':
            bobot_pangkat[kode] = bobot_ternormalisasi
        else: # Cost
            bobot_pangkat[kode] = -bobot_ternormalisasi

    # 3. Hitung Vektor S (Pemangkatan)
    total_vektor_S = 0.0
    hasil_sementara = []

    for data in data_penilaian:
        # FILTER: Lewati menu yang belum diberi nilai gizi oleh Ahli Gizi (nilai_c1 masih kosong/None)
        if data['nilai_c1'] is None:
            continue

        # Mencegah error pembagian/pangkat 0 (terutama untuk kriteria Cost)
        c1 = float(data['nilai_c1']) if float(data['nilai_c1']) > 0 else 0.0001
        c2 = float(data['nilai_c2']) if float(data['nilai_c2']) > 0 else 0.0001
        c3 = float(data['nilai_c3']) if float(data['nilai_c3']) > 0 else 0.0001
        c4 = float(data['nilai_c4']) if float(data['nilai_c4']) > 0 else 0.0001
        c5 = float(data['nilai_c5']) if float(data['nilai_c5']) > 0 else 0.0001

        # Rumus Inti WP: S = (C1^W1) * (C2^W2) * ...
        nilai_S = ( (c1 ** bobot_pangkat.get('c1', 0)) * (c2 ** bobot_pangkat.get('c2', 0)) * (c3 ** bobot_pangkat.get('c3', 0)) * (c4 ** bobot_pangkat.get('c4', 0)) * (c5 ** bobot_pangkat.get('c5', 0)) )
        
        data['vektor_S'] = nilai_S
        total_vektor_S += nilai_S
        hasil_sementara.append(data)

    # 4. Hitung Vektor V (Perangkingan Akhir)
    hasil_akhir = []
    for data in hasil_sementara:
        vektor_V = data['vektor_S'] / total_vektor_S if total_vektor_S > 0 else 0
        
        hasil_akhir.append({
            'id_alternatif': data['id_alternatif'],
            'kode_alternatif': data['kode_alternatif'],
            'jadwal_menu': data['jadwal_menu'],
            'nama_makanan': data['nama_makanan'],
            'catatan_rekomendasi': data['catatan_rekomendasi'], # Membawa serta catatan Ahli Gizi
            'skor_akhir': round(vektor_V, 4)
        })

    # 5. Urutkan berdasarkan Skor Akhir (dari terbesar ke terkecil)
    return sorted(hasil_akhir, key=lambda x: x['skor_akhir'], reverse=True)