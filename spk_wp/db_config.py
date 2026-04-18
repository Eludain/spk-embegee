import mysql.connector
from mysql.connector import Error

# ==========================================
# KONEKSI DATABASE
# ==========================================
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='spk_wp_balitav2',
            user='root',
            password=''  # GANTI dengan password root MySQL milikmu
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
        cursor.execute(
            "SELECT * FROM akun_sppg WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    return None


def login_ahli_gizi(username, password):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM akun_ahli_gizi WHERE username = %s AND password = %s",
            (username, password)
        )
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
        cursor.execute(
            "UPDATE kriteria SET bobot_awal = %s WHERE id_kriteria = %s",
            (bobot_baru, id_kriteria)
        )
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
        cursor.execute(
            "SELECT id_alternatif FROM alternatif WHERE kode_alternatif = %s",
            (kode,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result is None
    return False


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
        cursor.execute(
            "SELECT * FROM alternatif WHERE kode_alternatif = %s",
            (kode,)
        )
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
    """Menyimpan atau menghapus catatan pada menu tertentu."""
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alternatif SET catatan_rekomendasi=%s WHERE id_alternatif=%s",
            (catatan, id_alternatif)
        )
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
        sql = """
            SELECT a.id_alternatif, a.kode_alternatif, a.jadwal_menu, a.nama_makanan,
                   a.catatan_rekomendasi,
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
# 6. FUNGSI PEMILIHAN MENU (OTORITAS AHLI GIZI)
#    Membutuhkan kolom tambahan di tabel alternatif:
#      - is_selected  TINYINT(1) DEFAULT 0
#      - skor_terpilih DOUBLE DEFAULT NULL
# ==========================================
def reset_semua_pilihan_menu():
    """
    Menghapus flag is_selected dan skor_terpilih dari semua menu,
    sehingga hanya satu menu yang bisa berstatus terpilih pada satu waktu.
    """
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("UPDATE alternatif SET is_selected = 0, skor_terpilih = NULL")
        conn.commit()
        cursor.close()
        conn.close()


def tandai_menu_terpilih(id_alternatif, skor):
    """
    Menandai satu menu sebagai menu yang dipilih ahli gizi,
    menyimpan juga skor WP-nya untuk ditampilkan di halaman SPPG.
    Pastikan reset_semua_pilihan_menu() dipanggil sebelum fungsi ini.
    """
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE alternatif SET is_selected = 1, skor_terpilih = %s WHERE id_alternatif = %s",
            (skor, id_alternatif)
        )
        conn.commit()
        cursor.close()
        conn.close()


def ambil_menu_terpilih():
    """
    Mengambil satu menu yang sudah ditandai terpilih oleh ahli gizi
    (is_selected = 1). Dipakai di halaman SPPG.
    Mengembalikan dict atau None jika belum ada.
    """
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id_alternatif, kode_alternatif, jadwal_menu, nama_makanan,
                   catatan_rekomendasi, skor_terpilih
            FROM alternatif
            WHERE is_selected = 1
            LIMIT 1
            """
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    return None


# ==========================================
# 7. FUNGSI HASIL RANKING WP
#    Membutuhkan tabel baru: hasil_ranking
#    DDL:
#      CREATE TABLE IF NOT EXISTS hasil_ranking (
#          id            INT AUTO_INCREMENT PRIMARY KEY,
#          kode_alternatif VARCHAR(20) NOT NULL,
#          jadwal_menu   VARCHAR(100),
#          nama_makanan  TEXT,
#          skor_akhir    DOUBLE NOT NULL,
#          peringkat     INT NOT NULL,
#          waktu_hitung  DATETIME DEFAULT CURRENT_TIMESTAMP,
#          INDEX idx_peringkat (peringkat)
#      );
# ==========================================
def simpan_hasil_ranking(hasil: list):
    """
    Menyimpan seluruh hasil perangkingan WP ke tabel hasil_ranking.
    Setiap kali dipanggil, data lama dihapus dan diganti yang baru
    sehingga tabel selalu mencerminkan perhitungan terakhir.

    Parameter:
        hasil  — list of dict, setiap dict minimal berisi:
                 kode_alternatif, jadwal_menu, nama_makanan, skor_akhir
                 (urutan list sudah merupakan urutan ranking dari tertinggi)
    """
    if not hasil:
        return

    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            # Hapus hasil ranking lama
            cursor.execute("DELETE FROM hasil_ranking")

            # Sisipkan hasil ranking baru
            sql = """
                INSERT INTO hasil_ranking
                    (kode_alternatif, jadwal_menu, nama_makanan, skor_akhir, peringkat)
                VALUES (%s, %s, %s, %s, %s)
            """
            rows = [
                (
                    row.get('kode_alternatif', ''),
                    row.get('jadwal_menu', ''),
                    row.get('nama_makanan', ''),
                    float(row.get('skor_akhir', 0)),
                    idx + 1,
                )
                for idx, row in enumerate(hasil)
            ]
            cursor.executemany(sql, rows)
            conn.commit()
        except Error as e:
            print(f"Error simpan_hasil_ranking: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


def ambil_hasil_ranking():
    """
    Mengambil seluruh hasil ranking WP yang tersimpan di DB,
    diurutkan dari peringkat terbaik. Dipakai di halaman SPPG.
    Mengembalikan list of dict atau None jika tabel kosong.
    """
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT kode_alternatif, jadwal_menu, nama_makanan,
                       skor_akhir, peringkat, waktu_hitung
                FROM hasil_ranking
                ORDER BY peringkat ASC
                """
            )
            result = cursor.fetchall()
            return result if result else None
        except Error as e:
            print(f"Error ambil_hasil_ranking: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None


# ==========================================
# 8. RINGKASAN DASHBOARD
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