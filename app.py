import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="ChurnSense · Bank Risk",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load():
    model    = pickle.load(open("models/best_model.pkl",    "rb"))
    scaler   = pickle.load(open("models/scaler.pkl",        "rb"))
    le_geo   = pickle.load(open("models/le_geo.pkl",        "rb"))
    le_gen   = pickle.load(open("models/le_gen.pkl",        "rb"))
    features = pickle.load(open("models/feature_names.pkl", "rb"))
    return model, scaler, le_geo, le_gen, features

model, scaler, le_geo, le_gen, feature_names = load()

def build_table(rows, verdict_color):
    html = '<table style="width:100%;border-collapse:collapse;">'
    for key, val, is_verdict in rows:
        clr = verdict_color if is_verdict else "#1c1917"
        fw  = "700" if is_verdict else "400"
        html += (
            '<tr style="border-bottom:1px solid #f0f0f0;">'
            '<td style="font-size:12px;color:#9ca3af;padding:7px 0;width:120px;">' + str(key) + '</td>'
            '<td style="font-size:13px;color:' + clr + ';padding:7px 0;font-weight:' + fw + ';">' + str(val) + '</td>'
            '</tr>'
        )
    html += '</table>'
    return html

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    background: #f8f9fa !important;
    color: #1a1a1a !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stSidebar"], .stDeployButton {
    display: none !important;
}

