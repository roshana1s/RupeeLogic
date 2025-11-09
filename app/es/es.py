from experta import *
import json

# --- Fact Definitions ---
class UserProfile(Fact):
    """Holds all user profile data."""
    pass

class InvestmentGoal(Fact):
    """Holds all user goal data."""
    pass

class Allocation(Fact):
    """A final recommendation fact. The UI will read these."""
    pass

# --- The Knowledge Engine ---
class RupeeLogicEngine(KnowledgeEngine):

    def __init__(self):
        """Initialize the engine and tracking for fired rules."""
        super().__init__()
        self.fired_rules = []  # Track which rules were fired

    @DefFacts()
    def _initial_facts(self):
        """Load the asset class knowledge base as facts."""
        with open("app/data/knowledge_base.json", "r") as f:
            kb = json.load(f)

        for asset, details in kb["asset_classes"].items():
            yield Fact(asset_class=asset, **details)

        # This fact signals the engine to start.
        yield Fact(run_analysis=True)

    # ==================================================================================
    # PHASE 1: CRITICAL FINANCIAL PRIORITIES (Highest Salience)
    # Rules: Emergency Fund & High-Interest Debt
    # ==================================================================================

    @Rule(
        UserProfile(monthly_expenses=MATCH.exp, current_savings=MATCH.sav),
        TEST(lambda exp, sav: sav < (exp * 6)),
        salience=100,
    )
    def rule_emergency_fund_priority(self):
        """
        RULE 1: Emergency Fund First
        Source: Financial Planning Standards - 6 months expenses recommended
        If savings < 6 months of expenses, prioritize building emergency fund
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 1",
                "rule_name": "Emergency Fund Priority",
                "salience": 100,
                "description": "Build 6-month emergency fund before investing",
                "condition": "Current savings < 6 months of monthly expenses",
                "action": "Allocate 50% to Savings Account and 50% to Money Market Funds",
            }
        )

        self.declare(
            Allocation(
                asset_class="savings_account",
                percent=50,
                reason="Build a 6-month emergency fund first for financial security and unexpected expenses.",
                reference="Financial planning best practice: 6 months expenses in liquid savings",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=50,
                reason="Higher returns than savings account while maintaining high liquidity for emergencies.",
                reference="Money market funds provide 7-8% returns vs 2-4% in savings accounts",
            )
        )

    @Rule(UserProfile(has_high_interest_debt=True), salience=95)
    def rule_debt_payoff_priority(self):
        """
        RULE 2: Pay Off High-Interest Debt First
        Source: Credit card rates in Sri Lanka: 24-36% p.a.
        Investment returns rarely beat credit card interest
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 2",
                "rule_name": "Debt Payoff Priority",
                "salience": 95,
                "description": "Pay off high-interest debt before investing",
                "condition": "Has high-interest debt (credit cards, personal loans)",
                "action": "Recommend 100% debt payment before any investments",
            }
        )

        self.declare(
            Allocation(
                asset_class="debt_payment",
                percent=100,
                reason="Pay off high-interest debt (credit cards: 24-36% p.a.) before investing. No investment consistently beats these rates.",
                reference="Sri Lankan credit card APR: 24-36% annually - Source: CBSL Financial Reports",
            )
        )

    # ==================================================================================
    # PHASE 2: SHORT-TERM GOALS (< 3 years) - Capital Preservation
    # ==================================================================================

    @Rule(
        NOT(Allocation()),
        InvestmentGoal(time_horizon=P(lambda x: x < 3)),
        salience=80,
    )
    def rule_short_term_goal(self):
        """
        RULE 3: Short-term goals require capital preservation
        Source: Investment horizon principle - volatility risk for short periods
        For goals < 3 years: No equity exposure, focus on guaranteed returns
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 3",
                "rule_name": "Short-Term Goal (< 3 years)",
                "salience": 80,
                "description": "Capital preservation for short-term goals",
                "condition": "Time horizon less than 3 years",
                "action": "Allocate 70% Fixed Deposits + 30% Treasury Bills (no equity exposure)",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=70,
                reason="Short-term goal requires guaranteed returns. FDs offer 9-11% p.a. with zero risk.",
                reference="Average FD rates in Sri Lanka: 9-11% p.a. (Commercial Bank, HNB, Sampath)",
            )
        )
        self.declare(
            Allocation(
                asset_class="treasury_bills",
                percent=30,
                reason="Government T-Bills provide secure short-term returns with sovereign guarantee.",
                reference="T-Bill rates: 10-12% p.a. - Central Bank of Sri Lanka primary auctions",
            )
        )

    # ==================================================================================
    # PHASE 3: RETIREMENT PLANNING (Age-based)
    # ==================================================================================

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: x >= 55)),
        InvestmentGoal(goal_type="Retirement"),
        salience=75,
    )
    def rule_near_retirement(self):
        """
        RULE 4: Near/In Retirement - Conservative Allocation
        Source: Age-based asset allocation - Preserve capital, generate income
        Formula: Equity % = 100 - Age (Conservative Sri Lankan: 80 - Age)
        Age 55+: Maximum 25% equity exposure
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 4",
                "rule_name": "Near Retirement Conservative",
                "salience": 75,
                "description": "Conservative portfolio for near-retirement age",
                "condition": "Age ≥ 55 years AND Goal = Retirement",
                "action": "Allocate 90% fixed income (FD, Bonds, Income Funds) + 10% blue chip stocks",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=40,
                reason="Capital preservation is critical near retirement. Guaranteed 9-11% annual returns.",
                reference="Conservative allocation for age 55+: 70-80% fixed income",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=30,
                reason="Long-term government bonds provide stable income with sovereign backing.",
                reference="Sri Lanka Development Bonds: 11-13% p.a. returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                reason="Professional bond fund management with better diversification than individual bonds.",
                reference="NDB Gilt Edge Fund, CAL Income Fund - typical returns 9-11%",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=10,
                reason="Small equity allocation for inflation protection through dividend-paying blue chips.",
                reference="Blue chip dividends: JKH, COMB, SAMP provide 3-5% dividend yields",
            )
        )

    # ==================================================================================
    # PHASE 4: AGGRESSIVE GROWTH (Young + High Risk + Long Term)
    # ==================================================================================

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: x < 35), risk_tolerance="High"),
        InvestmentGoal(time_horizon=P(lambda x: x >= 10)),
        salience=70,
    )
    def rule_aggressive_growth(self):
        """
        RULE 5: Aggressive Growth Portfolio
        Source: Modern Portfolio Theory - Young investors can tolerate volatility
        Age < 35 + High Risk + 10+ years = Maximum equity exposure
        Expected return: 18-25% p.a. with high volatility
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 5",
                "rule_name": "Aggressive Growth Portfolio",
                "salience": 70,
                "description": "Maximum equity exposure for young risk-takers",
                "condition": "Age < 35 AND Risk Tolerance = High AND Time Horizon ≥ 10 years",
                "action": "Allocate 75% equities (35% Equity Funds + 25% Blue Chips + 15% Growth Stocks) + 25% balanced/income",
            }
        )

        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=35,
                reason="Professional equity fund management provides diversification across CSE sectors.",
                reference="NDB Eagle Fund, CAL Equity Fund - historical returns: 15-20% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=25,
                reason="Direct investment in established companies (JKH, COMB, Dialog) for capital appreciation.",
                reference="CSE blue chips average return: 18-25% p.a. over 10+ years",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_growth_stocks",
                percent=15,
                reason="High-growth mid-cap stocks offer superior returns for risk-tolerant long-term investors.",
                reference="Growth stocks (Bairaha, Royal Ceramics): 25-40% potential returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=15,
                reason="Balanced funds provide automatic rebalancing between stocks and bonds.",
                reference="NDB Balanced Fund, CAL Growth & Income - typical returns: 12-15%",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=10,
                reason="Fixed income component for portfolio stability during market downturns.",
                reference="Bond funds provide 9-11% stable returns as portfolio anchor",
            )
        )

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: x < 40), risk_tolerance="High"),
        InvestmentGoal(time_horizon=P(lambda x: x >= 7)),
        salience=65,
    )
    def rule_growth_oriented(self):
        """
        RULE 6: Growth-Oriented Portfolio
        Age < 40 + High Risk + 7+ years
        Slightly more conservative than aggressive, but still equity-focused
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 6",
                "rule_name": "Growth-Oriented Portfolio",
                "salience": 65,
                "description": "Equity-focused with moderate stability",
                "condition": "Age < 40 AND Risk Tolerance = High AND Time Horizon ≥ 7 years",
                "action": "Allocate 70% equities + 30% bonds/income funds",
            }
        )

        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=30,
                reason="Equity funds for diversified growth exposure with professional management.",
                reference="Equity unit trusts historical performance: 15-20% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=25,
                reason="Balanced approach combining growth and stability.",
                reference="Balanced funds provide 12-15% returns with lower volatility",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=20,
                reason="Direct blue chip holdings for long-term wealth creation.",
                reference="Blue chip stocks: JKH, Commercial Bank, Hayleys - 18-25% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=15,
                reason="Bond component for downside protection and income generation.",
                reference="Income funds: 9-11% stable returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="corporate_bonds",
                percent=10,
                reason="Higher yields than government bonds with acceptable credit risk.",
                reference="Corporate debentures (DFCC, JKH): 12-14% p.a.",
            )
        )

    # ==================================================================================
    # PHASE 5: BALANCED/MODERATE PORTFOLIOS
    # ==================================================================================

    @Rule(
        NOT(Allocation()),
        UserProfile(risk_tolerance="Moderate"),
        InvestmentGoal(time_horizon=P(lambda x: x >= 5)),
        salience=60,
    )
    def rule_moderate_balanced(self):
        """
        RULE 7: Moderate Risk - Balanced Portfolio
        Source: 60-40 rule (60% equity, 40% bonds) for moderate investors
        Suitable for middle-aged investors with medium risk tolerance
        Expected return: 12-15% p.a.
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 7",
                "rule_name": "Moderate Balanced Portfolio",
                "salience": 60,
                "description": "Classic 60-40 balanced allocation",
                "condition": "Risk Tolerance = Moderate AND Time Horizon ≥ 5 years",
                "action": "Allocate 60% growth assets (balanced/equity funds) + 40% fixed income",
            }
        )

        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=40,
                reason="One-stop solution for balanced growth - automatically maintains 50-50 equity-debt mix.",
                reference="Balanced funds: NDB Wealth Balanced, CAL Growth & Income - 12-15% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=20,
                reason="Equity component for growth while professional managers handle volatility.",
                reference="Equity exposure provides inflation-beating returns over medium term",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                reason="Fixed income for stability and regular returns.",
                reference="Bond funds deliver predictable 9-11% annual income",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=10,
                reason="Select blue chip exposure for dividend income and capital appreciation.",
                reference="Blue chip dividends provide 3-5% yield plus capital gains",
            )
        )
        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=10,
                reason="Capital preservation component with guaranteed returns.",
                reference="FDs provide 9-11% guaranteed returns as portfolio anchor",
            )
        )

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: 35 <= x < 50), risk_tolerance="Moderate"),
        salience=55,
    )
    def rule_middle_age_moderate(self):
        """
        RULE 8: Middle-aged Moderate Investor
        Age 35-50 + Moderate risk
        Building wealth while managing responsibilities
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 8",
                "rule_name": "Middle-Age Moderate Investor",
                "salience": 55,
                "description": "Balanced portfolio for mid-career professionals",
                "condition": "Age 35-50 AND Risk Tolerance = Moderate",
                "action": "Allocate 60% balanced/equity funds + 40% bonds",
            }
        )

        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=35,
                reason="Balanced funds ideal for busy professionals - automatic portfolio management.",
                reference="Balanced allocation suitable for age 35-50 demographic",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=25,
                reason="Equity exposure for long-term growth to meet retirement goals.",
                reference="Still 15-20 years to retirement - can handle equity volatility",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=25,
                reason="Fixed income for portfolio stability and income needs.",
                reference="Income funds provide stable 9-11% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=15,
                reason="Government securities for risk-free component of portfolio.",
                reference="T-Bonds: 11-13% p.a. with sovereign guarantee",
            )
        )

    # ==================================================================================
    # PHASE 6: CONSERVATIVE PORTFOLIOS (Low Risk)
    # ==================================================================================

    @Rule(
        NOT(Allocation()),
        UserProfile(risk_tolerance="Low"),
        salience=50,
    )
    def rule_conservative_portfolio(self):
        """
        RULE 9: Conservative Portfolio - Capital Preservation
        Source: Conservative allocation for risk-averse investors
        Focus: Preserve capital, generate steady income
        Expected return: 9-12% p.a. with minimal volatility
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 9",
                "rule_name": "Conservative Portfolio",
                "salience": 50,
                "description": "Capital preservation with minimal risk",
                "condition": "Risk Tolerance = Low",
                "action": "Allocate 80% fixed income (FDs, Bonds, Income Funds) + 20% balanced funds",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=40,
                reason="Guaranteed returns with zero market risk. Suitable for conservative investors.",
                reference="FD rates: 9-11% p.a. across major banks (Commercial, HNB, Sampath)",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=30,
                reason="Government backing ensures capital safety with better returns than FDs.",
                reference="Treasury Bonds: 11-13% p.a. - Central Bank of Sri Lanka",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                reason="Professional bond fund management with diversification benefits.",
                reference="Gilt-edge funds: NDB Wealth, CAL Income Fund - 9-11% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                reason="Liquidity buffer with better returns than savings accounts.",
                reference="Money market funds: 7-8% returns with instant liquidity",
            )
        )

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: x >= 50), risk_tolerance="Low"),
        salience=52,
    )
    def rule_pre_retirement_conservative(self):
        """
        RULE 10: Pre-retirement Conservative (Age 50+, Low Risk)
        Focus on capital preservation with minimal equity
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 10",
                "rule_name": "Pre-Retirement Conservative",
                "salience": 52,
                "description": "Conservative allocation for pre-retirement (age 50+)",
                "condition": "Age ≥ 50 AND Risk Tolerance = Low",
                "action": "Allocate 85% fixed income + 15% balanced/blue chips",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=35,
                reason="Guaranteed returns crucial as retirement approaches.",
                reference="FDs provide predictable income for retirement planning",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=30,
                reason="Long-term government securities for stable retirement income.",
                reference="Government bonds: 11-13% p.a. with sovereign backing",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                reason="Bond funds for diversified fixed income exposure.",
                reference="Income funds managed by professionals with steady returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=10,
                reason="Small balanced fund allocation for moderate growth.",
                reference="Limited equity exposure through balanced funds",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=5,
                reason="Emergency liquidity buffer.",
                reference="Money market funds for immediate cash needs",
            )
        )

    # ==================================================================================
    # PHASE 7: SPECIFIC GOAL-BASED ALLOCATIONS
    # ==================================================================================

    @Rule(
        NOT(Allocation()),
        InvestmentGoal(goal_type="Child Education"),
        InvestmentGoal(time_horizon=P(lambda x: 5 <= x < 10)),
        salience=58,
    )
    def rule_education_planning(self):
        """
        RULE 11: Child's Education Planning (5-10 years)
        Goal-specific: Education costs rising 8-10% annually in Sri Lanka
        Need growth to beat inflation while preserving capital
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 11",
                "rule_name": "Education Planning",
                "salience": 58,
                "description": "Balanced growth for education savings (5-10 years)",
                "condition": "Goal = Child Education AND Time Horizon 5-10 years",
                "action": "Allocate 65% balanced/equity funds + 35% fixed income",
            }
        )

        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=40,
                reason="Balanced growth to beat education inflation (8-10% annually) while managing risk.",
                reference="Education costs in Sri Lanka rising 8-10% annually - need equity exposure",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=25,
                reason="Equity component for growth over medium-term education timeline.",
                reference="5-10 year horizon allows for equity market participation",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                reason="Fixed income for stability as education date approaches.",
                reference="Bond funds provide stable returns: 9-11% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=15,
                reason="Guaranteed component to ensure minimum fund availability.",
                reference="FDs ensure guaranteed funds for education expenses",
            )
        )

    @Rule(
        NOT(Allocation()),
        InvestmentGoal(goal_type="Home Purchase"),
        InvestmentGoal(time_horizon=P(lambda x: 3 <= x < 7)),
        salience=57,
    )
    def rule_home_purchase_planning(self):
        """
        RULE 12: Home Purchase Goal (3-7 years)
        Property down payment requires capital preservation with moderate growth
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 12",
                "rule_name": "Home Purchase Planning",
                "salience": 57,
                "description": "Conservative allocation for home down payment (3-7 years)",
                "condition": "Goal = Home Purchase AND Time Horizon 3-7 years",
                "action": "Allocate 60% fixed income (FDs, bonds) + 40% balanced/equity",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=40,
                reason="Guaranteed capital for home down payment - cannot risk market volatility.",
                reference="Down payment funds need capital guarantee: FDs 9-11% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=30,
                reason="Moderate growth to accumulate larger down payment while managing risk.",
                reference="Balanced funds provide 12-15% growth potential",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                reason="Stable bond returns to supplement fixed deposits.",
                reference="Bond funds: 9-11% returns with lower risk than equities",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                reason="Liquidity for quick access when property opportunity arises.",
                reference="Money market funds provide instant liquidity",
            )
        )

    # ==================================================================================
    # PHASE 8: DEFAULT RULE (Lowest Priority)
    # ==================================================================================

    @Rule(NOT(Allocation()), salience=-10)
    def rule_default_recommendation(self):
        """
        RULE 13: Default Moderate Portfolio
        Fallback rule when no specific conditions are met
        Safe, balanced approach suitable for most investors
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 13",
                "rule_name": "Default Balanced Portfolio",
                "salience": -10,
                "description": "Fallback balanced portfolio when no specific rules match",
                "condition": "No other rules matched",
                "action": "Allocate 60% Balanced Funds + 30% Income Funds + 10% Money Market",
            }
        )

        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=60,
                reason="Balanced fund is the safest default - automatically maintains diversified portfolio.",
                reference="Default allocation: Balanced funds suitable for most investors",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=30,
                reason="Fixed income component for stability.",
                reference="Bond funds provide stable 9-11% annual returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                reason="Liquidity buffer for emergencies.",
                reference="Money market funds: 7-8% with high liquidity",
            )
        )
