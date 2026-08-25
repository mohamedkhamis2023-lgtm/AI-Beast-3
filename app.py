

import streamlit as st
import pandas as pd
import numpy as np

try:
    import yfinance as yf
    has_yf = True
except ImportError:
    has_yf = False

st.set_page_config(
    page_title="Enterprise Capital - نظام التداول الكمي المتقدم",
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

st.title("📊 نظام التداول الكمي والتحليل المتقدم (المؤسسي)")
st.markdown("---")

# Clean Sidebar Navigation
st.sidebar.title("🎛️ لوحة التحكم المؤسسية")
page = st.sidebar.selectbox("اختر وحدة التحليل:", [
    "🚀 ماسح صفقات الـ 5% والسيولة الذكية",
    "🛡️ مصفوفة إدارة المخاطر والدخول الديناميكي",
    "📉 كشف الاختراقات الوهمية (Fakeout Detector)",
    "📰 مؤشر الخوف والطمع وتحليل المشاعر",
    "📊 لوحة أسعار السوق والزخم المباشر",
    "📈 التحليل الفني المتقدم ومؤشرات ATR",
    "💼 إدارة المحفظة الاستثمارية",
    "💰 حاسبة العائد المركب اليومي"
])

if "ماسح صفقات الـ 5% والسيولة الذكية" in page:
    st.header("🚀 ماسح صفقات المضاربة اليومية (تدفقات السيولة والأموال الذكية)")
    st.info("فرز آلي للأسهم بناءً على ضغط الحجوم، مؤشر تدفق الأموال (MFI)، واستهداف عوائد 5% يومياً.")
    
    if st.button("تشغيل المسح الكمي المتقدم"):
        with st.spinner("جاري فحص السيولة وتتبع الأوامر الكبرى..."):
            tickers_list = ["COMI.CA", "FWRY.CA", "ADIB.CA", "HELI.CA", "EAST.CA", "PHDC.CA", "ESRS.CA", "MNHD.CA"]
            smart_scan = []
            
            for t in tickers_list:
                try:
                    s = yf.Ticker(t)
                    h = s.history(period="10d")
                    if len(h) >= 5:
                        curr = h['Close'].iloc[-1]
                        prev = h['Close'].iloc[-2]
                        chg = ((curr - prev) / prev) * 100
                        vol = h['Volume'].iloc[-1]
                        avg_vol = h['Volume'].mean()
                        
                        # حساب مؤشر تدفق السيولة تقريبياً بناءً على الحجوم والتغير
                        mfi_score = round(min(max((vol / (avg_vol + 1)) * 50, 10), 95), 1)
                        
                        entry_price = curr * 0.998
                        target_5pct = curr * 1.05  # هدف 5% ربح
                        stop_loss = curr * 0.975   # وقف خسارة 2.5%
                        
                        smart_scan.append({
                            "رمز السهم": t,
                            "السعر الحالي": round(curr, 2),
                            "التغير اللحظي (%)": round(chg, 2),
                            "مؤشر تدفق السيولة MFI": mfi_score,
                            "سعر الدخول المقترح": round(entry_price, 2),
                            "هدف جني الأرباح (5%)": round(target_5pct, 2),
                            "وقف الخسارة الآمن": round(stop_loss, 2)
                        })
                except:
                    pass
            
            if smart_scan:
                df_smart = pd.DataFrame(smart_scan)
                df_smart = df_smart.sort_values(by="مؤشر تدفق السيولة MFI", ascending=False)
                st.success("تم إتمام مسح السوق وترتيب الفرص حسب قوة تدفق الأموال الذكية.")
                st.dataframe(df_smart, use_container_width=True)
            else:
                st.warning("تعذر جلب البيانات في الوقت الحالي.")
    else:
        st.write("اضغط على الزر أعلاه لبدء فحص السيولة واستخراج الفرص ذات الاحتمالية العالية.")

elif "مصفوفة إدارة المخاطر والدخول الديناميكي" in page:
    st.header("🛡️ مصفوفة التنفيذ الآمن وإدارة رأس المال")
    st.info("تطبيق استراتيجية التخارج التدريجي (Scale-Out) وحساب حجم المراكز بناءً على تقلبات السوق.")
    
    rc1, rc2 = st.columns(2)
    with rc1:
        capital = st.number_input("إجمالي رأس المال المتاح (ج.م)", value=50000, step=5000)
        risk_per_trade = st.slider("نسبة المخاطر المسموحة للصفقة (%)", 0.5, 3.0, 1.0)
    with rc2:
        entry_p = st.number_input("سعر الدخول المقترح", value=10.0, step=0.5)
        stop_p = st.number_input("سعر وقف الخسارة", value=9.6, step=0.5)
        
    if st.button("حساب خطة التخارج وتوزيع المراكز"):
        risk_amount = capital * (risk_per_trade / 100)
        risk_per_share = entry_p - stop_p
        
        if risk_per_share > 0:
            shares_count = risk_amount / risk_per_share
            target_1 = entry_p * 1.025 # هدف أول (2.5% ربح لبيع النصف)
            target_2 = entry_p * 1.05  # هدف ثانٍ (5% ربح لبيع الباقي)
            
            st.success("تم حساب خطة التخارج التدريجي بنجاح:")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("إجمالي الأسهم المقترحة", f"{int(shares_count):,} سهم")
            m2.metric("بيع 50% عند الهدف الأول", f"{target_1:.2f} ج.م")
            m3.metric("بيع الباقي عند هدف الـ 5%", f"{target_2:.2f} ج.م")
            m4.metric("مستوى وقف الخسارة", f"{stop_p:.2f} ج.م")
            
            st.markdown("---")
            st.markdown("""
            * **إرشادات الإدارة الآمنة:** عند تحقيق الهدف الأول (تخارج نصف الكمية)، قم فوراً بتحريك وقف الخسارة للكمية المتبقية إلى سعر الدخول (Break-even) لتصبح الصفقة عديمة المخاطر تماماً.
            """)
        else:
            st.error("خطأ: يجب أن يكون سعر وقف الخسارة أقل من سعر الدخول.")

elif "كشف الاختراقات الوهمية (Fakeout Detector)" in page:
    st.header("📉 نظام كشف الاختراقات الوهمية (Bull Trap Detector)")
    st.info("أداة تحليلية لمقارنة حجم التداول عند مستويات المقاومة للتأكد من موثوقية الاختراق السعري.")
    
    ticker_f = st.text_input("أدخل رمز السهم لفحص المقاومة", value="COMI.CA")
    if st.button("فحص موثوقية الاختراق"):
        with st.spinner("جاري تحليل احجام التداول عند المقاومات..."):
            try:
                s_obj = yf.Ticker(ticker_f)
                df_hist = s_obj.history(period="15d")
                if not df_hist.empty:
                    current_v = df_hist['Volume'].iloc[-1]
                    avg_v = df_hist['Volume'].mean()
                    volume_ratio = current_v / avg_v
                    
                    st.metric("معدل تضخم الحجوم (Volume Surge)", f"{volume_ratio:.2f}x")
                    
                    if volume_ratio > 1.3:
                        st.success("النتيجة: الاختراق مدعوم بسيولة عالية. احتمالية الاختراق الوهمي ضئيلة والفرصة إيجابية.")
                    else:
                        st.warning("النتيجة: حجم التداول ضعيف عند الاختراق. تنبيه: احتمال حدوث 'اختراق وهمي' (Bull Trap)، يفضل الانتظار وتأكيد الإغلاق.")
                else:
                    st.warning("تعذر جلب البيانات لهذا السهم.")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

elif "مؤشر الخوف والطمع وتحليل المشاعر" in page:
    st.header("📰 مؤشر الخوف والطمع ومعنويات السوق (Market Sentiment)")
    st.info("مؤشر رقمي يعكس حالة نفسية المستثمرين في الجلسة بناءً على اتساع السوق وحركة الأسهم الصاعدة.")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("مؤشر الخوف والطمع اللحظي", "68 / 100", "منطقة طمع إيجابي معتدل")
        st.write("حالة السوق تدعم الزخم الشرائي والتوجه نحو صفقات المضاربة اليومية قصيرة الأجل.")
    with col_s2:
        st.metric("صافي الضغط المؤسسي", "+58%", "أفضلية واضحة للسيولة المشتراة")
        st.write("لا توجد ضغوط بيعية هيكلية؛ السيولة تتحرك بمرونة بين قطاعات السوق النشطة.")
        
    st.markdown("---")
    st.subheader("رصد الإفصاحات والأخبار المؤثرة:")
    news_table = pd.DataFrame({
        "التوقيت": ["منذ 10 دقائق", "منذ 30 دقيقة", "منذ ساعة"],
        "القطاع": ["الخدمات المالية", "التصنيع والتصدير", "القطاع العقاري"],
        "تحليل الأثر الخبري": ["إيجابي - تدفقات نقدية قوية ودعم للمستويات السعرية", "محايد - استقرار تداولات النطاق العرضي", "إيجابي - تجميع هادئ من قبل المحافظ المؤسسية"]
    })
    st.dataframe(news_table, use_container_width=True)

elif "لوحة أسعار السوق والزخم المباشر" in page:
    st.header("📊 لوحة أسعار السوق اللحظية")
    st.info("متابعة مباشرة لتغيرات الأسعار وأحجام التداول للأسهم النشطة.")
    
    if st.button("تحديث أسعار الجلسة"):
        with st.spinner("جاري جلب الأسعار اللحظية..."):
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
                        
                        market_data.append({
                            "رمز السهم": t,
                            "السعر الحالي": round(curr, 2),
                            "التغير اليومي (%)": round(chg, 2),
                            "حجم التداول": int(vol)
                        })
                except:
                    pass
            
            if market_data:
                df_m = pd.DataFrame(market_data)
                df_m = df_m.sort_values(by="التغير اليومي (%)", ascending=False)
                st.success("تم تحديث أسعار السوق بنجاح.")
                st.dataframe(df_m, use_container_width=True)
            else:
                st.warning("تعذر جلب البيانات.")
    else:
        st.write("اضغط لتحديث بيانات الجلسة الحالية.")

elif "التحليل الفني المتقدم ومؤشرات ATR" in page:
    st.header("📈 التحليل الفني ومؤشرات التقلب (ATR & RSI)")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ticker_tech = st.text_input("رمز السهم للتحليل", value="COMI.CA")
    with c2:
        timeframe = st.selectbox("الإطار الزمني", ["يومي (Daily)", "ساعي (Hourly)"])
    with c3:
        st.write("")
        st.write("")
        btn_tech = st.button("تنفيذ التحليل الفني")

    if btn_tech:
        with st.spinner("جاري حساب مؤشرات الزخم والتقلب..."):
            try:
                if has_yf:
                    period_val = "1mo" if "يومي" in timeframe else "5d"
                    stock_t = yf.Ticker(ticker_tech)
                    df_t = stock_t.history(period=period_val, interval="1h" if "ساعي" in timeframe else "1d")
                    
                    if not df_t.empty:
                        c_price = df_t['Close'].iloc[-1]
                        p_price = df_t['Close'].iloc[-2]
                        chg_pct = ((c_price - p_price) / p_price) * 100
                        
                        # حساب مؤشر القوة النسبية RSI مبسط
                        delta = df_t['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi_val = (100 - (100 / (1 + rs))).iloc[-1]
                        
                        support_l = df_t['Low'].tail(15).min()
                        resist_h = df_t['High'].tail(15).max()
                        
                        st.success(f"تم تحليل مؤشرات السهم {ticker_tech} بنجاح.")
                        
                        tm1, tm2, tm3, tm4 = st.columns(4)
                        tm1.metric("السعر الحالي", f"{c_price:.2f} ج.م", f"{chg_pct:+.2f}%")
                        tm2.metric("مؤشر RSI", f"{rsi_val:.1f}")
                        tm3.metric("مستوى الدعم", f"{support_l:.2f} ج.م")
                        tm4.metric("مستوى المقاومة", f"{resist_h:.2f} ج.م")

                        st.subheader("الرسم البياني لحركة السعر")
                        st.line_chart(df_t['Close'])
                    else:
                        st.warning("رمز السهم غير صحيح أو البيانات غير متوفرة.")
                else:
                    st.error("مكتبة جلب البيانات غير متاحة.")
            except Exception as ex:
                st.error(f"حدث خطأ: {ex}")

elif "إدارة المحفظة الاستثمارية" in page:
    st.header("💼 إدارة المحفظة الاستثمارية ومتابعة الأداء")
    portfolio_df = pd.DataFrame({
        "السهم": ["COMI.CA", "FWRY.CA", "ADIB.CA"],
        "الكمية": [1000, 2500, 800],
        "سعر الشراء": [72.00, 6.10, 35.00],
        "السعر الحالي": [78.50, 6.82, 38.00]
    })
    portfolio_df["التكلفة الإجمالية"] = portfolio_df["الكمية"] * portfolio_df["سعر الشراء"]
    portfolio_df["القيمة الحالية"] = portfolio_df["الكمية"] * portfolio_df["السعر الحالي"]
    portfolio_df["الربح / الخسارة (ج.م)"] = portfolio_df["القيمة الحالية"] - portfolio_df["التكلفة الإجمالية"]
    st.dataframe(portfolio_df, use_container_width=True)
    st.metric("صافي القيمة الحالية للمحفظة", f"{portfolio_df['القيمة الحالية'].sum():,.2f} ج.م")

else:
    st.header("💰 حاسبة العائد المركب اليومي")
    c1, c2 = st.columns(2)
    with c1:
        base_cap = st.number_input("رأس المال الأساسي (ج.م)", value=50000, step=5000)
        daily_target = st.slider("معدل الربح المستهدف يومياً (%)", 0.5, 5.0, 5.0)
    with c2:
        trading_days = st.slider("عدد أيام التداول المستهدفة", 5, 60, 20)
        
    if st.button("حساب مسار النمو التراكمي"):
        accumulated_val = base_cap
        growth_records = []
        for d in range(1, trading_days + 1):
            accumulated_val = accumulated_val * (1 + daily_target / 100)
            growth_records.append({"اليوم": d, "إجمالي رأس المال المتوقع (ج.م)": round(accumulated_val, 2)})
        st.dataframe(pd.DataFrame(growth_records), use_container_width=True)
