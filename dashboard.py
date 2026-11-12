from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Ruang Nilai | Student Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "data.csv"

SCORE_COLUMNS = ["math score", "reading score", "writing score"]
SCORE_LABELS = {
    "math score": "Matematika",
    "reading score": "Membaca",
    "writing score": "Menulis",
}
GREEN = "#23865B"
DARK_GREEN = "#155C40"
MINT = "#DDF3E7"
GRAY = "#64748B"
PALE = "#F4F7F5"

# ----------------------------- VISUAL STYLE -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --green: #23865B;
    --green-dark: #155C40;
    --green-soft: #DDF3E7;
    --ink: #1F2933;
    --muted: #64748B;
    --line: #DCE7DF;
    --surface: #FFFFFF;
    --canvas: #F4F7F5;
}
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}
.stApp { background: var(--canvas); }
.block-container {
    max-width: 1440px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #EDF4EF !important;
    border-right: 1px solid #DDE8E0;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.6rem; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #234B38 !important;
}

/* Typography */
h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.035em;
}
h1 { font-weight: 800 !important; }
h2, h3 { font-weight: 750 !important; }
p, li { color: #52615A; }

/* Metric cards */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 17px 18px;
    box-shadow: 0 3px 12px rgba(31, 55, 42, .035);
}
[data-testid="stMetricLabel"] p {
    color: #728078 !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #1D6747 !important;
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
}
[data-testid="stMetricDelta"] { font-size: .75rem; }

/* High-contrast Plotly text: titles, axis labels, ticks, legends and colorbars */
div[data-testid="stPlotlyChart"] .js-plotly-plot .gtitle {
    fill: #1F2933 !important;
}
div[data-testid="stPlotlyChart"] .js-plotly-plot .xtick text,
div[data-testid="stPlotlyChart"] .js-plotly-plot .ytick text,
div[data-testid="stPlotlyChart"] .js-plotly-plot .legend text,
div[data-testid="stPlotlyChart"] .js-plotly-plot .cbaxis text {
    fill: #405247 !important;
}
div[data-testid="stPlotlyChart"] .js-plotly-plot .xtitle,
div[data-testid="stPlotlyChart"] .js-plotly-plot .ytitle {
    fill: #26382E !important;
}

/* Charts and tables */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 9px 10px 2px 10px;
    box-shadow: 0 3px 12px rgba(31, 55, 42, .025);
}
div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 14px;
    overflow: hidden;
}
hr { border-color: #E3EBE5; }

/* Selectbox */
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #DCE7DF !important;
    border-radius: 10px !important;
    color: #26382E !important;
}

