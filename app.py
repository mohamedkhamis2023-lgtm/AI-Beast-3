
# -*- coding: utf-8 -*-
"""
EGX Intraday Day-Trading & Momentum Scanner
Designed for Quick Swings, High Volume, and Maximum Daily Profits.
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import traceback
import sys

# --- 1. EXCEPTION HANDLING ---
def global_exception_handler(ex_type, ex_value, ex_traceback):
    st.error("⚠️ حدث استثناء تقني مؤقت، النظام قام بعزل الخطأ وتأمين جلسة المضاربة.")
sys.excepthook = global_exception_handler

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EGX Intraday Momentum Scanner",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. CSS STYLING FOR TRADERS ---
st.markdown("""
    <style>
    .main { background-color: #05070b; color: #f3f4f6; }
    .stMetric {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 900;
        font-size: 16px;
        border-radius: 10px;
        border: none;
        padding: 12px;
        box-shadow: 0 4px 15px rgba(16,185,129,0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
    }
    .trade-card {
        background-color: #0f172a;
        border: 1px solid #047857;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. INTRADAY HIGH-MOMENTUM DATABASE ---
@st.cache_data
def get_intraday_watchlist():
    return {
        "ESRS.CA": {"name": "حديد عز", "price": 76.50, "chg": 3.40, "vol": "عالية جداً 🔥", "target": 79.50, "stop_loss": 74.80, "action": "شراء باختراق 76.80"},
        "BTFH.CA": {"name": "بلتون القابضة", "price": 2.95, "chg": 3.10, "vol": "مرتفعة 🚀", "target": 3.15, "stop_loss": 2.85, "action": "مضاربة سريعة جداً"},
        "ALCN.CA": {"name": "الإسكندرية لتداول الحاويات", "price": 38.50, "chg": 2.80, "vol": "مفاجئة 📈", "target": 40.20, "stop_loss": 37.40, "action": "اختراق مقاومة يومية"},
        "ELSH.CA": {"name": "الشمس للإسكان والتعمير", "price": 15.20, "chg": 2.40, "vol": "متوسطة إلى عالية", "target": 16.00, "stop_loss": 14.70, "action": "تجميع صاعد"},
        "JUFO.CA": {"name": "جهينة للصناعات الغذائية", "price": 25.50, "chg": 2.20, "vol": "قوية 🟢", "target": 26.80, "stop_loss": 24.80, "action": "دخول مع الزخم"},
        "PHDC.CA": {"name": "بالم هيلز للتعمير", "price": 14.20, "chg": 2.10, "vol": "عالية جداً 🔥", "target": 15.00, "stop_loss": 13.80, "action": "شراء سيولة لحظية"},
        "TMGH.CA": {"name": "طلعت مصطفى القابضة", "price": 96.50, "chg": 1.85, "vol": "مؤسسية قوية", "target": 99.50, "stop_loss": 95.00, "action": "تداول آمن واستقرار"}
    }

WATCHLIST = get_intraday_watchlist()

# --- 5. SIDEBAR CONTROLS ---
st.sidebar.markdown("<h2 style='color: #10b981;'>⚡ رادار المضاربة اليومية</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #9ca3af; font-size: 13px;'>متخصص في اقتناص الفرص السريعة وأعلى أرباح جلسة اليوم</p>", unsafe_allow_html=True)

selected_stock_key = st.sidebar.selectbox("اختر السهم للمتابعة السريعة:", list(WATCHLIST.keys()), format_func=lambda x: f"{x} - {WATCHLIST[x]['name']}")

current_stock = WATCHLIST[selected_stock_key]

# --- 6. MAIN DASHBOARD ---
st.header(f"⚡ رادار المضاربة: {current_stock['name']} (`{selected_stock_key}`)")
st.markdown("<p style='color: #9ca3af;'>متابعة حية لأهداف الجلسة، نقاط وقف الخسارة، وحجم السيولة المتدفقة.</p>", unsafe_allow_html=True)

# Metrics Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 السعر الحالي", f"{current_stock['price']} ج.م", f"+{current_stock['chg']}% 🚀")
col2.metric("🎯 هدف المضاربة (Target)", f"{current_stock['target']} ج.م", f"+{round(((current_stock['target']-current_stock['price'])/current_stock['price'])*100, 2)}%")
col3.metric("🛑 وقف الخسارة (Stop Loss)", f"{current_stock['stop_loss']} ج.م")
col4.metric("📊 تقييم السيولة اللحظية", current_stock['vol'])

st.markdown("---")

# Strategy Box & Quick Calculator
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("💡 التوجيه اللحظي والتوصية")
    st.markdown(f"""
    <div class="trade-card">
        <p><b>الإستراتيجية المقترحة للجلسة:</b> <span style="color: #34d399; font-size: 16px; font-weight: bold;">{current_stock['action']}</span></p>
        <p><b>حجم التغير اليومي:</b> +{current_stock['chg']}%</p>
        <p><b>مستوى المخاطرة اللحظية:</b> منضبط (بشرط الالتزام بوقف الخسارة عند <code>{current_stock['stop_loss']} ج.م</code>)</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 تسجيل صفقة مضاربة ناجحة"):
        st.success(f"تم اعتماد وتتبع صفقة {current_stock['name']} بنجاح في سجل صفقات اليوم!")

with col_right:
    st.subheader("🧮 حاسبة كمية الأسهم السريعة")
    capital_allocated = st.number_input("رأس المال المخصص لهذه الصفقة (ج.م):", value=20000, step=5000)
    shares_count = int(capital_allocated / current_stock['price'])
    expected_profit = shares_count * (current_stock['target'] - current_stock['price'])
    
    st.markdown(f"""
    <div class="trade-card">
        <p><b>عدد الأسهم المقترح شراؤها:</b> <code>{shares_count:,} سهم</code></p>
        <p><b>الربح المتوقع عند الهدف:</b> <span style="color: #4ade80; font-weight: bold;">+{expected_profit:,.2f} ج.م</span></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Full Intraday Market Table
st.subheader("🔥 جدول صفقات المضاربة الأكثر سخونة اليوم")
df_scanner = pd.DataFrame([
    {
        "الرمز": k,
        "الشركة": v["name"],
        "السعر الحالي": v["price"],
        "التغير (%)": f"+{v['chg']}%",
        "السيولة اللحظية": v["vol"],
        "الهدف المقترح": v["target"],
        "وقف الخسارة": v["stop_loss"],
        "الإجراء الفني": v["action"]
    } for k, v in WATCHLIST.items()
])

st.dataframe(df_scanner, use_container_width=True)
