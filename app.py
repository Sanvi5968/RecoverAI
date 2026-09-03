import streamlit as st
import pandas as pd

from agent import ask_recovery_agent, execute_action


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Revenue Recovery Agent",
    page_icon="💳",
    layout="wide"
)


# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv(
    "data/agent_results.csv",
    encoding="latin1"
)


# -----------------------------
# Helper Functions
# -----------------------------

def format_inr(value):
    if value >= 1_00_00_000:
        return f"₹{value / 1_00_00_000:.2f} Cr"
    elif value >= 1_00_000:
        return f"₹{value / 1_00_000:.2f} L"
    elif value >= 1_000:
        return f"₹{value / 1_000:.2f} K"
    else:
        return f"₹{value:.2f}"


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("🤖 RecoverAI")

    st.caption("AI Revenue Recovery Agent")

    st.divider()

    st.markdown("### 📌 About")

    st.write(
        "An AI-powered system that analyzes failed "
        "payments and recommends recovery actions."
    )

    st.divider()

    st.markdown("### 🧠 AI Pipeline")

    st.write("1. ML Prediction")
    st.write("2. Decision Engine")
    st.write("3. Llama 3.2 Agent")
    st.write("4. Recovery Tool")

    st.divider()

    st.markdown("### 📊 Dataset")

    st.write(
        f"Transactions: **{len(df):,}**"
    )


# -----------------------------
# Header
# -----------------------------

st.title("🤖 AI Revenue Recovery Agent")

st.write(
    "AI-powered system for analyzing and recovering failed payments."
)


# -----------------------------
# Business Metrics
# -----------------------------

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


st.divider()


# -----------------------------
# Transaction Selection
# -----------------------------

st.subheader("🔎 Analyze Failed Payment")

transaction_id = st.selectbox(
    "Select Transaction",
    df["transaction_id"].tolist()
)

transaction = df[
    df["transaction_id"] == transaction_id
].iloc[0]


# -----------------------------
# Transaction Information
# -----------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.write("**Transaction ID**")

    st.write(
        transaction["transaction_id"]
    )


with col2:

    st.write("**Amount**")

    st.write(
        f"₹{transaction['amount']:,.2f}"
    )


with col3:

    st.write("**Payment Method**")

    st.write(
        transaction["payment_method"]
    )


with col4:

    st.write("**Failure Reason**")

    st.write(
        transaction["failure_reason"]
    )


# -----------------------------
# AI Recovery Decision
# -----------------------------

st.subheader("🧠 AI Recovery Decision")

probability = float(
    transaction["recovery_probability"]
)

priority = transaction["priority"]

recommended_action = (
    transaction["recommended_action"]
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Recovery Probability",
        f"{probability:.2f}%"
    )


with col2:

    st.metric(
        "Priority",
        priority
    )


with col3:

    st.metric(
        "Recommended Action",
        recommended_action
    )


# -----------------------------
# AI Agent
# -----------------------------

if st.button("🤖 Ask AI Recovery Agent"):

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
        "AI Agent is analyzing the payment..."
    ):

        try:

            ai_response = ask_recovery_agent(
                agent_context
            )

            st.success(
                "AI analysis completed."
            )

            st.markdown(
                "### 🤖 AI Agent Response"
            )

            st.write(
                ai_response
            )

        except Exception as e:

            st.error(
                f"AI Agent Error: {e}"
            )


# -----------------------------
# Recovery Action
# -----------------------------

st.divider()

st.subheader("⚡ Recovery Action")


# -----------------------------
# Initialize Action Log
# -----------------------------

if "action_log" not in st.session_state:

    st.session_state.action_log = []


# -----------------------------
# Execute Recovery Action
# -----------------------------

if st.button(
    f"Execute: {recommended_action}"
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


    # -----------------------------
    # Save Action Log Permanently
    # -----------------------------

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

    st.json(
        result
    )


# -----------------------------
# Recovery Overview
# -----------------------------

st.divider()

st.subheader("📊 Recovery Overview")


col1, col2 = st.columns(2)


# -----------------------------
# Priority Distribution
# -----------------------------

with col1:

    st.write("**Recovery Priority Distribution**")

    priority_counts = (
        df["priority"]
        .value_counts()
        .reindex(["High", "Medium", "Low"])
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


# -----------------------------
# Recovery Actions
# -----------------------------

with col2:

    st.write("**Recommended Recovery Actions**")

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

# -----------------------------
# Action Log
# -----------------------------

if st.session_state.action_log:

    st.divider()

    st.subheader(
        "📋 Recovery Action Log"
    )

    action_log_df = pd.DataFrame(
        st.session_state.action_log
    )

    st.dataframe(
        action_log_df,
        width="stretch"
    )