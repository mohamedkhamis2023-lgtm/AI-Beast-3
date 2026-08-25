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
    "🏆 فحص أفضل الأسهم وإدارة المخاطر",
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

elif "فحص أفضل الأسهم وإدارة المخاطر" in page:
    st.header("🏆 الماسح السيادي لأفضل الأسهم ونقاط الدخول والخروج وإدارة المخاطر")
    st.info("يقوم هذا القسم بفحص قائمة الأسهم القيادية وحساب أسعار الدخول المثالية، وأهداف الخروج، ومستويات وقف الخسارة الصارمة.")
    
    # قائمة نموذجية لأهم الأسهم (يمكنك تعديلها بالرموز التي تريدها)
    default_watchlist = ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", "ABUK.CA"]
    
    if st.button("🔍 ابدأ مسح السوق وحساب استراتيجيات المخاطر"):
        with st.spinner("جاري فحص الأسهم وحساب التوصيات السيادية..."):
            results = []
            for t in default_watchlist:
                try:
                    s = yf.Ticker(t)
                    h = s.history(period="1mo")
                    if not h.empty:
                        cp = h['Close'].iloc[-1]
                        sup = h['Low'].min()
                        res = h['High'].max()
                        
                        # حساب إدارة المخاطر ونقاط الدخول والخروج الآمنة
                        entry_price = round(cp * 0.99, 2)  # الدخول قرب الدعم أو السعر الحالي
                        stop_loss = round(sup * 0.98, 2)   # وقف الخسارة تحت أقل دعم
                        target_price = round(res * 1.02, 2) # هدف الخروج عند المقاومة أو أعلى
                        
                        risk = entry_price - stop_loss
                        reward = target_price - entry_price
                        rr_ratio = round(reward / risk, 2) if risk > 0 else 0
                        
                        results.append({
                            "السهم": t,
                            "السعر الحالي (ج.م)": round(cp, 2),
                            "نقطة الدخول المقترحة": entry_price,
                            "وقف الخسارة (حماية رأس المال)": stop_loss,
                            "هدف الخروج (المقاومة)": target_price,
                            "نسبة العائد للمخاطرة": f"1 : {rr_ratio}"
                        })
                except:
                    continue
            
            if results:
                df_res = pd.DataFrame(results)
                st.subheader("📋 جدول التوصيات السيادية وإدارة المخاطر")
                st.dataframe(df_res, use_container_width=True)
                st.success("تم حساب المخاطر والأهداف بنجاح بناءً على الخوارزميات الرياضية المحترفة!")
            else:
                st.warning("تعذر جلب بيانات الفحص حالياً، حاول مرة أخرى بعد قليل.")

elif "حاسبة العائد المركب" in page:
    st.header("💰 حاسبة التداول والعائد المركب السيادي")
    # [باقي الكود الخاص بالحاسبة...]
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