/* MULTISELECT - kotak filter senada dengan sidebar (selector lebar, tidak bergantung versi Streamlit) */
section[data-testid="stSidebar"] [data-baseweb="select"],
section[data-testid="stSidebar"] [data-baseweb="select"] div,
section[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-baseweb="select"] > div,
[data-baseweb="select"] > div > div {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #26382E !important;
}
[data-baseweb="select"] > div {
    border: 1px solid #BFD8C9 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-baseweb="select"] > div:hover,
[data-baseweb="select"] > div:focus-within {
    border-color: #23865B !important;
    box-shadow: 0 0 0 3px rgba(35, 134, 91, .15) !important;
}

/* Chip terpilih: harus lebih spesifik daripada aturan di atas */
section[data-testid="stSidebar"] [data-baseweb="select"] span[data-baseweb="tag"],
section[data-testid="stSidebar"] [data-baseweb="select"] div[data-baseweb="tag"],
[data-baseweb="select"] [data-baseweb="tag"] {
    background: #23865B !important;
    background-color: #23865B !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="tag"] *,
[data-baseweb="select"] [data-baseweb="tag"] * {
    background: transparent !important;
    background-color: transparent !important;
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* Teks input dan placeholder */
[data-baseweb="select"] input {
    color: #26382E !important;
    caret-color: #23865B !important;
}
[data-baseweb="select"] input::placeholder { color: #849087 !important; }

/* Ikon hapus dan dropdown */
section[data-testid="stSidebar"] [data-baseweb="select"] svg:not([data-baseweb="tag"] svg) {
    color: #64786B !important;
    fill: #64786B !important;
}

/* MULTISELECT - Streamlit versi baru (tanpa baseweb) */
[data-testid="stMultiSelect"] div:has(> [data-testid="stMultiSelectTagsContainer"]) {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #BFD8C9 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-testid="stMultiSelect"] div:has(> [data-testid="stMultiSelectTagsContainer"]):hover,
[data-testid="stMultiSelect"] div:has(> [data-testid="stMultiSelectTagsContainer"])[data-focus-within],
[data-testid="stMultiSelect"] div:has(> [data-testid="stMultiSelectTagsContainer"]):focus-within {
    border-color: #23865B !important;
    box-shadow: 0 0 0 3px rgba(35, 134, 91, .15) !important;
}
[data-testid="stMultiSelect"] [data-tag] {
    background: #23865B !important;
    background-color: #23865B !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
}
[data-testid="stMultiSelect"] [data-tag] * {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}
[data-testid="stMultiSelect"] input {
    color: #26382E !important;
    caret-color: #23865B !important;
    background: transparent !important;
}
[data-testid="stMultiSelect"] svg {
    color: #64786B;
    fill: #64786B;
}
[data-testid="stMultiSelect"] [data-tag] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}
[data-testid="stMultiSelectDropdown"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #DCE7DF !important;
}
[data-testid="stMultiSelectDropdown"] [role="option"] {
    background: #FFFFFF !important;
    color: #26382E !important;
}
[data-testid="stMultiSelectDropdown"] [role="option"]:hover,
[data-testid="stMultiSelectDropdown"] [role="option"][data-focused],
[data-testid="stMultiSelectDropdown"] [role="option"][aria-selected="true"] {
    background: #DDF3E7 !important;
    color: #155C40 !important;
}

/* Dropdown menu */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
}
[data-baseweb="popover"] [role="option"] {
    background: #FFFFFF !important;
    color: #26382E !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [role="option"][aria-selected="true"] {
    background: #DDF3E7 !important;
    color: #155C40 !important;
}

/* Radio controls */
[data-testid="stRadio"] label { color: #34483B !important; }

/* Hero */
.hero {
    background: linear-gradient(115deg, #155C40 0%, #23865B 58%, #56A879 100%);
    border-radius: 22px;
    padding: 30px 34px;
    color: #FFFFFF;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}
.hero:after {
    content: "";
    position: absolute;
    width: 260px; height: 260px;
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 50%;
    right: -45px; top: -130px;
    box-shadow: 0 0 0 28px rgba(255,255,255,.045), 0 0 0 58px rgba(255,255,255,.035);
}
.hero-kicker {
    color: #C9F1D9; font-size: .76rem; font-weight: 800;
    letter-spacing: .14em; text-transform: uppercase; margin-bottom: 10px;
}
.hero-title {
    font-family: 'Manrope', sans-serif; font-size: clamp(1.7rem, 3vw, 2.5rem);
    line-height: 1.12; font-weight: 800; color: #FFFFFF; margin: 0 0 10px 0;
}
.hero-desc { color: #E2F5E9; font-size: .96rem; max-width: 760px; margin: 0; }
.hero-tag {
    display: inline-block; margin-top: 19px; padding: 6px 11px;
    border: 1px solid rgba(255,255,255,.28); border-radius: 30px;
    color: #F2FFF6; font-size: .75rem; font-weight: 700;
}

/* Section headings and insight blocks */
.section-head {
    display: flex; align-items: center; gap: 12px;
    margin: 27px 0 5px 0;
}
.section-no {
    display: inline-flex; align-items: center; justify-content: center;
    width: 34px; height: 34px; border-radius: 11px;
    background: #DDF3E7; color: #176344; font-weight: 800; font-size: .9rem;
}
.section-title {
    font-family: 'Manrope', sans-serif; font-size: 1.25rem;
    font-weight: 800; color: #24352B;
}
.section-sub { color: #77847C; font-size: .88rem; margin: 0 0 14px 46px; }
.insight {
    background: #EAF5EE; border-left: 4px solid #23865B;
    border-radius: 0 12px 12px 0; padding: 13px 16px;
    color: #315A43; font-size: .88rem; margin: 8px 0 15px 0;
}
.soft-card {
    background: #FFFFFF; border: 1px solid #E4EBE6; border-radius: 16px;
    padding: 17px 19px; height: 100%;
}
.soft-label {
    color: #758279; font-size: .76rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .07em;
}
.soft-value {
    color: #1D6747; font-family: 'Manrope', sans-serif;
    font-size: 1.55rem; font-weight: 800; margin-top: 4px;
}
.soft-note { color: #7B8980; font-size: .78rem; margin-top: 3px; }
.footer-note { color: #87938B; font-size: .76rem; text-align: center; padding-top: 22px; }

[data-testid="stExpander"] {
    border: 1px solid #E1EAE3;
    border-radius: 13px;
    background: #FFFFFF;
}
.stButton button {
    background: #23865B;
    color: #FFFFFF;
    border: 0;
    border-radius: 10px;
}
.stButton button:hover {
    background: #155C40;
    color: #FFFFFF;
    border: 0;
}
@media (max-width: 700px) {
    .hero { padding: 24px 22px; border-radius: 17px; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)
# ----------------------------- DATA -----------------------------
@st.cache_data
def load_data(path: str) -> tuple[pd.DataFrame, int, int]:
    raw = pd.read_csv(path)
    missing_before = int(raw.isna().sum().sum())
    duplicates_before = int(raw.duplicated().sum())

    df = raw.copy()
    df.columns = df.columns.str.strip().str.lower()

    for col in SCORE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.drop_duplicates().copy()

    for col in SCORE_COLUMNS:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    categories = [
        "gender", "race/ethnicity", "parental level of education",
        "lunch", "test preparation course"
    ]
    for col in categories:
        if df[col].isna().any() and not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])

    df["average score"] = df[SCORE_COLUMNS].mean(axis=1)
    df["total score"] = df[SCORE_COLUMNS].sum(axis=1)
    return df, missing_before, duplicates_before


if not DATA_PATH.exists():
    st.error("File data/data.csv tidak ditemukan. Letakkan CSV di dalam folder data.")
    st.stop()

data, missing_before, duplicates_before = load_data(str(DATA_PATH))

# ----------------------------- SIDEBAR -----------------------------
with st.sidebar:
    st.markdown("## 🌿 Ruang Nilai")
    st.caption("Student Academic Performance")
    st.markdown("---")
    st.markdown("### Saring data")
    genders = sorted(data["gender"].dropna().unique().tolist())
    preps = sorted(data["test preparation course"].dropna().unique().tolist())
    lunches = sorted(data["lunch"].dropna().unique().tolist())

    chosen_gender = st.multiselect("Gender", genders, default=genders)
    chosen_prep = st.multiselect("Persiapan ujian", preps, default=preps)
    chosen_lunch = st.multiselect("Kategori makan siang", lunches, default=lunches)

    st.markdown("---")
    st.markdown("**Panduan filter**")
    st.caption("Pilih satu atau beberapa kategori. Seluruh ringkasan dan grafik akan mengikuti pilihan ini.")
    if st.button("Atur ulang filter", use_container_width=True):
        st.rerun()

filtered = data[
    data["gender"].isin(chosen_gender)
    & data["test preparation course"].isin(chosen_prep)
    & data["lunch"].isin(chosen_lunch)
].copy()

# ----------------------------- HERO -----------------------------
st.markdown("""
<div class="hero">
  <div class="hero-kicker">Statistika dan Probabilitas 1 · Kelas A</div>
  <div class="hero-title">Membaca Performa<br>Akademik Siswa</div>
  <p class="hero-desc">Eksplorasi nilai matematika, membaca, dan menulis melalui ringkasan statistik dan visualisasi interaktif.</p>
  <span class="hero-tag">DATA EXPLORATION / 01</span>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:end;">'
    '<div><div style="font-size:.75rem;color:#23865B;font-weight:800;letter-spacing:.1em;">OVERVIEW</div>'
    '<div style="font-family:Manrope;font-size:1.35rem;font-weight:800;color:#25372C;">Gambaran umum data</div></div>'
    '<div style="font-size:.8rem;color:#849087;">Sumber: Kaggle · Students Performance in Exams</div></div>',
    unsafe_allow_html=True
)

if filtered.empty:
    st.warning("Tidak ada siswa yang cocok dengan filter saat ini. Pilih kembali kategori pada sidebar.")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Siswa terpilih", f"{len(filtered):,}", help="Jumlah baris setelah filter.")
m2.metric("Rata-rata keseluruhan", f"{filtered['average score'].mean():.1f}", help="Rata-rata dari tiga mata pelajaran.")
m3.metric("Median keseluruhan", f"{filtered['average score'].median():.1f}")
m4.metric("Rata-rata tertinggi", f"{filtered['average score'].max():.1f}")

# Chart defaults
plot_config = dict(
    template="plotly_white",
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font=dict(
        family="DM Sans, sans-serif",
        size=13,
        color="#26382E"
    ),
    xaxis=dict(
        title_font=dict(size=13, color="#26382E"),
        tickfont=dict(size=12, color="#405247"),
        color="#405247",
        showgrid=True,
        gridcolor="#E5ECE7",
        zerolinecolor="#D5E1D9",
        linecolor="#D5E1D9"
    ),
    yaxis=dict(
        title_font=dict(size=13, color="#26382E"),
        tickfont=dict(size=12, color="#405247"),
        color="#405247",
        showgrid=True,
        gridcolor="#E5ECE7",
        zerolinecolor="#D5E1D9",
        linecolor="#D5E1D9"
    ),
    legend=dict(
        font=dict(size=12, color="#26382E"),
        title_font=dict(size=12, color="#26382E")
    ),
    margin=dict(l=48, r=35, t=68, b=48)
)

green_scale = ["#DDF3E7", "#A9DCC0", "#65B58B", "#23865B", "#155C40"]

# ----------------------------- QUESTION 1 -----------------------------
st.markdown('<div class="section-head"><span class="section-no">01</span><span class="section-title">Apakah persiapan ujian berkaitan dengan nilai?</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Bandingkan capaian tiga mata pelajaran antara siswa yang menyelesaikan persiapan ujian dan yang tidak.</div>', unsafe_allow_html=True)

prep = (
    filtered.groupby("test preparation course")[SCORE_COLUMNS]
    .mean().reset_index()
    .melt(id_vars="test preparation course", var_name="Mata Pelajaran", value_name="Rata-rata")
)
prep["Mata Pelajaran"] = prep["Mata Pelajaran"].map(SCORE_LABELS)
fig_prep = px.bar(
    prep, x="test preparation course", y="Rata-rata", color="Mata Pelajaran",
    barmode="group", color_discrete_sequence=["#155C40", "#65B58B", "#B9DCC7"],
    labels={"test preparation course": "Persiapan ujian", "Rata-rata": "Rata-rata nilai (0–100)"},
    range_y=[0, 100],
)
fig_prep.update_layout(**plot_config, legend_title_text="")
fig_prep.update_traces(marker_line_width=0, marker_cornerradius=5)
st.plotly_chart(fig_prep, use_container_width=True)

if {"completed", "none"}.issubset(set(filtered["test preparation course"].unique())):
    means = filtered.groupby("test preparation course")["average score"].mean()
    delta = means["completed"] - means["none"]
    direction = "lebih tinggi" if delta >= 0 else "lebih rendah"
    st.markdown(
        f'<div class="insight"><b>Catatan analisis:</b> Pada data terpilih, rata-rata kelompok yang menyelesaikan persiapan ujian '
        f'{abs(delta):.2f} poin {direction} dibanding kelompok yang tidak mengikuti persiapan. '
        'Perbedaan ini menunjukkan pola pada dataset, bukan bukti sebab-akibat.</div>',
        unsafe_allow_html=True
    )
else:
    st.info("Pilih kedua kategori persiapan ujian pada sidebar untuk melihat perbandingan langsung.")

# ----------------------------- QUESTION 2 -----------------------------
st.markdown('<div class="section-head"><span class="section-no">02</span><span class="section-title">Bagaimana hubungan antar mata pelajaran?</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Korelasi dan scatter plot membantu melihat apakah nilai pada satu pelajaran bergerak searah dengan pelajaran lain.</div>', unsafe_allow_html=True)

c_corr, c_scatter = st.columns([0.92, 1.35], gap="large")
corr = filtered[SCORE_COLUMNS].corr().rename(index=SCORE_LABELS, columns=SCORE_LABELS)
with c_corr:
    fig_corr = px.imshow(
        corr, text_auto=".2f", zmin=-1, zmax=1, aspect="auto",
        color_continuous_scale=["#DCE8E0", "#FFFFFF", "#23865B"],
        labels={"color": "Korelasi"},
    )
    fig_corr.update_layout(
        **plot_config,
        title="Matriks korelasi",
        coloraxis_colorbar=dict(
            title=dict(text="Korelasi", font=dict(size=13, color="#26382E")),
            tickfont=dict(size=12, color="#405247"),
            outlinecolor="#D5E1D9"
        )
    )
    fig_corr.update_traces(
        textfont=dict(color="#FFFFFF", size=14),
        xgap=1,
        ygap=1
    )
    st.plotly_chart(fig_corr, use_container_width=True)
with c_scatter:
    col_x, col_y = st.columns(2)
    with col_x:
        x_choice = st.selectbox("Sumbu X", SCORE_COLUMNS, index=0, format_func=lambda x: SCORE_LABELS[x], key="x_new")
    with col_y:
        y_choice = st.selectbox("Sumbu Y", SCORE_COLUMNS, index=1, format_func=lambda x: SCORE_LABELS[x], key="y_new")
    fig_scatter = px.scatter(
        filtered, x=x_choice, y=y_choice, color="gender",
        color_discrete_sequence=["#23865B", "#A5B4AA"],
        opacity=0.65,
        labels={x_choice: f"Nilai {SCORE_LABELS[x_choice]}", y_choice: f"Nilai {SCORE_LABELS[y_choice]}", "gender": "Gender"},
    )
    fig_scatter.update_layout(**plot_config, title="Sebaran hubungan nilai", legend_title_text="")
    fig_scatter.update_traces(marker=dict(size=8, line=dict(width=0.5, color="white")))
    st.plotly_chart(fig_scatter, use_container_width=True)

corr_value = filtered[x_choice].corr(filtered[y_choice])
st.markdown(
    f'<div class="insight"><b>Interpretasi:</b> Korelasi Pearson antara nilai {SCORE_LABELS[x_choice].lower()} dan '
    f'{SCORE_LABELS[y_choice].lower()} adalah <b>{corr_value:.3f}</b>. Nilai positif menunjukkan kecenderungan bergerak searah; '
    'korelasi tidak otomatis berarti hubungan sebab-akibat.</div>',
    unsafe_allow_html=True
)

# ----------------------------- QUESTION 3 -----------------------------
st.markdown('<div class="section-head"><span class="section-no">03</span><span class="section-title">Apakah kelompok siswa memiliki sebaran nilai berbeda?</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Pilih karakteristik kelompok untuk membandingkan median, rentang, dan variasi rata-rata nilai.</div>', unsafe_allow_html=True)

group_mode = st.radio("Bandingkan berdasarkan", ["Gender", "Kategori makan siang"], horizontal=True)
group_col = "gender" if group_mode == "Gender" else "lunch"
group_title = "Gender" if group_mode == "Gender" else "Kategori makan siang"

fig_box = px.box(
    filtered, x=group_col, y="average score", color=group_col,
    points="outliers",
    color_discrete_sequence=["#23865B", "#B8C9BE", "#65B58B"],
    labels={group_col: group_title, "average score": "Rata-rata nilai (0–100)"},
)
fig_box.update_layout(**plot_config, title=f"Distribusi nilai berdasarkan {group_title}", showlegend=False)
st.plotly_chart(fig_box, use_container_width=True)
st.markdown(
    '<div class="insight"><b>Cara membaca:</b> Garis di tengah kotak menunjukkan median. Kotak menggambarkan rentang kuartil, '
    'sedangkan titik di luar whisker dapat menunjukkan nilai pencilan (outlier).</div>',
    unsafe_allow_html=True
)

# ----------------------------- STATISTICS -----------------------------
st.markdown('<div class="section-head"><span class="section-no">04</span><span class="section-title">Ringkasan statistik dan distribusi</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Ukuran pemusatan dan penyebaran untuk setiap mata pelajaran.</div>', unsafe_allow_html=True)

desc = filtered[SCORE_COLUMNS].describe().T
desc["Median"] = filtered[SCORE_COLUMNS].median()
desc["IQR"] = filtered[SCORE_COLUMNS].quantile(.75) - filtered[SCORE_COLUMNS].quantile(.25)
desc = desc.rename(index=SCORE_LABELS)
desc = desc[["count", "mean", "Median", "std", "min", "25%", "50%", "75%", "max", "IQR"]]
desc.columns = ["Jumlah", "Mean", "Median", "Std. Deviasi", "Minimum", "Q1", "Q2", "Q3", "Maksimum", "IQR"]
st.dataframe(desc.round(2), use_container_width=True)

left, right = st.columns([1.2, 1], gap="large")
with left:
    score_choice = st.selectbox("Pilih nilai untuk melihat distribusi", SCORE_COLUMNS, format_func=lambda x: SCORE_LABELS[x], key="distribution_score")
    fig_hist = px.histogram(
        filtered, x=score_choice, nbins=20,
        color_discrete_sequence=["#65B58B"],
        labels={score_choice: "Nilai", "count": "Jumlah siswa"},
    )
    fig_hist.update_layout(**plot_config, title=f"Distribusi nilai {SCORE_LABELS[score_choice].lower()}")
    fig_hist.update_traces(marker_line_color="white", marker_line_width=1)
    st.plotly_chart(fig_hist, use_container_width=True)
with right:
    q1 = filtered[score_choice].quantile(.25)
    q3 = filtered[score_choice].quantile(.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outlier_count = int(((filtered[score_choice] < lower) | (filtered[score_choice] > upper)).sum())
    st.markdown('<div class="soft-card"><div class="soft-label">Deteksi outlier · metode IQR</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="soft-value">{outlier_count} siswa</div><div class="soft-note">Nilai {SCORE_LABELS[score_choice].lower()} berada di luar batas IQR.</div><hr>', unsafe_allow_html=True)
    st.markdown(f'<div class="soft-label">Rentang kuartil (IQR)</div><div class="soft-value">{iqr:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="soft-note">Batas bawah: {lower:.2f} · Batas atas: {upper:.2f}</div></div>', unsafe_allow_html=True)

# ----------------------------- DATA QUALITY -----------------------------
with st.expander("Lihat informasi data dan proses pembersihan"):
    a, b, c = st.columns(3)
    a.metric("Baris pada file asli", f"{len(data) + duplicates_before:,}")
    b.metric("Missing value awal", f"{missing_before}")
    c.metric("Duplikat awal", f"{duplicates_before}")
    st.write(
        "Pengolahan data mencakup perapian nama kolom, konversi nilai pelajaran ke tipe numerik, "
        "penghapusan baris duplikat, penanganan nilai kosong (median untuk numerik dan modus untuk kategori), "
        "serta pembuatan kolom rata-rata dan total nilai."
    )
    st.write("Dataset memiliki 1.000 baris dan 8 kolom pada file sumber, dengan 3 kolom nilai numerik dan 5 kolom kategori.")

st.markdown(
    '<div class="footer-note">Ruang Nilai · Student Performance Analysis · Dataset: Kaggle / Students Performance in Exams<br>'
    'Dataset tidak memiliki kolom tanggal/waktu, sehingga dashboard ini berfokus pada perbandingan dan hubungan antarvariabel.</div>',
    unsafe_allow_html=True
)
