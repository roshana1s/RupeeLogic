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
st.markdown("### 📋 Enter Your Financial Information")
st.info("💡 Leave fields empty to use assumptions where applicable.")

with st.form("investment_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Personal Details")
        age = st.number_input(
            "Your Age",
            min_value=18,
            max_value=80,
            value=None,
            step=1,
            help="Your current age (Default: 30 if not provided)",
            placeholder="e.g., 30",
        )

        monthly_income = st.number_input(
            "Monthly Income (LKR)",
            min_value=20000,
            max_value=5000000,
            value=None,
            step=10000,
            help="Your monthly gross income (Default: 150,000 if not provided)",
            placeholder="e.g., 150000",
        )

        monthly_expenses = st.number_input(
            "Monthly Expenses (LKR)",
            min_value=10000,
            max_value=1000000,
            value=None,
            step=5000,
            help="Average monthly living expenses (Default: 75,000 if not provided)",
            placeholder="e.g., 75000",
        )

        current_savings = st.number_input(
            "Current Savings (LKR)",
            min_value=0,
            max_value=100000000,
            value=None,
            step=50000,
            help="Total savings for investment (Default: 500,000 if not provided)",
            placeholder="e.g., 500000",
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
            help="Your primary investment goal (Default: Wealth Building)",
        )

        time_horizon = st.selectbox(
            "Investment Timeline",
            options=[
                "1-2 years (Short-term)",
                "3-5 years (Medium-term)",
                "6-10 years (Long-term)",
                "More than 10 years (Very Long-term)",
            ],
            index=None,
            help="How long do you plan to invest? (Default: 6-10 years if not selected)",
            placeholder="Select timeline...",
        )

        # Convert time horizon to years
        time_mapping = {
            "1-2 years (Short-term)": 2,
            "3-5 years (Medium-term)": 4,
            "6-10 years (Long-term)": 8,
            "More than 10 years (Very Long-term)": 15,
        }
        time_years = time_mapping.get(time_horizon) if time_horizon else None

        risk_tolerance = st.selectbox(
            "Risk Tolerance Level",
            options=["Low", "Moderate", "High"],
            index=None,
            help="How comfortable are you with market fluctuations? (Default: Moderate)",
            placeholder="Select risk level...",
        )

    # Submit button
    submitted = st.form_submit_button(
        "🚀 Generate My Investment Portfolio", type="primary", use_container_width=True
    )

# Display calculated emergency fund status (only if monthly_expenses is provided)
if monthly_expenses is not None:
    emergency_fund_needed = monthly_expenses * 6
    emergency_fund_status = (
        (current_savings / emergency_fund_needed * 100)
        if emergency_fund_needed > 0 and current_savings is not None
        else 0
    )
else:
    emergency_fund_needed = 0
    emergency_fund_status = 0

