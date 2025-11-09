# RupeeLogic 💰

**Expert Investment Portfolio Advisor for Sri Lanka**

RupeeLogic is an expert system that provides personalized investment portfolio recommendations for Sri Lankan investors based on their financial profile, goals, risk tolerance, and investment timeline.

---

## 🎯 Features

- **Two Interaction Modes**:
  - **📝 Form Mode**: Traditional structured form for quick input
  - **💬 Chat Mode**: AI-powered conversational interface using GPT-4o-mini
- **Intelligent Rule-Based System**: Uses 13 expert investment rules based on established financial planning principles
- **Sri Lankan Market Focus**: All recommendations use real investment products available in Sri Lanka
- **Comprehensive Asset Classes**: Covers 15+ investment options from savings accounts to CSE stocks
- **User-Friendly Interface**: Clean Streamlit interface with visual portfolio allocation
- **Explainable AI**: Clear explanations of reasoning behind each recommendation with references
- **Goal-Based Planning**: Tailored recommendations for retirement, education, home purchase, and wealth building
- **Specific LKR Amounts**: Shows exactly how much to invest from savings and monthly income

---

## 📁 Project Structure

```
RupeeLogic/
│
├── app/
│   ├── es.py                    # Expert system rules and knowledge engine
│   ├── main.py                  # Streamlit user interface
│   └── knowledge_base.json      # Investment asset classes knowledge base
│
```
RupeeLogic/
│
├── app/
│   ├── es.py                    # Expert system rules and knowledge engine
│   ├── form.py                  # Form-based user interface (Streamlit)
│   ├── chat.py                  # Chat-based AI interface with GPT-4o-mini
│   └── knowledge_base.json      # Investment asset classes knowledge base
│
├── home.py                      # Main entry point with page navigation
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (API keys)
└── README.md                    # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (for Chat Mode)

### Installation Steps

1. **Clone or download the repository**
   ```bash
   cd RupeeLogic
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Get your API key from: https://platform.openai.com/api-keys

4. **Run the application**
   ```bash
   streamlit run home.py
   ```

5. **Access the application**
   - The application will open in your default web browser
   - Default URL: `http://localhost:8501`

---

## 💼 Investment Asset Classes Covered

### 1. **Savings Account**
- **Risk**: Very Low
- **Returns**: 2-4% p.a.
- **Examples**: Commercial Bank Savings Plus, HNB Salary Saver, Sampath Savari, NSB Savari, People's Bank Sahana
- **Source**: Bank websites (2024)

### 2. **Fixed Deposits (FDs)**
- **Risk**: Very Low
- **Returns**: 8-12% p.a.
- **Examples**: Commercial Bank, HNB, Sampath Bank, NDB, BOC Fixed Deposits
- **Source**: Central Bank of Sri Lanka (CBSL) interest rate data, bank websites

### 3. **Treasury Bills (T-Bills)**
- **Risk**: Very Low (Government backed)
- **Returns**: 9-13% p.a.
- **Examples**: 91, 182, 364-day bills via CBSL auctions
- **Source**: Central Bank of Sri Lanka auction results

### 4. **Government Bonds (Treasury Bonds)**
- **Risk**: Very Low (Sovereign guarantee)
- **Returns**: 10-14% p.a.
- **Examples**: Sri Lanka Development Bonds
- **Source**: Central Bank of Sri Lanka, EPF investment reports

### 5. **Corporate Debentures**
- **Risk**: Low to Medium
- **Returns**: 11-15% p.a.
- **Examples**: DFCC Bank, Commercial Bank, John Keells Holdings, Hayleys, Dialog Axiata
- **Source**: Colombo Stock Exchange (CSE) corporate announcements

### 6. **Money Market Unit Trusts**
- **Risk**: Very Low
- **Returns**: 6-9% p.a.
- **Examples**: NDB Wealth Money Plus Fund, CAL Money Market Fund, Acuity Money Market Fund
- **Source**: Unit Trust Association of Sri Lanka (UTASL)

### 7. **Income/Bond Unit Trusts**
- **Risk**: Low
- **Returns**: 8-12% p.a.
- **Examples**: NDB Wealth Gilt Edge Fund, CAL Income Fund, Softlogic Gilt Edge Fund
- **Source**: Unit Trust Association of Sri Lanka, fund fact sheets

