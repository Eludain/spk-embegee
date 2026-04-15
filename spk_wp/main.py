import streamlit as st
import pandas as pd
import db_config
import wp_logic

st.set_page_config(page_title="Sistem Rekomendasi Menu MBG - V2", layout="wide")

# ==========================================
# INISIALISASI SESSION STATE
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_info = None
if 'menu_aktif' not in st.session_state:
    st.session_state.menu_aktif = "Daftar Bahan Baku" 
if 'menu_aktif_gizi' not in st.session_state:
    st.session_state.menu_aktif_gizi = "Rancang Menu"
if 'hasil_wp' not in st.session_state:
    st.session_state.hasil_wp = None

def proses_logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_info = None
    st.session_state.hasil_wp = None
    st.rerun()

def tampilkan_tabel_dengan_paginasi(df, baris_per_halaman=10, key_prefix="tabel", config=None):
    total_baris = len(df)
    if total_baris == 0:
        st.info("Belum ada data.")
        return

    total_halaman = (total_baris - 1) // baris_per_halaman + 1
    
    if total_halaman > 1:
        col1, col2 = st.columns([1, 5])
        with col1:
            halaman_aktif = st.number_input(f"Halaman (1 - {total_halaman})", min_value=1, max_value=total_halaman, step=1, key=f"{key_prefix}_page")
    else:
        halaman_aktif = 1
        
    mulai_idx = (halaman_aktif - 1) * baris_per_halaman
    akhir_idx = mulai_idx + baris_per_halaman
    st.dataframe(df.iloc[mulai_idx:akhir_idx], hide_index=True, use_container_width=True, column_config=config)

# ==========================================
# HALAMAN LOGIN
# ==========================================
def halaman_login():
    st.title("Sistem Pemilihan Jenis Makanan Terbaik Menggunakan Metode Weighted Product")
    #st.write("Pendekatan Bottom-Up: Ketersediaan Bahan -> Rancang Menu -> Evaluasi Gizi (WP)")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Portal Kepala SPPG (Logistik)")
        user_sppg = st.text_input("Username SPPG", key="u_sppg", autocomplete="new-password")
        pass_sppg = st.text_input("Password SPPG", type="password", key="p_sppg", autocomplete="new-password")
        if st.button("Login SPPG"):
            akun = db_config.login_sppg(user_sppg, pass_sppg)
            if akun:
                st.session_state.logged_in = True
                st.session_state.role = 'sppg'
                st.session_state.user_info = akun
                st.rerun()
            else:
                st.error("Kredensial salah!")

    with col2:
        st.subheader("🩺 Portal Ahli Gizi (Pakar)")
        user_gizi = st.text_input("Username Ahli Gizi", key="u_gizi", autocomplete="new-password")
        pass_gizi = st.text_input("Password Ahli Gizi", type="password", key="p_gizi", autocomplete="new-password")
        if st.button("Login Ahli Gizi"):
            akun = db_config.login_ahli_gizi(user_gizi, pass_gizi)
            if akun:
                st.session_state.logged_in = True
                st.session_state.role = 'ahli_gizi'
                st.session_state.user_info = akun
                st.rerun()
            else:
                st.error("Kredensial salah!")