if submitted:

    with st.spinner(
        "Analyzing your financial profile and generating recommendations..."
    ):

        # ====== BACKEND DEFAULT VALUES ======
        # Apply defaults for any fields the user didn't fill
        DEFAULT_AGE = 30
        DEFAULT_MONTHLY_INCOME = 150000
        DEFAULT_MONTHLY_EXPENSES = 75000
        DEFAULT_CURRENT_SAVINGS = 500000
        DEFAULT_GOAL_TYPE = "Wealth Building"
        DEFAULT_TIME_YEARS = 8  # 6-10 years
        DEFAULT_RISK_TOLERANCE = "Moderate"

        # Apply defaults where user input is None
        final_age = age if age is not None else DEFAULT_AGE
        final_monthly_income = (
            monthly_income if monthly_income is not None else DEFAULT_MONTHLY_INCOME
        )
        final_monthly_expenses = (
            monthly_expenses
            if monthly_expenses is not None
            else DEFAULT_MONTHLY_EXPENSES
        )
        final_current_savings = (
            current_savings if current_savings is not None else DEFAULT_CURRENT_SAVINGS
        )
        final_goal_type = goal_type if goal_type else DEFAULT_GOAL_TYPE
        final_time_years = time_years if time_years is not None else DEFAULT_TIME_YEARS
        final_risk_tolerance = (
            risk_tolerance if risk_tolerance else DEFAULT_RISK_TOLERANCE
        )

        # Track which defaults were used for display
        defaults_used = []
        if age is None:
            defaults_used.append(f"Age: {DEFAULT_AGE}")
        if monthly_income is None:
            defaults_used.append(f"Monthly Income: LKR {DEFAULT_MONTHLY_INCOME:,}")
        if monthly_expenses is None:
            defaults_used.append(f"Monthly Expenses: LKR {DEFAULT_MONTHLY_EXPENSES:,}")
        if current_savings is None:
            defaults_used.append(f"Current Savings: LKR {DEFAULT_CURRENT_SAVINGS:,}")
        if not goal_type:
            defaults_used.append(f"Goal: {DEFAULT_GOAL_TYPE}")
        if time_years is None:
            defaults_used.append(f"Timeline: 6-10 years")
        if not risk_tolerance:
            defaults_used.append(f"Risk Tolerance: {DEFAULT_RISK_TOLERANCE}")

        # Show which defaults were applied
        if defaults_used:
            st.info(f"**ℹ️ Default values applied for:** {', '.join(defaults_used)}")

        # 1. Initialize Engine
        engine = RupeeLogicEngine()
        engine.reset()

        # 2. Declare User Facts (using final values with defaults applied)
        engine.declare(
            UserProfile(
                age=final_age,
                monthly_income=final_monthly_income,
                monthly_expenses=final_monthly_expenses,
                current_savings=final_current_savings,
                has_high_interest_debt=has_high_interest_debt,
                risk_tolerance=final_risk_tolerance,
            )
        )
        engine.declare(
            InvestmentGoal(goal_type=final_goal_type, time_horizon=final_time_years)
        )

        # 3. Run Engine
        engine.run()

        # 4. Get Results
        allocations = [f for f in engine.facts.values() if isinstance(f, Allocation)]
        alternative_allocations = engine.alternative_plans  # Get alternative plans
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
                
                **Why this matters:** {debt_payment[0]['reference']}**
                
                **Recommended Action:**
                1. Stop new investments temporarily
                2. Pay off credit card balances completely
                3. Avoid accumulating new high-interest debt
                4. Return to this tool once debt-free for investment planning
                """
                )
                st.stop()

            # Separate primary and alternative plans
            primary_allocations = [
                a for a in allocations if a.get("plan_type") == "primary"
            ]

            # Calculate monthly investment amount using final values
            monthly_investable = final_monthly_income - final_monthly_expenses

            # Determine display values for time horizon
            time_horizon_display = (
                time_horizon if time_horizon else "6-10 years (Long-term)"
            )

            # ========== INVESTMENT OVERVIEW ==========
            st.markdown("## 💼 Your Investment Overview")

            col_overview1, col_overview2, col_overview3 = st.columns(3)

            with col_overview1:
                st.metric("💰 Current Savings", f"LKR {final_current_savings:,.0f}")
                st.metric("📅 Monthly Investable", f"LKR {monthly_investable:,.0f}")

            with col_overview2:
                st.metric("⚡ Risk Tolerance", final_risk_tolerance)
                st.metric("🎯 Investment Goal", final_goal_type)

            with col_overview3:
                st.metric("⏰ Time Horizon", time_horizon_display)
                st.metric("🔢 Your Age", f"{final_age} years")

            st.markdown("---")

            # ========== PRIMARY PLAN ==========
            if primary_allocations:
                st.markdown("## 🎯 PRIMARY INVESTMENT PLAN")

                # Get confidence for primary plan
                primary_confidence = primary_allocations[0].get("confidence", 85)

                # Create data for primary plan
                primary_chart_data = []
                primary_detail_data = []

                for alloc in primary_allocations:
                    asset_class_key = alloc["asset_class"]
                    asset_info = asset_details.get(asset_class_key, {})

                    if asset_info:
                        primary_chart_data.append(
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
                        primary_detail_data.append(
                            {"asset_info": asset_info, "allocation": alloc}
                        )

                df_primary = pd.DataFrame(primary_chart_data)

                # Calculate expected returns
                total_expected_low = 0
                total_expected_high = 0
                for alloc in primary_allocations:
                    asset_info = asset_details.get(alloc["asset_class"], {})
                    typical_return = asset_info.get("typical_return", "0-0%")

                    # Skip non-numeric returns (N/A, etc.)
                    if typical_return == "N/A" or not typical_return:
                        continue

                    try:
                        if "-" in typical_return:
                            low, high = typical_return.replace("%", "").split("-")
                            total_expected_low += float(low) * alloc["percent"] / 100
                            total_expected_high += float(high) * alloc["percent"] / 100
                        else:
                            val = float(typical_return.replace("%", ""))
                            total_expected_low += val * alloc["percent"] / 100
                            total_expected_high += val * alloc["percent"] / 100
                    except (ValueError, AttributeError):
                        # Skip if conversion fails
                        continue

                # Show key highlights first
                st.success(
                    f"✅ **Confidence Level: {primary_confidence}%** - Our top recommended strategy for your profile"
                )

                col_highlight1, col_highlight2, col_highlight3 = st.columns(3)
                with col_highlight1:
                    st.metric("📊 Asset Classes", f"{len(primary_allocations)}")
                with col_highlight2:
                    st.metric(
                        "📈 Expected Annual Return",
                        f"{total_expected_low:.1f}% - {total_expected_high:.1f}%",
                    )
                with col_highlight3:
                    st.metric(
                        "💰 First Year Total",
                        f"LKR {(final_current_savings + monthly_investable * 12):,.0f}",
                    )

                st.markdown("")

                # Textual breakdown of investments
                st.markdown("### 📝 Investment Breakdown")
                for idx, item in enumerate(primary_detail_data, 1):
                    asset_info = item["asset_info"]
                    alloc = item["allocation"]

                    amount_from_savings = (
                        alloc["percent"] / 100
                    ) * final_current_savings
                    amount_monthly = (alloc["percent"] / 100) * monthly_investable

                    # Use different colored boxes for variety
                    if idx % 3 == 1:
                        st.info(
                            f"""