.block-container, [data-testid="block-container"] {
    padding: 0 !important; max-width: 100% !important;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container, .stMarkdown { margin: 0 !important; padding: 0 !important; }

/* LABELS */
div[data-testid="stSelectbox"] label p,
div[data-testid="stNumberInput"] label p,
div[data-testid="stSlider"] label p,
div[data-testid="stRadio"] label p,
[data-testid="stWidgetLabel"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #374151 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    margin-top: 14px !important;
    margin-bottom: 5px !important;
}

/* SELECTBOX */
div[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 8px !important;
    color: #1a1a1a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
div[data-testid="stSelectbox"] > div > div:hover { border-color: #1d4ed8 !important; }
div[data-testid="stSelectbox"] span { color: #1a1a1a !important; }
div[data-testid="stSelectbox"] svg  { fill: #9ca3af !important; }
[data-baseweb="popover"] [role="option"] {
    background: #ffffff !important; color: #1a1a1a !important;
}
[data-baseweb="popover"] [role="option"]:hover { background: #eff6ff !important; }

/* NUMBER INPUT */
div[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 8px !important;
    color: #1a1a1a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #1d4ed8 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.08) !important;
}
div[data-testid="stNumberInput"] button {
    background: #ffffff !important;
    border: 1.5px solid #e5e7eb !important;
    color: #9ca3af !important; border-radius: 6px !important;
}

/* SLIDER */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: #e5e7eb !important;
    height: 4px !important; border-radius: 4px !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2) {
    background: #1d4ed8 !important;
}
[data-testid="stSlider"] [role="slider"] {
    background: #1d4ed8 !important;
    border: 3px solid #ffffff !important;
    box-shadow: 0 0 0 2px #1d4ed8, 0 2px 6px rgba(29,78,216,0.3) !important;
    width: 18px !important; height: 18px !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #1d4ed8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important; font-weight: 600 !important;
    background: transparent !important;
}
[data-testid="stSlider"] [data-testid="stTickBar"] > div {
    color: #9ca3af !important;
    font-size: 10px !important;
}

/* RADIO */
[data-testid="stRadio"] > div {
    display: flex !important; flex-direction: row !important; gap: 8px !important;
}
[data-testid="stRadio"] label {
    flex: 1 !important; padding: 9px 14px !important;
    background: #ffffff !important;
    border: 1.5px solid #e5e7eb !important;
    border-radius: 8px !important; cursor: pointer !important;
    display: flex !important; align-items: center !important;
    gap: 8px !important; transition: all 0.15s !important;
}
[data-testid="stRadio"] label:hover { border-color: #1d4ed8 !important; }
[data-testid="stRadio"] label span:last-child {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; font-weight: 400 !important;
    color: #1a1a1a !important;
    letter-spacing: 0 !important; text-transform: none !important;
}
[data-baseweb="radio"] > div {
    background: transparent !important;
    border: 2px solid #d1d5db !important;
    width: 14px !important; height: 14px !important;
}
[data-baseweb="radio"][aria-checked="true"] > div {
    background: #1d4ed8 !important; border-color: #1d4ed8 !important;
}

/* BUTTON */
[data-testid="stButton"] > button {
    width: 100% !important; padding: 14px !important;
    background: #1d4ed8 !important; color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important; font-weight: 600 !important;
    letter-spacing: 0 !important; text-transform: none !important;
    border: none !important; border-radius: 8px !important;
    cursor: pointer !important; margin-top: 24px !important;
    transition: all 0.15s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: #1e40af !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(29,78,216,0.3) !important;
}

[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ══ NAV ═══════════════════════════════════════
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;
            padding:0 48px; height:60px; background:#ffffff;
            border-bottom:1px solid #e5e7eb;">
  <div style="display:flex; align-items:center; gap:10px;">
    <div style="width:32px; height:32px; background:#1d4ed8; border-radius:8px;
                display:flex; align-items:center; justify-content:center; font-size:15px;">
      🏦
    </div>
    <div>
      <div style="font-size:16px; font-weight:700; color:#1a1a1a;">
        Churn<span style="color:#1d4ed8;">Sense</span>
      </div>
      <div style="font-size:11px; color:#9ca3af; margin-top:-1px;">
        Bank Customer Risk Platform
      </div>
    </div>
  </div>
  <div style="display:flex; align-items:center; gap:6px; padding:6px 14px;
              background:#f0fdf4; border:1px solid #bbf7d0; border-radius:20px;">
    <span style="width:7px; height:7px; background:#16a34a; border-radius:50%;
                 display:inline-block;"></span>
    <span style="font-size:12px; font-weight:500; color:#15803d;">Model Active</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══ HERO ══════════════════════════════════════
st.markdown("""
<div style="background:#1e3a8a; padding:44px 48px 40px;">
  <div style="font-size:12px; font-weight:500; color:#93c5fd;
              margin-bottom:12px; letter-spacing:0.5px;">
    Customer Churn Prediction System
  </div>
  <div style="font-size:clamp(30px,3.5vw,48px); font-weight:700;
              color:#ffffff; line-height:1.15; margin-bottom:12px;">
    Identify At-Risk Customers<br>
    <span style="color:#60a5fa;">Before They Leave.</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══ STATS ROW ═════════════════════════════════
st.markdown("<div style='background:#1e3a8a; padding:0 48px;'>", unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns(4)
stats = [
    (sc1, "10,000", "Customer Profiles",  "Training dataset size",   False),
    (sc2, "86.6%",  "Model Accuracy",     "Random Forest",           True),
    (sc3, "3",      "Models Compared",    "LR · DT · RF",            False),
    (sc4, "~20%",   "Industry Churn Rate","Average baseline",         False),
]
for col, num, label, sub, hi in stats:
    col.markdown(
        '<div style="padding:20px 0 24px; border-right:1px solid rgba(255,255,255,0.08);">'
        '<div style="font-size:30px; font-weight:700; color:' + ('#60a5fa' if hi else '#60a5fa') + '; margin-bottom:6px;">' + num + '</div>'
        '<div style="font-size:13px; font-weight:500; color:#e2e8f0; margin-bottom:2px;">' + label + '</div>'
        '<div style="font-size:11px; color:#93c5fd;">' + sub + '</div>'
        '</div>',
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)


# ══ MAIN BODY ═════════════════════════════════
st.markdown("<div style='padding:36px 48px; background:#f8f9fa;'>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")


# ─── LEFT ─────────────────────────────────────
with left:
    st.markdown(
        '<div style="font-size:13px; font-weight:600; color:#1d4ed8;'
        'padding-bottom:10px; border-bottom:2px solid #1d4ed8; margin-bottom:4px;">'
        'Step 1 — Enter Customer Details</div>',
        unsafe_allow_html=True
    )

    def section(icon, title):
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px;'
            'margin-top:20px; margin-bottom:10px;">'
            '<span style="font-size:14px;">' + icon + '</span>'
            '<span style="font-size:12px; font-weight:600; color:#374151;">' + title + '</span>'
            '<div style="flex:1; height:1px; background:#e5e7eb; margin-left:4px;"></div>'
            '</div>',
            unsafe_allow_html=True
        )

    section("", "Personal Information")
    c1, c2 = st.columns(2)
    with c1: geography = st.selectbox("Country", le_geo.classes_)
    with c2: gender    = st.selectbox("Gender",  le_gen.classes_)

    c3, c4 = st.columns(2)
    with c3: age    = st.slider("Age",            18, 92, 38)
    with c4: tenure = st.slider("Tenure (Years)", 0,  10, 5)

    section("", "Financial Information")
    c5, c6 = st.columns(2)
    with c5:
        credit_score = st.slider("Credit Score", 300, 850, 650)
        balance      = st.number_input("Account Balance ($)", 0.0, value=76000.0, step=500.0)
    with c6:
        num_products     = st.selectbox("Number of Products", [1, 2, 3, 4])
        estimated_salary = st.number_input("Annual Salary ($)", 0.0, value=85000.0, step=500.0)

    section("", "Account Details")
    c7, c8 = st.columns(2)
    with c7: has_cr_card = st.radio("Has Credit Card?",  ["Yes", "No"], horizontal=True)
    with c8: is_active   = st.radio("Active Member?",    ["Yes", "No"], horizontal=True)

    predict = st.button("Run Churn Prediction →", use_container_width=True)
    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)


# ─── RIGHT ────────────────────────────────────
with right:
    st.markdown(
        '<div style="font-size:13px; font-weight:600; color:#1d4ed8;'
        'padding-bottom:10px; border-bottom:2px solid #1d4ed8; margin-bottom:24px;">'
        'Step 2 — View Prediction Result</div>',
        unsafe_allow_html=True
    )

    if not predict:
        st.markdown("""
        <div style="background:#ffffff; border:1.5px dashed #d1d5db; border-radius:12px;
                    padding:52px 32px; text-align:center; margin-bottom:16px;">
          <div style="font-size:36px; margin-bottom:12px; opacity:0.3;">🏦</div>
          <div style="font-size:16px; font-weight:600; color:#374151; margin-bottom:8px;">
            Waiting for Input
          </div>
          <div style="font-size:13px; color:#9ca3af; line-height:1.6;">
            Fill in the customer details on the left<br>
            and click the button to see the prediction.
          </div>
        </div>""", unsafe_allow_html=True)

        # Quick facts
        st.markdown(
            '<div style="font-size:13px; font-weight:600; color:#374151;'
            'margin-bottom:12px;">Key Insights from Model Training</div>',
            unsafe_allow_html=True
        )
        facts = [
            ("", "Germany has the highest churn rate among all 3 countries."),
            ("", "Customers aged 40–60 are most likely to leave the bank."),
            ("", "Customers with only 1 product churn significantly more."),
            ("", "Inactive members are 3x more likely to churn."),
        ]
        for icon, text in facts:
            st.markdown(
                '<div style="display:flex; align-items:flex-start; gap:10px;'
                'padding:10px 14px; background:#ffffff; border:1px solid #e5e7eb;'
                'border-radius:8px; margin-bottom:8px;">'
                '<span style="font-size:16px;">' + icon + '</span>'
                '<span style="font-size:13px; color:#374151; line-height:1.5;">' + text + '</span>'
                '</div>',
                unsafe_allow_html=True
            )

    else:
        geo_enc = le_geo.transform([geography])[0]
        gen_enc = le_gen.transform([gender])[0]
        cr_card = 1 if has_cr_card == "Yes" else 0
        active  = 1 if is_active   == "Yes" else 0

        inp = pd.DataFrame([[
            credit_score, geo_enc, gen_enc, age, tenure,
            balance, num_products, cr_card, active, estimated_salary
        ]], columns=feature_names)

        prob       = model.predict_proba(scaler.transform(inp))[0][1]
        prediction = model.predict(scaler.transform(inp))[0]
        pct        = int(prob * 100)
        stay       = 100 - pct

        if prediction == 1:
            r_bg    = "#fef2f2"
            r_bdr   = "#fca5a5"
            r_top   = "#0e0a0a"
            r_color = "#131111"
            r_icon  = ""
            r_label = "High Churn Risk"
            r_sub   = "This customer is likely to leave. Take action now."
            actions = [
                ("", "Call the customer",    "Assign a relationship manager to contact within 24 hours."),
                ("", "Offer a better rate",  "Present a personalised rate revision or fee waiver."),
                ("", "Bundle more products", "Offer a second product — it reduces churn by 60%."),
                ("", "Get their feedback",   "Schedule a satisfaction review call to understand issues."),
            ]
        else:
            r_bg    = "#f0fdf4"
            r_bdr   = "#86efac"
            r_top   = "#16a34a"
            r_color = "#16a34a"
            r_icon  = ""
            r_label = "Low Churn Risk"
            r_sub   = "This customer is stable. Focus on growing the relationship."
            actions = [
                ("", "Upsell a product",    "Identify a premium product they'd benefit from."),
                ("", "Upgrade their tier",  "Enrol them in a loyalty or rewards programme."),
                ("", "Offer wealth advice",  "Suggest an investment or wealth management session."),
                ("", "Check satisfaction",  "Do a quick NPS or feedback call this quarter."),
            ]

        # RESULT CARD
        st.markdown(
            '<div style="background:' + r_bg + '; border:1px solid ' + r_bdr + ';'
            'border-left:4px solid ' + r_top + '; border-radius:10px;'
            'padding:24px; margin-bottom:16px;">'
            '<div style="display:flex; justify-content:space-between; align-items:center;">'
            '<div>'
            '<div style="font-size:13px; color:' + r_color + '; font-weight:600; margin-bottom:6px;">'
            + r_icon + ' &nbsp;' + r_label + '</div>'
            '<div style="font-size:22px; font-weight:700; color:#1a1a1a; margin-bottom:6px;">'
            + str(pct) + '% Churn Probability</div>'
            '<div style="font-size:13px; color:#6b7280;">' + r_sub + '</div>'
            '</div></div>'
            '<div style="margin-top:16px;">'
            '<div style="height:8px; background:#e5e7eb; border-radius:8px; overflow:hidden;">'
            '<div style="height:8px; width:' + str(pct) + '%; background:' + r_color + '; border-radius:8px;"></div>'
            '</div>'
            '<div style="display:flex; justify-content:space-between; margin-top:4px;">'
            '<span style="font-size:11px; color:#9ca3af;">0% — Safe</span>'
            '<span style="font-size:11px; color:#9ca3af;">100% — Will Leave</span>'
            '</div></div></div>',
            unsafe_allow_html=True
        )

        # METRICS
        mx1, mx2, mx3, mx4 = st.columns(4)
        for col, val, lbl, clr in [
            (mx1, str(pct) + "%",  "Churn Risk",  r_color),
            (mx2, str(stay) + "%", "Will Stay",   "#16a34a"),
            (mx3, "RF",            "Model Used",  "#1d4ed8"),
            (mx4, "86.6%",         "Accuracy",    "#1d4ed8"),
        ]:
            col.markdown(
                '<div style="background:#ffffff; border:1px solid #e5e7eb; border-radius:8px;'
                'padding:14px 10px; text-align:center; margin-bottom:14px;">'
                '<div style="font-size:20px; font-weight:700; color:' + clr + '; margin-bottom:4px;">' + val + '</div>'
                '<div style="font-size:11px; color:#9ca3af;">' + lbl + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        # SNAPSHOT + ACTIONS
        snap_col, act_col = st.columns(2, gap="medium")

        with snap_col:
            rows = [
                ("Country",      geography,                False),
                ("Gender",       gender,                   False),
                ("Age",          str(age) + " years",      False),
                ("Tenure",       str(tenure) + " years",   False),
                ("Credit Score", str(credit_score),        False),
                ("Balance",      "$" + f"{balance:,.0f}",  False),
                ("Products",     str(num_products),        False),
                ("Credit Card",  has_cr_card,              False),
                ("Active",       is_active,                False),
                ("Result",       r_label,                  True),
            ]
            table_html = build_table(rows, r_color)
            st.markdown(
                '<div style="background:#ffffff; border:1px solid #e5e7eb;'
                'border-radius:10px; padding:16px;">'
                '<div style="font-size:12px; font-weight:600; color:#374151;'
                'margin-bottom:12px;">Customer Summary</div>'
                + table_html + '</div>',
                unsafe_allow_html=True
            )

        with act_col:
            acts_html = ""
            for em, t, d in actions:
                acts_html += (
                    '<div style="display:flex; gap:10px; padding:10px 0;'
                    'border-bottom:1px solid #f3f4f6; align-items:flex-start;">'
                    '<span style="font-size:18px; flex-shrink:0;">' + em + '</span>'
                    '<div>'
                    '<div style="font-size:13px; font-weight:600; color:#1a1a1a;'
                    'margin-bottom:2px;">' + t + '</div>'
                    '<div style="font-size:12px; color:#6b7280; line-height:1.5;">' + d + '</div>'
                    '</div></div>'
                )
            st.markdown(
                '<div style="background:#ffffff; border:1px solid #e5e7eb;'
                'border-radius:10px; padding:16px;">'
                '<div style="font-size:12px; font-weight:600; color:#374151;'
                'margin-bottom:4px;">Recommended Actions</div>'
                + acts_html + '</div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)