### 8. **Balanced Unit Trusts**
- **Risk**: Medium
- **Returns**: 10-18% p.a.
- **Examples**: NDB Wealth Balanced Fund, CAL Growth & Income Fund, Softlogic Balanced Fund
- **Source**: UTASL, individual fund performance reports

### 9. **Equity Unit Trusts**
- **Risk**: High
- **Returns**: 12-25% p.a.
- **Examples**: NDB Wealth Eagle Fund, CAL Equity Fund, JB Vantage Equity Fund
- **Source**: UTASL performance data, fund managers' reports

### 10. **CSE Blue Chip Stocks**
- **Risk**: High
- **Returns**: 15-30% p.a.
- **Examples**: John Keells Holdings (JKH), Commercial Bank (COMB), Hayleys (HAYL), Dialog Axiata (DIAL), LOLC Holdings, Sampath Bank, Tokyo Cement
- **Source**: Colombo Stock Exchange historical data, company reports

### 11. **CSE Growth Stocks**
- **Risk**: Very High
- **Returns**: 20-50% p.a.
- **Examples**: Bairaha Farms, Royal Ceramics, Access Engineering, Sunshine Holdings
- **Source**: Colombo Stock Exchange market data

### 12. **Exchange Traded Funds (ETFs)**
- **Risk**: Medium to High
- **Returns**: 10-20% p.a.
- **Examples**: S&P SL20 ETF (tracks top 20 CSE companies)
- **Source**: Colombo Stock Exchange ETF information

### 13. **Real Estate Investment**
- **Risk**: Medium
- **Returns**: 8-15% p.a.
- **Examples**: Residential/commercial properties in Colombo, Kandy, Galle
- **Source**: Real estate market analysis, property indices

### 14. **Gold Investment**
- **Risk**: Medium
- **Returns**: 5-12% p.a.
- **Examples**: Physical gold, Ceylinco Gold Saver, Commercial Bank Gold Saver, HNB Gold Savings
- **Source**: Bank gold savings programs, market data

### 15. **EPF/ETF Contributions**
- **Risk**: Very Low
- **Returns**: 9-13% p.a.
- **Examples**: Employees' Provident Fund (EPF), Employees' Trust Fund (ETF)
- **Source**: Central Bank EPF annual reports

---

## 🧠 Expert System Rules & References

### Rule 1: Emergency Fund Priority (Salience: 100)
**Trigger Condition**: Current savings < 6 months of monthly expenses
- **Investment Principle**: Financial Planning Standards - Every household should maintain 6 months of expenses in liquid savings
- **Source**: "The Total Money Makeover" by Dave Ramsey, Sri Lanka Financial Planning guidelines
- **Academic Reference**: Financial Planning Association (FPA) emergency fund recommendations
- **Allocation**: 50% Savings Account + 50% Money Market Funds
- **Rationale**: Before any investment, ensure financial security through emergency fund
- **Sri Lankan Context**: Given economic volatility, emergency fund is critical

### Rule 2: Debt Payoff Priority (Salience: 95)
**Trigger Condition**: Has high-interest debt (Credit Cards > 15% p.a.)
- **Investment Principle**: No investment consistently beats credit card interest rates
- **Source**: Central Bank of Sri Lanka Financial Reports
- **Data**: Sri Lankan credit card APR: 24-36% annually
- **Academic Reference**: "The Millionaire Next Door" by Thomas Stanley - debt-free foundation
- **Allocation**: 100% debt payment before any investments
- **Mathematical Rationale**: Paying 30% credit card debt = guaranteed 30% return (better than any investment)

### Rule 3: Short-Term Goal (< 3 years) (Salience: 80)
**Trigger Condition**: Time horizon less than 3 years
- **Investment Principle**: Capital preservation for short-term goals - volatility risk too high
- **Source**: Modern Portfolio Theory - investment horizon vs. asset allocation
- **Academic Reference**: "A Random Walk Down Wall Street" by Burton Malkiel
- **Data**: Average FD rates in Sri Lanka: 9-11% p.a. (Commercial Bank, HNB, Sampath)
- **Allocation**: 70% Fixed Deposits + 30% Treasury Bills
- **Rationale**: No equity exposure - need guaranteed returns for short timeline

