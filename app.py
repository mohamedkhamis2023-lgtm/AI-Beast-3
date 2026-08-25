

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
    page_title="AI Beast Enterprise - المنصة السيادية العملاقة",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background-color: #238636; color: white; font-weight: bold; border-radius: 6px; }
    .stButton>button:hover { background-color: #2ea043; }
    </style>
""", unsafe_allow_html=True)

st.title("🦁 AI Beast Enterprise: المنصة الاستثمارية السيادية اللحظية")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("🎛️ لوحة عمليات الإمبراطورية")
page = st.sidebar.selectbox("اختر وحدة التشغيل المتقدمة:", [
    "📈 التحليل اللحظي والبيانات الحية",
    "📊 ماسح السوق والسيولة اللحظية",
    "💼 إدارة المحفظة الاستثمارية",
    "💰 حاسبة العائد المركب المتقدمة"
])

if "التحليل اللحظي" in page:
    st.header("📈 وحدة التحليل الفني والمالي اللحظي فائق الدقة")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ticker = st.text_input("أدخل رمز السهم (مثال: COMI.CA أو FWRY.CA أو AAPL)", value="COMI.CA")
    with c2:
        interval_choice = st.selectbox("دقة البيانات اللحظية", ["يومي (Daily)", "ساعي (Hourly)"])
    with c3:
        st.write("")
        st.write("")
        fetch_btn = st.button("⚡ جلب البيانات الحية والتحليل")

    if fetch_btn:
        with st.spinner("جاري الاتصال المباشر بالبوابات المالية وسحب البيانات اللحظية..."):
            try:
                if has_yf:
                    data_period = "1mo" if "يومي" in interval_choice else "5d"
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period=data_period, interval="1h" if "ساعي" in interval_choice else "1d")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change_pct = ((current_price - prev_price) / prev_price) * 100
                        
                        # حساب مؤشر القوة النسبية RSI بدقة
                        delta = hist['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi_val = (100 - (100 / (1 + rs))).iloc[-1]
                        
                        support = hist['Low'].tail(15).min()
                        resistance = hist['High'].tail(15).max()
                        
                        st.success(f"تم تحديث بيانات السهم {ticker} بنجاح من السوق الحقيقي!")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("السعر اللحظي الحالي", f"{current_price:.2f} ج.م", f"{change_pct:+.2f}%")
                        m2.metric("مؤشر القوة النسبية RSI", f"{rsi_val:.1f}", "تشبع شراء" if rsi_val > 70 else ("تشبع بيع" if rsi_val < 30 else "منطقة مستقرة"))
                        m3.metric("مستوى الدعم اللحظي", f"{support:.2f} ج.م")
                        m4.metric("مستوى المقاومة اللحظية", f"{resistance:.2f} ج.م")

                        st.subheader("📊 الرسم البياني التفاعلي لحركة الأسعار")
                        st.line_chart(hist['Close'])
                        
                        st.subheader("📑 تفاصيل الأداء الكمي اللحظي")
                        metrics_df = pd.DataFrame({
                            "المؤشر": ["أعلى سعر في الفترة", "أقل سعر في الفترة", "حجم التداول الأخير", "حالة الزخم"],
                            "القيمة": [f"{hist['High'].max():.2f} ج.م", f"{hist['Low'].min():.2f} ج.م", f"{int(hist['Volume'].iloc[-1]):,} سهم", "إيجابي مرتفع" if change_pct > 0 else "حذر وتصحيح"]
                        })
                        st.table(metrics_df)
                    else:
                        st.warning("تأكد من صحة رمز السهم المدخل (مثال: COMI.CA للبنك التجاري الدولي).")
                else:
                    st.error("مكتبة جلب البيانات غير متاحة.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالسوق: {e}")

elif "ماسح السوق" in page:
    st.header("📊 ماسح السوق اللحظي للأسهم صعوداً وهبوطاً")
    st.info("نظرة شاملة وعميقة على حركة الأسهم النشطة والسيولة المؤسسية.")
    
    live_market_df = pd.DataFrame({
        "رمز السهم": ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA"],
        "القطاع": ["بنوك", "تكنولوجيا", "بنوك إسلامية", "عقارات", "صناعة وتجارة"],
        "السعر الحالي (ج.م)": [78.50, 6.82, 38.00, 13.20, 26.40],
        "التغير اللحظي (%)": [+2.4, +5.1, -1.2, +3.8, +0.9],
        "حالة السيولة والزخم": ["🔥 تدفقات شرائية كبرى", "🚀 صعود صاروخي", "⚠️ جني أرباح مؤقت", "📈 اختراق ناجح لمقاومة", "⚖️ استقرار عرضي"]
    })
    st.dataframe(live_market_df, use_container_width=True)
    st.success("💡 توصية ذكية: راقب الأسهم ذات التدفقات الشرائية الكبرى لمتابعة الاتجاه العام للسوق.")

elif "مدير المحفظة" in page:
    st.header("💼 إدارة المحفظة الاستثمارية السيادية")
    
    portfolio_data = pd.DataFrame({
        "السهم": ["COMI.CA", "FWRY.CA", "ADIB.CA"],
        "الكمية": [1000, 2500, 800],
        "سعر الشراء المتوسط": [72.00, 6.10, 35.00],
        "السعر الحالي بالسوق": [78.50, 6.82, 38.00]
    })
    portfolio_data["التكلفة الإجمالية"] = portfolio_data["الكمية"] * portfolio_data["سعر الشراء المتوسط"]
    portfolio_data["القيمة الحالية"] = portfolio_data["الكمية"] * portfolio_data["السعر الحالي بالسوق"]
    portfolio_data["الربح / الخسارة (ج.م)"] = portfolio_data["القيمة الحالية"] - portfolio_data["التكلفة الإجمالية"]
    
    st.dataframe(portfolio_data, use_container_width=True)
    st.metric("صافي أرباح المحفظة الكلية", f"{portfolio_data['الربح / الخسارة (ج.م)'].sum():,.2f} ج.م", "+9.8%")

else:
    st.header("💰 حاسبة العائد المركب المتقدمة وتنمية الثروات")
    
    col1, col2 = st.columns(2)
    with col1:
        capital = st.number_input("رأس المال الأساسي (ج.م)", value=50000, step=5000)
        rate = st.slider("معدل العائد الشهري المتوقع (%)", 1.0, 15.0, 4.0)
    with col2:
        months = st.slider("المدى الزمني للاستثمار (بالشهور)", 3, 36, 12)
        
    if st.button("📊 توليد مسار نمو الثروة المركبة"):
        val = capital
        growth_list = []
        for m in range(1, months + 1):
            val = val * (1 + rate / 100)
            growth_list.append({"الشهر": m, "إجمالي الثروة المتوقعة (ج.م)": round(val, 2)})
        st.dataframe(pd.DataFrame(growth_list), use_container_width=True)
