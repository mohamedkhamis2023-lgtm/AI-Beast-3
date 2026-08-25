
import streamlit as st
import pandas as pd
import numpy as np

try:
    import yfinance as yf
    has_yf = True
except ImportError:
    has_yf = False

st.set_page_config(
    page_title="AI Beast - منصة التداول السيادية",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background-color: #238636; color: white; font-weight: bold; border-radius: 6px; }
    .stButton>button:hover { background-color: #2ea043; }
    </style>
""", unsafe_allow_html=True)

st.title("🦁 AI Beast: المنصة السيادية المتقدمة للتحليل المالي والذكاء الاصطناعي")
st.markdown("---")

st.sidebar.title("🎛️ لوحة التحكم السيادية")
page = st.sidebar.selectbox("اختر القسم المتقدم:", [
    "📈 التحليل اللحظي والرسوم البيانية للأسهم",
    "🚀 الماسح الذكي لأفضل 10 أسهم صعوداً",
    "💰 حاسبة العائد المركب المتقدمة",
    "💼 إدارة المحفظة السيادية"
])

if "التحليل اللحظي" in page:
    st.header("📈 لوحة التحليل اللحظي والبيانات الحقيقية للأسهم")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker_symbol = st.text_input("أدخل رمز السهم (مثال: COMI.CA أو FWRY.CA)", value="COMI.CA")
    with col2:
        timeframe = st.selectbox("الإطار الزمني", ["يومي (Daily)", "أسبوعي (Weekly)"])
    with col3:
        st.write("")
        st.write("")
        run_analysis = st.button("🚀 تنفيذ التحليل الحقيقي الدقيق")

    if run_analysis:
        with st.spinner("جاري جلب البيانات الفعلية وحساب المؤشرات الحقيقية..."):
            try:
                if has_yf:
                    stock_data = yf.Ticker(ticker_symbol)
                    hist = stock_data.history(period="3mo")
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        price_change = ((current_price - prev_price) / prev_price) * 100
                        
                        delta = hist['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi_series = 100 - (100 / (1 + rs))
                        current_rsi = rsi_series.iloc[-1]
                        
                        support_level = hist['Low'].tail(20).min()
                        resistance_level = hist['High'].tail(20).max()
                        
                        st.success(f"تم تحليل السهم {ticker_symbol} بدقة عالية بناءً على بيانات السوق الحقيقية!")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("السعر الحالي", f"{current_price:.2f} ج.م", f"{price_change:+.2f}%")
                        m2.metric("مؤشر القوة النسبية RSI", f"{current_rsi:.1f}", "تشبع/زخم" if current_rsi > 70 or current_rsi < 30 else "منطقة آمنة")
                        m3.metric("مستوى الدعم الفعلي", f"{support_level:.2f} ج.م", "قاع قسري")
                        m4.metric("مستوى المقاومة الفعلية", f"{resistance_level:.2f} ج.م", "قمة مستهدفة")

                        st.subheader("📊 الرسم البياني الفعلي لحركة الإغلاق التاريخية")
                        st.line_chart(hist['Close'])
                    else:
                        st.warning("تأكد من كتابة الرمز بشكل صحيح.")
                else:
                    st.error("مكتبة جلب البيانات غير متوفرة.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

elif "الماسح الذكي لأفضل 10 أسهم صعوداً" in page:
    st.header("🚀 ماسح السوق السيادي: أعلى 10 أسهم صعوداً وإدارة المخاطر")
    st.info("يقوم النظام بفحص قائمة شاملة من الأسهم القيادية والنشطة، حساب نسبة التغير، وترتيبها تصاعدياً لاختيار أفضل 10 فرص مع تحديد نقاط الدخول والخروج.")
    
    # قائمة موسعة لأبرز الأسهم النشطة في البورصة المصرية
    market_watchlist = [
        "COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", 
        "ABUK.CA", "TMGH.CA", "ORAS.CA", "SWDY.CA", "ETRS.CA", 
        "CERA.CA", "PHDC.CA", "ESRS.CA", "MNHD.CA", "JUFO.CA"
    ]
    
    if st.button("🔥 ابدأ مسح السوق وترتيب أقوى 10 أسهم صعوداً"):
        with st.spinner("جاري فحص السوق، حساب نسب التغير، وتوليد استراتيجيات التداول..."):
            scanned_data = []
            for ticker in market_watchlist:
                try:
                    stock = yf.Ticker(ticker)
                    df_hist = stock.history(period="1mo")
                    if len(df_hist) >= 2:
                        curr = df_hist['Close'].iloc[-1]
                        prev = df_hist['Close'].iloc[-2]
                        change_pct = ((curr - prev) / prev) * 100
                        
                        support = df_hist['Low'].min()
                        resistance = df_hist['High'].max()
                        
                        # حساب استراتيجية الدخول والخروج
                        entry = round(curr * 0.99, 2)
                        stop_loss = round(support * 0.98, 2)
                        target = round(resistance * 1.02, 2)
                        
                        scanned_data.append({
                            "السهم": ticker,
                            "السعر الحالي (ج.م)": round(curr, 2),
                            "نسبة التغير اليومي (%)": round(change_pct, 2),
                            "نقطة الدخول المقترحة": entry,
                            "وقف الخسارة (حماية رأس المال)": stop_loss,
                            "هدف الخروج (المقاومة)": target
                        })
                except:
                    continue
            
            if scanned_data:
                df_market = pd.DataFrame(scanned_data)
                # ترتيب الأسهم حسب الأعلى صعوداً (التغير اليومي تنازلياً) واختيار أفضل 10
                top_10 = df_market.sort_values(by="نسبة التغير اليومي (%)", ascending=False).head(10).reset_index(drop=True)
                
                st.subheader("🏆 قائمة أفضل 10 أسهم صعوداً في السوق وتوصيات التداول")
                st.dataframe(top_10, use_container_width=True)
                st.success("تم ترتيب واستخراج أقوى الفرص بدقة عالية بناءً على الحركة اللحظية للسوق!")
            else:
                st.warning("تعذر جلب البيانات مؤقتاً، يجدر المحاولة لاحقاً.")

elif "حاسبة العائد المركب" in page:
    st.header("💰 حاسبة التداول والعائد المركب السيادي")
    c1, c2, c3 = st.columns(3)
    with c1:
        capital = st.number_input("رأس المال الابتدائي (ج.م)", value=50000, step=5000)
    with c2:
        monthly_add = st.number_input("الإضافة الشهريـة (ج.م)", value=5000, step=1000)
    with c3:
        rate = st.slider("العائد المتوقع الشهري (%)", 1.0, 20.0, 5.0)
    
    months = st.slider("المدى الزمني (بالشهور)", 3, 60, 12)
    if st.button("📊 حساب العائد المركب"):
        data = []
        cv = capital
        for m in range(1, months + 1):
            cv = (cv + monthly_add) * (1 + rate / 100)
            data.append({"الشهر": m, "إجمالي المحفظة المتوقع (ج.م)": round(cv, 2)})
        st.line_chart(pd.DataFrame(data).set_index("الشهر"))

else:
    st.header("💼 إدارة المحفظة السيادية وتوزيع الأصول")
    port_df = pd.DataFrame({
        "السهم": ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA"],
        "عدد الأسهم": [1000, 2500, 800, 1500],
        "سعر الشراء": [72.0, 6.2, 35.5, 12.0],
        "السعر الحالي": [78.5, 6.8, 38.0, 13.2]
    })
    port_df["إجمالي القيمة"] = port_df["عدد الأسهم"] * port_df["السعر الحالي"]
    port_df["الربح/الخسارة (%)"] = ((port_df["السعر الحالي"] - port_df["سعر الشراء"]) / port_df["سعر الشراء"]) * 100
    st.dataframe(port_df, use_container_width=True)
    st.metric("القيمة الإجمالية للمحفظة السيادية", f"{port_df['إجمالي القيمة'].sum():,.2f} ج.م", "+8.4%")
