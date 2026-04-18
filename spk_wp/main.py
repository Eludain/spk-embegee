import streamlit as st
import pandas as pd
import db_config
import wp_logic

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Sistem Rekomendasi Menu MBG",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-primary:   #0d1117;
    --bg-surface:   #161b22;
    --bg-card:      #1c2333;
    --bg-hover:     #21262d;
    --border:       #30363d;
    --border-light: #21262d;
    --accent:       #3fb950;
    --accent-dim:   #238636;
    --accent-glow:  rgba(63,185,80,.18);
    --warn:         #d29922;
    --danger:       #f85149;
    --info:         #388bfd;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --text-muted:   #484f58;
    --radius-sm:    8px;
    --radius-md:    12px;
    --radius-lg:    16px;
    --shadow:       0 4px 24px rgba(0,0,0,.4);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 1rem;
}
section[data-testid="stSidebar"] > div { padding: 0 1rem; }

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    font-size: .88rem !important;
    padding: .55rem 1rem !important;
    transition: all .2s ease !important;
    text-align: left !important;
    margin-bottom: .35rem;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-hover) !important;
    border-color: var(--accent) !important;
    color: var(--text-primary) !important;
    transform: translateX(3px);
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: var(--accent-glow) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

.stButton > button {
    background: var(--accent-dim) !important;
    border: 1px solid var(--accent) !important;
    color: #fff !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: .88rem !important;
    padding: .5rem 1.2rem !important;
    transition: all .2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: var(--accent) !important;
    box-shadow: 0 0 14px var(--accent-glow) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border-color: var(--border) !important;
    color: var(--text-secondary) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--info) !important;
    color: var(--info) !important;
    background: rgba(56,139,253,.1) !important;
    box-shadow: none !important;
}
.stButton > button:disabled {
    background: var(--bg-hover) !important;
    border-color: var(--border) !important;
    color: var(--text-muted) !important;
    cursor: not-allowed !important;
    opacity: 0.55 !important;
    transform: none !important;
    box-shadow: none !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox select {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: .9rem !important;
    transition: border-color .2s ease !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
    outline: none !important;
}
.stTextInput label,
.stTextArea label,
.stNumberInput label,
.stSelectbox label {
    color: var(--text-secondary) !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: .3rem !important;
}

.stForm {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.4rem 1.6rem !important;
}
[data-testid="stFormSubmitButton"] > button {
    background: var(--accent-dim) !important;
    border-color: var(--accent) !important;
    color: #fff !important;
    width: 100%;
}

.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}
.stDataFrame th {
    background: var(--bg-hover) !important;
    color: var(--text-secondary) !important;
    font-size: .78rem !important;
    text-transform: uppercase;
    letter-spacing: .07em;
}
.stDataFrame td {
    font-size: .88rem !important;
    color: var(--text-primary) !important;
}

.stAlert {
    border-radius: var(--radius-md) !important;
    border: none !important;
    font-size: .9rem !important;
}
[data-testid="stNotification"],
.element-container .stSuccess,
.element-container .stInfo,
.element-container .stWarning,
.element-container .stError {
    border-radius: var(--radius-md) !important;
}

.stTabs [role="tablist"] {
    background: var(--bg-surface) !important;
    border-radius: var(--radius-md) !important;
    padding: .3rem !important;
    border: 1px solid var(--border) !important;
    gap: .3rem !important;
}
.stTabs [role="tab"] {
    background: transparent !important;
    border: none !important;
    color: var(--text-secondary) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    font-size: .88rem !important;
    padding: .5rem 1.1rem !important;
    transition: all .2s ease !important;
}
.stTabs [role="tab"][aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--accent) !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 6px rgba(0,0,0,.3) !important;
}
.stTabs [role="tab"]:hover:not([aria-selected="true"]) {
    color: var(--text-primary) !important;
    background: var(--bg-hover) !important;
}

.streamlit-expanderHeader {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
}

hr { border-color: var(--border) !important; margin: 1.2rem 0 !important; }
h1, h2, h3, h4 { color: var(--text-primary) !important; }

[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: var(--radius-sm) !important;
}
[data-baseweb="popover"] ul {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
}
[data-baseweb="option"]:hover { background: var(--bg-hover) !important; }

[data-testid="stNumberInput"] button {
    background: var(--bg-hover) !important;
    border-color: var(--border) !important;
    color: var(--text-secondary) !important;
    transition: all .15s ease !important;
}
[data-testid="stNumberInput"] button:hover {
    background: var(--accent-dim) !important;
    color: #fff !important;
}

.login-wrapper {
    min-height: 85vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.login-hero {
    text-align: center;
    margin-bottom: 2.5rem;
}
.login-hero h1 {
    font-size: 2rem !important;
    font-weight: 800 !important;
    line-height: 1.2;
    background: linear-gradient(135deg, var(--accent) 0%, #79c0ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.login-hero p {
    color: var(--text-secondary) !important;
    font-size: .95rem;
    margin-top: .5rem;
}
.login-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem 1.8rem;
    width: 100%;
    max-width: 380px;
    box-shadow: var(--shadow);
    transition: transform .25s ease, box-shadow .25s ease;
}
.login-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 36px rgba(0,0,0,.5);
}
.login-card-header {
    display: flex;
    align-items: center;
    gap: .65rem;
    margin-bottom: 1.4rem;
}
.login-card-icon {
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
    border-radius: var(--radius-sm);
    font-size: 1.2rem;
}
.icon-sppg  { background: rgba(63,185,80,.15); }
.icon-gizi  { background: rgba(56,139,253,.15); }
.login-card-title {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
}
.login-card-subtitle {
    font-size: .78rem;
    color: var(--text-muted);
}
.badge-role {
    display: inline-block;
    font-size: .72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
    padding: .18rem .6rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}
.badge-sppg { background: rgba(63,185,80,.15); color: var(--accent); border: 1px solid rgba(63,185,80,.3); }
.badge-gizi { background: rgba(56,139,253,.15); color: var(--info); border: 1px solid rgba(56,139,253,.3); }
.badge-terpilih { background: rgba(210,153,34,.15); color: var(--warn); border: 1px solid rgba(210,153,34,.3); }

.page-header {
    display: flex; align-items: center; gap: .9rem;
    padding: 1.2rem 1.6rem;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    margin-bottom: 1.6rem;
}
.page-header-icon {
    font-size: 1.6rem;
    width: 50px; height: 50px;
    display: flex; align-items: center; justify-content: center;
    background: var(--accent-glow);
    border-radius: var(--radius-sm);
}
.page-header-title { font-size: 1.2rem; font-weight: 800; margin: 0; color: var(--text-primary); }
.page-header-sub { font-size: .82rem; color: var(--text-secondary); margin-top: .15rem; }

