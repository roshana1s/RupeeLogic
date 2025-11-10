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


class AlternativeAllocation(Fact):
    """Alternative investment plan recommendations."""

    pass


# --- The Knowledge Engine ---
class RupeeLogicEngine(KnowledgeEngine):

    def __init__(self):
        """Initialize the engine and tracking for fired rules."""
        super().__init__()
        self.fired_rules = []  # Track which rules were fired
        self.primary_plan_confidence = 85  # Default confidence for primary plan
        self.alternative_plans = []  # Track alternative plans

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
        Reference: https://www.investopedia.com/terms/e/emergency_fund.asp
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 1",
                "rule_name": "Emergency Fund Priority",
                "salience": 100,
                "confidence": 85,
                "description": "Build 6-month emergency fund before investing",
                "condition": "Current savings < 6 months of monthly expenses",
                "action": "Primary Plan: 50% Savings Account + 50% Money Market Funds",
            }
        )

        # PRIMARY PLAN (85% confidence)
        self.declare(
            Allocation(
                asset_class="savings_account",
                percent=50,
                plan_type="primary",
                confidence=85,
                reason="Build a 6-month emergency fund first for financial security and unexpected expenses.",
                reference="Financial planning best practice: 6 months expenses in liquid savings - Dave Ramsey, Total Money Makeover",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=50,
                plan_type="primary",
                confidence=85,
                reason="Higher returns than savings account while maintaining high liquidity for emergencies.",
                reference="Money market funds provide 7-8% returns vs 2-4% in savings accounts",
            )
        )

        # ALTERNATIVE PLAN 1 (70% confidence) - More conservative
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Maximum Liquidity",
                "confidence": 70,
                "allocations": [
                    {
                        "asset_class": "savings_account",
                        "percent": 80,
                        "reason": "Prioritize immediate access to emergency funds over returns.",
                        "reference": "Ultra-safe approach for risk-averse individuals",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 20,
                        "reason": "Small allocation for slightly better returns while keeping most in instant-access savings.",
                        "reference": "Recommended by conservative financial planners",
                    },
                ],
            }
        )

        # ALTERNATIVE PLAN 2 (65% confidence) - More aggressive returns
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 2: Enhanced Returns",
                "confidence": 65,
                "allocations": [
                    {
                        "asset_class": "savings_account",
                        "percent": 30,
                        "reason": "Minimum emergency cash for 1-2 months immediate expenses.",
                        "reference": "Tiered emergency fund approach",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 40,
                        "reason": "Core emergency fund with better returns and T+1 liquidity.",
                        "reference": "Money market funds average 7-8% in Sri Lanka",
                    },
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 30,
                        "reason": "Highest returns (9-11%) with 14-day withdrawal option for portion of emergency fund.",
                        "reference": "Commercial banks offer FD withdrawals with minimal penalty",
                    },
                ],
            }
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
                plan_type="primary",
                confidence=95,
                reason="Pay off high-interest debt (credit cards: 24-36% p.a.) before investing. No investment consistently beats these rates.",
                reference="Sri Lankan credit card APR: 24-36% annually - Source: CBSL Financial Reports",
            )
        )

    @Rule(
        UserProfile(monthly_income=MATCH.inc, monthly_expenses=MATCH.exp),
        TEST(lambda inc, exp: exp >= inc),
        salience=98,
    )
    def rule_expenses_exceed_income(self):
        """
        RULE 2A: Expenses Equal or Exceed Income - CRITICAL
        Edge case: Living beyond means
        Focus on expense reduction and income increase
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 2A",
                "rule_name": "Expenses Exceed Income - Budget Crisis",
                "salience": 98,
                "description": "Expenses >= Income - Focus on budgeting first",
                "condition": "Monthly expenses >= Monthly income",
                "action": "PRIORITY: Reduce expenses or increase income before investing",
            }
        )

        self.declare(
            Allocation(
                asset_class="budget_management",
                percent=100,
                plan_type="primary",
                confidence=99,
                reason="⚠️ CRITICAL: Your monthly expenses equal or exceed your income. You cannot invest sustainably in this situation. Focus on: 1) Reducing discretionary expenses, 2) Increasing income through side hustles or career advancement, 3) Building a basic emergency fund from current savings.",
                reference="Financial Planning 101: Income must exceed expenses for sustainable investing - Dave Ramsey Total Money Makeover",
            )
        )

    @Rule(
        UserProfile(
            monthly_income=MATCH.inc,
            monthly_expenses=MATCH.exp,
            current_savings=MATCH.sav,
        ),
        TEST(
            lambda inc, exp, sav: (inc - exp) > 0
            and (inc - exp) < 10000
            and sav < 100000
        ),
        salience=97,
    )
    def rule_very_low_investable_amount(self):
        """
        RULE 2B: Very Low Investable Amount
        Edge case: Monthly surplus < LKR 10,000 and low savings
        Focus on building emergency fund first
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 2B",
                "rule_name": "Very Low Investable Amount",
                "salience": 97,
                "description": "Monthly surplus < LKR 10,000 - Build foundation first",
                "condition": "Monthly investable < 10,000 AND Current savings < 100,000",
                "action": "100% savings account to build emergency fund",
            }
        )

        self.declare(
            Allocation(
                asset_class="savings_account",
                percent=100,
                plan_type="primary",
                confidence=90,
                reason="With limited monthly surplus (< LKR 10,000) and low savings, focus 100% on building a cash emergency fund first. Most investments require minimum amounts of LKR 10,000-50,000.",
                reference="Build LKR 100,000+ emergency fund before diversifying - minimum for most unit trusts",
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
                "confidence": 85,
                "description": "Capital preservation for short-term goals",
                "condition": "Time horizon less than 3 years",
                "action": "Allocate 70% Fixed Deposits + 30% Treasury Bills (no equity exposure)",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=70,
                plan_type="primary",
                confidence=85,
                reason="Short-term goal requires guaranteed returns. FDs offer 9-11% p.a. with zero risk.",
                reference="Average FD rates in Sri Lanka: 9-11% p.a. (Commercial Bank, HNB, Sampath)",
            )
        )
        self.declare(
            Allocation(
                asset_class="treasury_bills",
                percent=30,
                plan_type="primary",
                confidence=85,
                reason="Government T-Bills provide secure short-term returns with sovereign guarantee.",
                reference="T-Bill rates: 10-12% p.a. - Central Bank of Sri Lanka primary auctions",
            )
        )

        # ALTERNATIVE PLAN 1 (78% confidence) - Maximum Safety
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: 100% Bank Deposits",
                "confidence": 78,
                "description": "Maximum safety with bank deposits only",
                "allocations": [
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 100,
                        "reason": "All funds in guaranteed fixed deposits for absolute certainty.",
                        "reference": "Zero risk approach for very conservative short-term goals",
                    },
                ],
            }
        )

        # ALTERNATIVE PLAN 2 (80% confidence) - Government Focus
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 2: Government Securities",
                "confidence": 80,
                "description": "Focus on government-backed securities",
                "allocations": [
                    {
                        "asset_class": "treasury_bills",
                        "percent": 60,
                        "reason": "Sovereign guarantee with better liquidity than FDs.",
                        "reference": "T-Bills can be sold in secondary market if needed",
                    },
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 40,
                        "reason": "Bank deposits for portion requiring absolute guarantee.",
                        "reference": "Mix of government and bank securities",
                    },
                ],
            }
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
                "confidence": 88,
                "description": "Conservative portfolio for near-retirement age",
                "condition": "Age ≥ 55 years AND Goal = Retirement",
                "action": "Allocate 90% fixed income (FD, Bonds, Income Funds) + 10% blue chip stocks",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=40,
                plan_type="primary",
                confidence=88,
                reason="Capital preservation is critical near retirement. Guaranteed 9-11% annual returns.",
                reference="Conservative allocation for age 55+: 70-80% fixed income",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=30,
                plan_type="primary",
                confidence=88,
                reason="Long-term government bonds provide stable income with sovereign backing.",
                reference="Sri Lanka Development Bonds: 11-13% p.a. returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=88,
                reason="Professional bond fund management with better diversification than individual bonds.",
                reference="NDB Gilt Edge Fund, CAL Income Fund - typical returns 9-11%",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=10,
                plan_type="primary",
                confidence=88,
                reason="Small equity allocation for inflation protection through dividend-paying blue chips.",
                reference="Blue chip dividends: JKH, COMB, SAMP provide 3-5% dividend yields",
            )
        )

        # ALTERNATIVE PLAN 1 (80% confidence) - Income Focus
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Maximum Income",
                "confidence": 80,
                "description": "Focus on income generation in retirement",
                "allocations": [
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 35,
                        "reason": "Maximum income from bond funds.",
                        "reference": "Steady monthly income stream",
                    },
                    {
                        "asset_class": "government_bonds",
                        "percent": 30,
                        "reason": "Government securities for stable income.",
                        "reference": "11-13% p.a. guaranteed",
                    },
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 25,
                        "reason": "Guaranteed fixed deposits.",
                        "reference": "9-11% safe returns",
                    },
                    {
                        "asset_class": "cse_blue_chip_stocks",
                        "percent": 10,
                        "reason": "Dividend income from blue chips.",
                        "reference": "3-5% dividend yield",
                    },
                ],
            }
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
                "confidence": 78,
                "description": "Maximum equity exposure for young risk-takers",
                "condition": "Age < 35 AND Risk Tolerance = High AND Time Horizon ≥ 10 years",
                "action": "Allocate 75% equities (35% Equity Funds + 25% Blue Chips + 15% Growth Stocks) + 25% balanced/income",
            }
        )

        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=35,
                plan_type="primary",
                confidence=78,
                reason="Professional equity fund management provides diversification across CSE sectors.",
                reference="NDB Eagle Fund, CAL Equity Fund - historical returns: 15-20% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=25,
                plan_type="primary",
                confidence=78,
                reason="Direct investment in established companies (JKH, COMB, Dialog) for capital appreciation.",
                reference="CSE blue chips average return: 18-25% p.a. over 10+ years",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_growth_stocks",
                percent=15,
                plan_type="primary",
                confidence=78,
                reason="High-growth mid-cap stocks offer superior returns for risk-tolerant long-term investors.",
                reference="Growth stocks (Bairaha, Royal Ceramics): 25-40% potential returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=15,
                plan_type="primary",
                confidence=78,
                reason="Balanced funds provide automatic rebalancing between stocks and bonds.",
                reference="NDB Balanced Fund, CAL Growth & Income - typical returns: 12-15%",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=10,
                plan_type="primary",
                confidence=78,
                reason="Fixed income component for portfolio stability during market downturns.",
                reference="Bond funds provide 9-11% stable returns as portfolio anchor",
            )
        )

        # ALTERNATIVE PLAN 1 (70% confidence) - Maximum Aggression
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Ultra-Aggressive Growth",
                "confidence": 70,
                "description": "Maximum equity exposure for highest growth potential",
                "allocations": [
                    {
                        "asset_class": "cse_growth_stocks",
                        "percent": 40,
                        "reason": "Maximum growth stock exposure for long-term wealth building.",
                        "reference": "High-growth stocks can deliver 30-50% returns",
                    },
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 35,
                        "reason": "Professional diversification across sectors.",
                        "reference": "Equity funds for broad market exposure",
                    },
                    {
                        "asset_class": "cse_blue_chip_stocks",
                        "percent": 25,
                        "reason": "Blue chips for dividend income and stability.",
                        "reference": "Balance growth with quality companies",
                    },
                ],
            }
        )

        # ALTERNATIVE PLAN 2 (75% confidence) - Diversified Growth
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 2: Balanced Aggression",
                "confidence": 75,
                "description": "Aggressive but more diversified approach",
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 45,
                        "reason": "Core equity through professional management.",
                        "reference": "Let experts handle stock selection",
                    },
                    {
                        "asset_class": "cse_blue_chip_stocks",
                        "percent": 30,
                        "reason": "Direct ownership of top companies.",
                        "reference": "JKH, COMB, Dialog for long-term",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 15,
                        "reason": "Some balanced exposure for automatic rebalancing.",
                        "reference": "Reduces need for manual adjustments",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 10,
                        "reason": "Small fixed income cushion.",
                        "reference": "Provides stability during crashes",
                    },
                ],
            }
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
                "confidence": 76,
                "description": "Equity-focused with moderate stability",
                "condition": "Age < 40 AND Risk Tolerance = High AND Time Horizon ≥ 7 years",
                "action": "Allocate 70% equities + 30% bonds/income funds",
            }
        )

        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=30,
                plan_type="primary",
                confidence=76,
                reason="Equity funds for diversified growth exposure with professional management.",
                reference="Equity unit trusts historical performance: 15-20% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=25,
                plan_type="primary",
                confidence=76,
                reason="Balanced approach combining growth and stability.",
                reference="Balanced funds provide 12-15% returns with lower volatility",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=20,
                plan_type="primary",
                confidence=76,
                reason="Direct blue chip holdings for long-term wealth creation.",
                reference="Blue chip stocks: JKH, Commercial Bank, Hayleys - 18-25% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=15,
                plan_type="primary",
                confidence=76,
                reason="Bond component for downside protection and income generation.",
                reference="Income funds: 9-11% stable returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="corporate_bonds",
                percent=10,
                plan_type="primary",
                confidence=76,
                reason="Higher yields than government bonds with acceptable credit risk.",
                reference="Corporate debentures (DFCC, JKH): 12-14% p.a.",
            )
        )

        # ALTERNATIVE PLAN 1 (68% confidence) - Growth Focus
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Enhanced Growth",
                "confidence": 68,
                "description": "More equity exposure for higher returns",
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 40,
                        "reason": "Higher equity allocation for growth.",
                        "reference": "Maximize long-term returns",
                    },
                    {
                        "asset_class": "cse_blue_chip_stocks",
                        "percent": 30,
                        "reason": "Direct stock ownership for control.",
                        "reference": "Blue chips: JKH, COMB, Dialog",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 20,
                        "reason": "Balanced component for stability.",
                        "reference": "Professional rebalancing",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 10,
                        "reason": "Fixed income for downside protection.",
                        "reference": "9-11% stable returns",
                    },
                ],
            }
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
                plan_type="primary",
                confidence=75,
                reason="One-stop solution for balanced growth - automatically maintains 50-50 equity-debt mix.",
                reference="Balanced funds: NDB Wealth Balanced, CAL Growth & Income - 12-15% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=75,
                reason="Equity component for growth while professional managers handle volatility.",
                reference="Equity exposure provides inflation-beating returns over medium term",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=75,
                reason="Fixed income for stability and regular returns.",
                reference="Bond funds deliver predictable 9-11% annual income",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=10,
                plan_type="primary",
                confidence=75,
                reason="Select blue chip exposure for dividend income and capital appreciation.",
                reference="Blue chip dividends provide 3-5% yield plus capital gains",
            )
        )
        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=10,
                plan_type="primary",
                confidence=75,
                reason="Capital preservation component with guaranteed returns.",
                reference="FDs provide 9-11% guaranteed returns as portfolio anchor",
            )
        )

        # ALTERNATIVE PLAN 1 (65% confidence) - More Growth
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Growth-Oriented",
                "confidence": 65,
                "description": "Higher equity exposure for growth",
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 40,
                        "reason": "Increased equity allocation for higher growth potential.",
                        "reference": "Equity funds: 15-20% long-term returns",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 30,
                        "reason": "Balanced core holding.",
                        "reference": "Auto-rebalancing feature",
                    },
                    {
                        "asset_class": "cse_blue_chip_stocks",
                        "percent": 15,
                        "reason": "Direct stock ownership.",
                        "reference": "Blue chips: JKH, COMB, Dialog",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 15,
                        "reason": "Fixed income stability.",
                        "reference": "9-11% stable returns",
                    },
                ],
            }
        )

        # ALTERNATIVE PLAN 2 (70% confidence) - More Conservative
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 2: Conservative Balance",
                "confidence": 70,
                "description": "Lower volatility with more fixed income",
                "allocations": [
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 50,
                        "reason": "Larger balanced allocation for stability.",
                        "reference": "One-stop diversified solution",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 30,
                        "reason": "Increased fixed income for reduced volatility.",
                        "reference": "Bond funds 9-11%",
                    },
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 20,
                        "reason": "Guaranteed returns component.",
                        "reference": "FDs 9-11% guaranteed",
                    },
                ],
            }
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
                "confidence": 77,
                "description": "Balanced portfolio for mid-career professionals",
                "condition": "Age 35-50 AND Risk Tolerance = Moderate",
                "action": "Allocate 60% balanced/equity funds + 40% bonds",
            }
        )

        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=35,
                plan_type="primary",
                confidence=77,
                reason="Balanced funds ideal for busy professionals - automatic portfolio management.",
                reference="Balanced allocation suitable for age 35-50 demographic",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=25,
                plan_type="primary",
                confidence=77,
                reason="Equity exposure for long-term growth to meet retirement goals.",
                reference="Still 15-20 years to retirement - can handle equity volatility",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=25,
                plan_type="primary",
                confidence=77,
                reason="Fixed income for portfolio stability and income needs.",
                reference="Income funds provide stable 9-11% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=15,
                plan_type="primary",
                confidence=77,
                reason="Government securities for risk-free component of portfolio.",
                reference="T-Bonds: 11-13% p.a. with sovereign guarantee",
            )
        )

        # ALTERNATIVE PLAN 1 (72% confidence) - Growth Tilt
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Growth-Focused",
                "confidence": 72,
                "description": "Higher equity for mid-career growth",
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 35,
                        "reason": "Increased equity for wealth building.",
                        "reference": "Still time to recover from volatility",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 35,
                        "reason": "Core balanced holding.",
                        "reference": "Automatic rebalancing",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 20,
                        "reason": "Fixed income stability.",
                        "reference": "Bond funds 9-11%",
                    },
                    {
                        "asset_class": "government_bonds",
                        "percent": 10,
                        "reason": "Sovereign security component.",
                        "reference": "Safe anchor",
                    },
                ],
            }
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
                "confidence": 82,
                "description": "Capital preservation with minimal risk",
                "condition": "Risk Tolerance = Low",
                "action": "Allocate 80% fixed income (FDs, Bonds, Income Funds) + 20% balanced funds",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=40,
                plan_type="primary",
                confidence=82,
                reason="Guaranteed returns with zero market risk. Suitable for conservative investors.",
                reference="FD rates: 9-11% p.a. across major banks (Commercial, HNB, Sampath)",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=30,
                plan_type="primary",
                confidence=82,
                reason="Government backing ensures capital safety with better returns than FDs.",
                reference="Treasury Bonds: 11-13% p.a. - Central Bank of Sri Lanka",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=82,
                reason="Professional bond fund management with diversification benefits.",
                reference="Gilt-edge funds: NDB Wealth, CAL Income Fund - 9-11% returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                plan_type="primary",
                confidence=82,
                reason="Liquidity buffer with better returns than savings accounts.",
                reference="Money market funds: 7-8% returns with instant liquidity",
            )
        )

        # ALTERNATIVE PLAN 1 (75% confidence) - Ultra Conservative
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Maximum Safety",
                "confidence": 75,
                "description": "100% guaranteed returns focus",
                "allocations": [
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 60,
                        "reason": "Maximum allocation to guaranteed bank deposits.",
                        "reference": "Zero market risk",
                    },
                    {
                        "asset_class": "government_bonds",
                        "percent": 30,
                        "reason": "Government-backed securities.",
                        "reference": "Sovereign guarantee",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 10,
                        "reason": "Liquidity buffer.",
                        "reference": "Instant access",
                    },
                ],
            }
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
                "confidence": 84,
                "description": "Conservative allocation for pre-retirement (age 50+)",
                "condition": "Age ≥ 50 AND Risk Tolerance = Low",
                "action": "Allocate 85% fixed income + 15% balanced/blue chips",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=35,
                plan_type="primary",
                confidence=84,
                reason="Guaranteed returns crucial as retirement approaches.",
                reference="FDs provide predictable income for retirement planning",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=30,
                plan_type="primary",
                confidence=84,
                reason="Long-term government securities for stable retirement income.",
                reference="Government bonds: 11-13% p.a. with sovereign backing",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=84,
                reason="Bond funds for diversified fixed income exposure.",
                reference="Income funds managed by professionals with steady returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=10,
                plan_type="primary",
                confidence=84,
                reason="Small balanced fund allocation for moderate growth.",
                reference="Limited equity exposure through balanced funds",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=5,
                plan_type="primary",
                confidence=84,
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
                "confidence": 79,
                "description": "Balanced growth for education savings (5-10 years)",
                "condition": "Goal = Child Education AND Time Horizon 5-10 years",
                "action": "Allocate 65% balanced/equity funds + 35% fixed income",
            }
        )

        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=40,
                plan_type="primary",
                confidence=79,
                reason="Balanced growth to beat education inflation (8-10% annually) while managing risk.",
                reference="Education costs in Sri Lanka rising 8-10% annually - need equity exposure",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=25,
                plan_type="primary",
                confidence=79,
                reason="Equity component for growth over medium-term education timeline.",
                reference="5-10 year horizon allows for equity market participation",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=79,
                reason="Fixed income for stability as education date approaches.",
                reference="Bond funds provide stable returns: 9-11% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=15,
                plan_type="primary",
                confidence=79,
                reason="Guaranteed component to ensure minimum fund availability.",
                reference="FDs ensure guaranteed funds for education expenses",
            )
        )

        # ALTERNATIVE PLAN 1 (73% confidence) - Growth Focus
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Higher Growth",
                "confidence": 73,
                "description": "More equity to beat education inflation",
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 35,
                        "reason": "Higher equity for inflation-beating returns.",
                        "reference": "Education costs rise 8-10% annually",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 35,
                        "reason": "Balanced growth with stability.",
                        "reference": "Professional management",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 20,
                        "reason": "Fixed income component.",
                        "reference": "9-11% stable returns",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 10,
                        "reason": "Liquidity for education needs.",
                        "reference": "Quick access when needed",
                    },
                ],
            }
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
                "confidence": 81,
                "description": "Conservative allocation for home down payment (3-7 years)",
                "condition": "Goal = Home Purchase AND Time Horizon 3-7 years",
                "action": "Allocate 60% fixed income (FDs, bonds) + 40% balanced/equity",
            }
        )

        self.declare(
            Allocation(
                asset_class="fixed_deposits",
                percent=40,
                plan_type="primary",
                confidence=81,
                reason="Guaranteed capital for home down payment - cannot risk market volatility.",
                reference="Down payment funds need capital guarantee: FDs 9-11% p.a.",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=30,
                plan_type="primary",
                confidence=81,
                reason="Moderate growth to accumulate larger down payment while managing risk.",
                reference="Balanced funds provide 12-15% growth potential",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=81,
                reason="Stable bond returns to supplement fixed deposits.",
                reference="Bond funds: 9-11% returns with lower risk than equities",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                plan_type="primary",
                confidence=81,
                reason="Liquidity for quick access when property opportunity arises.",
                reference="Money market funds provide instant liquidity",
            )
        )

    # ==================================================================================
    # NEW RULES: Additional Investment Scenarios with Alternative Plans
    # ==================================================================================

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: 25 <= x < 35), risk_tolerance="Moderate"),
        InvestmentGoal(goal_type="Wealth Building", time_horizon=P(lambda x: x >= 6)),
        salience=68,
    )
    def rule_young_professional_wealth(self):
        """
        RULE 14: Young Professional Wealth Building
        Age 25-35, Moderate Risk, Long-term wealth building (6+ years)
        Reference: https://www.investopedia.com/articles/personal-finance/032216/how-your-asset-allocation-impacts-returns.asp
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 14",
                "rule_name": "Young Professional Wealth Building",
                "salience": 68,
                "confidence": 80,
                "description": "Balanced growth strategy for young professionals",
                "condition": "Age 25-35 AND Moderate Risk AND Wealth Building goal (6+ years)",
                "action": "Primary: 65% equity + 35% bonds",
            }
        )

        # PRIMARY PLAN (80% confidence) - Balanced Growth
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=40,
                plan_type="primary",
                confidence=80,
                reason="Professional management with automatic rebalancing between stocks (50%) and bonds (50%).",
                reference="NDB Balanced Fund, CAL Growth & Income - average 12-15% returns - https://www.cse.lk",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=25,
                plan_type="primary",
                confidence=80,
                reason="Additional equity exposure for long-term growth potential.",
                reference="Equity funds average 15-20% returns over 10 years",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=80,
                reason="Fixed income stability during market volatility.",
                reference="Bond funds provide 9-11% stable returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=15,
                plan_type="primary",
                confidence=80,
                reason="Liquidity buffer for opportunities and emergencies.",
                reference="Money market funds: 7-8% with T+1 liquidity",
            )
        )

        # ALTERNATIVE PLAN 1 (70% confidence) - More Aggressive
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Growth-Focused",
                "confidence": 70,
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 45,
                        "reason": "Maximum equity exposure through professional management.",
                        "reference": "Suitable if comfortable with short-term volatility",
                    },
                    {
                        "asset_class": "cse_blue_chip_stocks",
                        "percent": 20,
                        "reason": "Direct stock ownership in established companies.",
                        "reference": "JKH, COMB, Dialog - dividend + growth",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 25,
                        "reason": "Core balanced allocation for stability.",
                        "reference": "Automatic rebalancing feature",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 10,
                        "reason": "Minimal cash buffer.",
                        "reference": "7-8% liquid returns",
                    },
                ],
            }
        )

        # ALTERNATIVE PLAN 2 (75% confidence) - More Conservative
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 2: Stability-Focused",
                "confidence": 75,
                "allocations": [
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 50,
                        "reason": "Higher balanced fund allocation for auto-diversification.",
                        "reference": "Set-and-forget approach",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 30,
                        "reason": "Increased fixed income for lower volatility.",
                        "reference": "Bond funds 9-11% stable",
                    },
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 15,
                        "reason": "Modest equity exposure for growth.",
                        "reference": "Reduced market risk",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 5,
                        "reason": "Emergency liquidity.",
                        "reference": "Instant access funds",
                    },
                ],
            }
        )

    @Rule(
        NOT(Allocation()),
        UserProfile(
            age=P(lambda x: 35 <= x < 45), monthly_income=P(lambda x: x >= 200000)
        ),
        InvestmentGoal(time_horizon=P(lambda x: x >= 7)),
        salience=66,
    )
    def rule_high_income_growth(self):
        """
        RULE 15: High-Income Professional Growth
        Age 35-45, High income (200K+), medium-long term
        Reference: https://www.investopedia.com/terms/h/high-net-worth-individuals-hnwi.asp
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 15",
                "rule_name": "High-Income Professional Portfolio",
                "salience": 66,
                "confidence": 82,
                "description": "Diversified growth for high earners",
                "condition": "Age 35-45 AND Monthly income ≥ LKR 200,000 AND Time horizon ≥ 7 years",
                "action": "Primary: Diversified across multiple asset classes",
            }
        )

        # PRIMARY PLAN (82% confidence)
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=30,
                plan_type="primary",
                confidence=82,
                reason="Core equity allocation managed by professionals.",
                reference="Diversification across CSE sectors - https://www.cse.lk",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=20,
                plan_type="primary",
                confidence=82,
                reason="Direct ownership of premium Sri Lankan companies.",
                reference="Blue chips: JKH, COMB, Dialog, Hemas",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=82,
                reason="Balanced component for automatic rebalancing.",
                reference="50-50 equity-debt mix",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=15,
                plan_type="primary",
                confidence=82,
                reason="Sovereign guarantee with attractive yields.",
                reference="SLDB 11-13% annual returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=10,
                plan_type="primary",
                confidence=82,
                reason="Fixed income stability.",
                reference="Bond funds 9-11%",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=5,
                plan_type="primary",
                confidence=82,
                reason="Liquidity for opportunities.",
                reference="7-8% returns, instant access",
            )
        )

        # ALTERNATIVE PLAN 1 (72% confidence) - Real Estate Focus
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Property-Oriented",
                "confidence": 72,
                "allocations": [
                    {
                        "asset_class": "real_estate",
                        "percent": 40,
                        "reason": "Real estate as primary wealth builder.",
                        "reference": "Colombo property appreciation 8-12% annually",
                    },
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 25,
                        "reason": "Equity growth component.",
                        "reference": "Stock market exposure",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 20,
                        "reason": "Liquid balanced allocation.",
                        "reference": "Easy to liquidate if needed",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 15,
                        "reason": "Cash buffer for property deals.",
                        "reference": "Quick access to capital",
                    },
                ],
            }
        )

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: x < 30), current_savings=P(lambda x: x < 100000)),
        InvestmentGoal(goal_type="Wealth Building"),
        salience=64,
    )
    def rule_beginner_investor(self):
        """
        RULE 16: Beginner Investor - Small Capital
        Young with limited savings, just starting investment journey
        Reference: https://www.investopedia.com/articles/younginvestors/08/eight-tips.asp
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 16",
                "rule_name": "Beginner Investor Portfolio",
                "salience": 64,
                "confidence": 85,
                "description": "Simple, low-cost portfolio for beginners",
                "condition": "Age < 30 AND Savings < LKR 100,000 AND Wealth Building goal",
                "action": "Primary: Start with unit trusts for diversification",
            }
        )

        # PRIMARY PLAN (85% confidence) - Simple & Diversified
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=60,
                plan_type="primary",
                confidence=85,
                reason="Best starter investment - instant diversification with professional management. Low minimum investment.",
                reference="Most balanced funds accept minimum LKR 5,000 - NDB, CAL, Softlogic",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=30,
                plan_type="primary",
                confidence=85,
                reason="Build emergency fund while earning better than savings account returns.",
                reference="7-8% returns with same-day liquidity",
            )
        )
        self.declare(
            Allocation(
                asset_class="savings_account",
                percent=10,
                plan_type="primary",
                confidence=85,
                reason="Instant access cash for true emergencies.",
                reference="Maintain 1 month expenses liquid",
            )
        )

        # ALTERNATIVE PLAN 1 (70% confidence) - Aggressive Learning
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Learn & Grow",
                "confidence": 70,
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 50,
                        "reason": "Learn equity investing through fund managers.",
                        "reference": "Higher growth potential for young investors",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 30,
                        "reason": "Core diversified holding.",
                        "reference": "Automatic rebalancing",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 20,
                        "reason": "Safety net while learning.",
                        "reference": "Reduce risk while gaining experience",
                    },
                ],
            }
        )

    @Rule(
        NOT(Allocation()),
        UserProfile(age=P(lambda x: 45 <= x < 55), risk_tolerance="Moderate"),
        InvestmentGoal(goal_type="Retirement", time_horizon=P(lambda x: 10 <= x < 15)),
        salience=72,
    )
    def rule_pre_retirement_planning(self):
        """
        RULE 17: Pre-Retirement Planning (10-15 years out)
        Age 45-55, planning for retirement in 10-15 years
        Reference: https://www.investopedia.com/retirement-planning-guide-4689695
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 17",
                "rule_name": "Pre-Retirement Accumulation",
                "salience": 72,
                "confidence": 83,
                "description": "Balanced growth with gradual shift to income",
                "condition": "Age 45-55 AND Moderate Risk AND Retirement goal (10-15 years)",
                "action": "Primary: 50% equity + 50% fixed income",
            }
        )

        # PRIMARY PLAN (83% confidence)
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=35,
                plan_type="primary",
                confidence=83,
                reason="Core balanced allocation for auto-diversification as you approach retirement.",
                reference="Ideal for pre-retirement phase",
            )
        )
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=83,
                reason="Continued equity exposure for growth, but measured.",
                reference="Still 10-15 years to ride out volatility",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=20,
                plan_type="primary",
                confidence=83,
                reason="Building fixed income base for retirement income.",
                reference="Bond funds 9-11% annual returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="government_bonds",
                percent=15,
                plan_type="primary",
                confidence=83,
                reason="Sovereign guaranteed returns as safety anchor.",
                reference="SLDB provides 11-13% secure returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                plan_type="primary",
                confidence=83,
                reason="Liquidity as you approach retirement.",
                reference="7-8% with instant access",
            )
        )

        # ALTERNATIVE PLAN 1 (75% confidence) - Income Focus
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Income-Oriented",
                "confidence": 75,
                "allocations": [
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 35,
                        "reason": "Maximum income generation focus.",
                        "reference": "Building retirement income stream",
                    },
                    {
                        "asset_class": "government_bonds",
                        "percent": 25,
                        "reason": "Government guaranteed returns.",
                        "reference": "11-13% sovereign bonds",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 25,
                        "reason": "Some growth potential.",
                        "reference": "Balanced approach",
                    },
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 15,
                        "reason": "Capital preservation increasing.",
                        "reference": "9-11% guaranteed returns",
                    },
                ],
            }
        )

        # ALTERNATIVE PLAN 2 (68% confidence) - Growth Extension
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 2: Extended Growth",
                "confidence": 68,
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 40,
                        "reason": "Higher equity if retirement well-funded.",
                        "reference": "Maximize growth if on track",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 30,
                        "reason": "Balanced core.",
                        "reference": "Automatic rebalancing",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 20,
                        "reason": "Income component.",
                        "reference": "Stable returns",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 10,
                        "reason": "Liquidity buffer.",
                        "reference": "Emergency access",
                    },
                ],
            }
        )

    @Rule(
        NOT(Allocation()),
        UserProfile(
            monthly_income=P(lambda x: x >= 150000),
            monthly_expenses=P(lambda x: x < 75000),
        ),
        InvestmentGoal(time_horizon=P(lambda x: x >= 5)),
        salience=62,
    )
    def rule_high_savings_rate(self):
        """
        RULE 18: High Savings Rate Investor
        High income with low expenses (50%+ savings rate)
        Reference: https://www.mrmoneymustache.com/2012/01/13/the-shockingly-simple-math-behind-early-retirement/
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 18",
                "rule_name": "High Savings Rate Accelerator",
                "salience": 62,
                "confidence": 80,
                "description": "Aggressive wealth building for high savers",
                "condition": "Monthly income ≥ LKR 150,000 AND Monthly expenses < LKR 75,000 (50%+ savings rate)",
                "action": "Primary: Maximize growth with diversification",
            }
        )

        # PRIMARY PLAN (80% confidence)
        self.declare(
            Allocation(
                asset_class="equity_unit_trusts",
                percent=35,
                plan_type="primary",
                confidence=80,
                reason="High savings rate allows aggressive equity allocation.",
                reference="Can weather volatility with continued contributions",
            )
        )
        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=25,
                plan_type="primary",
                confidence=80,
                reason="Balanced component for automatic risk management.",
                reference="Professional rebalancing",
            )
        )
        self.declare(
            Allocation(
                asset_class="cse_blue_chip_stocks",
                percent=15,
                plan_type="primary",
                confidence=80,
                reason="Direct stock ownership for dividend income stream.",
                reference="Blue chip dividends 3-5%",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=15,
                plan_type="primary",
                confidence=80,
                reason="Fixed income for stability.",
                reference="9-11% bond returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                plan_type="primary",
                confidence=80,
                reason="Liquidity to buy market dips.",
                reference="Keep powder dry for opportunities",
            )
        )

        # ALTERNATIVE PLAN 1 (73% confidence) - FIRE Strategy
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Financial Independence Path",
                "confidence": 73,
                "allocations": [
                    {
                        "asset_class": "equity_unit_trusts",
                        "percent": 45,
                        "reason": "Maximum equity for early retirement goal.",
                        "reference": "FIRE movement strategy",
                    },
                    {
                        "asset_class": "cse_blue_chip_stocks",
                        "percent": 20,
                        "reason": "Dividend income for future passive income.",
                        "reference": "Building income stream",
                    },
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 20,
                        "reason": "Balanced diversification.",
                        "reference": "Risk management",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 15,
                        "reason": "Income component.",
                        "reference": "Stability anchor",
                    },
                ],
            }
        )

    # ==================================================================================
    # PHASE 8: DEFAULT RULE (Lowest Priority)
    # ==================================================================================

    @Rule(NOT(Allocation()), salience=-10)
    def rule_default_recommendation(self):
        """
        RULE 19: Default Moderate Portfolio
        Fallback rule when no specific conditions are met
        Safe, balanced approach suitable for most investors
        Reference: https://www.investopedia.com/terms/b/balancedinvestmentstrategy.asp
        """
        self.fired_rules.append(
            {
                "rule_number": "Rule 19",
                "rule_name": "Default Balanced Portfolio",
                "salience": -10,
                "confidence": 75,
                "description": "Fallback balanced portfolio when no specific rules match",
                "condition": "No other rules matched",
                "action": "Allocate 60% Balanced Funds + 30% Income Funds + 10% Money Market",
            }
        )

        self.declare(
            Allocation(
                asset_class="balanced_unit_trusts",
                percent=60,
                plan_type="primary",
                confidence=75,
                reason="Balanced fund is the safest default - automatically maintains diversified portfolio.",
                reference="Default allocation: Balanced funds suitable for most investors - https://www.investopedia.com/ask/answers/021816/what-difference-between-targeted-and-balanced-mutual-fund.asp",
            )
        )
        self.declare(
            Allocation(
                asset_class="income_unit_trusts",
                percent=30,
                plan_type="primary",
                confidence=75,
                reason="Fixed income component for stability.",
                reference="Bond funds provide stable 9-11% annual returns",
            )
        )
        self.declare(
            Allocation(
                asset_class="money_market_funds",
                percent=10,
                plan_type="primary",
                confidence=75,
                reason="Liquidity buffer for emergencies.",
                reference="Money market funds: 7-8% with high liquidity",
            )
        )

        # ALTERNATIVE PLAN 1 (65% confidence) - Conservative Default
        self.alternative_plans.append(
            {
                "plan_name": "Alternative Plan 1: Conservative Default",
                "confidence": 65,
                "allocations": [
                    {
                        "asset_class": "balanced_unit_trusts",
                        "percent": 50,
                        "reason": "Reduced balanced allocation.",
                        "reference": "More conservative approach",
                    },
                    {
                        "asset_class": "income_unit_trusts",
                        "percent": 30,
                        "reason": "Same income allocation.",
                        "reference": "Stability focus",
                    },
                    {
                        "asset_class": "money_market_funds",
                        "percent": 15,
                        "reason": "Higher liquidity.",
                        "reference": "More cash available",
                    },
                    {
                        "asset_class": "fixed_deposits",
                        "percent": 5,
                        "reason": "Small guaranteed component.",
                        "reference": "Capital preservation",
                    },
                ],
            }
        )