### Rule 4: Near Retirement Conservative (Age 55+) (Salience: 75)
**Trigger Condition**: Age ≥ 55 years AND Goal = Retirement
- **Investment Principle**: Age-based asset allocation - Equity % = 100 - Age (Conservative: 80 - Age)
- **Source**: John Bogle's age-based allocation formula
- **Academic Reference**: "The Intelligent Investor" by Benjamin Graham - defensive investor profile
- **Data**: Sri Lanka Development Bonds: 11-13% p.a. returns
- **Allocation**: 40% FDs + 30% Government Bonds + 20% Income Funds + 10% Blue Chip Stocks
- **Rationale**: Preserve capital, generate income, minimal equity for inflation protection

### Rule 5: Aggressive Growth Portfolio (Salience: 70)
**Trigger Condition**: Age < 35 AND Risk Tolerance = High AND Time Horizon ≥ 10 years
- **Investment Principle**: Young investors can tolerate volatility - time to recover from market downturns
- **Source**: Modern Portfolio Theory - risk tolerance vs. investment horizon
- **Academic Reference**: Jeremy Siegel's "Stocks for the Long Run"
- **Data**: CSE blue chips average return: 18-25% p.a. over 10+ years
- **Allocation**: 75% equities (35% Equity Funds + 25% Blue Chips + 15% Growth Stocks) + 25% balanced/income
- **Expected Return**: 18-25% p.a. with high volatility
- **Rationale**: Maximum growth potential with time to weather market cycles

### Rule 6: Growth-Oriented Portfolio (Salience: 65)
**Trigger Condition**: Age < 40 AND Risk Tolerance = High AND Time Horizon ≥ 7 years
- **Investment Principle**: Equity-focused with moderate stability
- **Source**: 70-30 growth allocation principle
- **Data**: Equity unit trusts historical performance: 15-20% p.a.
- **Allocation**: 70% equities + 30% bonds/income funds
- **Expected Return**: 15-20% p.a.

### Rule 7: Moderate Balanced Portfolio (Salience: 60)
**Trigger Condition**: Risk Tolerance = Moderate AND Time Horizon ≥ 5 years
- **Investment Principle**: 60-40 rule (60% equity, 40% bonds) for moderate investors
- **Source**: Traditional balanced portfolio allocation - Vanguard research
- **Academic Reference**: "The Intelligent Asset Allocator" by William Bernstein
- **Data**: NDB Wealth Balanced, CAL Growth & Income - 12-15% returns
- **Allocation**: 60% growth assets (40% Balanced + 20% Equity + 10% Blue Chips) + 40% fixed income
- **Expected Return**: 12-15% p.a.
- **Rationale**: Balance growth and stability for medium-term wealth building

### Rule 8: Middle-Age Moderate Investor (Salience: 55)
**Trigger Condition**: Age 35-50 AND Risk Tolerance = Moderate
- **Investment Principle**: Balanced portfolio for mid-career professionals building wealth
- **Source**: Life-cycle investing - target-date fund principles
- **Data**: 15-20 years to retirement allows equity volatility
- **Allocation**: 60% balanced/equity funds + 40% bonds
- **Rationale**: Still time for growth, but increasing stability needs

### Rule 9: Conservative Portfolio (Salience: 50)
**Trigger Condition**: Risk Tolerance = Low
- **Investment Principle**: Capital preservation with minimal risk
- **Source**: Benjamin Graham's defensive investor strategy
- **Academic Reference**: "The Intelligent Investor" - margin of safety principle
- **Data**: FD rates: 9-11% p.a. across major banks (Commercial, HNB, Sampath)
- **Allocation**: 80% fixed income (40% FDs + 30% Bonds + 20% Income Funds) + 20% balanced funds
- **Expected Return**: 9-12% p.a. with minimal volatility
- **Rationale**: Prioritize safety over growth

### Rule 10: Pre-Retirement Conservative (Salience: 52)
**Trigger Condition**: Age ≥ 50 AND Risk Tolerance = Low
- **Investment Principle**: Focus on capital preservation and income generation
- **Source**: Retirement income planning principles
- **Data**: Government bonds: 11-13% p.a. with sovereign backing
- **Allocation**: 85% fixed income + 15% balanced/blue chips
- **Rationale**: Retirement approaching - cannot afford major losses

