import streamlit as st
import pandas as pd
import sqlite3
from main import get_data_from_database

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

# Database Connection
conn = sqlite3.connect("amazon.db")

# Sidebar
page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "🤖 AI Assistant"]
)

# ==================================
# DASHBOARD PAGE
# ==================================
if page == "📊 Dashboard":

    st.title("📊 Sales Analytics Dashboard")

    # KPI SECTION
    total_sales = pd.read_sql(
        "SELECT SUM(total_amount) AS total_sales FROM orders",
        conn
    )

    total_orders = pd.read_sql(
        "SELECT COUNT(*) AS total_orders FROM orders",
        conn
    )

    total_products = pd.read_sql(
        "SELECT COUNT(*) AS total_products FROM products",
        conn
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Total Sales",
            round(float(total_sales.iloc[0, 0]), 2)
        )

    with col2:
        st.metric(
            "📦 Total Orders",
            int(total_orders.iloc[0, 0])
        )

    with col3:
        st.metric(
            "🛍 Total Products",
            int(total_products.iloc[0, 0])
        )

    st.divider()

    # SALES BY PRODUCT
    st.subheader("📈 Product Sales")

    sales_product = pd.read_sql("""
    SELECT
        p.name,
        SUM(oi.quantity) AS quantity
    FROM products p
    JOIN order_items oi
    ON p.product_id = oi.product_id
    GROUP BY p.name
    ORDER BY quantity DESC
    """, conn)

    st.bar_chart(
        sales_product.set_index("name")
    )

    st.divider()

    # PRODUCT TABLE
    st.subheader("📋 Product Performance")

    st.dataframe(
        sales_product,
        use_container_width=True
    )

    st.divider()

    # TOP PRODUCTS
    st.subheader("🏆 Top Selling Products")

    st.dataframe(
        sales_product.head(5),
        use_container_width=True
    )

# ==================================
# AI ASSISTANT PAGE
# ==================================
else:

    st.title("🤖 AI Data Analyst")

    question = st.text_input(
        "Ask a question about your database",
        placeholder="Example: Show total sales, top products, average order value..."
    )

    if st.button("Analyze", use_container_width=True):

        if question.strip():

            try:

                sql_query, results = get_data_from_database(question)

                st.success("Query Executed Successfully")

                st.subheader("Generated SQL")

                st.code(
                    sql_query,
                    language="sql"
                )

                st.subheader("Results")

                if results:

                    if len(results) == 1 and len(results[0]) == 1:

                        st.metric(
                            "Result",
                            results[0][0]
                        )

                    else:

                        df = pd.DataFrame(results)

                        st.dataframe(
                            df,
                            use_container_width=True
                        )

                        try:

                            if len(df.columns) >= 2:

                                st.subheader("Visualization")

                                chart_df = df.copy()

                                chart_df.columns = [
                                    f"Column_{i}"
                                    for i in range(len(chart_df.columns))
                                ]

                                st.bar_chart(
                                    chart_df.set_index(
                                        chart_df.columns[0]
                                    )
                                )

                        except:
                            pass

                else:
                    st.warning("No data found")

            except Exception as e:
                st.error(str(e))

conn.close()