**{idx}. {asset_info['name']}** - {alloc['percent']}% of portfolio

💰 **Investment:** LKR {amount_from_savings:,.0f} from savings{f" + LKR {amount_monthly:,.0f}/month" if monthly_investable > 0 else ""}

📖 **What it is:** {asset_info['description']}

💡 **Why recommend:** {alloc['reason']}

🔴 **Risk:** {asset_info['risk']} | 📈 **Return:** {asset_info.get('typical_return', asset_info['return'])} | 💧 **Liquidity:** {asset_info['liquidity']}
                        """
                        )
                    elif idx % 3 == 2:
                        st.success(
                            f"""
**{idx}. {asset_info['name']}** - {alloc['percent']}% of portfolio

💰 **Investment:** LKR {amount_from_savings:,.0f} from savings{f" + LKR {amount_monthly:,.0f}/month" if monthly_investable > 0 else ""}

📖 **What it is:** {asset_info['description']}

💡 **Why recommend:** {alloc['reason']}

🔴 **Risk:** {asset_info['risk']} | 📈 **Return:** {asset_info.get('typical_return', asset_info['return'])} | 💧 **Liquidity:** {asset_info['liquidity']}
                        """
                        )
                    else:
                        st.warning(
                            f"""
**{idx}. {asset_info['name']}** - {alloc['percent']}% of portfolio

💰 **Investment:** LKR {amount_from_savings:,.0f} from savings{f" + LKR {amount_monthly:,.0f}/month" if monthly_investable > 0 else ""}

📖 **What it is:** {asset_info['description']}

💡 **Why recommend:** {alloc['reason']}

