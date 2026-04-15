import mysql.connector
from mysql.connector import Error

# ==========================================
# KONEKSI DATABASE
# ==========================================
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='spk_wp_balitav2', # Nama database baru
            user='root',
            password='' # GANTI dengan password root MySQL milikmu
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error saat terhubung ke MySQL: {e}")
        return None

# ==========================================
# 1. FUNGSI AUTENTIKASI
# ==========================================
def login_sppg(username, password):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM akun_sppg WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    return None

def login_ahli_gizi(username, password):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM akun_ahli_gizi WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    return None

# ==========================================
# 2. FUNGSI BAHAN BAKU (OTORITAS SPPG)
# ==========================================
def tambah_bahan_baku(nama_bahan):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bahan_baku (nama_bahan) VALUES (%s)", (nama_bahan,))
        conn.commit()
        cursor.close()
        conn.close()

def ambil_semua_bahan_baku():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bahan_baku ORDER BY id_bahan DESC")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    return []

def hapus_bahan_baku(id_bahan):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bahan_baku WHERE id_bahan = %s", (id_bahan,))
        conn.commit()
        cursor.close()
        conn.close()

# ==========================================
# 3. FUNGSI KRITERIA (OTORITAS AHLI GIZI)
# ==========================================
def ambil_semua_kriteria():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kriteria ORDER BY id_kriteria ASC")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    return []

def update_bobot_kriteria(id_kriteria, bobot_baru):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE kriteria SET bobot_awal = %s WHERE id_kriteria = %s", (bobot_baru, id_kriteria))
        conn.commit()
        cursor.close()
        conn.close()

# ==========================================
# 4. FUNGSI ALTERNATIF / MENU (OTORITAS AHLI GIZI)
# ==========================================
def cek_kode_unik(kode):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT id_alternatif FROM alternatif WHERE kode_alternatif = %s", (kode,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is None

def tambah_alternatif(kode, jadwal_menu, nama_makanan):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        sql = "INSERT INTO alternatif (kode_alternatif, jadwal_menu, nama_makanan) VALUES (%s, %s, %s)"
        cursor.execute(sql, (kode, jadwal_menu, nama_makanan))
        conn.commit()
        cursor.close()
        conn.close()

def ambil_semua_alternatif():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alternatif ORDER BY id_alternatif ASC")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    return []

def ambil_alternatif_by_kode(kode):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM alternatif WHERE kode_alternatif = %s", (kode,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    return None

def update_alternatif(id_alternatif, kode, jadwal_menu, nama_makanan):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        sql = "UPDATE alternatif SET kode_alternatif=%s, jadwal_menu=%s, nama_makanan=%s WHERE id_alternatif=%s"
        cursor.execute(sql, (kode, jadwal_menu, nama_makanan, id_alternatif))
        conn.commit()
        cursor.close()
        conn.close()

def hapus_alternatif(id_alternatif):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alternatif WHERE id_alternatif = %s", (id_alternatif,))
        conn.commit()
        cursor.close()
        conn.close()

def update_catatan_rekomendasi(id_alternatif, catatan):
    """Menyimpan deskripsi khusus untuk menu yang mendapat peringkat 1"""
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE alternatif SET catatan_rekomendasi=%s WHERE id_alternatif=%s", (catatan, id_alternatif))
        conn.commit()
        cursor.close()
        conn.close()

# ==========================================
# 5. FUNGSI PENILAIAN (OTORITAS AHLI GIZI)
# ==========================================
def simpan_penilaian(id_alternatif, c1, c2, c3, c4, c5):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        sql = """
            INSERT INTO penilaian (id_alternatif, nilai_c1, nilai_c2, nilai_c3, nilai_c4, nilai_c5) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
            nilai_c1=%s, nilai_c2=%s, nilai_c3=%s, nilai_c4=%s, nilai_c5=%s
        """
        cursor.execute(sql, (id_alternatif, c1, c2, c3, c4, c5, c1, c2, c3, c4, c5))
        conn.commit()
        cursor.close()
        conn.close()

def ambil_semua_penilaian_lengkap():
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        # Menyesuaikan query SELECT dengan nama kolom yang baru
        sql = """
            SELECT a.id_alternatif, a.kode_alternatif, a.jadwal_menu, a.nama_makanan, a.catatan_rekomendasi,
                   p.nilai_c1, p.nilai_c2, p.nilai_c3, p.nilai_c4, p.nilai_c5
            FROM alternatif a
            LEFT JOIN penilaian p ON a.id_alternatif = p.id_alternatif
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    return []

# ==========================================
# 6. RINGKASAN DASHBOARD
# ==========================================
def ambil_ringkasan_dashboard():
    conn = get_db_connection()
    summary = {'total_bahan': 0, 'total_menu': 0, 'menu_dinilai': 0}
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM bahan_baku")
        summary['total_bahan'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM alternatif")
        summary['total_menu'] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM penilaian")
        summary['menu_dinilai'] = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    return summary