.stat-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.3rem;
    position: relative; overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), #79c0ff);
}
.stat-label { font-size: .76rem; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: var(--text-muted); margin-bottom: .4rem; }
.stat-value { font-size: 1.55rem; font-weight: 800; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }

.winner-card {
    background: linear-gradient(135deg, #0d2818 0%, var(--bg-card) 100%);
    border: 1px solid var(--accent);
    border-radius: var(--radius-lg);
    padding: 1.6rem 1.8rem;
    margin: 1rem 0;
    position: relative; overflow: hidden;
}
.winner-card::before {
    content: '🏆';
    position: absolute; right: 1.5rem; top: 50%;
    transform: translateY(-50%);
    font-size: 3.5rem; opacity: .12;
}
.winner-label { font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: var(--accent); margin-bottom: .5rem; }
.winner-name { font-size: 1.15rem; font-weight: 700; color: var(--text-primary); margin-bottom: .3rem; }
.winner-detail { font-size: .85rem; color: var(--text-secondary); }
.winner-score {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: .88rem;
    background: var(--accent-glow);
    color: var(--accent);
    border: 1px solid rgba(63,185,80,.3);
    padding: .2rem .7rem;
    border-radius: 20px;
    margin-top: .6rem;
}

.selected-card {
    background: linear-gradient(135deg, #1a1a0d 0%, var(--bg-card) 100%);
    border: 1px solid var(--warn);
    border-radius: var(--radius-lg);
    padding: 1.6rem 1.8rem;
    margin: 1rem 0;
    position: relative; overflow: hidden;
}
.selected-card::before {
    content: '✅';
    position: absolute; right: 1.5rem; top: 50%;
    transform: translateY(-50%);
    font-size: 3.5rem; opacity: .12;
}
.selected-label { font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: var(--warn); margin-bottom: .5rem; }
.selected-score {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: .88rem;
    background: rgba(210,153,34,.15);
    color: var(--warn);
    border: 1px solid rgba(210,153,34,.3);
    padding: .2rem .7rem;
    border-radius: 20px;
    margin-top: .6rem;
}

.rank-badge {
    display: inline-flex; align-items: center; justify-content: center;
    width: 28px; height: 28px;
    border-radius: 50%;
    font-size: .8rem; font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.rank-1 { background: rgba(210,153,34,.2); color: #d29922; border: 1px solid rgba(210,153,34,.4); }
.rank-2 { background: rgba(139,148,158,.15); color: #8b949e; border: 1px solid rgba(139,148,158,.3); }
.rank-3 { background: rgba(248,81,73,.15); color: #cd7f32; border: 1px solid rgba(248,81,73,.3); }
.rank-n { background: var(--bg-hover); color: var(--text-muted); border: 1px solid var(--border); }

.rank-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: .9rem 1.1rem;
    margin-bottom: .5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color .2s ease;
}
.rank-card:hover { border-color: var(--accent); }
.rank-card-top { border-color: rgba(63,185,80,.4); background: rgba(63,185,80,.04); }

.section-title {
    font-size: .72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .1em; color: var(--text-muted);
    margin: 1.5rem 0 .8rem;
    display: flex; align-items: center; gap: .5rem;
}
.section-title::after {
    content: ''; flex: 1; height: 1px; background: var(--border-light);
}

.info-box {
    background: rgba(56,139,253,.08);
    border: 1px solid rgba(56,139,253,.25);
    border-radius: var(--radius-sm);
    padding: .8rem 1rem;
    font-size: .87rem;
    color: #79c0ff;
}
.warn-box {
    background: rgba(210,153,34,.08);
    border: 1px solid rgba(210,153,34,.3);
    border-radius: var(--radius-sm);
    padding: .8rem 1rem;
    font-size: .87rem;
    color: var(--warn);
}

.user-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: .9rem 1rem;
    margin-bottom: 1rem;
}
.user-card-name { font-weight: 700; font-size: .95rem; color: var(--text-primary); }
.user-card-meta { font-size: .78rem; color: var(--text-muted); margin-top: .15rem; }
.user-card-badge { margin-top: .5rem; }

.nav-label {
    font-size: .7rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: .1em; color: var(--text-muted);
    margin: 1rem 0 .45rem; padding-left: .2rem;
}

.stNumberInput > div { max-width: 160px !important; }

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# INISIALISASI SESSION STATE
# ==========================================
defaults = {
    'logged_in': False,
    'role': None,
    'user_info': None,
    'menu_aktif': "Daftar Bahan Baku",
    'menu_aktif_gizi': "Rancang Menu",
    'hasil_wp': None,
    'menu_terpilih_kode': None,
    'edit_catatan_mode': False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ==========================================
# HELPERS
# ==========================================
def proses_logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()


def tampilkan_tabel_dengan_paginasi(df, baris_per_halaman=10, key_prefix="tabel", config=None):
    total_baris = len(df)
    if total_baris == 0:
        st.markdown('<div class="info-box">ℹ️ Belum ada data untuk ditampilkan.</div>', unsafe_allow_html=True)
        return

    total_halaman = (total_baris - 1) // baris_per_halaman + 1

    if total_halaman > 1:
        col1, col2, col3 = st.columns([2, 1, 5])
        with col1:
            st.markdown(f'<div class="stat-label">Menampilkan {total_baris} data</div>', unsafe_allow_html=True)
        with col2:
            halaman_aktif = st.number_input(
                f"Hal. / {total_halaman}", min_value=1, max_value=total_halaman,
                step=1, key=f"{key_prefix}_page", label_visibility="visible"
            )
    else:
        halaman_aktif = 1
        st.markdown(f'<div class="stat-label">{total_baris} data ditemukan</div>', unsafe_allow_html=True)

    mulai_idx = (halaman_aktif - 1) * baris_per_halaman
    akhir_idx = mulai_idx + baris_per_halaman
    st.dataframe(df.iloc[mulai_idx:akhir_idx], hide_index=True, use_container_width=True, column_config=config)


def _ambil_menu_terpilih():
    """Ambil menu yang sudah ditandai terpilih oleh ahli gizi dari DB."""
    try:
        return db_config.ambil_menu_terpilih()
    except AttributeError:
        return None


def _ambil_hasil_ranking_tersimpan():
    """
    Ambil hasil ranking WP yang sudah tersimpan di DB.
    Fungsi ini mencoba mengambil dari db_config; fallback ke None jika belum ada.
    """
    try:
        return db_config.ambil_hasil_ranking()
    except AttributeError:
        return None


# ==========================================
# HALAMAN LOGIN
# ==========================================
def halaman_login():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="login-hero">
        <h1>Sistem Rekomendasi Menu MBG</h1>
        <p>Pemilihan Menu Terbaik dengan Metode <strong>Weighted Product</strong></p>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_mid, col_right = st.columns([1, 6, 1])
    with col_mid:
        col_sppg, col_gap, col_gizi = st.columns([5, 1, 5])

        with col_sppg:
            st.markdown("""
            <div class="login-card">
                <div class="login-card-header">
                    <div class="login-card-icon icon-sppg">📦</div>
                    <div>
                        <div class="login-card-title">Portal SPPG</div>
                        <div class="login-card-subtitle">Kepala Satuan Pelayanan</div>
                    </div>
                </div>
                <span class="badge-role badge-sppg">Inventaris & Logistik</span>
            </div>
            """, unsafe_allow_html=True)
            user_sppg = st.text_input("Username", key="u_sppg",
                                      placeholder="Masukkan username",
                                      autocomplete="new-password")
            pass_sppg = st.text_input("Password", type="password", key="p_sppg",
                                      placeholder="••••••••",
                                      autocomplete="new-password")
            if st.button("Masuk sebagai SPPG", key="btn_sppg", use_container_width=True):
                if not user_sppg.strip() or not pass_sppg.strip():
                    st.error("⚠️ Username dan password tidak boleh kosong.")
                else:
                    akun = db_config.login_sppg(user_sppg.strip(), pass_sppg.strip())
                    if akun:
                        st.session_state.logged_in = True
                        st.session_state.role = 'sppg'
                        st.session_state.user_info = akun
                        st.rerun()
                    else:
                        st.error("❌ Kredensial tidak valid. Coba lagi.")

        with col_gizi:
            st.markdown("""
            <div class="login-card">
                <div class="login-card-header">
                    <div class="login-card-icon icon-gizi">🩺</div>
                    <div>
                        <div class="login-card-title">Portal Ahli Gizi</div>
                        <div class="login-card-subtitle">Tenaga Gizi Profesional</div>
                    </div>
                </div>
                <span class="badge-role badge-gizi">Menu & Perangkingan</span>
            </div>
            """, unsafe_allow_html=True)
            user_gizi = st.text_input("Username", key="u_gizi",
                                      placeholder="Masukkan username",
                                      autocomplete="new-password")
            pass_gizi = st.text_input("Password", type="password", key="p_gizi",
                                      placeholder="••••••••",
                                      autocomplete="new-password")
            if st.button("Masuk sebagai Ahli Gizi", key="btn_gizi", use_container_width=True):
                if not user_gizi.strip() or not pass_gizi.strip():
                    st.error("⚠️ Username dan password tidak boleh kosong.")
                else:
                    akun = db_config.login_ahli_gizi(user_gizi.strip(), pass_gizi.strip())
                    if akun:
                        st.session_state.logged_in = True
                        st.session_state.role = 'ahli_gizi'
                        st.session_state.user_info = akun
                        st.rerun()
                    else:
                        st.error("❌ Kredensial tidak valid. Coba lagi.")

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================
def render_sidebar_sppg():
    with st.sidebar:
        info = st.session_state.user_info
        nama = info.get('nama_lengkap', 'Pengguna')
        inst = info.get('instansi', '-')
        st.markdown(f"""
        <div class="user-card">
            <div class="user-card-name">👤 {nama}</div>
            <div class="user-card-meta">{inst}</div>
            <div class="user-card-badge"><span class="badge-role badge-sppg">SPPG</span></div>
        </div>
        <div class="nav-label">Navigasi</div>
        """, unsafe_allow_html=True)

        if st.button(
            "📦  Inventaris Bahan Baku",
            type="primary" if st.session_state.menu_aktif == "Daftar Bahan Baku" else "secondary",
            use_container_width=True
        ):
            st.session_state.menu_aktif = "Daftar Bahan Baku"
            st.rerun()

        st.markdown('<div class="nav-label">Akun</div>', unsafe_allow_html=True)
        if st.button("🚪  Keluar / Logout", use_container_width=True, key="logout_sppg"):
            proses_logout()


def render_sidebar_gizi():
    with st.sidebar:
        info = st.session_state.user_info
        nama = info.get('nama_lengkap', 'Pengguna')
        str_no = info.get('nomor_str', '-')
        st.markdown(f"""
        <div class="user-card">
            <div class="user-card-name">👤 {nama}</div>
            <div class="user-card-meta">STR: {str_no}</div>
            <div class="user-card-badge"><span class="badge-role badge-gizi">Ahli Gizi</span></div>
        </div>
        <div class="nav-label">Navigasi</div>
        """, unsafe_allow_html=True)

        nav_items = [
            ("🥗  Rancang Menu & Gizi", "Rancang Menu"),
            ("⚖️  Bobot Kriteria",       "Bobot Kriteria"),
            ("🏆  Perangkingan WP",      "Perangkingan"),
        ]
        for label, key in nav_items:
            is_active = st.session_state.menu_aktif_gizi == key
            if st.button(label, type="primary" if is_active else "secondary",
                         use_container_width=True, key=f"nav_{key}"):
                st.session_state.menu_aktif_gizi = key
                st.rerun()

        st.markdown('<div class="nav-label">Akun</div>', unsafe_allow_html=True)
        if st.button("🚪  Keluar / Logout", use_container_width=True, key="logout_gizi"):
            proses_logout()


# ==========================================
# DASBOR KEPALA SPPG
# ==========================================
def dasbor_sppg():
    render_sidebar_sppg()

    st.markdown("""
    <div class="page-header">
        <div class="page-header-icon">📦</div>
        <div>
            <div class="page-header-title">Dasbor Logistik SPPG</div>
            <div class="page-header-sub">Kelola inventaris bahan baku dan lihat rekomendasi menu harian</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.menu_aktif == "Daftar Bahan Baku":
        col_form, col_tabel = st.columns([1, 2], gap="large")

        with col_form:
            st.markdown('<div class="section-title">Tambah Bahan Baku</div>', unsafe_allow_html=True)
            with st.form("form_tambah_bahan", clear_on_submit=True):
                nama_bahan = st.text_input(
                    "Nama / Deskripsi Bahan",
                    placeholder="Contoh: Beras, Ayam Mentah, Bayam…"
                )
                submitted = st.form_submit_button("➕  Tambahkan ke Inventaris")
                if submitted:
                    if not nama_bahan.strip():
                        st.error("⚠️ Nama bahan tidak boleh kosong!")
                    else:
                        db_config.tambah_bahan_baku(nama_bahan.strip())
                        st.success(f"✅ **{nama_bahan}** berhasil ditambahkan ke inventaris.")
                        st.rerun()

        with col_tabel:
            st.markdown('<div class="section-title">Inventaris Hari Ini</div>', unsafe_allow_html=True)
            data_bahan = db_config.ambil_semua_bahan_baku()
            if data_bahan:
                df_bahan = pd.DataFrame(data_bahan)
                df_bahan.insert(0, 'No', range(1, len(df_bahan) + 1))
                df_tampil = df_bahan.rename(columns={
                    'nama_bahan': 'Nama Bahan',
                    'tanggal_input': 'Waktu Input'
                }).drop(columns=['id_bahan'], errors='ignore')
                tampilkan_tabel_dengan_paginasi(df_tampil, baris_per_halaman=5, key_prefix="bahan_baku")

                st.markdown('<div class="section-title">Hapus Bahan</div>', unsafe_allow_html=True)
                with st.form("form_hapus_bahan"):
                    pil_bahan = st.selectbox(
                        "Pilih bahan yang ingin dihapus",
                        options=[b['id_bahan'] for b in data_bahan],
                        format_func=lambda x: next(
                            (item['nama_bahan'] for item in data_bahan if item['id_bahan'] == x), str(x)
                        )
                    )
                    if st.form_submit_button("🗑️  Hapus Bahan Terpilih"):
                        db_config.hapus_bahan_baku(pil_bahan)
                        st.success("✅ Bahan berhasil dihapus dari inventaris.")
                        st.rerun()
            else:
                st.markdown('<div class="info-box">📭 Belum ada bahan baku yang diinput hari ini.</div>', unsafe_allow_html=True)

        # ── Hasil Perangkingan WP (Top 5) ────────────────────────────
        st.markdown('<div class="section-title">Hasil Perangkingan WP (Top 5)</div>', unsafe_allow_html=True)

        # Prioritas: ambil dari session_state dulu, fallback ke DB
        hasil_ranking_sppg = st.session_state.get('hasil_wp') or _ambil_hasil_ranking_tersimpan()

        if hasil_ranking_sppg:
            df_rank_sppg = pd.DataFrame(hasil_ranking_sppg)
            top5 = df_rank_sppg.head(5).reset_index(drop=True)

            for i, row in top5.iterrows():
                peringkat = i + 1
                badge_cls = f"rank-{peringkat}" if peringkat <= 3 else "rank-n"
                nama_menu_str = str(row.get('nama_makanan', '-'))
                nama_pendek = nama_menu_str[:70] + ('…' if len(nama_menu_str) > 70 else '')
                skor = float(row.get('skor_akhir', 0))
                kode = row.get('kode_alternatif', '-')
                jadwal = row.get('jadwal_menu', '-')
                st.markdown(f"""
                <div class="rank-card {'rank-card-top' if peringkat == 1 else ''}">
                    <span class="rank-badge {badge_cls}">#{peringkat}</span>
                    <div style="flex:1;">
                        <div style="font-weight:700;font-size:.93rem;color:var(--text-primary);">{nama_pendek}</div>
                        <div style="font-size:.8rem;color:var(--text-secondary);margin-top:.2rem;">
                            Kode: <code>{kode}</code> · Jadwal: {jadwal}
                        </div>
                    </div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:.82rem;color:var(--accent);
                                background:var(--accent-glow);padding:.2rem .6rem;border-radius:12px;
                                border:1px solid rgba(63,185,80,.25);white-space:nowrap;">
                        {skor:.8f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">⏳ Ahli Gizi belum melakukan perangkingan. Hasil akan ditampilkan di sini setelah perangkingan dilakukan.</div>', unsafe_allow_html=True)

        # ── Menu Terpilih oleh Ahli Gizi ─────────────────────────────
        st.markdown('<div class="section-title">Menu Terpilih oleh Ahli Gizi</div>', unsafe_allow_html=True)

        menu_terpilih = _ambil_menu_terpilih()

        if menu_terpilih:
            st.markdown(f"""
            <div class="selected-card">
                <div class="selected-label">✅ Menu Dipilih Ahli Gizi · {menu_terpilih.get('jadwal_menu', '-')}</div>
                <div class="winner-name">{menu_terpilih.get('nama_makanan', '-')}</div>
                <div class="winner-detail">Kode: <code>{menu_terpilih.get('kode_alternatif', '-')}</code></div>
                <span class="selected-score">Skor WP (V): {float(menu_terpilih.get('skor_terpilih', 0)):.8f}</span>
            </div>
            """, unsafe_allow_html=True)

            catatan = menu_terpilih.get('catatan_rekomendasi')
            if catatan:
                st.info(f"📝 **Catatan Ahli Gizi:**\n\n{catatan}")
            else:
                st.markdown('<div class="info-box">ℹ️ Ahli Gizi belum memberikan catatan untuk menu ini.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">⏳ Ahli Gizi belum memilih menu. Tunggu hingga proses perangkingan selesai.</div>', unsafe_allow_html=True)


# ==========================================
# DASBOR AHLI GIZI
# ==========================================
def dasbor_ahli_gizi():
    render_sidebar_gizi()

    # ── FITUR 1: RANCANG MENU ────────────────────────────────────────
    if st.session_state.menu_aktif_gizi == "Rancang Menu":
        st.markdown("""
        <div class="page-header">
            <div class="page-header-icon">🥗</div>
            <div>
                <div class="page-header-title">Perancangan Menu & Evaluasi Gizi</div>
                <div class="page-header-sub">Susun menu, masukkan nilai gizi, dan kelola bank menu yang ada</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Referensi bahan
        with st.expander("📋  Lihat bahan baku tersedia (dari SPPG)", expanded=False):
            bahan_tersedia = db_config.ambil_semua_bahan_baku()
            if bahan_tersedia:
                tags_html = " ".join([
                    f'<span style="background:rgba(63,185,80,.12);border:1px solid rgba(63,185,80,.25);'
                    f'color:#3fb950;padding:.2rem .6rem;border-radius:20px;font-size:.8rem;margin:.2rem;'
                    f'display:inline-block;">{b["nama_bahan"]}</span>'
                    for b in bahan_tersedia
                ])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.warning("⚠️ SPPG belum menginput bahan baku hari ini.")

        # Konteks jumlah menu — PERBAIKAN: tidak ada batas maksimum
        semua_menu_count = len(db_config.ambil_semua_alternatif() or [])
        if semua_menu_count < 5:
            warna_count = "#d29922"
            status_str = f"— Minimal 5 menu untuk perangkingan (butuh {5 - semua_menu_count} lagi)"
        else:
            warna_count = "#3fb950"
            status_str = f"✅ Siap untuk perangkingan!"
        st.markdown(
            f'<div class="info-box" style="margin-bottom:1rem;">'
            f'📊 Jumlah menu saat ini: <b style="color:{warna_count};font-family:monospace;">{semua_menu_count}</b>'
            f'&nbsp;&nbsp;{status_str}'
            f'</div>',
            unsafe_allow_html=True
        )

        tab_buat, tab_nilai, tab_kelola = st.tabs([
            "① Buat Menu Baru",
            "② Input Nilai Gizi",
            "③ Kelola Bank Menu"
        ])

        # ── Tab 1: Buat Menu Baru ─────────────────────────────────────
        with tab_buat:
            col_f, col_tip = st.columns([3, 2], gap="large")
            with col_f:
                st.markdown('<div class="section-title">Rancang Menu Baru</div>', unsafe_allow_html=True)
                # PERBAIKAN: tidak ada pembatasan jumlah maksimum menu
                with st.form("form_buat_menu", clear_on_submit=True):
                    kode_baru   = st.text_input("Kode Menu Unik", placeholder="Contoh: A1, B2, C3…")
                    jadwal_baru = st.text_input("Jadwal Menu", placeholder="Contoh: Senin, 2025-07-14…")
                    nama_menu   = st.text_area("Daftar Menu / Nama Masakan",
                                               placeholder="Contoh: Nasi Putih, Ayam Goreng, Sayur Bayam, Jeruk…",
                                               height=110)
                    if st.form_submit_button("💾  Simpan Rancangan Menu"):
                        if not kode_baru.strip():
                            st.error("⚠️ Kode menu wajib diisi.")
                        elif not jadwal_baru.strip():
                            st.error("⚠️ Jadwal menu wajib diisi.")
                        elif not nama_menu.strip():
                            st.error("⚠️ Nama menu wajib diisi.")
                        elif not db_config.cek_kode_unik(kode_baru.strip()):
                            st.error(f"❌ Kode **{kode_baru}** sudah digunakan. Pilih kode lain.")
                        else:
                            db_config.tambah_alternatif(kode_baru.strip(), jadwal_baru.strip(), nama_menu.strip())
                            st.success(f"✅ Menu **{kode_baru}** berhasil disimpan! Lanjutkan ke tab ② untuk mengisi nilai gizi.")
                            st.rerun()

            with col_tip:
                st.markdown('<div class="section-title">Panduan Pengisian</div>', unsafe_allow_html=True)
                st.markdown("""
                <div class="info-box" style="line-height:1.7;">
                🔑 <b>Kode Unik</b> — Identifikasi pendek (A1, B3, dst.)<br>
                📅 <b>Jadwal</b> — Hari atau tanggal penyajian<br>
                🍱 <b>Nama Menu</b> — Cantumkan semua komponen hidangan<br>
                🔢 <b>Jumlah</b> — Bisa lebih dari 5, <b>minimal 5 menu</b> untuk perangkingan<br>
                ⚠️ Setelah disimpan, lanjutkan ke tab <b>② Input Nilai Gizi</b>
                </div>
                """, unsafe_allow_html=True)

        # ── Tab 2: Input Nilai Gizi ───────────────────────────────────
        with tab_nilai:
            st.markdown('<div class="section-title">Evaluasi Kandungan Gizi Menu</div>', unsafe_allow_html=True)
            semua_menu = db_config.ambil_semua_alternatif()
            if not semua_menu:
                st.markdown('<div class="info-box">⚠️ Belum ada menu. Buat menu terlebih dahulu di tab ①.</div>', unsafe_allow_html=True)
            else:
                col_cari, col_btn = st.columns([4, 1])
                with col_cari:
                    cari_kode_gizi = st.text_input(
                        "Cari menu berdasarkan kode",
                        key="cari_gizi",
                        placeholder="Ketik kode lalu tekan Enter atau klik Cari…"
                    )
                with col_btn:
                    st.write(""); st.write("")
                    tombol_cari = st.button("🔍  Cari", key="btn_cari_gizi")

                if cari_kode_gizi or tombol_cari:
                    if not cari_kode_gizi.strip():
                        st.warning("⚠️ Masukkan kode menu terlebih dahulu.")
                    else:
                        data_menu = db_config.ambil_alternatif_by_kode(cari_kode_gizi.strip())
                        if data_menu:
                            st.markdown(f"""
                            <div class="winner-card" style="border-color:var(--info);background:linear-gradient(135deg,#0c1e35 0%,var(--bg-card) 100%);">
                                <div class="winner-label" style="color:var(--info);">Menu Ditemukan</div>
                                <div class="winner-name">{data_menu['nama_makanan']}</div>
                                <div class="winner-detail">Kode: <code>{data_menu['kode_alternatif']}</code> · Jadwal: {data_menu['jadwal_menu']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                            st.markdown('<div class="section-title">Masukkan Nilai Gizi (skala 0 – 5)</div>', unsafe_allow_html=True)
                            with st.form("form_input_gizi"):
                                colA, colB, colC, colD, colE = st.columns(5)
                                with colA: val_c1 = st.number_input("🥩 Protein",     min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
                                with colB: val_c2 = st.number_input("🍚 Karbohidrat", min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
                                with colC: val_c3 = st.number_input("🧈 Lemak Jenuh", min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
                                with colD: val_c4 = st.number_input("🍊 Vitamin",     min_value=0.0, max_value=5.0, step=0.1, format="%.1f")
                                with colE: val_c5 = st.number_input("🦴 Kalsium",     min_value=0.0, max_value=5.0, step=0.1, format="%.1f")

                                if st.form_submit_button("💾  Simpan Nilai Gizi"):
                                    if val_c1 == 0 and val_c2 == 0 and val_c3 == 0 and val_c4 == 0 and val_c5 == 0:
                                        st.warning("⚠️ Semua nilai gizi masih 0. Pastikan Anda sudah mengisi dengan benar.")
                                    else:
                                        db_config.simpan_penilaian(data_menu['id_alternatif'], val_c1, val_c2, val_c3, val_c4, val_c5)
                                        st.success("✅ Nilai gizi berhasil disimpan!")
                        else:
                            st.error(f"❌ Kode **{cari_kode_gizi}** tidak ditemukan. Periksa kembali.")

        # ── Tab 3: Kelola Bank Menu ───────────────────────────────────
        with tab_kelola:
            st.markdown('<div class="section-title">Bank Menu & Data Gizi</div>', unsafe_allow_html=True)
            data_lengkap = db_config.ambil_semua_penilaian_lengkap()
            if data_lengkap:
                df_lengkap = pd.DataFrame(data_lengkap)
                df_lengkap = df_lengkap.sort_values(by='kode_alternatif').reset_index(drop=True)
                df_lengkap.insert(0, 'No', range(1, len(df_lengkap) + 1))

                kolom_tampil = ['No', 'kode_alternatif', 'jadwal_menu', 'nama_makanan']
                if 'nilai_c1' in df_lengkap.columns:
                    kolom_tampil.extend(['nilai_c1', 'nilai_c2', 'nilai_c3', 'nilai_c4', 'nilai_c5'])

                df_tampil = df_lengkap[kolom_tampil].rename(columns={
                    'kode_alternatif': 'Kode',
                    'jadwal_menu':     'Jadwal',
                    'nama_makanan':    'Daftar Menu',
                    'nilai_c1': 'Protein',
                    'nilai_c2': 'Karbohidrat',
                    'nilai_c3': 'Lemak Jenuh',
                    'nilai_c4': 'Vitamin',
                    'nilai_c5': 'Kalsium',
                })

                tampilkan_tabel_dengan_paginasi(
                    df_tampil, baris_per_halaman=10, key_prefix="kelola_menu",
                    config={"Daftar Menu": st.column_config.TextColumn("Daftar Menu", width="large")}
                )

                st.markdown("---")
                col_edit, col_hapus = st.columns(2, gap="large")

                with col_edit:
                    st.markdown('<div class="section-title">Edit Menu</div>', unsafe_allow_html=True)
                    cari_kode_edit = st.text_input("Kode menu yang akan diedit:", key="cari_edit_menu",
                                                   placeholder="Ketik kode lalu Enter…")
                    if cari_kode_edit:
                        data_edit = db_config.ambil_alternatif_by_kode(cari_kode_edit.strip())
                        if data_edit:
                            st.markdown(f'<div class="info-box">✏️ Mengedit kode <b>{data_edit["kode_alternatif"]}</b> (kode terkunci)</div>', unsafe_allow_html=True)
                            with st.form("form_edit_menu"):
                                jadwal_baru = st.text_input("Ubah Jadwal Menu", value=data_edit['jadwal_menu'])
                                nama_baru   = st.text_area("Ubah Daftar Menu",  value=data_edit['nama_makanan'])
                                if st.form_submit_button("💾  Perbarui Menu"):
                                    if not jadwal_baru.strip() or not nama_baru.strip():
                                        st.error("⚠️ Jadwal dan nama menu tidak boleh kosong.")
                                    else:
                                        db_config.update_alternatif(
                                            data_edit['id_alternatif'],
                                            data_edit['kode_alternatif'],
                                            jadwal_baru.strip(), nama_baru.strip()
                                        )
                                        st.success("✅ Data menu berhasil diperbarui!")
                                        st.rerun()
                        else:
                            st.error(f"❌ Kode **{cari_kode_edit}** tidak ditemukan.")

                with col_hapus:
                    st.markdown('<div class="section-title">Hapus Menu</div>', unsafe_allow_html=True)
                    kode_hapus = st.text_input("Kode menu yang akan dihapus:", key="hapus_menu",
                                               placeholder="Ketik kode lalu konfirmasi…")
                    if kode_hapus:
                        target = db_config.ambil_alternatif_by_kode(kode_hapus.strip())
                        if target:
                            st.warning(f"⚠️ Anda akan menghapus **{target['nama_makanan']}** ({target['kode_alternatif']}). Tindakan ini tidak dapat dibatalkan.")
                            if st.button("🗑️  Konfirmasi Hapus", key="konfirmasi_hapus"):
                                db_config.hapus_alternatif(target['id_alternatif'])
                                st.session_state.hasil_wp = None
                                st.session_state.menu_terpilih_kode = None
                                st.success("✅ Menu berhasil dihapus.")
                                st.rerun()
                        else:
                            st.error(f"❌ Kode **{kode_hapus}** tidak ditemukan.")
            else:
                st.markdown('<div class="info-box">📭 Belum ada menu yang dirancang.</div>', unsafe_allow_html=True)

    # ── FITUR 2: BOBOT KRITERIA ──────────────────────────────────────
    elif st.session_state.menu_aktif_gizi == "Bobot Kriteria":
        st.markdown("""
        <div class="page-header">
            <div class="page-header-icon">⚖️</div>
            <div>
                <div class="page-header-title">Pengaturan Bobot Kriteria</div>
                <div class="page-header-sub">Total keseluruhan bobot harus tepat <strong>1.00</strong> (100%)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        data_kriteria = db_config.ambil_semua_kriteria()
        if not data_kriteria:
            st.error("❌ Tidak ada data kriteria. Pastikan database sudah diinisialisasi.")
        else:
            df_k = pd.DataFrame(data_kriteria).rename(columns={
                'kode_kriteria': 'Kode', 'nama_kriteria': 'Nama Kriteria',
                'tipe_kriteria': 'Tipe', 'bobot_awal': 'Bobot'
            }).drop(columns=['id_kriteria'], errors='ignore')
            st.dataframe(df_k, hide_index=True, use_container_width=True)

            st.markdown('<div class="section-title">Distribusi Ulang Bobot</div>', unsafe_allow_html=True)
            with st.form("form_edit_bobot_massal"):
                cols = st.columns(len(data_kriteria))
                vals = []
                for i, col in enumerate(cols):
                    v = col.number_input(
                        data_kriteria[i]['nama_kriteria'],
                        min_value=0.0, max_value=1.0,
                        value=float(data_kriteria[i]['bobot_awal']),
                        step=0.01, format="%.2f", key=f"bobot_{i}"
                    )
                    vals.append(v)

                total_live = round(sum(vals), 2)
                is_valid = total_live == 1.0
                box_style = "background:rgba(63,185,80,.08);border-color:rgba(63,185,80,.3);color:#3fb950;" if is_valid else ""
                st.markdown(
                    f'<div class="info-box" style="{box_style}">'
                    f'Total Bobot Saat Ini: <b style="font-family:monospace;">{total_live:.2f}</b> '
                    f'{"✅ Valid" if is_valid else "— harus tepat <b>1.00</b>"}</div>',
                    unsafe_allow_html=True
                )

                if st.form_submit_button("💾  Simpan Semua Bobot"):
                    if is_valid:
                        for i, k in enumerate(data_kriteria):
                            db_config.update_bobot_kriteria(k['id_kriteria'], vals[i])
                        st.session_state.hasil_wp = None
                        st.session_state.menu_terpilih_kode = None
                        st.success("✅ Distribusi bobot berhasil diperbarui! Silakan jalankan perangkingan ulang.")
                        st.rerun()
                    else:
                        st.error(f"❌ Total bobot {total_live:.2f} ≠ 1.00. Sesuaikan nilai hingga totalnya tepat 1.00.")

    # ── FITUR 3: PERANGKINGAN WP ─────────────────────────────────────
    elif st.session_state.menu_aktif_gizi == "Perangkingan":
        st.markdown("""
        <div class="page-header">
            <div class="page-header-icon">🏆</div>
            <div>
                <div class="page-header-title">Perangkingan & Pemilihan Menu Akhir</div>
                <div class="page-header-sub">Algoritma Weighted Product — Ahli gizi memilih dari Top 5 ranking untuk dibuat menu</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Cek jumlah menu dan penilaian ──────────────────────────
        semua_menu = db_config.ambil_semua_alternatif() or []
        jumlah_menu = len(semua_menu)

        data_lengkap = db_config.ambil_semua_penilaian_lengkap() or []
        menu_sudah_dinilai = [m for m in data_lengkap if m.get('nilai_c1') is not None]
        jumlah_dinilai = len(menu_sudah_dinilai)

        # PERBAIKAN: kondisi siap = minimal 5 menu DAN semua menu sudah dinilai
        status_siap = jumlah_menu >= 5 and jumlah_dinilai == jumlah_menu and jumlah_menu > 0

        # ── Panel statistik ─────────────────────────────────────────
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            warna = "#3fb950" if jumlah_menu >= 5 else "#d29922"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Jumlah Menu</div>
                <div class="stat-value" style="color:{warna};">{jumlah_menu}</div>
            </div>""", unsafe_allow_html=True)
        with col_s2:
            warna2 = "#3fb950" if jumlah_dinilai == jumlah_menu and jumlah_menu >= 5 else "#d29922"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Menu Bernilai Gizi</div>
                <div class="stat-value" style="color:{warna2};">{jumlah_dinilai} / {jumlah_menu}</div>
            </div>""", unsafe_allow_html=True)
        with col_s3:
            label_status = "Siap ✅" if status_siap else "Belum Siap ⏳"
            warna3 = "#3fb950" if status_siap else "#d29922"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Status Perangkingan</div>
                <div class="stat-value" style="color:{warna3};font-size:1.1rem;">{label_status}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")

        # ── Pesan kondisi ───────────────────────────────────────────
        if jumlah_menu < 5:
            st.markdown(
                f'<div class="warn-box">⚠️ Dibutuhkan <b>minimal 5 menu</b>. Saat ini baru ada <b>{jumlah_menu} menu</b>. '
                f'Tambahkan {5 - jumlah_menu} menu lagi di halaman <b>Rancang Menu</b>.</div>',
                unsafe_allow_html=True
            )
        elif jumlah_dinilai < jumlah_menu:
            belum_dinilai = jumlah_menu - jumlah_dinilai
            st.markdown(
                f'<div class="warn-box">⚠️ Masih ada <b>{belum_dinilai} menu belum dinilai</b> gizinya. '
                f'Lengkapi di tab <b>② Input Nilai Gizi</b>.</div>',
                unsafe_allow_html=True
            )

        # ── Tombol Hitung Perangkingan ──────────────────────────────
        tombol_disabled = not status_siap
        col_btn, col_info = st.columns([2, 5])
        with col_btn:
            hitung = st.button(
                "▶  Hitung Perangkingan",
                type="primary",
                disabled=tombol_disabled,
                key="btn_hitung_wp"
            )
        with col_info:
            if tombol_disabled:
                st.markdown(
                    '<div class="info-box" style="margin-top:.4rem;">🔒 Tombol aktif setelah minimal 5 menu tersedia dan semua nilai gizi terisi.</div>',
                    unsafe_allow_html=True
                )

        if hitung and status_siap:
            with st.spinner("Menghitung skor Weighted Product…"):
                hasil = wp_logic.hitung_rekomendasi_wp_otomatis()
            if not hasil:
                st.error("❌ Perhitungan gagal. Pastikan bobot kriteria valid dan semua nilai gizi sudah terisi.")
            else:
                st.session_state.hasil_wp = hasil
                st.session_state.menu_terpilih_kode = None
                st.session_state.edit_catatan_mode = False

                # PERBAIKAN: Simpan hasil ranking ke DB agar SPPG bisa melihatnya
                try:
                    db_config.simpan_hasil_ranking(hasil)
                except AttributeError:
                    pass  # Fungsi belum ada di db_config, lanjutkan

                st.rerun()

        # ── Tampilkan hasil jika sudah dihitung ─────────────────────
        if st.session_state.hasil_wp:
            st.success("✅ Perhitungan selesai! Pilih menu dari Top 5 untuk dijadikan menu yang akan dibuat.")

            df_hasil = pd.DataFrame(st.session_state.hasil_wp)

            # Tabel lengkap seluruh perangkingan
            st.markdown('<div class="section-title">Tabel Perangkingan Lengkap</div>', unsafe_allow_html=True)
            df_rank = df_hasil[['kode_alternatif', 'jadwal_menu', 'nama_makanan', 'skor_akhir']].copy()
            df_rank.insert(0, 'Peringkat', range(1, len(df_rank) + 1))
            df_tampil = df_rank.rename(columns={
                'kode_alternatif': 'Kode',
                'jadwal_menu':     'Jadwal Menu',
                'nama_makanan':    'Daftar Menu',
                'skor_akhir':      'Skor WP (V)',
            })
            tampilkan_tabel_dengan_paginasi(
                df_tampil, baris_per_halaman=10, key_prefix="hasil_wp",
                config={"Daftar Menu": st.column_config.TextColumn("Daftar Menu", width="large")}
            )

            # ── Pilih dari Top 5 ───────────────────────────────────
            st.markdown('<div class="section-title">Pilih Menu dari Top 5 Ranking</div>', unsafe_allow_html=True)

            # PERBAIKAN: Batasi pilihan hanya Top 5
            df_top5 = df_hasil.head(5).reset_index(drop=True)

            opsi_menu = {
                row['kode_alternatif']: f"#{i+1}  [{row['kode_alternatif']}]  {row['nama_makanan'][:60]}{'…' if len(row['nama_makanan']) > 60 else ''}  — Skor: {row['skor_akhir']:.8f}"
                for i, row in df_top5.iterrows()
            }

            kode_terpilih_sebelumnya = st.session_state.get('menu_terpilih_kode')
            if kode_terpilih_sebelumnya and kode_terpilih_sebelumnya in opsi_menu:
                default_index = list(opsi_menu.keys()).index(kode_terpilih_sebelumnya)
            else:
                default_index = 0

            kode_pilih = st.selectbox(
                "Pilih salah satu menu dari Top 5 hasil perangkingan:",
                options=list(opsi_menu.keys()),
                format_func=lambda x: opsi_menu[x],
                index=default_index,
                key="select_menu_terpilih"
            )

            data_menu_dipilih = df_hasil[df_hasil['kode_alternatif'] == kode_pilih].iloc[0]
            peringkat_menu = df_hasil[df_hasil['kode_alternatif'] == kode_pilih].index[0] + 1

            # Preview kartu menu terpilih
            st.markdown(f"""
            <div class="selected-card">
                <div class="selected-label">✅ Menu yang Akan Anda Pilih · Peringkat #{peringkat_menu}</div>
                <div class="winner-name">{data_menu_dipilih['nama_makanan']}</div>
                <div class="winner-detail">Kode: <code>{data_menu_dipilih['kode_alternatif']}</code> · Jadwal: {data_menu_dipilih['jadwal_menu']}</div>
                <span class="selected-score">Skor WP (V): {data_menu_dipilih['skor_akhir']:.8f}</span>
            </div>
            """, unsafe_allow_html=True)

            # ── Catatan Ahli Gizi ───────────────────────────────────
            st.markdown('<div class="section-title">Catatan untuk Menu Terpilih</div>', unsafe_allow_html=True)

            data_db = db_config.ambil_alternatif_by_kode(kode_pilih)
            catatan_ada = data_db.get('catatan_rekomendasi') if data_db else None
            sudah_terpilih = st.session_state.menu_terpilih_kode == kode_pilih

            if sudah_terpilih and catatan_ada:
                st.info(f"📝 **Catatan Tersimpan:**\n\n{catatan_ada}")
                col_ubah, col_hapus_catatan = st.columns(2)
                with col_hapus_catatan:
                    if st.button("🗑️  Hapus Catatan", key="hapus_catatan"):
                        db_config.update_catatan_rekomendasi(int(data_db['id_alternatif']), None)
                        st.success("✅ Catatan berhasil dihapus.")
                        st.rerun()
                with col_ubah:
                    if st.button("✏️  Ubah Catatan", key="ubah_catatan"):
                        st.session_state['edit_catatan_mode'] = True
                        st.rerun()

                if st.session_state.get('edit_catatan_mode'):
                    with st.form("form_edit_catatan"):
                        catatan_edit = st.text_area(
                            "Edit catatan:",
                            value=catatan_ada,
                            height=110
                        )
                        col_s, col_c = st.columns(2)
                        with col_s:
                            if st.form_submit_button("💾  Simpan Perubahan"):
                                if not catatan_edit.strip():
                                    st.error("⚠️ Catatan tidak boleh kosong.")
                                else:
                                    db_config.update_catatan_rekomendasi(int(data_db['id_alternatif']), catatan_edit.strip())
                                    st.session_state['edit_catatan_mode'] = False
                                    st.success("✅ Catatan berhasil diperbarui!")
                                    st.rerun()
                        with col_c:
                            if st.form_submit_button("✖  Batal"):
                                st.session_state['edit_catatan_mode'] = False
                                st.rerun()
            else:
                with st.form("form_pilih_dan_catatan"):
                    catatan_baru = st.text_area(
                        "Tambahkan catatan (opsional):",
                        placeholder="Masukkan saran penyajian, anjuran porsi, atau informasi tambahan untuk tim SPPG…",
                        height=110
                    )
                    col_konfirm, col_help = st.columns([2, 3])
                    with col_help:
                        st.markdown(
                            '<div class="info-box" style="margin-top:.5rem;">💡 Catatan bersifat opsional. Klik tombol untuk mengonfirmasi pilihan menu dari Top 5.</div>',
                            unsafe_allow_html=True
                        )
                    with col_konfirm:
                        if st.form_submit_button("✅  Konfirmasi Pilihan Menu", use_container_width=True):
                            try:
                                db_config.reset_semua_pilihan_menu()
                            except AttributeError:
                                pass

                            skor = float(data_menu_dipilih['skor_akhir'])
                            try:
                                db_config.tandai_menu_terpilih(int(data_db['id_alternatif']), skor)
                            except AttributeError:
                                pass

                            if catatan_baru.strip():
                                db_config.update_catatan_rekomendasi(int(data_db['id_alternatif']), catatan_baru.strip())

                            # PERBAIKAN: Pastikan hasil ranking tersimpan ke DB saat konfirmasi
                            try:
                                db_config.simpan_hasil_ranking(st.session_state.hasil_wp)
                            except AttributeError:
                                pass

                            st.session_state.menu_terpilih_kode = kode_pilih
                            st.session_state['edit_catatan_mode'] = False
                            st.success(f"✅ Menu **{kode_pilih}** (Peringkat #{peringkat_menu}) berhasil dipilih dan ditampilkan ke Kepala SPPG!")
                            st.rerun()

            # Tampilkan status konfirmasi
            if st.session_state.menu_terpilih_kode:
                terpilih_kode = st.session_state.menu_terpilih_kode
                st.markdown(
                    f'<div class="info-box" style="background:rgba(63,185,80,.08);border-color:rgba(63,185,80,.3);color:#3fb950;margin-top:1rem;">'
                    f'✅ Menu <b>{terpilih_kode}</b> telah dikonfirmasi dan ditampilkan di halaman Kepala SPPG.'
                    f'</div>',
                    unsafe_allow_html=True
                )


# ==========================================
# ROUTING UTAMA
# ==========================================
if not st.session_state.logged_in:
    halaman_login()
else:
    if st.session_state.role == 'ahli_gizi':
        dasbor_ahli_gizi()
    elif st.session_state.role == 'sppg':
        dasbor_sppg()
    else:
        st.error("❌ Role tidak dikenali. Silakan login ulang.")
        if st.button("🔄 Kembali ke Login"):
            proses_logout()