🔴 **Risk:** {asset_info['risk']} | 📈 **Return:** {asset_info.get('typical_return', asset_info['return'])} | 💧 **Liquidity:** {asset_info['liquidity']}
                        """
                        )

                st.markdown("")

                # Collapsible section for table and charts
                with st.expander("📊 **View Detailed Table & Charts**", expanded=True):
                    st.markdown("#### 💼 Asset Allocation Table")
                    formatted_df_primary = df_primary.copy()
                    formatted_df_primary["Amount from Savings (LKR)"] = (
                        formatted_df_primary["Allocation (%)"].apply(
                            lambda x: f"{(x/100 * final_current_savings):,.0f}"
                        )
                    )
                    if monthly_investable > 0:
                        formatted_df_primary["Monthly Investment (LKR)"] = (
                            formatted_df_primary["Allocation (%)"].apply(
                                lambda x: f"{(x/100 * monthly_investable):,.0f}"
                            )
                        )
                    formatted_df_primary["Allocation (%)"] = formatted_df_primary[
                        "Allocation (%)"
                    ].apply(lambda x: f"{x}%")

                    st.dataframe(
                        formatted_df_primary, use_container_width=True, hide_index=True
                    )

                    st.markdown("")

                    # Display primary plan chart
                    col_chart, col_summary = st.columns([3, 2])

                    with col_chart:
                        st.markdown("#### 📊 Portfolio Visualization")
                        fig_primary = px.pie(
                            df_primary,
                            values="Allocation (%)",
                            names="Asset Class",
                            title="",
                            hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Bold,
                        )
                        fig_primary.update_traces(
                            textposition="outside",
                            textinfo="label+percent",
                            textfont_size=14,
                            marker=dict(line=dict(color="white", width=2)),
                        )
                        fig_primary.update_layout(
                            showlegend=False,
                            height=450,
                            font=dict(size=13, family="Arial"),
                            margin=dict(t=30, b=30, l=30, r=30),
                        )
                        st.plotly_chart(fig_primary, use_container_width=True)

                    with col_summary:
                        st.markdown("#### 📋 Allocation Bars")
                        for _, row in df_primary.iterrows():
                            st.markdown(f"**{row['Asset Class']}**")
                            st.progress(int(row["Allocation (%)"]) / 100)
                            st.caption(
                                f"{row['Allocation (%)']}% • Risk: {row['Risk']}"
                            )
                            st.markdown("")

                # Where to invest section
                with st.expander(
                    "🏦 **Where to Invest (Banks & Providers)**",
                    expanded=False,
                ):
                    for idx, item in enumerate(primary_detail_data, 1):
                        asset_info = item["asset_info"]
                        alloc = item["allocation"]

                        st.markdown(
                            f"### {idx}. {asset_info['name']} ({alloc['percent']}%)"
                        )

                        col_a, col_b = st.columns([2, 1])

                        with col_a:
                            st.markdown(
                                f"**📝 Description:** {asset_info['description']}"
                            )
                            st.markdown(f"**💡 Why:** {alloc['reason']}")

                            st.markdown("**🏦 Where to Invest:**")
                            examples = asset_info.get("examples", "")
                            if isinstance(examples, list):
                                for ex in examples[:5]:
                                    st.markdown(f"- {ex}")
                            else:
                                st.markdown(f"- {examples}")

                            # Show provider links if available
                            provider_links = asset_info.get("provider_links", [])
                            if provider_links:
                                st.markdown("**🔗 Provider Links:**")
                                for provider in provider_links[:5]:
                                    st.markdown(
                                        f"- [{provider['name']}]({provider['url']})"
                                    )

                        with col_b:
                            st.metric("Risk Level", asset_info["risk"])
                            st.metric(
                                "Expected Return",
                                asset_info.get("typical_return", asset_info["return"]),
                            )
                            st.metric("Liquidity", asset_info["liquidity"])
                            st.metric(
                                "Min. Investment",
                                asset_info.get("min_investment", "N/A"),
                            )

                        if idx < len(primary_detail_data):
                            st.markdown("---")

                st.markdown("---")
                st.markdown("")

            # ========== ALTERNATIVE PLANS ==========
            if alternative_allocations and len(alternative_allocations) > 0:
                st.markdown("## 🔄 ALTERNATIVE INVESTMENT PLANS")
                st.markdown(
                    "Consider these alternative strategies based on different assumptions:"
                )
                st.markdown("")

                for plan_idx, alt_plan in enumerate(alternative_allocations, 1):
                    with st.expander(
                        f"🔹 **Alternative Plan {plan_idx}** - Click to view details",
                        expanded=False,
                    ):
                        # Get confidence
                        plan_confidence = alt_plan.get("confidence", 70)
                        st.success(
                            f"**Confidence Level: {plan_confidence}%** - {alt_plan.get('description', 'Alternative strategy')}"
                        )

                        # Create data for this alternative plan
                        alt_chart_data = []
                        alt_detail_data = []

                        for alloc in alt_plan.get("allocations", []):
                            asset_class_key = alloc["asset_class"]
                            asset_info = asset_details.get(asset_class_key, {})

                            if asset_info:
                                alt_chart_data.append(
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
                                alt_detail_data.append(
                                    {"asset_info": asset_info, "allocation": alloc}
                                )

                        df_alt = pd.DataFrame(alt_chart_data)

                        # Calculate expected returns for this alt plan
                        alt_expected_low = 0
                        alt_expected_high = 0
                        for alloc in alt_plan.get("allocations", []):
                            asset_info = asset_details.get(alloc["asset_class"], {})
                            typical_return = asset_info.get("typical_return", "0-0%")

                            # Skip non-numeric returns
                            if typical_return == "N/A" or not typical_return:
                                continue

                            try:
                                if "-" in typical_return:
                                    low, high = typical_return.replace("%", "").split(
                                        "-"
                                    )
                                    alt_expected_low += (
                                        float(low) * alloc["percent"] / 100
                                    )
                                    alt_expected_high += (
                                        float(high) * alloc["percent"] / 100
                                    )
                                else:
                                    val = float(typical_return.replace("%", ""))
                                    alt_expected_low += val * alloc["percent"] / 100
                                    alt_expected_high += val * alloc["percent"] / 100
                            except (ValueError, AttributeError):
                                continue

                        # Key metrics for this alternative
                        col_alt1, col_alt2, col_alt3 = st.columns(3)
                        with col_alt1:
                            st.metric("📊 Asset Classes", f"{len(alt_detail_data)}")
                        with col_alt2:
                            st.metric(
                                "📈 Expected Return",
                                f"{alt_expected_low:.1f}% - {alt_expected_high:.1f}%",
                            )
                        with col_alt3:
                            st.metric(
                                "💰 First Year Total",
                                f"LKR {(final_current_savings + monthly_investable * 12):,.0f}",
                            )

                        st.markdown("")

                        # Textual breakdown
                        st.markdown("#### 📝 Investment Breakdown")
                        for idx, item in enumerate(alt_detail_data, 1):
                            asset_info = item["asset_info"]
                            alloc = item["allocation"]

                            amount_from_savings = (
                                alloc["percent"] / 100
                            ) * final_current_savings
                            amount_monthly = (
                                alloc["percent"] / 100
                            ) * monthly_investable

                            st.info(
                                f"""
