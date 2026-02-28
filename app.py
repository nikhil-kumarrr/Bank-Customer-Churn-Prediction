import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="ChurnSense · Risk Intelligence",
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:      #f5f4f0;
    --s1:      #ffffff;
    --s2:      #f0eeea;
    --border:  #e0ddd6;
    --dark:    #111111;
    --accent:  #00a86b;
    --accent2: #007a4d;
    --muted:   #6b7280;
    --muted2:  #9ca3af;
    --red:     #dc2626;
    --redl:    #fef2f2;
    --greenl:  #f0fdf4;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    background-color: var(--bg) !important;
    color: var(--dark) !important;
    font-family: 'Outfit', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebar"],
.stDeployButton { visibility: hidden !important; display: none !important; }

.block-container,
[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 100% !important;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container, .stMarkdown { margin: 0 !important; padding: 0 !important; }

/* ── WIDGET LABELS ── */
div[data-testid="stSelectbox"] label p,
div[data-testid="stNumberInput"] label p,
div[data-testid="stSlider"] label p,
div[data-testid="stRadio"] label p,
[data-testid="stWidgetLabel"] p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
    color: #6b7280 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    margin-top: 16px !important;
    margin-bottom: 6px !important;
}

/* ── SELECTBOX ── */
div[data-testid="stSelectbox"] > div > div {
    background: var(--s1) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--dark) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--accent) !important;
}
div[data-testid="stSelectbox"] span { color: var(--dark) !important; }
div[data-testid="stSelectbox"] svg  { fill: #9ca3af !important; }

/* ── NUMBER INPUT ── */
div[data-testid="stNumberInput"] input {
    background: var(--s1) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--dark) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,168,107,0.1) !important;
    outline: none !important;
}
div[data-testid="stNumberInput"] button {
    background: var(--s1) !important;
    border: 1.5px solid var(--border) !important;
    color: #9ca3af !important;
    border-radius: 6px !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: #e0ddd6 !important;
    height: 4px !important;
    border-radius: 4px !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2) {
    background: var(--accent) !important;
}
[data-testid="stSlider"] [role="slider"] {
    background: var(--accent) !important;
    border: 3px solid #ffffff !important;
    box-shadow: 0 0 0 2px var(--accent) !important;
    width: 20px !important;
    height: 20px !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: var(--accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    background: transparent !important;
}
[data-testid="stSlider"] [data-testid="stTickBar"] > div {
    color: #9ca3af !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
}

/* ── RADIO ── */
[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 10px !important;
}
[data-testid="stRadio"] label {
    flex: 1 !important;
    padding: 9px 14px !important;
    background: var(--s1) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    transition: all 0.2s !important;
}
[data-testid="stRadio"] label:hover {
    border-color: var(--accent) !important;
}
[data-testid="stRadio"] label span:last-child {
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--dark) !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
[data-baseweb="radio"] > div {
    background: transparent !important;
    border: 2px solid #d1d5db !important;
    width: 14px !important;
    height: 14px !important;
}
[data-baseweb="radio"][aria-checked="true"] > div {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    width: 100% !important;
    padding: 16px !important;
    background: var(--dark) !important;
    color: #ffffff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    margin-top: 28px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: var(--accent) !important;
    transform: translateY(-1px) !important;
}

[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ══ NAV ═══════════════════════════════════════════════════════
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;
            padding:16px 48px; background:#111111; border-bottom:1px solid #222;">
  <div style="display:flex; align-items:center; gap:12px;">
    <div style="width:32px; height:32px; background:#00a86b;
                border-radius:8px; display:flex; align-items:center;
                justify-content:center; font-size:15px;">🏦</div>
    <div>
      <div style="font-family:'Outfit',sans-serif; font-size:16px; font-weight:800;
                  color:#ffffff; letter-spacing:0.5px;">
        Churn<span style="color:#00a86b;">Sense</span>
      </div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                  letter-spacing:2px; color:#4b5563; margin-top:1px;">
        BANK RISK INTELLIGENCE
      </div>
    </div>
  </div>
  <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
              letter-spacing:2px; color:#4b5563; border:1px solid #333;
              padding:6px 16px; border-radius:100px;
              display:flex; align-items:center; gap:8px;">
    <span style="width:6px;height:6px;background:#00a86b;border-radius:50%;
                 display:inline-block;box-shadow:0 0 6px #00a86b;"></span>
    PREDICTION ENGINE &nbsp;·&nbsp; V1.0
  </div>
</div>
""", unsafe_allow_html=True)


# ══ HERO ══════════════════════════════════════════════════════
st.markdown("""
<div style="padding:48px 48px 40px; background:#111111;
            border-bottom:3px solid #00a86b;">
  <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
              letter-spacing:4px; color:#00a86b; text-transform:uppercase;
              margin-bottom:16px;">◈ Customer Retention Intelligence System</div>
  <div style="font-family:'Outfit',sans-serif; font-size:clamp(36px,4vw,58px);
              font-weight:800; line-height:1.05; color:#ffffff; margin-bottom:16px;">
    Predict Churn.<br>
    <span style="color:#00a86b;">Before It Happens.</span>
  </div>
  <div style="font-size:14px; font-weight:300; color:#9ca3af;
              max-width:500px; line-height:1.85;">
    Feed customer parameters into the engine. Get a data-driven prediction
    powered by EDA insights and a trained Random Forest model — instantly.
  </div>
</div>
""", unsafe_allow_html=True)


# ══ STATS ROW ═════════════════════════════════════════════════
st.markdown("<div style='background:#111111; padding:0 48px 0;'>", unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
for col, num, label, sub, hi in [
    (s1, "10,000", "Customer Profiles",  "Records in training data", False),
    (s2, "86.6%",  "Model Accuracy",     "Random Forest classifier", True),
    (s3, "3",      "Models Evaluated",   "LR · DT · RF compared",   False),
    (s4, "~20%",   "Avg Churn Rate",     "Industry baseline",        False),
]:
    col.markdown(f"""
    <div style="padding:24px 0 28px; border-right:1px solid #1f1f1f;">
      <div style="font-family:'Outfit',sans-serif; font-size:34px; font-weight:800;
                  color:{'#00a86b' if hi else '#ffffff'}; line-height:1; margin-bottom:8px;">
        {num}
      </div>
      <div style="font-size:12px; font-weight:600; color:#d1d5db; margin-bottom:3px;">{label}</div>
      <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                  letter-spacing:1px; color:#4b5563;">{sub}</div>
    </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# ══ MAIN BODY ═════════════════════════════════════════════════
st.markdown("<div style='padding:40px 48px; background:#f5f4f0;'>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")


# ─── LEFT ─────────────────────────────────────────────────────
with left:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                letter-spacing:4px; color:#00a86b; text-transform:uppercase;
                padding-bottom:12px; border-bottom:1.5px solid #e0ddd6;
                margin-bottom:4px; font-weight:500;">
      01 — Client Risk Assessment Form
    </div>""", unsafe_allow_html=True)

    # Personal
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px;
                margin-top:22px; margin-bottom:14px;">
      <span style="font-size:13px;">👤</span>
      <span style="font-family:'JetBrains Mono',monospace; font-size:8px;
                   letter-spacing:3px; color:#9ca3af; text-transform:uppercase;">
        Personal Information
      </span>
      <div style="flex:1; height:1px; background:#e0ddd6;"></div>
    </div>""", unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        geography = st.selectbox("Country / Geography", le_geo.classes_)
    with p2:
        gender = st.selectbox("Gender", le_gen.classes_)

    a1, a2 = st.columns(2)
    with a1:
        age = st.slider("Client Age", 18, 92, 38)
    with a2:
        tenure = st.slider("Years with Bank", 0, 10, 5)

    # Financial
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px;
                margin-top:22px; margin-bottom:14px;">
      <span style="font-size:13px;">💼</span>
      <span style="font-family:'JetBrains Mono',monospace; font-size:8px;
                   letter-spacing:3px; color:#9ca3af; text-transform:uppercase;">
        Financial Profile
      </span>
      <div style="flex:1; height:1px; background:#e0ddd6;"></div>
    </div>""", unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        credit_score = st.slider("Credit Score", 300, 850, 650)
        balance      = st.number_input("Account Balance ($)", 0.0, value=76000.0, step=500.0)
    with f2:
        num_products     = st.selectbox("Banking Products Held", [1, 2, 3, 4])
        estimated_salary = st.number_input("Annual Salary ($)", 0.0, value=85000.0, step=500.0)

    # Account Status
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px;
                margin-top:22px; margin-bottom:14px;">
      <span style="font-size:13px;">💳</span>
      <span style="font-family:'JetBrains Mono',monospace; font-size:8px;
                   letter-spacing:3px; color:#9ca3af; text-transform:uppercase;">
        Account Status
      </span>
      <div style="flex:1; height:1px; background:#e0ddd6;"></div>
    </div>""", unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        has_cr_card = st.radio("Holds Credit Card?", ["Yes", "No"], horizontal=True)
    with m2:
        is_active = st.radio("Active Account Member?", ["Yes", "No"], horizontal=True)

    predict = st.button("RUN RISK ASSESSMENT ◈", use_container_width=True)
    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)


# ─── RIGHT ────────────────────────────────────────────────────
with right:
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                letter-spacing:4px; color:#00a86b; text-transform:uppercase;
                padding-bottom:12px; border-bottom:1.5px solid #e0ddd6;
                margin-bottom:24px; font-weight:500;">
      02 — Risk Intelligence Report
    </div>""", unsafe_allow_html=True)

    if not predict:
        st.markdown("""
        <div style="text-align:center; padding:72px 24px;
                    background:#ffffff; border:1.5px dashed #e0ddd6;
                    border-radius:10px; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
          <div style="font-size:32px; opacity:0.15; margin-bottom:16px;">◈</div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                      letter-spacing:3px; color:#9ca3af; text-transform:uppercase;
                      margin-bottom:10px;">Awaiting Analysis</div>
          <div style="font-size:13px; color:#9ca3af; line-height:1.7;">
            Set parameters on the left<br>and click Run Assessment
          </div>
        </div>""", unsafe_allow_html=True)

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
            css      = "background:#fef2f2; border:1.5px solid #fca5a5;"
            icon     = "✕"
            label    = "HIGH CHURN RISK"
            sublabel = "Client flagged for immediate retention action"
            color    = "#dc2626"
            bar_color= "#dc2626"
            actions  = [
                ("📞", "Priority Call",   "Assign senior RM within 24 hours for direct outreach."),
                ("💰", "Retention Offer", "Present tailored rate revision or fee waiver package."),
                ("🎯", "Product Bundle",  "Offer multi-product bundle — reduces churn by 60%."),
                ("📋", "Exit Interview",  "Schedule proactive satisfaction review call."),
            ]
        else:
            css      = "background:#f0fdf4; border:1.5px solid #86efac;"
            icon     = "✓"
            label    = "LOW CHURN RISK"
            sublabel = "Client profile stable — continue standard engagement"
            color    = "#16a34a"
            bar_color= "#16a34a"
            actions  = [
                ("📈", "Upsell Review", "Identify premium product opportunities this quarter."),
                ("🏆", "Loyalty Tier",  "Upgrade client to Platinum loyalty programme."),
                ("💎", "Wealth Mgmt",   "Propose wealth management consultation."),
                ("💬", "NPS Survey",    "Schedule quarterly satisfaction touchpoint."),
            ]

        # RESULT BOX
        st.markdown(f"""
        <div style="{css} border-radius:10px; padding:32px; text-align:center;
                    margin-bottom:14px; box-shadow:0 1px 3px rgba(0,0,0,0.06);">
          <div style="font-family:'Outfit',sans-serif; font-size:42px; font-weight:800;
                      color:{color}; letter-spacing:1px; margin-bottom:4px;">
            {icon} &nbsp; {pct}%
          </div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:10px;
                      letter-spacing:3px; color:{color}; text-transform:uppercase;
                      margin-bottom:6px;">{label}</div>
          <div style="font-size:13px; color:#6b7280; margin-bottom:20px;">{sublabel}</div>
          <div style="height:4px; background:rgba(0,0,0,0.08); border-radius:2px;
                      max-width:200px; margin:0 auto; overflow:hidden;">
            <div style="height:4px; width:{pct}%; background:{bar_color};
                        border-radius:2px;"></div>
          </div>
        </div>""", unsafe_allow_html=True)

        # METRICS
        mx1, mx2, mx3, mx4 = st.columns(4)
        for col, val, lbl, clr in [
            (mx1, f"{pct}%",  "Churn Risk",  color),
            (mx2, f"{stay}%", "Retention",   "#16a34a"),
            (mx3, "RF",       "Model",       "#111111"),
            (mx4, "86.6%",    "Accuracy",    "#111111"),
        ]:
            col.markdown(f"""
            <div style="background:#ffffff; border:1px solid #e0ddd6; border-radius:10px;
                        padding:14px 10px; text-align:center; margin-bottom:14px;
                        box-shadow:0 1px 3px rgba(0,0,0,0.04);">
              <div style="font-family:'Outfit',sans-serif; font-size:20px; font-weight:800;
                          color:{clr}; margin-bottom:4px;">{val}</div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:8px;
                          letter-spacing:1.5px; color:#9ca3af; text-transform:uppercase;">
                {lbl}
              </div>
            </div>""", unsafe_allow_html=True)

        # SUMMARY TABLE
        st.markdown(f"""
        <div style="background:#ffffff; border:1px solid #e0ddd6; border-radius:10px;
                    padding:20px 20px; margin-bottom:14px;
                    box-shadow:0 1px 3px rgba(0,0,0,0.04);">
          <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                      letter-spacing:3px; color:#9ca3af; text-transform:uppercase;
                      margin-bottom:14px;">Client Summary</div>
          <table style="width:100%; border-collapse:collapse;">
            {''.join([f"""
            <tr style="border-bottom:1px solid #f3f4f6;">
              <td style="font-family:'JetBrains Mono',monospace; font-size:9px;
                         color:#9ca3af; letter-spacing:1px; text-transform:uppercase;
                         padding:8px 0; width:140px;">{k}</td>
              <td style="font-size:13px; color:#111111; padding:8px 0;
                         font-weight:{'600' if bold else '400'};
                         color:{vc};">{v}</td>
            </tr>""" for k, v, bold, vc in [
                ("Geography",   geography,          False, "#111111"),
                ("Gender",      gender,             False, "#111111"),
                ("Age",         age,                False, "#111111"),
                ("Tenure",      f"{tenure} yrs",    False, "#111111"),
                ("Credit Score",credit_score,       False, "#111111"),
                ("Balance",     f"${balance:,.0f}", False, "#111111"),
                ("Products",    num_products,       False, "#111111"),
                ("Credit Card", has_cr_card,        False, "#111111"),
                ("Active Mbr",  is_active,          False, "#111111"),
                ("Verdict",     label,              True,  color),
            ]])}
          </table>
        </div>""", unsafe_allow_html=True)

        # ACTIONS
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace; font-size:9px;
                    letter-spacing:4px; color:#00a86b; text-transform:uppercase;
                    padding-bottom:12px; border-bottom:1.5px solid #e0ddd6;
                    margin-bottom:8px; font-weight:500;">
          03 — Banker Action Plan
        </div>""", unsafe_allow_html=True)

        for icon_e, title, desc in actions:
            st.markdown(f"""
            <div style="display:flex; gap:12px; padding:12px 0;
                        border-bottom:1px solid #f3f4f6; align-items:flex-start;">
              <div style="width:32px; height:32px; background:#f5f4f0;
                          border:1px solid #e0ddd6; border-radius:8px;
                          display:flex; align-items:center; justify-content:center;
                          font-size:14px; flex-shrink:0;">{icon_e}</div>
              <div>
                <div style="font-size:13px; font-weight:600; color:#111111;
                            margin-bottom:2px;">{title}</div>
                <div style="font-size:12px; color:#6b7280; line-height:1.6;">{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style="text-align:center; padding:20px 0;
            border-top:1px solid #e0ddd6; background:#f5f4f0;">
  <span style="font-family:'JetBrains Mono',monospace; font-size:9px;
               letter-spacing:3px; color:#9ca3af; text-transform:uppercase;">
    ChurnSense &nbsp;·&nbsp; Bank Risk Intelligence &nbsp;·&nbsp; 2025
  </span>
</div>
""", unsafe_allow_html=True)