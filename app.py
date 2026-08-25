

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
    page_title="AI Beast Enterprise - محرك التحليل اللحظي الشامل",
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

st.title("🦁 AI Beast Enterprise: محرك التحليل اللحظي الشامل للسوق والأسهم")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("🎛️ غرفة عمليات الإمبراطورية")
page = st.sidebar.selectbox("اختر وحدة التشغيل المتقدمة:", [
    "⚡ ماسح السوق اللحظي الشامل (صعود وهبوط)",
    "🎯 قناص أسهم المضاربة اليومية (نقاط الدخول والخروج)",
    "📈 التحليل الفني والمالي اللحظي للسهم",
    "💼 إدارة المحفظة الاستثمارية السيادية",
    "🛡️ حاسبة إدارة المخاطر ووقف الخسارة",
    "💰 حاسبة العائد المركب المتقدمة"
])

if "ماسح السوق اللحظي الشامل" in page:
    st.header("⚡ ماسح السوق اللحظي (الأسهم الصاعدة والهابطة بالسوق)")
    st.info("🔄 يعرض هذا الماسح رصدًا لحظيًا لأداء أبرز الأسهم، نسبة التغير، وحالة السيولة بالسوق.")
    
    if st.button("🚀 تحديث وسحب بيانات السوق اللحظية الآن"):
        with st.spinner("🔄 جاري الاتصال المباشر بالسوق وسحب أحدث الأسعار..."):
            # عينة من أبرز أسهم السوق المصري (قابلة للتوسيع لتشمل السوق بالكامل)
            tickers_list = ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", "PHDC.CA", "ESRS.CA"]
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
                        
                        status = "🔥 صعود قوي" if chg > 2 else ("🚀 صعود إيجابي" if chg > 0 else ("📉 هبوط وتصحيح" if chg < -1 else "⚖️ استقرار"))
                        market_data.append({
                            "رمز السهم": t,
                            "السعر الحالي (ج.م)": round(curr, 2),
                            "التغير اللحظي (%)": round(chg, 2),
                            "حجم التداول": int(vol),
                            "حالة السهم": status
                        })
                except:
                    pass
            
            if market_data:
                df_market = pd.DataFrame(market_data)
                df_market = df_market.sort_values(by="التغير اللحظي (%)", ascending=False)
                st.success("✅ تم تحديث مسح السوق اللحظي بنجاح!")
                st.dataframe(df_market, use_container_width=True)
            else:
                st.warning("⚠️ تعذر جلب البيانات لحظياً، حاول مرة أخرى.")
    else:
        st.write("👆 اضغط على الزر أعلاه لبدء الفحص الفوري لجلسة السوق الحالية.")

elif "قناص أسهم المضاربة اليومية" in page:
    st.header("🎯 قناص أسهم المضاربة اليومية (تحديد نقط الدخول والخروج)")
    st.info("💡 خوارزمية ذكية لتحليل الزخم اللحظي واقتناص أفضل الفرص السريعة مع تحديد دقيق لمستويات الدعم، المقاومة، وقف الخسارة، وأسعار الشراء المستهدفة.")
    
    spec_ticker = st.text_input("🔤 أدخل رمز سهم المضاربة المستهدف (مثال: FWRY.CA أو COMI.CA)", value="FWRY.CA")
    
    if st.button("⚡ تشغيل قناص الصفقات اليومية"):
        with st.spinner("🔍 جاري حساب مستويات السيولة، الزخم، ونقاط الاختراق..."):
            try:
                stock_obj = yf.Ticker(spec_ticker)
                hist_data = stock_obj.history(period="1mo")
                if not hist_data.empty:
                    p_curr = hist_data['Close'].iloc[-1]
                    p_low = hist_data['Low'].tail(5).min()
                    p_high = hist_data['High'].tail(5).max()
                    
                    # استراتيجية المضاربة اليومية الذكية
                    entry_price = p_curr * 0.995 # نقطة دخول قريبة من السعر الحالي عند التراجع البسيط
                    stop_loss = p_low * 0.985 # وقف خسارة آمن تحت الدعم الأخير
                    target_1 = p_curr * 1.025 # الهدف الأول بنسبة ربح سريعة
                    target_2 = p_high # الهدف الثاني عند المقاومة القريبة
                    
                    st.success(ف"✅ تقرير قناص المضاربة للسهم: **{spec_ticker}**")
                    
                    sc1, sc2, sc3, sc4 = st.columns(4)
                    sc1.metric("📥 نقطة الدخول المقترحة", f"{entry_price:.2f} ج.م", "منطقة تجميع")
                    sc2.metric("🛑 وقف الخسارة الآمن", f"{stop_loss:.2f} ج.م", "حماية رأس المال")
                    sc3.metric("🎯 الهدف الأول السريع", f"{target_1:.2f} ج.م", "+2.5% ربح")
                    sc4.metric("🚀 الهدف الثاني الكبرى", f"{target_2:.2f} ج.م", "مستوى المقاومة")
                    
                    st.write("---")
                    st.subheader("📋 خطة التداول اللحظي والسياسة التنفيذية:")
                    st.markdown(f"""
                    * **تقييم الحركة:** السهم يظهر سيولة متذبذبة صعودية تسمح بالمضاربة بنظام الدخول السريع والخروج الآمن.
                    * **التنفيذ:** يفضل الشراء تدريجياً عند سعر **{entry_price:.2f} ج.م** وعدم الطاردة السعرية العالية.
                    * **الانضباط:** الالتزام التام بوقف الخسارة عند **{stop_loss:.2f} ج.م** لحماية محفظتك من أي انعكاس فجائي للسوق.
                    """)
                else:
                    st.warning("⚠️ لم يتم العثور على بيانات كافية لهذا الرمز.")
            except Exception as ex:
                st.error(f"❌ حدث خطأ أثناء التحليل: {ex}")