**{idx}. {asset_info['name']}** - {alloc['percent']}% of portfolio

💰 **Investment:** LKR {amount_from_savings:,.0f} from savings{f" + LKR {amount_monthly:,.0f}/month" if monthly_investable > 0 else ""}

📖 **What it is:** {asset_info['description']}

💡 **Why recommend:** {alloc['reason']}

🔴 **Risk:** {asset_info['risk']} | 📈 **Return:** {asset_info.get('typical_return', asset_info['return'])} | 💧 **Liquidity:** {asset_info['liquidity']}
                            """
                            )

                        st.markdown("")

                        # Table and charts in nested expander
                        with st.expander("📊 **View Table & Charts**", expanded=False):
                            st.markdown("#### Asset Allocation Table")
                            formatted_df_alt = df_alt.copy()
                            formatted_df_alt["Amount from Savings (LKR)"] = (
                                formatted_df_alt["Allocation (%)"].apply(
                                    lambda x: f"{(x/100 * final_current_savings):,.0f}"
                                )
                            )
                            if monthly_investable > 0:
                                formatted_df_alt[
                                    "Monthly Investment (LKR)"
                                ] = formatted_df_alt["Allocation (%)"].apply(
                                    lambda x: f"{(x/100 * monthly_investable):,.0f}"
                                )
                            formatted_df_alt["Allocation (%)"] = formatted_df_alt[
                                "Allocation (%)"
                            ].apply(lambda x: f"{x}%")

                            st.dataframe(
                                formatted_df_alt,
                                use_container_width=True,
                                hide_index=True,
                            )

                            st.markdown("")

                            # Display alternative plan chart
                            col_alt_chart, col_alt_summary = st.columns([3, 2])

                            with col_alt_chart:
                                st.markdown("#### 📊 Portfolio Visualization")
                                fig_alt = px.pie(
                                    df_alt,
                                    values="Allocation (%)",
                                    names="Asset Class",
                                    title="",
                                    hole=0.4,
                                    color_discrete_sequence=px.colors.qualitative.Pastel,
                                )
                                fig_alt.update_traces(
                                    textposition="outside",
                                    textinfo="label+percent",
                                    textfont_size=14,
                                    marker=dict(line=dict(color="white", width=2)),
                                )
                                fig_alt.update_layout(
                                    showlegend=False,
                                    height=400,
                                    font=dict(size=13, family="Arial"),
                                    margin=dict(t=30, b=30, l=30, r=30),
                                )
                                st.plotly_chart(fig_alt, use_container_width=True)

                            with col_alt_summary:
                                st.markdown("#### 📋 Allocation Bars")
                                for _, row in df_alt.iterrows():
                                    st.markdown(f"**{row['Asset Class']}**")
                                    st.progress(int(row["Allocation (%)"]) / 100)
                                    st.caption(
                                        f"{row['Allocation (%)']}% • Risk: {row['Risk']}"
                                    )
                                    st.markdown("")

                        # Provider information
                        with st.expander("🏦 **Where to Invest**", expanded=False):
                            for idx, item in enumerate(alt_detail_data, 1):
                                asset_info = item["asset_info"]

                                st.markdown(f"**{idx}. {asset_info['name']}**")

                                examples = asset_info.get("examples", "")
                                if isinstance(examples, list):
                                    for ex in examples[:5]:
                                        st.markdown(f"- {ex}")
                                else:
                                    st.markdown(f"- {examples}")

                                provider_links = asset_info.get("provider_links", [])
                                if provider_links:
                                    st.markdown("**🔗 Provider Links:**")
                                    for provider in provider_links[:5]:
                                        st.markdown(
                                            f"- [{provider['name']}]({provider['url']})"
                                        )

                                if idx < len(alt_detail_data):
                                    st.markdown("---")

                st.markdown("---")
                st.markdown("")

            # ========== OVERALL SUMMARY ==========
            st.markdown("## 📊 Investment Summary")

            # Calculate stats for primary plan
            if primary_allocations:
                df_chart = df_primary  # Use primary plan for overall metrics
                detail_data = primary_detail_data
            else:
                # Fallback if no primary plan
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
                        detail_data.append(
                            {"asset_info": asset_info, "allocation": alloc}
                        )
                df_chart = pd.DataFrame(chart_data)

            # Show investment summary
            st.info(
                f"""
            **💼 Your Investment Plan:**
            - 💰 **One-time Investment:** LKR {final_current_savings:,.0f} from current savings
            - 📅 **Monthly Investment:** LKR {monthly_investable:,.0f} ({final_monthly_income:,.0f} income - {final_monthly_expenses:,.0f} expenses)
            - 📈 **Total First Year:** LKR {(final_current_savings + (monthly_investable * 12)):,.0f}
            """
            )

            st.markdown("")

            col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)

            with col_sum1:
                st.metric(
                    "📁 Total Asset Classes",
                    f"{len(primary_allocations) if primary_allocations else len(allocations)}",
                )

            with col_sum2:
                st.metric("⚡ Your Risk Level", final_risk_tolerance)

            with col_sum3:
                st.metric("⏰ Time Horizon", time_horizon_display)

            with col_sum4:
                # Calculate expected return range for primary plan
                total_expected_low = 0
                total_expected_high = 0
                plan_allocs = (
                    primary_allocations if primary_allocations else allocations
                )
                for alloc in plan_allocs:
                    asset_info = asset_details.get(alloc["asset_class"], {})
                    typical_return = asset_info.get("typical_return", "0-0%")

                    # Skip non-numeric returns
                    if typical_return == "N/A" or not typical_return:
                        continue

                    try:
                        # Parse typical return (e.g., "9-11%" or "10%")
                        if "-" in typical_return:
                            low, high = typical_return.replace("%", "").split("-")
                            total_expected_low += float(low) * alloc["percent"] / 100
                            total_expected_high += float(high) * alloc["percent"] / 100
                        else:
                            val = float(typical_return.replace("%", ""))
                            total_expected_low += val * alloc["percent"] / 100
                            total_expected_high += val * alloc["percent"] / 100
                    except (ValueError, AttributeError):
                        continue

                st.metric(
                    "📈 Expected Return",
                    f"{total_expected_low:.1f}% - {total_expected_high:.1f}%",
                )

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