### Rule 11: Education Planning (Salience: 58)
**Trigger Condition**: Goal = Child Education AND Time Horizon 5-10 years
- **Investment Principle**: Beat education inflation while preserving capital
- **Source**: Education inflation data - Private schools/universities in Sri Lanka
- **Data**: Education costs in Sri Lanka rising 8-10% annually
- **Examples**: International school fees, private university costs increasing significantly
- **Allocation**: 65% balanced/equity funds + 35% fixed income
- **Rationale**: Need growth to beat 8-10% education inflation, but can't risk all capital

### Rule 12: Home Purchase Planning (Salience: 57)
**Trigger Condition**: Goal = Home Purchase AND Time Horizon 3-7 years
- **Investment Principle**: Down payment requires capital preservation
- **Source**: Real estate planning - guaranteed capital for property down payment
- **Data**: FDs 9-11% p.a., Balanced funds 12-15% growth potential
- **Allocation**: 60% fixed income (40% FDs + 20% Income Funds) + 40% balanced/equity
- **Rationale**: Cannot risk market volatility when property opportunity arises

### Rule 13: Default Balanced Recommendation (Salience: -10)
**Trigger Condition**: No other specific rules matched
- **Investment Principle**: Safe fallback - balanced approach suitable for most investors
- **Source**: Generic balanced allocation for unknown profiles
- **Allocation**: 60% Balanced Funds + 30% Income Funds + 10% Money Market
- **Rationale**: Conservative default when profile doesn't match specific strategies

---

## 📚 Academic & Professional References

### Investment Books Referenced
1. **"The Intelligent Investor"** by Benjamin Graham
   - Defensive vs. Enterprising investor profiles
   - Margin of safety principle
   - Value investing fundamentals

2. **"A Random Walk Down Wall Street"** by Burton Malkiel
   - Efficient Market Hypothesis
   - Index fund investing
   - Asset allocation strategies

3. **"Stocks for the Long Run"** by Jeremy Siegel
   - Long-term equity performance data
   - Risk-return tradeoffs over time
   - Historical market analysis

4. **"The Total Money Makeover"** by Dave Ramsey
   - Emergency fund principles
   - Debt elimination strategies
   - Baby steps to financial freedom

5. **"The Millionaire Next Door"** by Thomas Stanley
   - Wealth accumulation patterns
   - Debt-free living importance
   - Frugality and investment

6. **"The Intelligent Asset Allocator"** by William Bernstein
   - Modern Portfolio Theory applications
   - Rebalancing strategies
   - Risk management

### Financial Planning Standards
1. **Certified Financial Planner (CFP) Guidelines**
   - Emergency fund: 3-6 months expenses (Sri Lanka: 6 months recommended)
   - Age-based asset allocation formulas
   - Risk profiling methodologies

2. **Financial Planning Association (FPA)**
   - Best practices in financial planning
   - Client risk assessment
   - Goal-based planning approaches

3. **Modern Portfolio Theory (MPT)** - Harry Markowitz
   - Diversification benefits
   - Risk-return optimization
   - Efficient frontier concepts

### Sri Lankan Financial Data Sources
1. **Central Bank of Sri Lanka (CBSL)**
   - Interest rate statistics
   - T-Bill/T-Bond auction results
   - EPF/ETF performance data
   - Banking sector reports
   - Credit card APR data (24-36%)

2. **Colombo Stock Exchange (CSE)**
   - Historical returns data
   - Company financials
   - Market indices (ASPI, S&P SL20)

3. **Unit Trust Association of Sri Lanka (UTASL)**
   - Unit trust performance data
   - Fund fact sheets
   - Industry statistics

4. **Insurance Board of Sri Lanka (IBSL)**
   - Investment-linked insurance products
   - Regulatory guidelines

---

## 💡 Investment Principles Applied
**Principle**: Build 6-month emergency fund before aggressive investing
- **Source**: Standard financial planning practice
- **Reference**: "The Total Money Makeover" by Dave Ramsey, CFP Board guidelines
- **Sri Lankan Context**: 6 months expenses in liquid assets (savings + money market funds)

