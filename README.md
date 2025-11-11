# 💰 RupeeLogic - Financial Advisory Expert System for Sri Lankans

**A rule-based expert system, that provides personalized investment portfolio advice for Sri Lankans**

> “Empowering Sri Lankans with personalized investment advice”

---

## ✨ System Architecture

- **Knowledge Base:** Stores all investment options, rules from financial experts, and Sri Lankan market data.​

- **Inference Engine:** Takes your financial information and applies investment rules to figure out the best portfolios for you.​

- **User Interface:** Lets you enter your details through a form and chat naturally to get personalized investment advice.


## ✨ System Features

- **Operates in Narrow Domain:** Specializes only in Sri Lankan personal investment and portfolio management​

- **Dominates in Asking Questions:** Actively asks clarifying questions about income, goals, risk tolerance, and time horizon​

- **Processes Incomplete Information:** Makes reasonable assumptions, ignores irrelevant data, or prompts users for missing details​

- **Provides Alternative Solutions:** Offers multiple portfolio options (Conservative, Moderate, Aggressive) based on user profile​

- **Gives a Level of Assurance:** Shows confidence level (certainty/uncertainty) for each recommendation based on data completeness​

- **Provides Recommendations Over Exact Answers:** Categorizes advice for different investor types (Beginner-friendly FDs, Intermediate Unit Trusts, Advanced CSE Stocks)​

- **Explainability:** Shows which investment rules were fired and reasoning behind portfolio allocation decisions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for chat mode only)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/roshana1s/RupeeLogic.git
cd RupeeLogic
```

2. **Install dependencies**
```bash
pip install -r requirements.txt --no-deps
```
> **Note**: The `--no-deps` flag is used to avoid dependency conflicts. All required packages are specified in `requirements.txt`.

3. **Set up environment variables** (Optional - only for Chat Mode)
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

---

## 🎯 How to Run

### Start the Application

Run the Streamlit application on port 8000:

```bash
streamlit run app/main.py --server.port 8000
```

The application will open in your default browser at: **http://localhost:8000**

### Using the Application

#### **Form Mode** (No API key required)
1. Select "Form Mode" from the sidebar
2. Fill in your financial information:
   - Age, income, expenses, savings
   - Investment goals and timeline
   - Risk tolerance level
   - Leave fields empty to use default assumptions
3. Click "🚀 Generate My Investment Portfolio"
4. Review your personalized recommendations

#### **Chat Mode** (Requires OpenAI API key)
1. Set up your OpenAI API key in `.env` file
2. Select "Chat Mode" from the sidebar
3. Have a natural conversation about your finances
4. The AI assistant will guide you through the process
5. Generate recommendations directly from the chat

---

## 📁 Project Structure

```
RupeeLogic/
├── app/
│   ├── data/
│   │   └── knowledge_base.json      # Asset class definitions
│   ├── es/
│   │   └── RupeeLogicEngine.py      # Expert system rules & engine
│   ├── main.py                      # Main application entry
│   ├── form.py                      # Form mode interface
│   └── chat.py                      # Chat mode interface
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

---

## 🛠️ Technologies Used

- **Streamlit** - Web application framework
- **Experta** - Expert system / rule-based AI engine
- **OpenAI GPT-4o-mini** - Natural language processing (chat mode)
- **Plotly** - Interactive data visualizations
- **Pandas** - Data manipulation and analysis
- **Python 3.8+** - Core programming language

---

## 📊 Investment Rules Coverage

The expert system includes 23+ rules covering:

- ✅ Emergency fund prioritization
- ✅ High-interest debt payoff strategies
- ✅ Budget crisis management
- ✅ Short-term goals (< 3 years)
- ✅ Retirement planning (age-based)
- ✅ Aggressive growth portfolios
- ✅ Balanced/moderate allocations
- ✅ Conservative portfolios
- ✅ Goal-based planning (education, home purchase, etc.)
- ✅ Special scenarios (high net worth, beginners, FIRE, etc.)

---