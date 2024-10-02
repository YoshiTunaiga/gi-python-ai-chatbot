import streamlit as st

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['page'] = None

def login():
    st.set_page_config(
    page_title="Vite Care Management",
    page_icon=":hospital:",
    )

    st.write("# Welcome to Vite Care! 👋")

    st.sidebar.success("Select an option above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
            forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
            Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )
    if st.button("Log in"):
        st.session_state['logged_in'] = True
        st.session_state['page'] = "Dashboard"
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = None
        st.rerun()

# Pages for the app
login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# Constants
PAGES = ["Dashboard", "Reports", "Account"]

page = st.session_state['page']

dashboard = st.Page(
    "pages/Dashboard.py",
    title="Dashboard", 
    icon=":material/dashboard:", 
    default=(page=="Dashboard")
)

# Navigation bar for the app
if st.session_state['logged_in']:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()