# ==========================================
# ANTARMUKA KEPALA SPPG
# ==========================================
def dasbor_sppg():
    st.sidebar.title(f"Halo, {st.session_state.user_info['nama_lengkap']}")
    st.sidebar.write(f"Instansi: {st.session_state.user_info['instansi']}")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("Inventaris Bahan Baku", type="primary" if st.session_state.menu_aktif == "Daftar Bahan Baku" else "secondary", use_container_width=True):
        st.session_state.menu_aktif = "Daftar Bahan Baku"
        st.rerun()
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Keluar / Logout", use_container_width=True):
        proses_logout()

    st.title("Dasbor Logistik SPPG")
    st.write("Masukkan daftar bahan baku (sembako, sayur, lauk) yang tersedia hari ini.")

    if st.session_state.menu_aktif == "Daftar Bahan Baku":
        col_form, col_tabel = st.columns([1, 2])
        
        with col_form:
            st.subheader("Input Bahan Baku")
            with st.form("form_tambah_bahan"):
                nama_bahan = st.text_input("Nama/Deskripsi Bahan (Contoh: Beras, Ayam Mentah, Bayam)")
                if st.form_submit_button("Tambahkan ke Inventaris"):
                    if nama_bahan.strip() == "":
                        st.error("Nama bahan tidak boleh kosong!")
                    else:
                        db_config.tambah_bahan_baku(nama_bahan)
                        st.success(f"'{nama_bahan}' berhasil ditambahkan.")
                        st.rerun()
        
        with col_tabel:
            st.subheader("Daftar Bahan Tersedia Saat Ini")
            data_bahan = db_config.ambil_semua_bahan_baku()
            if data_bahan:
                df_bahan = pd.DataFrame(data_bahan)
                df_bahan.insert(0, 'No', range(1, len(df_bahan) + 1))
                df_bahan_tampil = df_bahan.rename(columns={'nama_bahan': 'Nama Bahan', 'tanggal_input': 'Waktu Input'}).drop(columns=['id_bahan'])
                tampilkan_tabel_dengan_paginasi(df_bahan_tampil, baris_per_halaman=5, key_prefix="bahan_baku")
                
                with st.form("form_hapus_bahan"):
                    pil_bahan = st.selectbox("Pilih Bahan untuk dihapus:", [b['id_bahan'] for b in data_bahan], 
                                             format_func=lambda x: next(item['nama_bahan'] for item in data_bahan if item['id_bahan'] == x))
                    if st.form_submit_button("Hapus Bahan"):
                        db_config.hapus_bahan_baku(pil_bahan)
                        st.success("Bahan dihapus.")
                        st.rerun()
            else:
                st.info("Belum ada bahan baku yang diinput hari ini.")
                
        st.markdown("---")
        st.subheader("🏆 Rekomendasi Menu Terpilih")
        hasil_wp_terkini = wp_logic.hitung_rekomendasi_wp_otomatis()
        
        if hasil_wp_terkini:
            pemenang = hasil_wp_terkini[0]
            data_pemenang = db_config.ambil_alternatif_by_kode(pemenang['kode_alternatif'])
            
            st.write(f"**Jadwal Rekomendasi Menu Tanggal** {pemenang['jadwal_menu']}")
            st.success(f"**Daftar Menu:** {pemenang['nama_makanan']}")
            
            if data_pemenang['catatan_rekomendasi']:
                st.info(f"📝 **Catatan / Keterangan Ahli Gizi:**\n\n{data_pemenang['catatan_rekomendasi']}")
            else:
                st.write("*Ahli Gizi belum memberikan catatan khusus untuk menu ini.*")
        else:
            st.info("Ahli Gizi belum melakukan perangkingan menu.")

