import streamlit as st

# Configure the page
st.set_page_config(
    page_title="RupeeLogic - Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for color scheme
st.markdown(
    """
<style>
    /* Main colors: #7339AB, #625AD8, #1F9CE4, #88F4FF */
    
    /* Headers and titles - only h1 gets the cyan color */
    h1 {
        color: #88F4FF !important;
    }
    
    h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* All regular text white */
    p, span, div, label {
        color: #ffffff !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1a1f2e !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    /* Main container */
    .main .block-container {
        background-color: rgba(31, 156, 228, 0.05);
        border-radius: 10px;
        padding: 2rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #625AD8 0%, #1F9CE4 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #7339AB 0%, #625AD8 100%);
        box-shadow: 0 4px 12px rgba(115, 57, 171, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 2px solid #625AD8;
        border-radius: 8px;
        color: #88F4FF;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #1F9CE4;
        box-shadow: 0 0 0 2px rgba(31, 156, 228, 0.2);
    }
    
    /* Success/Info boxes */
    .stSuccess {
        background-color: rgba(136, 244, 255, 0.1);
        border-left: 4px solid #88F4FF;
    }
    
    .stInfo {
        background-color: rgba(98, 90, 216, 0.1);
        border-left: 4px solid #625AD8;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(115, 57, 171, 0.2);
        border-radius: 8px;
        color: #88F4FF !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #88F4FF !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: rgba(98, 90, 216, 0.1);
        border-left: 3px solid #625AD8;
        border-radius: 8px;
    }
    
    /* Chat message text */
    .stChatMessage p,
    .stChatMessage div,
    .stChatMessage span,
    .stChatMessage li {
        color: #ffffff !important;
    }
    
    /* Links */
    a {
        color: #88F4FF !important;
    }
    
    a:hover {
        color: #1F9CE4 !important;
    }
    
    /* Radio buttons and checkboxes */
    .stRadio > label, .stCheckbox > label {
        color: #88F4FF !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(98, 90, 216, 0.2);
        border-radius: 8px 8px 0 0;
        color: #88F4FF;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #7339AB 0%, #625AD8 100%);
        color: white !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Define pages
form_page = st.Page("form.py", title="Form Mode", icon="📝", default=True)
chat_page = st.Page("chat.py", title="Chat Mode", icon="💬")

# Create navigation
pg = st.navigation([form_page, chat_page])

# Add header
st.sidebar.title("💰 RupeeLogic")
st.sidebar.markdown("**Expert Investment Portfolio Advisor for Sri Lanka**")
st.sidebar.markdown("---")

# Add description in sidebar
st.sidebar.markdown(
    """
### Choose Your Mode:

**📝 Form Mode**  
Fill out a structured form with your financial details and get instant recommendations.

**💬 Chat Mode**  
Have a natural conversation about your finances. The AI assistant will guide you and generate personalized recommendations.

---

### Features:
- 23 expert investment rules
- 15+ Sri Lankan asset classes
- Real investment products
- Explainable AI recommendations
- Specific LKR amount suggestions
"""
)

# Run the selected page
pg.run()