### Rule 2: High-Interest Debt Payoff
**Principle**: Pay off debt with interest >15% p.a. before investing
- **Source**: Credit card interest rates in Sri Lanka
- **Reference**: Central Bank of Sri Lanka Banking Statistics (Credit card APR: 24-36%)
- **Rationale**: Investment returns rarely beat credit card interest rates

### Rule 3: Short-Term Goals (< 3 years)
**Principle**: Capital preservation for short-term goals
- **Source**: Investment horizon principle - Bodie, Kane, Marcus "Investments"
- **Allocation**: 100% fixed income (FDs + T-Bills)
- **Rationale**: Cannot risk market volatility for near-term needs

### Rule 4: Retirement Planning (Age-Based)
**Principle**: Equity allocation = 100 - Age (Conservative Sri Lankan: 80 - Age)
- **Source**: Traditional age-based allocation rule
- **Reference**: Benjamin Graham "The Intelligent Investor"
- **Sri Lankan Adaptation**: More conservative given market volatility

### Rule 5: Aggressive Growth Portfolio
**Criteria**: Age < 35 + High Risk + 10+ year horizon
- **Source**: Modern Portfolio Theory (Markowitz)
- **Allocation**: 70%+ equity (stocks + equity funds)
- **Expected Return**: 18-25% p.a.
- **Reference**: CSE historical returns (10-year average)

### Rule 6: Growth-Oriented Portfolio
**Criteria**: Age < 40 + High Risk + 7+ year horizon
- **Allocation**: 60% equity, 40% fixed income
- **Expected Return**: 15-20% p.a.

### Rule 7: Moderate/Balanced Portfolio
**Principle**: 60-40 rule (60% equity, 40% bonds)
- **Source**: Traditional balanced allocation
- **Reference**: "A Random Walk Down Wall Street" by Burton Malkiel
- **Allocation**: Balanced and income unit trusts
- **Expected Return**: 12-15% p.a.

### Rule 8: Middle-Age Moderate Investor
**Criteria**: Age 35-50 + Moderate risk
- **Rationale**: Building wealth while managing family responsibilities
- **Allocation**: 60% equity, 40% fixed income

### Rule 9: Conservative Portfolio
**Principle**: Capital preservation focus
- **Criteria**: Low risk tolerance
- **Allocation**: 70-80% fixed income, 10-20% equity
- **Expected Return**: 9-12% p.a.

### Rule 10: Pre-Retirement Conservative
**Criteria**: Age 50+ + Low risk
- **Allocation**: 85% fixed income, 15% balanced/equity
- **Focus**: Income generation and capital preservation

### Rule 11: Education Planning
**Goal**: Child's education (5-10 years)
- **Context**: Education costs rising 8-10% annually in Sri Lanka
- **Source**: Private school/university fee increases
- **Allocation**: 65% equity, 35% fixed income
- **Need**: Beat education inflation while preserving capital

### Rule 12: Home Purchase Planning
**Goal**: Property down payment (3-7 years)
- **Allocation**: 60% fixed income, 30% balanced, 10% money market
- **Rationale**: Cannot risk market volatility for guaranteed down payment needs

### Rule 13: Default Moderate Portfolio
**Purpose**: Fallback when no specific conditions met
- **Allocation**: 60% balanced, 30% income, 10% money market
- **Rationale**: Safe default suitable for most investors

---

## 🏦 Investment Product Providers in Sri Lanka

### Unit Trust Companies
1. **NDB Wealth** - https://www.ndbwealth.com/
   - Money Plus Fund, Gilt Edge Fund, Balanced Fund, Eagle Equity Fund
   
2. **CAL (Colombo Trust Finance PLC)** - https://www.cal.lk/
   - Money Market Fund, Income Fund, Growth & Income Fund, Equity Fund

3. **Softlogic Stockbrokers** - https://www.softlogicstockbrokers.com/
   - Gilt Edge Fund, Balanced Fund, Equity Fund

4. **Guardian Acuity Asset Management** - https://www.gaam.lk/
   - Money Market Fund, Income Fund, Balanced Income Fund, Equity Fund

