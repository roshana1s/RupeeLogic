import streamlit as st
import json
import pandas as pd
import plotly.express as px

from es.es import RupeeLogicEngine, UserProfile, InvestmentGoal, Allocation

# Set page config
st.set_page_config(
    page_title="RupeeLogic - Sri Lankan Investment Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_kb():
    """Loads the knowledge base and asset details."""
    with open("app/data/knowledge_base.json", "r") as f:
        return json.load(f)


# Load data
kb = load_kb()
asset_details = kb.get("asset_classes", {})

# --- Header ---
st.title("💰 RupeeLogic")
st.markdown("Expert Investment Portfolio Advisor for Sri Lanka")
st.markdown("---")

# --- Main Input Form ---
st.markdown("### � Enter Your Financial Information")

with st.form("investment_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Personal Details")
        age = st.number_input(
            "Your Age",
            min_value=18,
            max_value=80,
            value=30,
            step=1,
            help="Your current age",
        )

        monthly_income = st.number_input(
            "Monthly Income (LKR)",
            min_value=20000,
            max_value=5000000,
            value=150000,
            step=10000,
            help="Your monthly gross income",
        )

        monthly_expenses = st.number_input(
            "Monthly Expenses (LKR)",
            min_value=10000,
            max_value=1000000,
            value=75000,
            step=5000,
            help="Average monthly living expenses",
        )

        current_savings = st.number_input(
            "Current Savings (LKR)",
            min_value=0,
            max_value=100000000,
            value=500000,
            step=50000,
            help="Total savings for investment",
        )

        has_high_interest_debt = st.checkbox(
            "I have high-interest debt (Credit Cards > 15% p.a.)", value=False
        )

    with col2:
        st.markdown("#### Investment Goals")
        goal_type = st.selectbox(
            "Primary Investment Goal",
            options=[
                "Wealth Building",
                "Retirement",
                "Child Education",
                "Home Purchase",
                "Emergency Fund",
            ],
        )

        time_horizon = st.selectbox(
            "Investment Timeline",
            options=[
                "1-2 years (Short-term)",
                "3-5 years (Medium-term)",
                "6-10 years (Long-term)",
                "More than 10 years (Very Long-term)",
            ],
            index=2,
        )

        # Convert time horizon to years
        time_mapping = {
            "1-2 years (Short-term)": 2,
            "3-5 years (Medium-term)": 4,
            "6-10 years (Long-term)": 8,
            "More than 10 years (Very Long-term)": 15,
        }
        time_years = time_mapping[time_horizon]

        risk_tolerance = st.selectbox(
            "Risk Tolerance Level",
            options=["Low", "Moderate", "High"],
            index=1,
            help="How comfortable are you with market fluctuations?",
        )

    # Submit button
    submitted = st.form_submit_button(
        "🚀 Generate My Investment Portfolio", type="primary", use_container_width=True
    )

# Display calculated emergency fund status
emergency_fund_needed = monthly_expenses * 6
emergency_fund_status = (
    (current_savings / emergency_fund_needed * 100)
    if emergency_fund_needed > 0
    else 100
)

if submitted:

    with st.spinner(
        "Analyzing your financial profile and generating recommendations..."
    ):

        # 1. Initialize Engine
        engine = RupeeLogicEngine()
        engine.reset()

        # 2. Declare User Facts
        engine.declare(
            UserProfile(
                age=age,
                monthly_income=monthly_income,
                monthly_expenses=monthly_expenses,
                current_savings=current_savings,
                has_high_interest_debt=has_high_interest_debt,
                risk_tolerance=risk_tolerance,
            )
        )
        engine.declare(InvestmentGoal(goal_type=goal_type, time_horizon=time_years))

        # 3. Run Engine
        engine.run()

        # 4. Get Results
        allocations = [f for f in engine.facts.values() if isinstance(f, Allocation)]
        fired_rules = engine.fired_rules  # Get the list of fired rules

        st.markdown("---")
        st.markdown("# 🎯 Your Investment Recommendations")
        st.markdown("")

        if allocations:
            # Check for debt payment priority
            debt_payment = [
                a for a in allocations if a.get("asset_class") == "debt_payment"
            ]

            if debt_payment:
                st.error("### ⚠️ PRIORITY ACTION REQUIRED")
                st.markdown(
                    f"""
                **{debt_payment[0]['reason']}**
                
                **Why this matters:** {debt_payment[0]['reference']}
                
                **Recommended Action:**
                1. Stop new investments temporarily
                2. Pay off credit card balances completely
                3. Avoid accumulating new high-interest debt
                4. Return to this tool once debt-free for investment planning
                """
                )
                st.stop()

            # Create DataFrame for visualization
            chart_data = []
            detail_data = []

            for alloc in allocations:
                asset_class_key = alloc["asset_class"]
                asset_info = asset_details.get(asset_class_key, {})

                if asset_info:
                    chart_data.append(
                        {
                            "Asset Class": asset_info["name"],
                            "Allocation (%)": alloc["percent"],
                            "Risk": asset_info["risk"],
                            "Expected Return": asset_info.get(
                                "typical_return", asset_info["return"]
                            ),
                            "Liquidity": asset_info["liquidity"],
                        }
                    )

                    detail_data.append({"asset_info": asset_info, "allocation": alloc})

            df_chart = pd.DataFrame(chart_data)

            # Calculate monthly investment amount (income - expenses)
            monthly_investable = monthly_income - monthly_expenses

            # Sort by allocation percentage to find the primary recommendation
            df_sorted = df_chart.sort_values("Allocation (%)", ascending=False)

            # --- PRIMARY RECOMMENDATION ---
            st.markdown("## ✅ Best Recommendation for You")

            primary = df_sorted.iloc[0]
            primary_asset_key = allocations[0]["asset_class"]
            primary_details = next(
                (
                    item
                    for item in detail_data
                    if item["asset_info"]["name"] == primary["Asset Class"]
                ),
                None,
            )

            # Calculate rupee amounts
            primary_amount_current = (primary["Allocation (%)"] / 100) * current_savings
            primary_amount_monthly = (
                primary["Allocation (%)"] / 100
            ) * monthly_investable

            # Create prominent display for primary recommendation
            col_main1, col_main2 = st.columns([2, 1])

            with col_main1:
                st.markdown(f"### 🏆 {primary['Asset Class']}")
                st.markdown(
                    f"#### Allocate **{primary['Allocation (%)']}%** of your portfolio here"
                )

                # Show specific amounts
                st.success(
                    f"💰 **Invest LKR {primary_amount_current:,.0f}** from current savings"
                )
                if monthly_investable > 0:
                    st.success(
                        f"📅 **Add LKR {primary_amount_monthly:,.0f}/month** from your income"
                    )

                if primary_details:
                    st.info(f"**Why?** {primary_details['allocation']['reason']}")

                    # Show where to invest
                    st.markdown("**🏦 Where to Invest:**")
                    examples = primary_details["asset_info"].get("examples", "")
                    if isinstance(examples, list):
                        for ex in examples[:3]:  # Show top 3
                            st.markdown(f"✅ {ex}")
                    else:
                        st.markdown(f"✅ {examples}")

            with col_main2:
                st.markdown("**📊 Key Metrics**")
                st.metric("🔴 Risk Level", primary["Risk"])
                st.metric("📈 Expected Return", primary["Expected Return"])
                st.metric("💧 Liquidity", primary["Liquidity"])

            st.markdown("---")

            # --- ADDITIONAL RECOMMENDATIONS ---
            if len(df_sorted) > 1:
                st.markdown("## 📋 Additional Recommendations")
                st.markdown("Diversify your portfolio with these asset classes:")
                st.markdown("")

                for idx, row in df_sorted.iloc[1:].iterrows():
                    # Calculate amounts for this asset
                    asset_amount_current = (
                        row["Allocation (%)"] / 100
                    ) * current_savings
                    asset_amount_monthly = (
                        row["Allocation (%)"] / 100
                    ) * monthly_investable

                    col_a, col_b, col_c = st.columns([3, 2, 2])

                    with col_a:
                        st.markdown(
                            f"**{row['Asset Class']}** ({row['Allocation (%)']}%)"
                        )
                        asset_detail = next(
                            (
                                item
                                for item in detail_data
                                if item["asset_info"]["name"] == row["Asset Class"]
                            ),
                            None,
                        )
                        if asset_detail:
                            st.caption(asset_detail["allocation"]["reason"])

                    with col_b:
                        st.caption(
                            f"💰 From savings: **LKR {asset_amount_current:,.0f}**"
                        )
                        if monthly_investable > 0:
                            st.caption(
                                f"📅 Monthly: **LKR {asset_amount_monthly:,.0f}**"
                            )

                    with col_c:
                        st.caption(f"🔴 Risk: {row['Risk']}")
                        st.caption(f"📈 Return: {row['Expected Return']}")

                st.markdown("---")

            # --- PORTFOLIO SUMMARY ---
            st.markdown("## 📊 Complete Portfolio Overview")

            # Show investment summary
            st.info(
                f"""
            **💼 Your Investment Plan:**
            - 💰 **One-time Investment:** LKR {current_savings:,.0f} from current savings
            - 📅 **Monthly Investment:** LKR {monthly_investable:,.0f} ({monthly_income:,.0f} income - {monthly_expenses:,.0f} expenses)
            - 📈 **Total First Year:** LKR {(current_savings + (monthly_investable * 12)):,.0f}
            """
            )

            st.markdown("")

            col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)

            with col_sum1:
                st.metric("📁 Total Asset Classes", f"{len(allocations)}")

            with col_sum2:
                st.metric("⚡ Your Risk Level", risk_tolerance)

            with col_sum3:
                st.metric("⏰ Time Horizon", time_horizon)

            with col_sum4:
                # Calculate expected return range
                total_expected_low = 0
                total_expected_high = 0
                for alloc in allocations:
                    asset_info = asset_details.get(alloc["asset_class"], {})
                    typical_return = asset_info.get("typical_return", "0-0%")

                    # Parse typical return (e.g., "9-11%" or "10%")
                    if "-" in typical_return:
                        low, high = typical_return.replace("%", "").split("-")
                        total_expected_low += float(low) * alloc["percent"] / 100
                        total_expected_high += float(high) * alloc["percent"] / 100
                    else:
                        val = float(typical_return.replace("%", ""))
                        total_expected_low += val * alloc["percent"] / 100
                        total_expected_high += val * alloc["percent"] / 100

                st.metric(
                    "📈 Expected Return",
                    f"{total_expected_low:.1f}% - {total_expected_high:.1f}%",
                )

            st.markdown("")

            # --- Display Portfolio Table (without gradient) ---
            st.markdown("### 💼 Asset Allocation Breakdown")

            # Add rupee amounts to dataframe
            formatted_df = df_chart.copy()
            formatted_df["Amount from Savings (LKR)"] = formatted_df[
                "Allocation (%)"
            ].apply(lambda x: f"{(x/100 * current_savings):,.0f}")
            if monthly_investable > 0:
                formatted_df["Monthly Investment (LKR)"] = formatted_df[
                    "Allocation (%)"
                ].apply(lambda x: f"{(x/100 * monthly_investable):,.0f}")
            formatted_df["Allocation (%)"] = formatted_df["Allocation (%)"].apply(
                lambda x: f"{x}%"
            )

            st.dataframe(formatted_df, use_container_width=True, hide_index=True)

            st.markdown("---")

            # --- Display Portfolio Visualization ---
            col_left, col_right = st.columns([3, 2])

            with col_left:
                st.markdown("### 📊 Visual Portfolio Breakdown")

                # Create better pie chart
                fig = px.pie(
                    df_chart,
                    values="Allocation (%)",
                    names="Asset Class",
                    title="",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Bold,
                )
                fig.update_traces(
                    textposition="outside",
                    textinfo="label+percent",
                    textfont_size=14,
                    marker=dict(line=dict(color="white", width=2)),
                )
                fig.update_layout(
                    showlegend=False,
                    height=450,
                    font=dict(size=13, family="Arial"),
                    margin=dict(t=30, b=30, l=30, r=30),
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_right:
                st.markdown("### 📋 Allocation Summary")

                # Create allocation bars
                for _, row in df_chart.iterrows():
                    st.markdown(f"**{row['Asset Class']}**")
                    st.progress(int(row["Allocation (%)"]) / 100)
                    st.caption(
                        f"{row['Allocation (%)']}% • Risk: {row['Risk']} • Return: {row['Expected Return']}"
                    )
                    st.markdown("")

            st.markdown("---")

            # --- Display Detailed Asset Information in Expander ---
            with st.expander("📖 **View Detailed Asset Information**", expanded=False):
                st.markdown("Learn more about each recommended asset class:")
                st.markdown("")

                for idx, item in enumerate(detail_data, 1):
                    asset_info = item["asset_info"]
                    alloc = item["allocation"]

                    # Create card-like display for each asset
                    st.markdown(
                        f"#### {idx}. {asset_info['name']} • {alloc['percent']}%"
                    )

                    col_a, col_b = st.columns([3, 2])

                    with col_a:
                        st.markdown("**📖 What Is This?**")
                        st.write(asset_info["description"])

                        st.markdown("**📚 Investment Principle:**")
                        st.caption(alloc["reference"])

                    with col_b:
                        # Key metrics
                        st.markdown("**📊 Key Metrics**")
                        m1, m2 = st.columns(2)
                        with m1:
                            st.metric("🔴 Risk", asset_info["risk"])
                            st.metric("💧 Liquidity", asset_info["liquidity"])
                        with m2:
                            st.metric(
                                "📈 Return",
                                asset_info.get("typical_return", asset_info["return"]),
                            )
                            st.metric(
                                "💰 Min. Investment",
                                asset_info.get("min_investment", "Varies"),
                            )

                    # Where to invest section
                    st.markdown("**🏦 Where to Invest:**")

                    # Format examples nicely
                    examples = asset_info.get("examples", "")
                    if isinstance(examples, list):
                        # Create grid for multiple examples
                        num_examples = len(examples)
                        if num_examples <= 3:
                            cols = st.columns(num_examples)
                            for i, ex in enumerate(examples):
                                with cols[i]:
                                    st.success(f"✅ {ex}")
                        else:
                            # Split into two rows
                            ex_col1, ex_col2, ex_col3 = st.columns(3)
                            for i, ex in enumerate(examples):
                                target_col = [ex_col1, ex_col2, ex_col3][i % 3]
                                with target_col:
                                    st.success(f"✅ {ex}")
                    else:
                        st.success(f"✅ {examples}")

                    if idx < len(detail_data):
                        st.markdown("---")

            st.markdown("---")

            # --- EXPLAINABILITY SECTION (Collapsible) ---
            if fired_rules:
                with st.expander(
                    "🧠 **Why These Recommendations? (Expert System Reasoning)**",
                    expanded=False,
                ):
                    st.markdown(
                        "The expert system analyzed your profile using these decision rules:"
                    )
                    st.markdown("")

                    # Display fired rules in a clean format
                    for idx, rule in enumerate(fired_rules, 1):
                        col1, col2, col3 = st.columns([1, 3, 2])

                        with col1:
                            # Rule badge
                            st.markdown(f"### {rule['rule_number']}")
                            st.caption(f"Priority: {rule['salience']}")

                        with col2:
                            st.markdown(f"**{rule['rule_name']}**")
                            st.caption(rule["description"])

                            # Show condition
                            st.markdown("**✅ Condition Met:**")
                            st.info(rule["condition"])

                        with col3:
                            st.markdown("**⚡ Action Taken:**")
                            st.success(rule["action"])

                        if idx < len(fired_rules):
                            st.markdown("---")

            st.markdown("---")

            # --- Next Steps ---
            st.subheader("✅ Next Steps")
            st.markdown(
                """
            **To implement your portfolio:**
            
            1. **Open investment accounts** with recommended institutions
            2. **Start with minimum investments** to understand each product
            3. **Set up automatic monthly investments** (SIP) for unit trusts
            4. **Review portfolio quarterly** and rebalance annually
            5. **Consult a licensed financial advisor** for personalized guidance
            
            **Important Reminders:**
            - Past performance doesn't guarantee future returns
            - Diversification reduces but doesn't eliminate risk
            - Keep emergency fund (6 months expenses) in liquid assets
            - Review and adjust as your life circumstances change
            """
            )

            # --- Disclaimer ---
            st.markdown("---")
            st.caption(
                """
            **Disclaimer:** RupeeLogic is an educational expert system for investment guidance. 
            This is not personalized financial advice. Please consult licensed financial advisors 
            before making investment decisions. Investment values can go down as well as up. 
            Consider your personal circumstances and read product disclosure documents carefully.
            """
            )

        else:
            st.error(
                "Unable to generate portfolio recommendations. Please check your inputs and try again."
            )

else:
    # Show information when button hasn't been clicked
    st.info(
        "👆 Complete your financial profile in the sidebar and click the button above to get started!"
    )

    st.markdown("---")
    st.markdown("### 🎯 What RupeeLogic Does")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        **📊 Smart Analysis**
        
        Uses expert investment rules based on:
        - Your age and risk profile
        - Investment timeline
        - Financial goals
        - Current savings status
        """
        )

    with col2:
        st.markdown(
            """
        **🇱🇰 Sri Lankan Focus**
        
        Recommends real local options:
        - CSE stocks and ETFs
        - Unit Trusts (NDB, CAL, etc.)
        - Bank FDs and T-Bills
        - Government Bonds
        """
        )

    with col3:
        st.markdown(
            """
        **🎓 Educational**
        
        Learn while you invest:
        - Understand each asset class
        - See the reasoning behind recommendations
        - Get real product examples
        - Follow best practices
        """
        )
