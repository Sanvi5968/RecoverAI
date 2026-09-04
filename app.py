
import streamlit as st
import pandas as pd

from agent import ask_recovery_agent, execute_action


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RecoverAI | Revenue Recovery",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] h1 {
        color: white;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 18px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.65rem 1rem;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        border-radius: 10px;
        background-color: white;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background-color: white;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        padding-top: 15px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv(
    "data/agent_results.csv",
    encoding="latin1"
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def format_inr(value):

    if value >= 1_00_00_000:
        return f"₹{value / 1_00_00_000:.2f} Cr"

    elif value >= 1_00_000:
        return f"₹{value / 1_00_000:.2f} L"

    elif value >= 1_000:
        return f"₹{value / 1_000:.2f} K"

    else:
        return f"₹{value:.2f}"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("💳 RecoverAI")

    st.caption("AI Revenue Recovery Platform")

    st.divider()

    st.markdown("### 📌 About")

    st.write(
        "RecoverAI analyzes failed payments, "
        "predicts recovery probability and "
        "recommends the best recovery action."
    )

    st.divider()

    st.markdown("### 🧠 AI Pipeline")

    st.write("01  —  ML Prediction")
    st.write("02  —  Decision Engine")
    st.write("03  —  Gemini AI Agent")
    st.write("04  —  Recovery Tool")
    st.write("05  —  Action Logging")

    st.divider()

    st.markdown("### 📊 Dataset")

    st.metric(
        "Transactions",
        f"{len(df):,}"
    )

    st.divider()

    st.caption(
        "RecoverAI • AI-powered payment recovery"
    )


# =========================================================
# HEADER
# =========================================================

st.title("💳 RecoverAI")

st.subheader(
    "Intelligent Revenue Recovery Agent for Failed Payments"
)

st.caption(
    "✦ AI-powered fintech system • ML + Gemini AI + Automated Recovery"
)

st.divider()


# =========================================================
# BUSINESS METRICS
# =========================================================

total_failed_value = df["amount"].sum()

recovered_value = df.loc[
    df["actual_recovered"] == 1,
    "amount"
].sum()

unrecovered_value = (
    total_failed_value - recovered_value
)

recovery_rate = (
    recovered_value / total_failed_value * 100
)


st.header("📊 Revenue Recovery Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Failed Value",
        format_inr(total_failed_value)
    )


with col2:
    st.metric(
        "Recovered Value",
        format_inr(recovered_value)
    )


with col3:
    st.metric(
        "Unrecovered Value",
        format_inr(unrecovered_value)
    )


with col4:
    st.metric(
        "Recovery Rate",
        f"{recovery_rate:.2f}%"
    )


# =========================================================
# TRANSACTION ANALYSIS
# =========================================================

st.divider()

st.header("🔎 Transaction Analysis")

transaction_id = st.selectbox(
    "Select a failed transaction",
    df["transaction_id"].tolist()
)


transaction = df[
    df["transaction_id"] == transaction_id
].iloc[0]


# =========================================================
# TRANSACTION INFORMATION
# =========================================================

st.subheader("Transaction Information")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Transaction ID",
        transaction["transaction_id"]
    )


with col2:
    st.metric(
        "Amount",
        f"₹{transaction['amount']:,.2f}"
    )


with col3:
    st.metric(
        "Payment Method",
        transaction["payment_method"]
    )


with col4:
    st.metric(
        "Failure Reason",
        transaction["failure_reason"]
    )


# =========================================================
# AI RECOVERY DECISION
# =========================================================

probability = float(
    transaction["recovery_probability"]
)

priority = transaction["priority"]

recommended_action = (
    transaction["recommended_action"]
)


st.subheader("🧠 AI Recovery Decision")

st.info(
    "✦ AI-powered recovery recommendation based on "
    "ML prediction and decision engine."
)


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Recovery Probability",
        f"{probability:.2f}%"
    )


with col2:
    st.metric(
        "Recovery Priority",
        priority
    )


with col3:
    st.metric(
        "Recommended Action",
        recommended_action
    )