5. **JB Vantage** - Unit trust products

6. **DCSL (Dimuthu Capital Services)** - Balanced and Equity Funds

**Source**: Unit Trust Association of Sri Lanka (UTASL) - https://www.utasl.lk/

### Major Banks (FDs, Savings, Gold)
1. **Commercial Bank of Ceylon** - https://www.combank.lk/
2. **Hatton National Bank (HNB)** - https://www.hnb.lk/
3. **Sampath Bank** - https://www.sampath.lk/
4. **National Development Bank (NDB)** - https://www.ndbbank.com/
5. **Bank of Ceylon (BOC)** - https://www.boc.lk/
6. **People's Bank** - https://www.peoplesbank.lk/
7. **National Savings Bank (NSB)** - https://www.nsb.lk/

**Source**: Central Bank of Sri Lanka Licensed Banks List

### Stockbrokers (CSE Trading)
1. **Bartleet Religare Securities** - https://www.bartleet.com/
2. **Asia Securities** - Leading broker
3. **NDB Stockbrokers** - https://www.ndbstockbrokers.com/
4. **John Keells Stockbrokers (JKSB)** - https://www.jksb.com/
5. **Capital Alliance** - Stockbroking services

**Source**: Colombo Stock Exchange Member Firms List

### Government Securities
- **Central Bank of Sri Lanka** - https://www.cbsl.gov.lk/
  - Treasury Bill auctions (weekly)
  - Treasury Bond auctions
  - EPF/ETF administration

---

## 📊 Key Financial Data Sources

### Sri Lankan Investment Market Data
1. **Central Bank of Sri Lanka (CBSL)** - https://www.cbsl.gov.lk/
   - Interest rate data
   - T-Bill/T-Bond auction results
   - EPF performance reports
   - Banking sector statistics
   - Credit card interest rates (24-36% APR)

2. **Colombo Stock Exchange (CSE)** - https://www.cse.lk/
   - Stock prices and indices
   - Company reports and disclosures
   - ETF information
   - Historical performance data

3. **Unit Trust Association of Sri Lanka (UTASL)** - https://www.utasl.lk/
   - Unit trust NAV (Net Asset Value)
   - Fund performance data
   - Industry statistics

4. **Securities and Exchange Commission of Sri Lanka (SEC)** - https://www.sec.gov.lk/
   - Regulatory information
   - Licensed entities
   - Investor protection guidelines

### International Investment Principles
1. **Benjamin Graham** - "The Intelligent Investor"
   - Value investing principles
   - Defensive investor strategies

2. **Burton Malkiel** - "A Random Walk Down Wall Street"
   - Efficient market hypothesis
   - Index investing benefits

3. **Harry Markowitz** - Modern Portfolio Theory
   - Diversification benefits
   - Risk-return optimization

4. **William Sharpe** - Capital Asset Pricing Model
   - Systematic vs unsystematic risk

5. **CFP Board** - Certified Financial Planner Guidelines
   - Emergency fund recommendations (6 months)
   - Debt payoff priorities
   - Age-based allocation

### Sri Lankan Economic Context
1. **Education Cost Inflation**: 8-10% annually
   - Source: Private school fee increases, university admission costs

2. **Real Estate Returns**: 8-15% annually
   - Source: Property market analysis, urban development trends

3. **Inflation Rate**: Historical 5-8% (normal years)
   - Source: Department of Census and Statistics

---

## 🔧 Technical Architecture

### Expert System Components

1. **Knowledge Base** (`knowledge_base.json`)
   - 15 asset classes with characteristics
   - Risk profiles (conservative, moderate, aggressive)
   - Investment rules and principles

2. **Inference Engine** (`es.py`)
   - Forward-chaining rule-based system
   - Uses `experta` Python library (CLIPS-like)
   - 13 investment rules with salience-based priority
   - Fact-based reasoning

3. **User Interface** (`main.py`)
   - Streamlit web application
   - Interactive input forms
   - Visual portfolio allocation (Plotly charts)
   - Educational content display

### Rule Execution Flow
1. User inputs financial profile
2. Facts declared: UserProfile, InvestmentGoal
3. Rules evaluated in priority order (salience)
4. Matching rules fire and declare Allocation facts
5. UI displays allocation with reasoning and product examples

