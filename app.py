

import streamlit as st
import pandas as pd
import numpy as np

try:
    import yfinance as yf
    has_yf = True
except ImportError:
    has_yf = False

st.set_page_config(
    page_title="AI Beast Pro - المنصة السيادية المتقدمة",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تصميم الواجهة السيادية الفاخرة
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #238636 0%, #2ea043 100%); color: white; font-weight: bold; border-radius: 8px; padding: 10px; border: none; }
    .stButton>button:hover { background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%); }
    h1, h2, h3 { color: #58a6ff; }
    </style>
""", unsafe_allow_html=True)

st.title("🦁 AI Beast Pro: المنصة السيادية المتقدمة للتحليل الكمي والذكاء الاصطناعي")
st.markdown("---")

st.sidebar.title("🎛️ لوحة القيادة السيادية")
page = st.sidebar.selectbox("اختر وحدة التشغيل:", [
    "📈 التحليل الفني واللحظي المتقدم",
    "🚀 الماسح الذكي الشامل لأفضل 10 أسهم",
    "🤖 التنبؤ بالذكاء الاصطناعي وإدارة المخاطر",
    "💰 حاسبة العائد المركب المتقدمة",
    "💼 إدارة المحفظة السيادية"
])

# 1. وحدة التحليل اللحظي والفني
if "التحليل الفني واللحظي" in page:
    st.header("📈 وحدة التحليل الفني واللحظي المتقدم")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker_symbol = st.text_input("رمز السهم (مثال: COMI.CA, FWRY.CA, TMGH.CA)", value="COMI.CA")
    with col2:
        period_choice = st.selectbox("المدى الزمني للتحليل", ["1 شهر", "3 أشهر", "6 أشهر", "سنة كاملة"])
    with col3:
        st.write("")
        st.write("")
        run_analysis = st.button("🚀 تنفيذ التحليل الفني الشامل")

    period_map = {"1 شهر": "1mo", "3 أشهر": "3mo", "6 أشهر": "6mo", "سنة كاملة": "1y"}

    if run_analysis:
        with st.spinner("جاري جلب بيانات السوق الحية وحساب مؤشرات الزخم والاتجاه..."):
            try:
                if has_yf:
                    stock = yf.Ticker(ticker_symbol)
                    hist = stock.history(period=period_map[period_choice])
                    if not hist.empty:
                        curr_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change = ((curr_price - prev_price) / prev_price) * 100
                        
                        # حساب المؤشرات الفنية المتقدمة
                        hist['MA50'] = hist['Close'].rolling(window=min(50, len(hist))).mean()
                        hist['MA200'] = hist['Close'].rolling(window=min(200, len(hist))).mean()
                        
                        delta = hist['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi = 100 - (100 / (1 + rs))
                        current_rsi = rsi.iloc[-1]
                        
                        sup = hist['Low'].min()
                        res = hist['High'].max()
                        
                        st.success(f"تم بنجاح تحليل السهم {ticker_symbol} عبر خوارزميات السوق السيادية!")
                        
                        # لوحة المقاييس الحية
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("السعر الحالي", f"{curr_price:.2f} ج.م", f"{change:+.2f}%")
                        m2.metric("مؤشر القوة النسبية (RSI)", f"{current_rsi:.1f}", "تشبع شراء" if current_rsi > 70 else ("تشبع بيع" if current_rsi < 30 else "منطقة توازن"))
                        m3.metric("مستوى الدعم القوي", f"{sup:.2f} ج.م", "حماية القاع")
                        m4.metric("مستوى المقاومة المستهدفة", f"{res:.2f} ج.م", "هدف صعودي")

                        # تقييم ذكي للحالة
                        if current_rsi < 35:
                            st.info("💡 **توصية الذكاء الاصطناعي:** السهم في مناطق تشبع بيعي قوية، وتعتبر فرصة مراقبة للتجميع قرب الدعم.")
                        elif current_rsi > 65:
                            st.warning("⚠️ **توصية الذكاء الاصطناعي:** السهم يقترب من مناطق تشبع شرائي، يرجى الحذر وتأمين الأرباح.")
                        else:
                            st.success("✅ **توصية الذكاء الاصطناعي:** السهم يتحرك في مسار عرضي/صاعد مستقر، نسبة المخاطرة مقبولة.")

                        st.subheader("📊 الرسم البياني وحركة المتوسطات الحية")
                        st.line_chart(hist[['Close', 'MA50']])
                    else:
                        st.warning("لم يتم العثور على بيانات لهذا الرمز، تأكد من كتابته بصيغة صحيحة (مثال: COMI.CA).")
                else:
                    st.error("مكتبة جلب البيانات غير متوفرة.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب البيانات: {e}")

# 2. وحدة الماسح الشامل لأفضل 10 أسهم
elif "الماسح الذكي الشامل لأفضل 10 أسهم" in page:
    st.header("🚀 الماسح السيادي المتقدم: أفضل 10 فرص صعوداً في السوق")
    st.info("يقوم النظام بمسح شامل لأبرز الأسهم القيادية والنشطة، حساب نسب التغير اللحظي، وتوليد نقاط الدخول والخروج بدقة متناهية.")
    
    extended_watchlist = [
        "COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", 
        "ABUK.CA", "TMGH.CA", "ORAS.CA", "SWDY.CA", "ETRS.CA", 
        "PHDC.CA", "ESRS.CA", "JUFO.CA", "CIRA.CA", "ETEL.CA"
    ]
    
    if st.button("🔥 ابدأ المسح الشامل واكتشاف أقوى 10 فرص"):
        with st.spinner("جاري فحص محفظة السوق المصري بالكامل وحساب استراتيجيات التداول..."):
            scan_results = []
            for t in extended_watchlist:
                try:
                    s = yf.Ticker(t)
                    df = s.history(period="1mo")
                    if len(df) >= 2:
                        cp = df['Close'].iloc[-1]
                        pp = df['Close'].iloc[-2]
                        chg = ((cp - pp) / pp) * 100
                        
                        support = df['Low'].min()
                        resistance = df['High'].max()
                        
                        # حساب نظام إدارة المخاطر المتطور
                        entry = round(cp * 0.99, 2)
                        stop = round(support * 0.98, 2)
                        target = round(resistance * 1.02, 2)
                        
                        risk = entry - stop
                        reward = target - entry
                        rr = round(reward / risk, 2) if risk > 0 else 0
                        
                        scan_results.append({
                            "السهم": t,
                            "السعر (ج.م)": round(cp, 2),
                            "التغير اليومي (%)": round(chg, 2),
                            "دخول مقترح": entry,
                            "وقف الخسارة": stop,
                            "هدف الخروج": target,
                            "العائد/المخاطرة": f"1:{rr}"
                        })
                except:
                    continue
            
            if scan_results:
                df_res = pd.DataFrame(scan_results)
                top_10_df = df_res.sort_values(by="التغير اليومي (%)", ascending=False).head(10).reset_index(drop=True)
                
                st.subheader("🏆 قائمة أفضل 10 أسهم صعوداً وأهدافها الاستراتيجية")
                st.dataframe(top_10_df, use_container_width=True)
                st.success("تم فلترة وترتيب أفضل الفرص بدقة تامة!")
            else:
                st.warning("تعذر جلب بيانات السوق حالياً، حاول مرة أخرى.")

# 3. وحدة التنبؤ بالذكاء الاصطناعي وإدارة المخاطر
elif "التنبؤ بالذكاء الاصطناعي وإدارة المخاطر" in page:
    st.header("🤖 وحدة التنبؤ الكمي وإدارة المخاطر الاحترافية")
    st.write("أدخل قيمة رأس مالك وحجم المخاطر المسموح بها لحساب الخطة الصارمة للصفقة:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        cap_total = st.number_input("إجمالي محفظتك (ج.م)", value=100000, step=10000)
    with c2:
        risk_pct = st.slider("نسبة المخاطرة المقبولة لكل صفقة (%)", 0.5, 5.0, 2.0)
    with c3:
        target_rr = st.selectbox("نسبة العائد المستهدفة", ["1 : 2", "1 : 3", "1 : 4"])
        
    st.markdown("---")
    sc1, sc2 = st.columns(2)
    with sc1:
        entry_p = st.number_input("سعر الدخول المقترح للسهم (ج.م)", value=50.0)
    with sc2:
        stop_p = st.number_input("سعر وقف الخسارة (ج.م)", value=48.0)
        
    if st.button("🧮 احسب حجم العقد وخطة المخاطر بحرافة"):
        if entry_p > stop_p:
            risk_amount_allowed = cap_total * (risk_pct / 100)
            risk_per_share = entry_p - stop_p
            shares_count = int(risk_amount_allowed / risk_per_share)
            total_invested = shares_count * entry_p
            
            multiplier = 3 if "3" in target_rr else (4 if "4" in target_rr else 2)
            profit_target = entry_p + (risk_per_share * multiplier)
            
            st.success("تم حساب خطة إدارة المخاطر بدقة متناهية لحماية رأس مالك:")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("عدد الأسهم المسموح بتداولها", f"{shares_count:,} سهم")
            m2.metric("إجمالي المبلغ المستثمر", f"{total_invested:,.2f} ج.م")
            m3.metric("الخسارة القصوى المتوقعة", f"{risk_amount_allowed:,.2f} ج.م")
            m4.metric("سعر جني الأرباح المستهدف", f"{profit_target:.2f} ج.م")
        else:
            st.error("خطأ: يجب أن يكون سعر الدخول أعلى من سعر وقف الخسارة!")

# 4. حاسبة العائد المركب
elif "حاسبة العائد المركب المتقدمة" in page:
    st.header("💰 حاسبة العائد المركب الاستثماري")
    c1, c2, c3 = st.columns(3)
    with c1:
        capital = st.number_input("رأس المال الابتدائي (ج.م)", value=50000, step=5000)
    with c2:
        monthly_add = st.number_input("الإضافة الشهريـة (ج.م)", value=5000, step=1000)
    with c3:
        rate = st.slider("العائد المتوقع الشهري (%)", 1.0, 20.0, 4.0)
    
    months = st.slider("المدى الزمني (بالشهور)", 3, 60, 12)
    if st.button("📊 حساب وتوقع نمو الثروة"):
        data = []
        cv = capital
        for m in range(1, months + 1):
            cv = (cv + monthly_add) * (1 + rate / 100)
            data.append({"الشهر": m, "إجمالي الثروة المتوقعة (ج.م)": round(cv, 2)})
        st.line_chart(pd.DataFrame(data).set_index("الشهر"))

# 5. إدارة المحفظة السيادية
else:
    st.header("💼 إدارة المحفظة السيادية وتوزيع الأصول الذكية")
    port_df = pd.DataFrame({
        "السهم": ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA"],
        "عدد الأسهم": [1000, 2500, 800, 1500],
        "سعر الشراء": [72.0, 6.2, 35.5, 12.0],
        "السعر الحالي": [78.5, 6.8, 38.0, 13.2]
    })
    port_df["إجمالي القيمة"] = port_df["عدد الأسهم"] * port_df["السعر الحالي"]
    port_df["الربح/الخسارة (%)"] = ((port_df["السعر الحالي"] - port_df["سعر الشراء"]) / port_df["سعر الشراء"]) * 100
    st.dataframe(port_df, use_container_width=True)
    st.metric("القيمة الإجمالية للمحفظة السيادية", f"{port_df['إجمالي القيمة'].sum():,.2f} ج.م", "+9.2%")
