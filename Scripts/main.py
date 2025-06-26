import streamlit as st
import pandas as pd
import mysql.connector
from datetime import date

st.set_page_config(page_title="Customer Management System", page_icon="https://cdn.pixabay.com/photo/2017/02/14/07/27/center-2064919_1280.jpg")
st.title("Customer Management System")

menu = st.sidebar.selectbox("Menu", ["Home", "User Login", "About"])

#DB connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mani@1704",
        database="Customer"
    )

if menu == "Home":
    st.subheader("Welcome to Customer Managment System")
    st.image("https://images.pexels.com/photos/8867482/pexels-photo-8867482.jpeg?cs=srgb&dl=pexels-yankrukov-8867482.jpg&fm=jpg")
    st.markdown("Manage customer records, interactions, and orders efficiently.")

elif menu == "About":
    st.info("This is an industry-level Customer Management System project built using Streamlit and MySQL.")

elif menu == "User Login":
    st.subheader("Login")

    if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['user_id'] = ""

    uid = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s AND user_pwd = %s", (uid, pwd))
        result = cursor.fetchone()
        if result:
            st.success("Login successful")
            st.session_state['login'] = True
            st.session_state['user_id'] = uid
        else:
            st.error("Invalid credentials")
        db.close()

    if st.session_state['login']:
        choice = st.selectbox("Actions", [
            "View Customers", "Add Customer", "Delete Customer",
            "View Orders", "Add Order", 
            "View Interactions", "Add Interaction"
        ])

        db = get_connection()
        cursor = db.cursor(dictionary=True)

        if choice == "View Customers":
            df = pd.read_sql("SELECT * FROM customers", db)
            st.dataframe(df)

        elif choice == "Add Customer":
            with st.form("add_cust"):
                cust_id = st.text_input("Customer ID")
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
                dob = st.date_input("Date of Birth")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                location = st.text_input("Location")
                reg_date = st.date_input("Registration Date", value=date.today())
                segment_id = st.text_input("Segment ID")
                submit = st.form_submit_button("Add Customer")
                if submit:
                    try:
                        cursor.execute("""
                            INSERT INTO customers 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (cust_id, full_name, email, phone, dob, gender, location, reg_date, segment_id))
                        db.commit()
                        st.success("Customer added successfully")
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif choice == "Delete Customer":
            cust_id = st.text_input("Customer ID to delete")
            if st.button("Delete"):
                cursor.execute("DELETE FROM customers WHERE cust_id = %s", (cust_id,))
                db.commit()
                st.warning("Customer deleted")

        elif choice == "View Orders":
            df = pd.read_sql("SELECT * FROM orders", db)
            st.dataframe(df)

        elif choice == "Add Order":
            with st.form("add_order"):
                order_id = st.text_input("Order ID")
                cust_id = st.text_input("Customer ID")
                order_date = st.date_input("Order Date", value=date.today())
                amount = st.number_input("Amount", min_value=0.0)
                status = st.selectbox("Status", ["Pending", "Shipped", "Delivered", "Cancelled"])
                submit = st.form_submit_button("Add Order")
                if submit:
                    cursor.execute("""
                        INSERT INTO orders 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (order_id, cust_id, order_date, amount, status))
                    db.commit()
                    st.success("Order added successfully")

        elif choice == "View Interactions":
            df = pd.read_sql("SELECT * FROM interactions", db)
            st.dataframe(df)

        elif choice == "Add Interaction":
            with st.form("add_interaction"):
                interaction_id = st.text_input("Interaction ID")
                cust_id = st.text_input("Customer ID")
                interaction_date = st.date_input("Date", value=date.today())
                channel = st.selectbox("Channel", ["Email", "Call", "Chat", "In-Person"])
                notes = st.text_area("Notes")
                submit = st.form_submit_button("Add Interaction")
                if submit:
                    cursor.execute("""
                        INSERT INTO interactions 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (interaction_id, cust_id, interaction_date, channel, notes))
                    db.commit()
                    st.success("Interaction added")

        db.close()
