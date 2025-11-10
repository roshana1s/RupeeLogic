import streamlit as st
import json

from es.es import RupeeLogicEngine, UserProfile, InvestmentGoal, Allocation
from core.config import config

# Page configuration
st.title("💬 RupeeLogic Chat Assistant")
st.markdown("Ask me about your investment portfolio in natural language!")


# Load knowledge base
@st.cache_data
def load_knowledge_base():
    with open("app/data/knowledge_base.json", "r") as f:
        return json.load(f)


knowledge_base = load_knowledge_base()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your RupeeLogic investment advisor. I'll help you create a personalized investment portfolio for Sri Lanka. \n\nTo get started, I need to know:\n- Your age\n- Your monthly income\n- Your monthly expenses\n- Your current savings\n- Whether you have high-interest debt\n- Your investment goal (Wealth Building, Retirement, Child Education, Home Purchase, or Emergency Fund)\n- Your investment timeline\n- Your risk tolerance (Low, Moderate, or High)\n\nFeel free to share this information in your own words!",
        }
    ]

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "age": None,
        "monthly_income": None,
        "monthly_expenses": None,
        "current_savings": None,
        "has_high_interest_debt": None,
        "goal_type": None,
        "time_horizon": None,
        "risk_tolerance": None,
    }

if "recommendation_generated" not in st.session_state:
    st.session_state.recommendation_generated = False

