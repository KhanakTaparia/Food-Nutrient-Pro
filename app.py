import streamlit as st
import pandas as pd
from datetime import date
import sqlite3

from auth_config import authenticator

st.set_page_config(page_title="Nutrition Pro Secure", layout="wide")

# ---------- LOGIN ----------
name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("Invalid login")

if auth_status is None:
    st.warning("Please login")
    st.stop()

if auth_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Welcome {name}")
    # ---------- DB ----------
    conn = sqlite3.connect("nutrition.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        user TEXT,
        date TEXT,
        food TEXT,
        grams REAL,
        calories REAL,
        protein REAL,
        carbs REAL,
        fat REAL
    )
    """)
    conn.commit()

    def add_meal(data):
        c.execute("INSERT INTO meals VALUES (?,?,?,?,?,?,?,?)", data)
        conn.commit()

    def get_user_meals(user):
        return c.execute("SELECT * FROM meals WHERE user=?", (user,)).fetchall()

    # ---------- DATA ----------
    df = pd.read_csv("data/foods.csv")

    # ---------- FUNCTION ----------
    def scale(row, grams):
        f = grams / 100
        return {
            "calories": row["calories"] * f,
            "protein": row["protein"] * f,
            "carbs": row["carbs"] * f,
            "fat": row["fat"] * f
        }

    # ---------- SIDEBAR ----------
    st.sidebar.header("🍽️ Add Meal")

    category = st.sidebar.selectbox("Category", df["category"].unique())
    filtered = df[df["category"] == category]

    search = st.sidebar.text_input("Search food 🔍")
    if search:
        filtered = filtered[filtered["food"].str.contains(search, case=False)]

    food = st.sidebar.selectbox("Food", filtered["food"])
    grams = st.sidebar.slider("Quantity (g)", 10, 500, 100)

    row = filtered[filtered["food"] == food].iloc[0]
    result = scale(row, grams)

    if st.sidebar.button("➕ Add Meal"):
        add_meal((
            username,
            str(date.today()),
            food,
            grams,
            result["calories"],
            result["protein"],
            result["carbs"],
            result["fat"]
        ))
        st.success("Meal added!")

    # ---------- LOAD USER DATA ----------
    rows = get_user_meals(username)

    df_user = pd.DataFrame(rows, columns=[
        "user","date","food","grams","calories","protein","carbs","fat"
    ])

    st.title(f"🥗 Nutrition Dashboard - {name}")

    # ---------- TODAY ----------
    today = df_user[df_user["date"] == str(date.today())]

    if not df_user.empty:

        totals = today[["calories","protein","carbs","fat"]].sum()

        # ---------- METRICS ----------
        st.subheader("📊 Today's Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Calories", round(totals["calories"],2))
        col2.metric("Protein", round(totals["protein"],2))
        col3.metric("Carbs", round(totals["carbs"],2))
        col4.metric("Fat", round(totals["fat"],2))

        # ---------- GOALS ----------
        st.subheader("🎯 Goals")

        cal_goal = st.number_input("Calories Goal", 1000, 5000, 2000)
        protein_goal = st.number_input("Protein Goal", 10, 300, 80)

        st.progress(min(totals["calories"]/cal_goal, 1.0))
        st.write(f"🔥 {round((totals['calories']/cal_goal)*100)}% of calorie goal")

        st.progress(min(totals["protein"]/protein_goal, 1.0))
        st.write(f"💪 {round((totals['protein']/protein_goal)*100)}% of protein goal")

        # ---------- CHARTS ----------
        st.subheader("📈 Analytics")

        st.bar_chart(totals)

        st.line_chart(df_user.groupby("date")["calories"].sum())

        # ---------- HISTORY ----------
        st.subheader("📜 Meal History")

        st.dataframe(df_user, use_container_width=True)

    else:
        st.info("Start adding meals to see your dashboard")