# =========================================================
# AI RECOVERY AGENT
# =========================================================

st.divider()

st.header("🤖 AI Recovery Agent")

st.caption(
    "Ask Gemini AI to explain why this recovery action was selected."
)


if st.button(
    "🤖 Ask AI Recovery Agent",
    type="primary",
    use_container_width=True
):

    agent_context = {

        "transaction_id":
            transaction["transaction_id"],

        "amount":
            float(transaction["amount"]),

        "payment_method":
            transaction["payment_method"],

        "failure_reason":
            transaction["failure_reason"],

        "recovery_probability":
            round(probability, 2),

        "priority":
            priority,

        "recommended_action":
            recommended_action,

        "action_status":
            transaction["action_status"],

        "actual_recovered":
            int(transaction["actual_recovered"])
    }


    with st.spinner(
        "🤖 Gemini AI is analyzing the payment..."
    ):

        try:

            ai_response = ask_recovery_agent(
                agent_context
            )

            st.success(
                "AI analysis completed successfully."
            )

            with st.expander(
                "🤖 View AI Agent Analysis",
                expanded=True
            ):

                st.write(ai_response)

        except Exception as e:

            st.error(
                f"AI Agent Error: {e}"
            )


# =========================================================
# RECOVERY ACTION
# =========================================================

st.divider()

st.header("⚡ Recovery Action")


st.info(
    f"Recommended action for **{transaction_id}**: "
    f"**{recommended_action}**"
)


# =========================================================
# INITIALIZE ACTION LOG
# =========================================================

if "action_log" not in st.session_state:

    st.session_state.action_log = []


# =========================================================
# EXECUTE RECOVERY ACTION
# =========================================================

if st.button(
    f"⚡ Execute: {recommended_action}",
    type="primary",
    use_container_width=True
):

    result = execute_action(
        recommended_action,
        transaction["transaction_id"],
        transaction["amount"]
    )


    # Add action to log

    st.session_state.action_log.append({

        "Transaction ID":
            transaction["transaction_id"],

        "Amount":
            float(transaction["amount"]),

        "Action":
            recommended_action,

        "Status":
            result["status"]
    })


    # Save action log

    action_log_df = pd.DataFrame(
        st.session_state.action_log
    )

    action_log_df.to_csv(
        "data/action_log.csv",
        index=False
    )


    st.success(
        result["message"]
    )


    with st.expander(
        "📄 View Action Response",
        expanded=True
    ):

        st.json(result)


# =========================================================
# RECOVERY ANALYTICS
# =========================================================

st.divider()

st.header("📈 Recovery Analytics")


col1, col2 = st.columns(2)


# =========================================================
# PRIORITY DISTRIBUTION
# =========================================================

with col1:

    st.subheader(
        "Recovery Priority Distribution"
    )

    priority_counts = (
        df["priority"]
        .value_counts()
        .reindex(
            ["High", "Medium", "Low"]
        )
        .fillna(0)
        .astype(int)
    )


    priority_chart = pd.DataFrame({
        "Transactions": priority_counts
    })


    st.bar_chart(
        priority_chart,
        horizontal=True
    )


# =========================================================
# RECOVERY ACTION DISTRIBUTION
# =========================================================

with col2:

    st.subheader(
        "Recommended Recovery Actions"
    )

    action_counts = (
        df["recommended_action"]
        .value_counts()
        .reindex([
            "Retry Payment",
            "Generate Payment Link",
            "Send Notification",
            "Defer Recovery"
        ])
        .fillna(0)
        .astype(int)
    )


    action_chart = pd.DataFrame({
        "Transactions": action_counts
    })


    st.bar_chart(
        action_chart,
        horizontal=True
    )


# =========================================================
# ACTION LOG
# =========================================================

if st.session_state.action_log:

    st.divider()

    st.header("📋 Recovery Action Log")


    action_log_df = pd.DataFrame(
        st.session_state.action_log
    )


    st.dataframe(
        action_log_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💳 RecoverAI • Intelligent Revenue Recovery • "
    "Powered by ML + Gemini AI"
)

