import streamlit as st
import pandas as pd
from ai_engine import generate_insights

st.set_page_config(
    page_title="AI Excel Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Excel Analyst")

uploaded_file = st.file_uploader(
    "Upload Excel or CSV File",
    type=["xlsx", "csv"]
)

if uploaded_file:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File Uploaded Successfully")

    # Preview
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # KPIs
    st.subheader("Business KPIs")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            len(df)
        )

    with col2:
        st.metric(
            "Columns",
            len(df.columns)
        )

    with col3:
        st.metric(
            "Missing Values",
            df.isnull().sum().sum()
        )

    st.divider()

    # Data Types
    st.subheader("Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str)
    })

    st.dataframe(info_df)

    st.divider()

    # Numeric Analysis
    numeric_cols = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_cols) > 0:

        st.subheader("Summary Statistics")

        st.dataframe(
            df[numeric_cols].describe()
        )

        selected_col = st.selectbox(
            "Select Column for Chart",
            numeric_cols
        )

        st.subheader("Distribution")

        st.bar_chart(
            df[selected_col]
        )

    st.divider()

    # Correlation
    if len(numeric_cols) > 1:

        st.subheader("Correlation Matrix")

        corr = df[numeric_cols].corr()

        st.dataframe(corr)

    st.divider()

    # AI Insights
    st.subheader("🤖 AI Insights")

    if st.button("Generate Insights"):

        with st.spinner("Analyzing Data..."):

            insights = generate_insights(df)

            st.markdown(insights)

    st.divider()

    # Natural Language Query
    st.subheader("Ask Questions About Data")

    user_question = st.text_input(
        "Example: Which column has highest average value?"
    )

    if st.button("Ask AI"):

        prompt = f"""
        Dataset Columns:
        {list(df.columns)}

        Dataset Sample:
        {df.head(10).to_string()}

        Question:
        {user_question}
        """

        from langchain_groq import ChatGroq

        llm = ChatGroq(
            groq_api_key="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",
            model_name="llama-3.3-70b-versatile"
        )

        answer = llm.invoke(prompt)

        st.markdown(answer.content)