---

## 📖 How to Use RupeeLogic

### Step 1: Enter Personal Information
- **Age**: Your current age (18-80)
- **Monthly Expenses**: Average monthly living costs
- **Current Savings**: Total investable amount
- **High-Interest Debt**: Check if you have credit cards/loans >15% interest

### Step 2: Define Investment Goals
- **Goal Type**: Retirement, Education, Home Purchase, or Wealth Building
- **Time Horizon**: How many years until you need the money (1-30)

### Step 3: Risk Assessment
Answer the question: "If your portfolio drops 20% in a year, you would:"
- Sell everything → Low risk tolerance
- Hold steady → Moderate risk tolerance
- Buy more → High risk tolerance

### Step 4: Generate Portfolio
- Click "Generate My Investment Portfolio"
- Review recommended allocation
- Read reasoning for each asset class
- Note where to invest (specific product names)

### Step 5: Implementation
1. Open accounts with recommended institutions
2. Start with minimum investments
3. Set up monthly SIP (Systematic Investment Plan) for unit trusts
4. Monitor quarterly, rebalance annually

---

## ⚠️ Important Disclaimers

1. **Not Financial Advice**: RupeeLogic is an educational expert system. It provides general investment guidance based on established principles, not personalized financial advice.

2. **Consult Professionals**: Always consult licensed financial advisors before making investment decisions.

3. **Market Risk**: All investments carry risk. Past performance does not guarantee future results. Investment values can go down as well as up.

4. **Personal Circumstances**: Consider your unique situation, tax implications, and read product disclosure documents carefully.

5. **Data Currency**: Investment products, returns, and regulations change. Verify current information with providers.

6. **No Liability**: The creators of RupeeLogic are not responsible for investment losses or decisions made based on this tool.

---

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **Experta**: Expert system / rule engine library
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **JSON**: Knowledge base storage

---

## 👨‍💻 Development & Contribution

### Running in Development Mode
```bash
streamlit run app/main.py --server.runOnSave true
```

### Code Structure Guidelines
- Keep rules in `es.py` with clear docstrings
- Update knowledge base in `knowledge_base.json` with sources
- Maintain UI simplicity in `main.py`
- Document all investment principles with references

---

## 📝 Version History

### Version 1.0.0 (November 2024)
- Initial release with 13 investment rules
- 15 asset classes covering Sri Lankan market
- Comprehensive knowledge base with real products
- User-friendly Streamlit interface
- Full documentation with references

---

## 🙏 Acknowledgments

### Data Sources
- Central Bank of Sri Lanka
- Colombo Stock Exchange
- Unit Trust Association of Sri Lanka
- Major Sri Lankan banks and financial institutions

### Investment Principles
- Benjamin Graham (Value Investing)
- Burton Malkiel (Random Walk Theory)
- Harry Markowitz (Modern Portfolio Theory)
- Certified Financial Planner (CFP) Board Guidelines

### Technologies
- Streamlit community
- Experta library maintainers
- Python community

---

## 📧 Contact & Support

For questions, suggestions, or issues:
- Review the documentation above
- Check product provider websites for current offerings
- Consult licensed financial advisors for personalized advice

---

## 📄 License

This project is created for educational purposes. Investment product names and company names are property of their respective owners. All investment principles and rules are based on publicly available financial planning literature and market data.

---

**Built with ❤️ for Sri Lankan Investors**

*Last Updated: November 2024*

---

## 🔗 Quick Reference Links

### Government & Regulatory
- Central Bank of Sri Lanka: https://www.cbsl.gov.lk/
- SEC Sri Lanka: https://www.sec.gov.lk/
- Colombo Stock Exchange: https://www.cse.lk/

### Investment Products
- UTASL (Unit Trusts): https://www.utasl.lk/
- CSE Trading: https://www.cse.lk/pages/trading/trading.component.html

### Financial Education
- CBSL Financial Literacy: https://www.cbsl.gov.lk/en/financial-system-stability/financial-literacy
- SEC Investor Education: https://www.sec.gov.lk/investor-education/

---

**Remember**: Start small, diversify, invest regularly, and stay invested for the long term! 🚀