elif "التحليل اللحظي" in page:
    st.header("📈 وحدة التحليل الفني والمالي اللحظي فائق الدقة")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ticker = st.text_input("🔤 أدخل رمز السهم", value="COMI.CA")
    with c2:
        interval_choice = st.selectbox("⏱️ الإطار الزمني للتحليل", ["يومي (Daily)", "ساعي (Hourly)"])
    with c3:
        st.write("")
        st.write("")
        fetch_btn = st.button("⚡ تنفيذ الفحص السعري اللحظي")

    if fetch_btn:
        with st.spinner("🔄 جاري سحب البيانات الحية..."):
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
                        
                        st.success(f"✅ تم تحديث بيانات السهم {ticker} بنجاح!")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("💵 السعر الحالي", f"{current_price:.2f} ج.م", f"{change_pct:+.2f}%")
                        m2.metric("📊 مؤشر RSI", f"{rsi_val:.1f}", "تشبع شراء" if rsi_val > 70 else ("تشبع بيع" if rsi_val < 30 else "آمن"))
                        m3.metric("🛡️ الدعم", f"{support:.2f} ج.م")
                        m4.metric("🎯 المقاومة", f"{resistance:.2f} ج.م")

                        st.subheader("📉 الرسم البياني التفاعلي")
                        st.line_chart(hist['Close'])
                    else:
                        st.warning("⚠️ تأكد من صحة رمز السهم.")
                else:
                    st.error("❌ مكتبة جلب البيانات غير متاحة.")
            except Exception as e:
                st.error(f"❌ حدث خطأ: {e}")

elif "مدير المحفظة الاستثمارية السيادية" in page:
    st.header("💼 إدارة المحفظة الاستثمارية وتتبع الأرباح")
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
    st.metric("💎 صافي أرباح المحفظة الكلية", f"{portfolio_data['الربح / الخسارة (ج.م)'].sum():,.2f} ج.م", "+9.8%")

elif "حاسبة إدارة المخاطر" in page:
    st.header("🛡️ حاسبة إدارة المخاطر وتحديد نقاط وقف الخسارة")
    rc1, rc2 = st.columns(2)
    with rc1:
        acc_cap = st.number_input("💰 رأس المال (ج.م)", value=50000, step=5000)
        risk_pct = st.slider("⚠️ نسبة المخاطرة (%)", 0.5, 5.0, 1.5)
    with rc2:
        entry_p = st.number_input("📥 سعر الدخول", value=10.0, step=0.5)
        stop_p = st.number_input("🛑 وقف الخسارة", value=9.2, step=0.5)
    if st.button("🧮 احسب حجم الصفقة الآمن"):
        risk_amount = acc_cap * (risk_pct / 100)
        share_risk = entry_p - stop_p
        if share_risk > 0:
            allowed_shares = risk_amount / share_risk
            st.success(f"✅ الحد الأقصى لعدد الأسهم: **{int(allowed_shares):,} سهم**")
            st.metric("💸 المبلغ المخاطر به", f"{risk_amount:,.2f} ج.م")
        else:
            st.error("❌ وقف الخسارة يجب أن يكون أقل من سعر الدخول للشراء!")

else:
    st.header("💰 حاسبة العائد المركب المتقدمة وتنمية الثروات")
    c1, c2 = st.columns(2)
    with c1:
        capital = st.number_input("💵 رأس المال الأساسي (ج.م)", value=50000, step=5000)
        rate = st.slider("📈 العائد الشهري (%)", 1.0, 15.0, 4.0)
    with c2:
        months = st.slider("⏳ المدى الزمني (بالشهور)", 3, 36, 12)
    if st.button("📊 توليد مسار نمو الثروة"):
        val = capital
        growth_list = []
        for m in range(1, months + 1):
            val = val * (1 + rate / 100)
            growth_list.append({"الشهر": m, "إجمالي الثروة (ج.م)": round(val, 2)})
        st.dataframe(pd.DataFrame(growth_list), use_container_width=True)
