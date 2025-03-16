import streamlit as st
import sqlite3

# Database Setup
def init_db(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS lost_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_name TEXT,
        item_desc TEXT,
        last_seen_location TEXT,
        status TEXT DEFAULT "Lost"
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS found_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        finder_name TEXT,
        item_desc TEXT,
        contact_info TEXT
    )''')
    conn.commit()

def get_conn():
    return sqlite3.connect('recoverease.db', timeout=10)

# User Functions
def register_user(username, password, is_admin=0):
    conn = get_conn()
    try:
        conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, password, is_admin))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # User already exists
    finally:
        conn.close()

def check_user(username, password):
    conn = get_conn()
    user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
    conn.close()
    return user

# Lost & Found Item Functions
def report_lost_item(owner_name, item_desc, last_seen_location):
    conn = get_conn()
    conn.execute('INSERT INTO lost_items (owner_name, item_desc, last_seen_location) VALUES (?, ?, ?)',
                 (owner_name, item_desc, last_seen_location))
    conn.commit()
    conn.close()

def report_found_item(finder_name, item_desc, contact_info):
    conn = get_conn()
    conn.execute('INSERT INTO found_items (finder_name, item_desc, contact_info) VALUES (?, ?, ?)',
                 (finder_name, item_desc, contact_info))
    conn.commit()
    conn.close()

def fetch_lost_items():
    conn = get_conn()
    items = conn.execute('SELECT * FROM lost_items').fetchall()
    conn.close()
    return items

def fetch_found_items():
    conn = get_conn()
    items = conn.execute('SELECT * FROM found_items').fetchall()
    conn.close()
    return items

# Delete Items from Database
def delete_lost_item(item_id):
    conn = get_conn()
    conn.execute('DELETE FROM lost_items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()

def delete_found_item(item_id):
    conn = get_conn()
    conn.execute('DELETE FROM found_items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()

# Add Custom CSS for Styling
def add_custom_css():
    st.markdown("""
        <style>
            body {
                background-color: #eaf4ff;
                font-family: Arial, sans-serif;
            }
            .main {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .navbar {
                background-color: black;
                padding: 10px;
                text-align: center;
            }
            .navbar a {
                color: white;
                text-decoration: none;
                margin: 0 15px;
                font-weight: bold;
            }
            .navbar a:hover {
                color: #00bfff;
            }
            .stButton button {
                background-color: #007bff !important;
                color: white !important;
                border-radius: 5px !important;
                border: none !important;
            }
            .stButton button:hover {
                background-color: #0056b3 !important;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #007bff;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# Navbar Function
def navbar():
    st.markdown("""
        <div class="navbar">
            <a href="/">HOME</a>
            <a href="/report-lost">REPORT LOST ITEM</a>
            <a href="/report-found">REPORT FOUND ITEM</a>
            <a href="/admin">ADMIN PANEL</a>
            <a href="/logout">LOGOUT</a>
        </div>
        """, unsafe_allow_html=True)

# Streamlit App Pages
def main():
    add_custom_css()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["username"] = ""

    menu = ["Home", "Login", "Register", "Report Lost", "Report Found", "Admin", "Logout"]
    
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        navbar()
        home_page()    
        
    elif choice == "Login":
        navbar()
        login_page()

    elif choice == "Register":
        navbar()
        register_page()

# Page Definitions

### Home Page ###
def home_page():
   pass