# ==========================================
# ANTARMUKA AHLI GIZI
# ==========================================
def dasbor_ahli_gizi():
    st.sidebar.title(f"Halo, {st.session_state.user_info['nama_lengkap']}")
    st.sidebar.write(f"STR: {st.session_state.user_info['nomor_str']}")
    st.sidebar.markdown("---")
    
    st.sidebar.write("**Navigasi Utama:**")
    if st.sidebar.button("Rancang Menu & Gizi", type="primary" if st.session_state.menu_aktif_gizi == "Rancang Menu" else "secondary", use_container_width=True):
        st.session_state.menu_aktif_gizi = "Rancang Menu"
        st.rerun()
    if st.sidebar.button("Bobot Kriteria", type="primary" if st.session_state.menu_aktif_gizi == "Bobot Kriteria" else "secondary", use_container_width=True):
        st.session_state.menu_aktif_gizi = "Bobot Kriteria"
        st.rerun()
    if st.sidebar.button("Perangkingan WP", type="primary" if st.session_state.menu_aktif_gizi == "Perangkingan" else "secondary", use_container_width=True):
        st.session_state.menu_aktif_gizi = "Perangkingan"
        st.rerun()
        
    st.sidebar.markdown("---")
    if st.sidebar.button("Keluar / Logout", use_container_width=True):
        proses_logout()

    # --- FITUR 1: RANCANG MENU & INPUT GIZI ---
    if st.session_state.menu_aktif_gizi == "Rancang Menu":
        st.title("Perancangan Menu & Evaluasi Gizi")
        
        with st.expander("Lihat daftar bahan baku yang tersedia", expanded=False):
            bahan_tersedia = db_config.ambil_semua_bahan_baku()
            if bahan_tersedia:
                st.success(", ".join([b['nama_bahan'] for b in bahan_tersedia]))
            else:
                st.warning("SPPG belum menginput bahan baku.")
        
        tab_buat, tab_nilai, tab_kelola = st.tabs(["1. Buat Menu Baru", "2. Input Kandungan Gizi", "3. Kelola Bank Menu"])
        
        with tab_buat:
            st.subheader("Rancang Menu dari Bahan Tersedia")
            with st.form("form_buat_menu"):
                kode_baru = st.text_input("Kode Menu Unik (Misal: A1, A2)")
                jadwal_baru = st.text_input("Jadwal Menu")
                nama_menu = st.text_area("Nama Menu")
                
                if st.form_submit_button("Simpan Rancangan Menu"):
                    if not db_config.cek_kode_unik(kode_baru):
                        st.error("Kode sudah terpakai!")
                    else:
                        db_config.tambah_alternatif(kode_baru, jadwal_baru, nama_menu)
                        st.success("Rancangan menu berhasil disimpan!")
                        
        with tab_nilai:
            st.subheader("Evaluasi Kandungan Gizi")
            semua_menu = db_config.ambil_semua_alternatif()
            if semua_menu:
                col_cari, col_btn = st.columns([4, 1])
                with col_cari:
                    cari_kode_gizi = st.text_input("Cari Kode Menu untuk dinilai:", key="cari_gizi")
                with col_btn:
                    st.write(""); st.write("")
                    tombol_cari = st.button("Cari Menu")

                if cari_kode_gizi or tombol_cari:
                    data_menu = db_config.ambil_alternatif_by_kode(cari_kode_gizi)
                    if data_menu:
                        st.info(f"Target Evaluasi: **{data_menu['jadwal_menu']} ({data_menu['nama_makanan']})**")
                        with st.form("form_input_gizi"):
                            st.write("Masukkan estimasi nilai gizi (Maks 5.0):")
                            colA, colB, colC, colD, colE = st.columns(5)
                            with colA: val_c1 = st.number_input("Protein", min_value=0.0, max_value=5.0, step=0.1)
                            with colB: val_c2 = st.number_input("Karbohidrat", min_value=0.0, max_value=5.0, step=0.1)
                            with colC: val_c3 = st.number_input("Lemak Jenuh", min_value=0.0, max_value=5.0, step=0.1)
                            with colD: val_c4 = st.number_input("Vitamin", min_value=0.0, max_value=5.0, step=0.1)
                            with colE: val_c5 = st.number_input("Kalsium", min_value=0.0, max_value=5.0, step=0.1)
                            
                            if st.form_submit_button("Ubah Nilai Gizi"):
                                db_config.simpan_penilaian(data_menu['id_alternatif'], val_c1, val_c2, val_c3, val_c4, val_c5)
                                st.success("Nilai Gizi berhasil diubah!")
                    else:
                        if cari_kode_gizi: st.error("Kode menu tidak ditemukan.")
            else:
                st.warning("Belum ada menu yang dirancang.")
                
        with tab_kelola:
            st.subheader("Data Menu & Gizi Saat Ini")
            data_lengkap = db_config.ambil_semua_penilaian_lengkap()
            if data_lengkap:
                df_lengkap = pd.DataFrame(data_lengkap)
                df_lengkap = df_lengkap.sort_values(by='kode_alternatif', ascending=True).reset_index(drop=True)
                
                kolom_tampil = ['kode_alternatif', 'jadwal_menu', 'nama_makanan']
                if 'nilai_c1' in df_lengkap.columns:
                    kolom_tampil.extend(['nilai_c1', 'nilai_c2', 'nilai_c3', 'nilai_c4', 'nilai_c5'])
                    
                df_tampil = df_lengkap[kolom_tampil].rename(columns={
                    'kode_alternatif': 'Kode', 
                    'jadwal_menu': 'Jadwal Menu', 
                    'nama_makanan': 'Daftar Menu',
                    'nilai_c1': 'Protein',
                    'nilai_c2': 'Karbohidrat',
                    'nilai_c3': 'Lemak Jenuh',
                    'nilai_c4': 'Vitamin',
                    'nilai_c5': 'Kalsium'
                })
                
                konfigurasi_kolom = {
                    "Daftar Menu": st.column_config.TextColumn("Daftar Menu", width="large")
                }
                
                tampilkan_tabel_dengan_paginasi(df_tampil, baris_per_halaman=10, key_prefix="kelola_menu", config=konfigurasi_kolom)
                
                st.write("**Hapus Menu**")
                kode_hapus = st.text_input("Ketik Kode Menu untuk Dihapus:", key="hapus_menu")
                if st.button("Hapus Menu Ini"):
                    target_hapus = db_config.ambil_alternatif_by_kode(kode_hapus)
                    if target_hapus:
                        db_config.hapus_alternatif(target_hapus['id_alternatif'])
                        st.success("Menu berhasil dihapus.")
                        st.rerun()
                    else:
                        st.error("Kode tidak ditemukan.")

    # --- FITUR 2: BOBOT KRITERIA ---
    elif st.session_state.menu_aktif_gizi == "Bobot Kriteria":
        st.title("Pengaturan Bobot Kriteria")
        data_kriteria = db_config.ambil_semua_kriteria()
        if data_kriteria:
            df_kriteria = pd.DataFrame(data_kriteria)
            df_kriteria_tampil = df_kriteria.rename(columns={
                'kode_kriteria': 'Kode', 'nama_kriteria': 'Nama Kriteria', 
                'tipe_kriteria': 'Tipe Kriteria', 'bobot_awal': 'Bobot'
            }).drop(columns=['id_kriteria'])
            st.dataframe(df_kriteria_tampil, hide_index=True, use_container_width=True)

            st.subheader("Distribusi Ulang Bobot Kriteria")
            st.info("Total keseluruhan bobot harus bernilai tepat 1.0 (100%)")
            
            # --- PERBAIKAN: Form Input Massal untuk 5 Kriteria Sekaligus ---
            with st.form("form_edit_bobot_massal"):
                col1, col2, col3, col4, col5 = st.columns(5)
                
                # Menggunakan nilai awal dari database sebagai pre-fill
                val_b1 = col1.number_input(f"{data_kriteria[0]['nama_kriteria']}", min_value=0.0, max_value=1.0, value=float(data_kriteria[0]['bobot_awal']), step=0.01)
                val_b2 = col2.number_input(f"{data_kriteria[1]['nama_kriteria']}", min_value=0.0, max_value=1.0, value=float(data_kriteria[1]['bobot_awal']), step=0.01)
                val_b3 = col3.number_input(f"{data_kriteria[2]['nama_kriteria']}", min_value=0.0, max_value=1.0, value=float(data_kriteria[2]['bobot_awal']), step=0.01)
                val_b4 = col4.number_input(f"{data_kriteria[3]['nama_kriteria']}", min_value=0.0, max_value=1.0, value=float(data_kriteria[3]['bobot_awal']), step=0.01)
                val_b5 = col5.number_input(f"{data_kriteria[4]['nama_kriteria']}", min_value=0.0, max_value=1.0, value=float(data_kriteria[4]['bobot_awal']), step=0.01)
                
                if st.form_submit_button("Update Semua Bobot"):
                    total_baru = round(val_b1 + val_b2 + val_b3 + val_b4 + val_b5, 2)
                    
                    if total_baru == 1.00:
                        # Jika totalnya pas 1.0, jalankan fungsi update 5 kali
                        db_config.update_bobot_kriteria(data_kriteria[0]['id_kriteria'], val_b1)
                        db_config.update_bobot_kriteria(data_kriteria[1]['id_kriteria'], val_b2)
                        db_config.update_bobot_kriteria(data_kriteria[2]['id_kriteria'], val_b3)
                        db_config.update_bobot_kriteria(data_kriteria[3]['id_kriteria'], val_b4)
                        db_config.update_bobot_kriteria(data_kriteria[4]['id_kriteria'], val_b5)
                        st.success("Berhasil! Distribusi bobot kriteria telah diperbarui.")
                        st.rerun()
                    else:
                        st.error(f"Gagal memperbarui bobot! Total bobot yang Anda masukkan adalah {total_baru}. Total keseluruhan wajib tepat 1.00.")

    # --- FITUR 3: PERANGKINGAN (WP) ---
    elif st.session_state.menu_aktif_gizi == "Perangkingan":
        st.title("Hasil Perangkingan & Rekomendasi Akhir")
        st.write("Seluruh jadwal dan menu yang telah Anda berikan nilai gizi akan dihitung dengan Algoritma Weighted Product")
        
        if st.button("Hitung Hasil", type="primary"):
            st.session_state.hasil_wp = wp_logic.hitung_rekomendasi_wp_otomatis()
            if not st.session_state.hasil_wp:
                st.error("Pastikan minimal ada 2 menu yang sudah dirancang DAN dievaluasi nilai gizinya.")
        
        if st.session_state.hasil_wp:
            st.success("Perhitungan berhasil!")
            df_hasil = pd.DataFrame(st.session_state.hasil_wp)
            menu_terbaik = df_hasil.iloc[0]
            
            st.markdown(f"""
            <div style="padding:20px; border-radius:10px; background-color:#1e3d59; color:white; margin-bottom:20px;">
                <h2>🏆 Rekomendasi Menu Tanggal {menu_terbaik['jadwal_menu']}</h2>
                <p><b>Daftar Menu:</b> {menu_terbaik['nama_makanan']}</p>
                <p><b>Skor WP (Vektor V):</b> {menu_terbaik['skor_akhir']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            data_terbaru = db_config.ambil_alternatif_by_kode(menu_terbaik['kode_alternatif'])
            catatan_saat_ini = data_terbaru['catatan_rekomendasi']
            
            if catatan_saat_ini:
                st.info(f"📝 **Catatan Tersimpan:**\n\n{catatan_saat_ini}")
                if st.button("Hapus Catatan"):
                    db_config.update_catatan_rekomendasi(int(menu_terbaik['id_alternatif']), None) 
                    st.success("Catatan berhasil dihapus!")
                    st.rerun()
            else:
                st.subheader("Tambahkan Catatan / Keterangan")
                with st.form("form_catatan_pemenang"):
                    catatan_baru = st.text_area("Catatan ini akan tersimpan di database sebagai keterangan:")
                    if st.form_submit_button("Simpan Catatan"):
                        db_config.update_catatan_rekomendasi(int(menu_terbaik['id_alternatif']), catatan_baru)
                        st.success("Catatan berhasil disimpan pada menu terbaik!")
                        st.rerun()
            
            st.markdown("---")
            st.subheader("Tabel Lengkap Perangkingan")
            df_tampil = df_hasil[['kode_alternatif', 'jadwal_menu', 'nama_makanan', 'skor_akhir']].rename(
                columns={'kode_alternatif': 'Kode', 'jadwal_menu': 'Jadwal Menu', 'nama_makanan': 'Daftar Menu', 'skor_akhir': 'Skor (V)'}
            )
            
            konfigurasi_kolom_hasil = {
                "Daftar Menu": st.column_config.TextColumn("Daftar Menu", width="large")
            }
            
            tampilkan_tabel_dengan_paginasi(df_tampil, baris_per_halaman=10, key_prefix="hasil_wp", config=konfigurasi_kolom_hasil)

# ==========================================
# KONTROL ALUR PROGRAM (ROUTING)
# ==========================================
if not st.session_state.logged_in:
    halaman_login()
else:
    if st.session_state.role == 'ahli_gizi':
        dasbor_ahli_gizi()
    elif st.session_state.role == 'sppg':
        dasbor_sppg()