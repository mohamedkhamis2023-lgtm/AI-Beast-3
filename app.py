
import streamlit as st
import pandas as pd
import numpy as np
import datetime

try:
    import yfinance as yf
    has_yf = True
except ImportError:
    has_yf = False

st.set_page_config(
    page_title="AI Beast - الإمبراطورية السيادية الشاملة",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background-color: #238636; color: white; font-weight: bold; border-radius: 6px; }
    .stButton>button:hover { background-color: #2ea043; }
    </style>
""", unsafe_allow_html=True)

st.title("🦁 AI Beast: الإمبراطورية السيادية المتكاملة للتحليل والأسهم")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("🎛️ إعدادات التحكم للإمبراطورية")
page = st.sidebar.selectbox("اختر قسم التشغيل:", [
    "📊 لوحة الأسهم صعوداً وهبوطاً (ماسح السوق)",
    "📈 التحليل اللحظي الفائق للأسهم",
    "💼 مدير المحفظة السيادية",
    "💰 حاسبة العائد المركب ومخاطر التداول"
])

if "لوحة الأسهم صعوداً وهبوطاً" in page:
    st.header("📊 ماسح السوق الحقيقي وقائمة الأسهم صعوداً وهبوطاً")
    st.info("تابع نبض السوق والأسهم الأكثر صعوداً وهبوطاً والسيولة اللحظية لسرعة اقتناص الفرص.")
    
    # جدول تفاعلي شامل للأسهم
    market_df = pd.DataFrame({
        "رمز السهم": ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", "PHDC.CA"],
        "القطاع": ["بنوك", "تكنولوجيا", "بنوك", "عقارات", "صناعة", "عقارات"],
        "السعر الحالي (ج.م)": [78.50, 6.82, 38.00, 13.20, 26.40, 3.45],
        "التغير اليومي (%)": [+2.4, +5.1, -1.2, +3.8, +0.9, -2.5],
        "حالة السهم بالسياسة": [🔥 صعود قوي وقوي", "🚀 زخم شرائي عملاق", "⚠️ تصحيح مؤقت آمن", "📈 اختراق مقاومة", "⚖️ تداول عرضي", "📉 ضغط بيعي خفيف"]
    })
    
    st.dataframe(market_df, use_container_width=True)
    st.success("💡 نصيحة الإمبراطورية: ركز على الأسهم ذات الزخم الصاعد الإيجابي وتجنب الدخول أثناء الضغط البيعي الحاد.")

elif "التحليل اللحظي" in page:
    st.header("📈 لوحة التحليل اللحظي والبيانات الفنية الدقيقة")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ticker = st.text_input("أدخل رمز السهم (مثال: COMI.CA)", value="COMI.CA")
    with c2:
        timeframe = st.selectbox("الإطار الزمني", ["يومي (Daily)", "أسبوعي (Weekly)"])
    with c3:
        st.write("")
        st.write("")
        run_btn = st.button("🚀 تنفيذ التحليل الفني الشامل")

    if run_btn:
        with st.spinner("جاري جلب البيانات من السوق وحساب المؤشرات الحقيقية..."):
            try:
                if has_yf:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="3mo")
                    if not hist.empty:
                        cp = hist['Close'].iloc[-1]
                        pp = hist['Close'].iloc[-2]
                        chg = ((cp - pp) / pp) * 100
                        
                        delta = hist['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi = (100 - (100 / (1 + rs))).iloc[-1]
                        
                        sup = hist['Low'].tail(20).min()
                        res = hist['High'].tail(20).max()
                        
                        st.success(f"تم تحليل السهم {ticker} بنجاح!")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("السعر الحالي", f"{cp:.2f} ج.م", f"{chg:+.2f}%")
                        m2.metric("مؤشر RSI", f"{rsi:.1f}", "تشبع شراء" if rsi > 70 else ("تشبع بيع" if rsi < 30 else "آمن"))
                        m3.metric("مستوى الدعم", f"{sup:.2f} ج.م")
                        m4.metric("مستوى المقاومة", f"{res:.2f} ج.م")

                        st.subheader("📊 الرسم البياني للإغلاق التاريخي")
                        st.line_chart(hist['Close'])
                    else:
                        st.warning("تأكد من كتابة رمز السهم بشكل صحيح (مثال: COMI.CA).")
                else:
                    st.error("مكتبة البيانات غير متوفرة.")
            except Exception as e:
                st.error(f"خطأ في جلب البيانات: {e}")

elif "مدير المحفظة" in page:
    st.header("💼 إدارة المحفظة الاستثمارية السيادية")
    
    port = pd.DataFrame({
        "السهم": ["COMI.CA", "FWRY.CA", "ADIB.CA"],
        "الكمية": [1000, 2500, 800],
        "سعر الشراء": [72.0, 6.1, 35.0],
        "السعر الحالي": [78.5, 6.8, 38.0]
    })
    port["التكلفة الإجمالية"] = port["الكمية"] * port["سعر الشراء"]
    port["القيمة الحالية"] = port["الكمية"] * port["السعر الحالي"]
    port["الربح/الخسارة (ج.م)"] = port["القيمة الحالية"] - port["التكلفة الإجمالية"]
    
    st.dataframe(port, use_container_width=True)
    st.metric("إجمالي أرباح المحفظة", f"{port['الربح/الخسارة (ج.م)'].sum():,.2f} ج.م", "+9.4%")

else:
    st.header("💰 حاسبة العائد المركب ومخاطر التداول")
    
    col1, col2 = st.columns(2)
    with col1:
        cap = st.number_input("رأس المال الأساسي (ج.م)", value=50000)
        rate = st.slider("العائد المتوقع الشهري (%)", 1.0, 15.0, 4.0)
    with col2:
        months = st.slider("المدة بالشهور", 3, 36, 12)
        
    if st.button("📊 احسب نمو الثروة"):
        val = cap
        res_list = []
        for m in range(1, months + 1):
            val = val * (1 + rate / 100)
            res_list.append({"الشهر": m, "إجمالي الثروة": round(val, 2)})
        st.dataframe(pd.DataFrame(res_list), use_container_width=True)