if "recommendation_context" not in st.session_state:
    st.session_state.recommendation_context = None

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Tell me about your financial situation..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if this is a follow-up question after recommendation
    if (
        st.session_state.recommendation_generated
        and st.session_state.recommendation_context
    ):
        # Handle follow-up questions about the recommendation
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    followup_prompt = f"""
                        You are a financial advisor assistant answering follow-up questions about an investment recommendation.

                        IMPORTANT INSTRUCTIONS:
                        - ONLY answer questions related to investment, finance, and the Sri Lankan investment market
                        - DO NOT answer questions outside the investment/finance domain
                        - DO NOT hallucinate or make up information
                        - ONLY use the information provided in the recommendation context below
                        - If asked about something not in the context, politely say you can only discuss the provided recommendations
                        - If asked a non-finance question, politely redirect to investment topics

                        User's Profile:
                        {json.dumps(st.session_state.user_data, indent=2)}

                        Recommendation Context (Expert System Output):
                        {st.session_state.recommendation_context}

                        User's follow-up question: {prompt}

                        Provide a clear, helpful answer based ONLY on the information above. Do not make assumptions or add information not present in the context.
                        """.strip()

                    messages = [
                        {
                            "role": "system",
                            "content": "You are a professional Sri Lankan investment advisor. Answer questions based ONLY on the provided context. Do not hallucinate. Stay strictly within the investment/finance domain.",
                        },
                        {"role": "user", "content": followup_prompt},
                    ]

                    answer = config.chat_llm(messages)
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )

                except Exception as e:
                    error_message = (
                        f"I encountered an error: {str(e)}. Please try again."
                    )
                    st.error(error_message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_message}
                    )
    else:
        # Extract information using GPT-4o-mini
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your information..."):
                # Create system prompt for information extraction
                system_prompt = f"""
                    You are a financial advisor assistant helping users fill out their investment profile. 

                    IMPORTANT INSTRUCTIONS:
                    - ONLY respond to questions about investments and personal finance
                    - DO NOT answer questions outside the investment/finance domain
                    - If user asks non-finance questions, politely redirect them to investment topics

                    Current user data collected:
                    {json.dumps(st.session_state.user_data, indent=2)}

                    Your tasks:
                    1. Extract ANY financial information from the user's message and update the relevant fields
                    2. Check which fields are still missing (have None values)
                    3. If all required fields are filled, indicate that you're ready to generate recommendations
                    4. If fields are missing, ask for the missing information in a friendly way
                    5. If user asks non-investment questions, politely say you can only help with investment advice

                    Field descriptions:
                    - age: User's age (integer between 18-80)
                    - monthly_income: Monthly income in LKR (integer)
                    - monthly_expenses: Monthly expenses in LKR (integer)
                    - current_savings: Total savings in LKR (integer)
                    - has_high_interest_debt: Whether they have credit card debt > 15% APR (true/false)
                    - goal_type: One of: "Wealth Building", "Retirement", "Child Education", "Home Purchase", "Emergency Fund"
                    - time_horizon: Investment timeline in years (integer, 1-20+)
                    - risk_tolerance: One of: "Low", "Moderate", "High"

                    Respond in JSON format:
                    {{
                        "extracted_data": {{"field_name": value}},  // Only include fields you extracted from user message
                        "updated_user_data": {{...}},  // Complete user data with updates
                        "missing_fields": ["field1", "field2"],  // List of fields that are still None
                        "all_fields_complete": true/false,
                        "message_to_user": "Your friendly response asking for missing info or confirming you'll generate recommendations"
                    }}

                User message: {prompt}
                """.strip()

                try:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ]

                    result = config.chat_llm_json(messages)

                    # Update user data with extracted information
                    if "updated_user_data" in result:
                        st.session_state.user_data.update(result["updated_user_data"])

                    # Display assistant response
                    assistant_message = result.get(
                        "message_to_user", "Let me help you with that."
                    )
                    st.markdown(assistant_message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_message}
                    )

                    # If all fields are complete, run the expert system
                    if (
                        result.get("all_fields_complete", False)
                        and not st.session_state.recommendation_generated
                    ):
                        st.session_state.recommendation_generated = True

                        # Run expert system
                        with st.spinner("Running expert system analysis..."):
                            engine = RupeeLogicEngine()
                            engine.reset()

                            # Declare facts
                            engine.declare(
                                UserProfile(
                                    age=st.session_state.user_data["age"],
                                    monthly_income=st.session_state.user_data[
                                        "monthly_income"
                                    ],
                                    monthly_expenses=st.session_state.user_data[
                                        "monthly_expenses"
                                    ],
                                    current_savings=st.session_state.user_data[
                                        "current_savings"
                                    ],
                                    has_high_interest_debt=st.session_state.user_data[
                                        "has_high_interest_debt"
                                    ],
                                    risk_tolerance=st.session_state.user_data[
                                        "risk_tolerance"
                                    ],
                                )
                            )
                            engine.declare(
                                InvestmentGoal(
                                    goal_type=st.session_state.user_data["goal_type"],
                                    time_horizon=st.session_state.user_data[
                                        "time_horizon"
                                    ],
                                )
                            )

                            # Run engine
                            engine.run()

                            # Get allocations and fired rules
                            allocations = [
                                f
                                for f in engine.facts.values()
                                if isinstance(f, Allocation)
                            ]
                            fired_rules = engine.fired_rules
                            alternative_plans = engine.alternative_plans

                            # Get asset details
                            asset_details = knowledge_base["asset_classes"]

                            # Prepare PRIMARY PLAN data for LLM
                            primary_allocations = [
                                a
                                for a in allocations
                                if a.get("plan_type") == "primary"
                            ]
                            if not primary_allocations:  # Fallback for old rules
                                primary_allocations = allocations

                            primary_plan_summary = []
                            for alloc in primary_allocations:
                                asset_info = asset_details.get(alloc["asset_class"], {})
                                primary_plan_summary.append(
                                    {
                                        "asset_class": asset_info.get(
                                            "name", alloc["asset_class"]
                                        ),
                                        "percentage": alloc["percent"],
                                        "confidence": alloc.get("confidence", 85),
                                        "reason": alloc.get("reason", ""),
                                        "reference": alloc.get("reference", ""),
                                        "risk": asset_info.get("risk", ""),
                                        "return": asset_info.get(
                                            "typical_return",
                                            asset_info.get("return", ""),
                                        ),
                                        "examples": asset_info.get("examples", ""),
                                    }
                                )

                            # Prepare ALTERNATIVE PLANS data
                            alternative_plans_summary = []
                            for alt_plan in alternative_plans:
                                plan_allocations = []
                                for alloc in alt_plan["allocations"]:
                                    asset_info = asset_details.get(
                                        alloc["asset_class"], {}
                                    )
                                    plan_allocations.append(
                                        {
                                            "asset_class": asset_info.get(
                                                "name", alloc["asset_class"]
                                            ),
                                            "percentage": alloc["percent"],
                                            "reason": alloc.get("reason", ""),
                                            "reference": alloc.get("reference", ""),
                                            "risk": asset_info.get("risk", ""),
                                            "return": asset_info.get(
                                                "typical_return",
                                                asset_info.get("return", ""),
                                            ),
                                            "examples": asset_info.get("examples", ""),
                                        }
                                    )
                                alternative_plans_summary.append(
                                    {
                                        "plan_name": alt_plan["plan_name"],
                                        "confidence": alt_plan["confidence"],
                                        "allocations": plan_allocations,
                                    }
                                )

                            # Calculate investment amounts
                            monthly_investable = (
                                st.session_state.user_data["monthly_income"]
                                - st.session_state.user_data["monthly_expenses"]
                            )

                            # Store recommendation context for follow-up questions
                            st.session_state.recommendation_context = {
                                "user_profile": st.session_state.user_data,
                                "monthly_investable": monthly_investable,
                                "fired_rules": fired_rules,
                                "primary_plan": primary_plan_summary,
                                "alternative_plans": alternative_plans_summary,
                            }

                            # Generate final recommendation using GPT
                            recommendation_prompt = f"""
                                You are a professional financial advisor. Generate a comprehensive, user-friendly investment recommendation report.

                                IMPORTANT INSTRUCTIONS:
                                - Base your recommendations ONLY on the data provided below
                                - DO NOT add information not present in the expert system output
                                - DO NOT hallucinate or make assumptions
                                - Show the PRIMARY PLAN with its confidence level FIRST
                                - Then show ALTERNATIVE PLANS if available

                                User Profile:
                                {json.dumps(st.session_state.user_data, indent=2)}

                                Monthly Investable Amount: LKR {monthly_investable:,}

                                Expert System Recommendations (Rules that fired):
                                {json.dumps(fired_rules, indent=2)}

                                PRIMARY INVESTMENT PLAN (Recommended - {primary_plan_summary[0]["confidence"] if primary_plan_summary else 85}% Confidence):
                                {json.dumps(primary_plan_summary, indent=2)}

                                ALTERNATIVE INVESTMENT PLANS (Optional):
                                {json.dumps(alternative_plans_summary, indent=2)}

                                Create a detailed recommendation report in markdown format with:

                                1. **Executive Summary** - Brief overview with confidence level
                                
                                2. **🎯 PRIMARY INVESTMENT PLAN (Recommended - XX% Confidence)**
                                   - Show this plan prominently as the main recommendation
                                   - Specific LKR amounts for each asset (from savings and monthly)
                                   - Why this plan is recommended
                                   - Risk levels and expected returns
                                   - Where to invest (specific institutions)
                                
                                3. **🔄 ALTERNATIVE INVESTMENT PLANS** (if available)
                                   - Show each alternative plan with its confidence level
                                   - Explain when to consider each alternative
                                   - Specific allocations for each alternative
                                
                                4. **Expert System Reasoning** - Explain which rules fired and why
                                
                                5. **Important Reminders** - Key investment principles

                            Use proper markdown formatting with headers, bullet points, bold text, and tables where appropriate.
                            Make it very user-friendly and easy to understand.
                            Clearly differentiate between PRIMARY and ALTERNATIVE plans.
                            """.strip()

                            messages = [
                                {
                                    "role": "system",
                                    "content": "You are a professional Sri Lankan investment advisor. Provide clear, actionable advice with specific LKR amounts based ONLY on the provided expert system data. Do not hallucinate.",
                                },
                                {"role": "user", "content": recommendation_prompt},
                            ]

                            final_recommendation = config.chat_llm(messages)

                            # Display the recommendation
                            st.markdown("---")
                            st.markdown(final_recommendation)
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": f"---\n{final_recommendation}",
                                }
                            )

                            # Add option to ask follow-up questions
                            st.markdown("---")
                            st.info(
                                "💡 Feel free to ask any follow-up questions about your portfolio!"
                            )

                except Exception as e:
                    error_message = (
                        f"I encountered an error: {str(e)}. Please try again."
                    )
                    st.error(error_message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_message}
                    )

