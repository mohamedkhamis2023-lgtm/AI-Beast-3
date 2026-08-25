

import streamlit as st
import pandas as pd
import numpy as np

try:
    import yfinance as yf
    has_yf = True
except ImportError:
    has_yf = False

st.set_page_config(
    page_title="Enterprise Capital - منصة التحليل المالي والأسواق",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional & Calm Enterprise Styling
st.markdown("""
    <style>
    .main { background-color: #0f141c; color: #e6edf3; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 8px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background-color: #1f6feb; color: white; font-weight: 500; border-radius: 6px; border: none; }
    .stButton>button:hover { background-color: #388bfd; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 منصة التحليل المالي ورصد الزخم اللحظي")
st.markdown("---")

# Clean Sidebar Navigation
st.sidebar.title("🎛️ لوحة التحكم الرئيسية")
page = st.sidebar.selectbox("اختر القسم المطلوب:", [
    "🚀 مسح الأسهم الصاعدة واقتناص الفرص",
    "📊 لوحة بيانات السوق اللحظية",
    "🎯 تحليل الفرص ونقاط الدخول والخروج",
    "📈 التحليل الفني والمالي للسهم",
    "💼 إدارة المحفظة الاستثمارية",
    "🛡️ حساب المخاطر ووقف الخسارة",
    "💰 حاسبة العائد المركب"
])

if "مسح الأسهم الصاعدة واقتناص الفرص" in page:
    st.header("🚀 ماسح الزخم وقائمة الأسهم الأعلى صعوداً")
    st.info("فحص تلقائي للسوق لفرز الأسهم ذات الصعود المرتفع وتحديد المستويات السعرية للتنفيذ.")
    
    if st.button("بدء فحص السوق ورصد الأسهم النشطة"):
        with st.spinner("جاري جلب بيانات الأسهم وفرز معدلات التغير..."):
            # عينة موسعة من الأسهم لفحصها
            tickers_list = ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", "PHDC.CA", "ESRS.CA", "MNHD.CA"]
            scanned_data = []
            
            for t in tickers_list:
                try:
                    s = yf.Ticker(t)
                    h = s.history(period="5d")
                    if len(h) >= 2:
                        curr = h['Close'].iloc[-1]
                        prev = h['Close'].iloc[-2]
                        chg = ((curr - prev) / prev) * 100
                        vol = h['Volume'].iloc[-1]
                        high_p = h['High'].max()
                        
                        # حساب مستويات مقترحة للدخول والخروج بناءً على حركة السعر
                        entry_rec = curr * 0.995
                        target_sale = curr * 1.05  # هدف ربح 5% كمرحلة أولى للمضاربة السريعة
                        stop_loss = curr * 0.97    # وقف خسارة 3%
                        
                        scanned_data.append({
                            "رمز السهم": t,
                            "السعر الحالي": round(curr, 2),
                            "التغير اليومي (%)": round(chg, 2),
                            "حجم التداول": int(vol),
                            "سعر الدخول المقترح": round(entry_rec, 2),
                            "هدف البيع (جني الأرباح)": round(target_sale, 2),
                            "وقف الخسارة الآمن": round(stop_loss, 2)
                        })
                except:
                    pass
            
            if scanned_data:
                df_scan = pd.DataFrame(scanned_data)
                # ترتيب الأسهم تنازلياً حسب نسبة الصعود لعرض الأعلى صعوداً أولاً
                df_scan = df_scan.sort_values(by="التغير اليومي (%)", ascending=False)
                st.success("تم تحديث الفحص بنجاح وترتيب الأسهم حسب معدل الصعود.")
                st.dataframe(df_scan, use_container_width=True)
            else:
                st.warning("تعذر جلب البيانات في الوقت الحالي، يرجى المحاولة مرة أخرى.")
    else:
        st.write("اضغط على الزر أعلاه لبدء رصد الأسهم الصاعدة وتحديد نقاط التداول اللحظي.")

elif "لوحة بيانات السوق اللحظية" in page:
    st.header("📊 لوحة بيانات السوق اللحظية")
    st.info("رصد مباشر لأداء الأسهم المدرجة وحركة التغير السعري.")
    
    if st.button("تحديث بيانات السوق الحالية"):
        with st.spinner("جاري جلب البيانات من السوق..."):
            tickers_list = ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", "PHDC.CA"]
            market_data = []
            
            for t in tickers_list:
                try:
                    s = yf.Ticker(t)
                    h = s.history(period="2d")
                    if len(h) >= 2:
                        curr = h['Close'].iloc[-1]
                        prev = h['Close'].iloc[-2]
                        chg = ((curr - prev) / prev) * 100
                        vol = h['Volume'].iloc[-1]
                        
                        trend = "صاعد إيجابي" if chg > 0 else "هابط / تصحيحي"
                        market_data.append({
                            "رمز السهم": t,
                            "السعر الحالي": round(curr, 2),
                            "التغير اليومي (%)": round(chg, 2),
                            "حجم التداول": int(vol),
                            "الحالة الفنية": trend
                        })
                except:
                    pass
            
            if market_data:
                df_market = pd.DataFrame(market_data)
                df_market = df_market.sort_values(by="التغير اليومي (%)", ascending=False)
                st.success("تم تحديث بيانات السوق بنجاح.")
                st.dataframe(df_market, use_container_width=True)
            else:
                st.warning("تعذر جلب البيانات في الوقت الحالي.")
    else:
        st.write("اضغط على الزر أعلاه لعرض وتحديث بيانات جلسة التداول الحالية.")

elif "تحليل الفرص ونقاط الدخول والخروج" in page:
    st.header("🎯 تحليل الفرص اليومية وتحديد المستويات السعرية")
    st.info("تحديد مستويات الدعم، المقاومة، أسعار الدخول، وأوقات جني الأرباح بناءً على الزخم.")
    
    spec_ticker = st.text_input("أدخل رمز السهم المراد تحليله (مثال: FWRY.CA)", value="FWRY.CA")
    
    if st.button("بدء التحليل الفني للفرصة"):
        with st.spinner("جاري معالجة بيانات السهم واستخراج المستويات..."):
            try:
                stock_obj = yf.Ticker(spec_ticker)
                hist_data = stock_obj.history(period="1mo")
                if not hist_data.empty:
                    p_curr = hist_data['Close'].iloc[-1]
                    p_low = hist_data['Low'].tail(5).min()
                    p_high = hist_data['High'].tail(5).max()
                    
                    entry_price = p_curr * 0.995
                    stop_loss = p_low * 0.985
                    target_1 = p_curr * 1.03  # هدف أول
                    target_2 = p_high         # هدف ثانٍ عند المقاومة
                    
                    st.success(f"تقرير التحليل الفني للسهم: {spec_ticker}")
                    
                    sc1, sc2, sc3, sc4 = st.columns(4)
                    sc1.metric("سعر الدخول المقترح", f"{entry_price:.2f} ج.م")
                    sc2.metric("مستوى وقف الخسارة", f"{stop_loss:.2f} ج.م")
                    sc3.metric("هدف البيع الأول (جني أرباح)", f"{target_1:.2f} ج.م")
                    sc4.metric("هدف البيع الثاني (مقاومة)", f"{target_2:.2f} ج.م")
                    
                    st.markdown("---")
                    st.subheader("إرشادات التنفيذ:")
                    st.markdown(f"""
                    * **استراتيجية التداول:** في الأسهم التي تسجل تدفقات سيولة عالية، يفضل البيع المجزأ عند الوصول للهدف الأول **{target_1:.2f} ج.م** لتأمين الأرباح.
                    * **إدارة المخاطر:** التزام صارم بوقف الخسارة عند **{stop_loss:.2f} ج.م** لتفادي أي انعكاس حاد للسعر.
                    """)
                else:
                    st.warning("لم يتم العثور على بيانات كافية لهذا الرمز.")
            except Exception as ex:
                st.error(f"حدث خطأ أثناء المعالجة: {ex}")

elif "التحليل الفني والمالي للسهم" in page:
    st.header("📈 التحليل الفني اللحظي للأسهم")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ticker = st.text_input("رمز السهم", value="COMI.CA")
    with c2:
        interval_choice = st.selectbox("الإطار الزمني", ["يومي (Daily)", "ساعي (Hourly)"])
    with c3:
        st.write("")
        st.write("")
        fetch_btn = st.button("تنفيذ التحليل")

    if fetch_btn:
        with st.spinner("جاري جلب البيانات الفنية..."):
            try:
                if has_yf:
                    data_period = "1mo" if "يومي" in interval_choice else "5d"
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period=data_period, interval="1h" if "ساعي" in interval_choice else "1d")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change_pct = ((current_price - prev_price) / prev_price) * 100
                        
                        delta = hist['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi_val = (100 - (100 / (1 + rs))).iloc[-1]
                        
                        support = hist['Low'].tail(15).min()
                        resistance = hist['High'].tail(15).max()
                        
                        st.success(f"تم تحديث بيانات السهم {ticker} بنجاح.")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("السعر الحالي", f"{current_price:.2f} ج.م", f"{change_pct:+.2f}%")
                        m2.metric("مؤشر القوة النسبية RSI", f"{rsi_val:.1f}")
                        m3.metric("مستوى الدعم", f"{support:.2f} ج.م")
                        m4.metric("مستوى المقاومة", f"{resistance:.2f} ج.م")

                        st.subheader("الرسم البياني التاريخي")
                        st.line_chart(hist['Close'])
                    else:
                        st.warning("تأكد من صحة رمز السهم.")
                else:
                    st.error("مكتبة جلب البيانات غير متاحة.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

elif "إدارة المحفظة الاستثمارية" in page:
    st.header("💼 إدارة المحفظة الاستثمارية وتقييم الأداء")
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
    st.metric("صافي القيمة الحالية للمحفظة", f"{portfolio_data['القيمة الحالية'].sum():,.2f} ج.م")

elif "حساب المخاطر ووقف الخسارة" in page:
    st.header("🛡️ حاسبة المخاطر وإدارة رأس المال")
    rc1, rc2 = st.columns(2)
    with rc1:
        acc_cap = st.number_input("إجمالي رأس المال (ج.م)", value=50000, step=5000)
        risk_pct = st.slider("نسبة المخاطرة المقبولة لكل صفقة (%)", 0.5, 5.0, 1.5)
    with rc2:
        entry_p = st.number_input("سعر الدخول", value=10.0, step=0.5)
        stop_p = st.number_input("سعر وقف الخسارة", value=9.2, step=0.5)
    if st.button("حساب حجم المركز الآمن"):
        risk_amount = acc_cap * (risk_pct / 100)
        share_risk = entry_p - stop_p
        if share_risk > 0:
            allowed_shares = risk_amount / share_risk
            st.success(f"الحد الأقصى لعدد الأسهم الآمن: **{int(allowed_shares):,} سهم**")
            st.metric("قيمة المخاطر المالية", f"{risk_amount:,.2f} ج.م")
        else:
            st.error("خطأ: سعر وقف الخسارة يجب أن يكون أقل من سعر الدخول.")

else:
    st.header("💰 حاسبة العائد المركب وتنمية الاستثمارات")
    c1, c2 = st.columns(2)
    with c1:
        capital = st.number_input("رأس المال الأساسي (ج.م)", value=50000, step=5000)
        rate = st.slider("معدل العائد الشهري المتوقع (%)", 1.0, 15.0, 4.0)
    with c2:
        months = st.slider("المدة الزمنية (بالشهور)", 3, 36, 12)
    if st.button("حساب مسار نمو رأس المال"):
        val = capital
        growth_list = []
        for m in range(1, months + 1):
            val = val * (1 + rate / 100)
            growth_list.append({"الشهر": m, "إجمالي القيمة المتوقعة (ج.م)": round(val, 2)})
        st.dataframe(pd.DataFrame(growth_list), use_container_width=True)
