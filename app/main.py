import streamlit as st

# Configure the page
st.set_page_config(
    page_title="RupeeLogic - Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
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
- 13 expert investment rules
- 15+ Sri Lankan asset classes
- Real investment products
- Explainable AI recommendations
- Specific LKR amount suggestions
"""
)

# Run the selected page
pg.run()