# Sidebar - show collected data
with st.sidebar:
    st.markdown("### 📊 Collected Information")

    for key, value in st.session_state.user_data.items():
        if value is not None:
            display_key = key.replace("_", " ").title()
            if isinstance(value, bool):
                display_value = "Yes" if value else "No"
            elif isinstance(value, (int, float)) and key in [
                "monthly_income",
                "monthly_expenses",
                "current_savings",
            ]:
                display_value = f"LKR {value:,}"
            else:
                display_value = str(value)
            st.success(f"**{display_key}:** {display_value}")
        else:
            display_key = key.replace("_", " ").title()
            st.warning(f"**{display_key}:** Not provided")

    if st.button("🔄 Clear Chat & Start New"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your RupeeLogic investment advisor. I'll help you create a personalized investment portfolio for Sri Lanka. \n\nTo get started, I need to know:\n- Your age\n- Your monthly income\n- Your monthly expenses\n- Your current savings\n- Whether you have high-interest debt\n- Your investment goal (Wealth Building, Retirement, Child Education, Home Purchase, or Emergency Fund)\n- Your investment timeline\n- Your risk tolerance (Low, Moderate, or High)\n\nFeel free to share this information in your own words!",
            }
        ]
        st.session_state.user_data = {
            "age": None,
            "monthly_income": None,
            "monthly_expenses": None,
            "current_savings": None,
            "has_high_interest_debt": None,
            "goal_type": None,
            "time_horizon": None,
            "risk_tolerance": None,
        }
        st.session_state.recommendation_generated = False
        st.session_state.recommendation_context = None
        st.rerun()
