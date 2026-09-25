import streamlit as st
from main import run_agent


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Autonomous Travel Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background: #f4f7fb;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ============================================================
   STREAMLIT TEXT VISIBILITY FIX
   ============================================================ */

/* Normal Streamlit markdown */
.stMarkdown {
    color: #0f172a !important;
}

.stMarkdown p {
    color: #334155 !important;
}

/* Headings */
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4,
.stMarkdown h5,
.stMarkdown h6 {
    color: #0f172a !important;
    font-weight: 800 !important;
}

/* Streamlit metrics */
[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

[data-testid="stMetricValue"] {
    color: #0f172a !important;
}

[data-testid="stMetricDelta"] {
    color: #475569 !important;
}

/* Expanders */
[data-testid="stExpander"] summary {
    color: #0f172a !important;
}

[data-testid="stExpander"] summary p {
    color: #0f172a !important;
}

/* Alerts */
[data-testid="stAlert"] {
    color: #0f172a !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    background: linear-gradient(
        135deg,
        #071a3d 0%,
        #0d2d66 55%,
        #1769aa 100%
    );

    border-radius: 26px;
    padding: 48px;

    color: white;

    box-shadow:
        0 20px 50px rgba(7, 26, 61, 0.20);

    margin-bottom: 30px;
}

.hero-badge {
    display: inline-block;

    background: rgba(255,255,255,0.12);

    border: 1px solid rgba(255,255,255,0.20);

    border-radius: 999px;

    padding: 7px 14px;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1px;

    margin-bottom: 18px;

    color: white;
}

.hero-title {
    font-size: 42px;

    font-weight: 800;

    line-height: 1.12;

    letter-spacing: -1px;

    color: white;
}

.hero-text {
    color: #dbeafe;

    font-size: 16px;

    line-height: 1.7;

    max-width: 850px;

    margin-top: 15px;
}


/* ============================================================
   SEARCH
   ============================================================ */

.search-card {
    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 20px;

    padding: 28px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);

    margin-bottom: 14px;
}

.search-title {
    font-size: 23px;

    font-weight: 800;

    color: #0f172a;
}

.search-subtitle {
    color: #64748b;

    font-size: 14px;

    margin-top: 5px;
}


/* ============================================================
   AGENT EXECUTION TIMELINE
   ============================================================ */

.agent-timeline {
    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 20px;

    padding: 24px;

    margin: 24px 0;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);
}

.timeline-header {
    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 20px;

    margin-bottom: 18px;
}

.timeline-title {
    font-size: 20px;

    font-weight: 800;

    color: #0f172a;
}

.timeline-subtitle {
    color: #64748b;

    font-size: 13px;

    margin-top: 5px;
}

.timeline-status {
    background: #ecfdf5;

    color: #047857;

    border: 1px solid #a7f3d0;

    border-radius: 999px;

    padding: 7px 13px;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 0.5px;

    white-space: nowrap;
}

.timeline-item {
    display: flex;

    align-items: center;

    gap: 14px;

    padding: 15px 12px;

    border-top: 1px solid #f1f5f9;
}

.timeline-number {
    width: 30px;

    height: 30px;

    border-radius: 50%;

    background: #eff6ff;

    color: #2563eb;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 12px;

    font-weight: 800;

    flex-shrink: 0;
}

.timeline-icon {
    width: 42px;

    height: 42px;

    border-radius: 12px;

    background: #f8fafc;

    border: 1px solid #e2e8f0;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 20px;

    flex-shrink: 0;
}

.timeline-content {
    flex: 1;
}

.timeline-step-title {
    font-size: 14px;

    font-weight: 750;

    color: #0f172a;
}

.timeline-description {
    font-size: 12px;

    color: #64748b;

    margin-top: 3px;

    line-height: 1.5;
}

.timeline-check {
    color: #059669;

    font-size: 18px;

    font-weight: 800;
}


/* ============================================================
   FLIGHT CARD
   ============================================================ */

.flight-card {
    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 18px;

    padding: 26px;

    margin-bottom: 16px;

    box-shadow:
        0 5px 18px rgba(15,23,42,0.05);
}

.flight-card:hover {
    box-shadow:
        0 10px 25px rgba(15,23,42,0.08);
}

.airline {
    font-size: 20px;

    font-weight: 800;

    color: #0f172a;
}

.flight-number {
    color: #64748b;

    font-size: 13px;

    margin-top: 3px;
}

.time {
    font-size: 25px;

    font-weight: 800;

    color: #0f172a;
}

.flight-price {
    font-size: 25px;

    font-weight: 800;

    color: #0f172a;

    text-align: right;
}

.per-passenger {
    color: #94a3b8;

    font-size: 11px;

    text-align: right;
}


/* ============================================================
   BADGES
   ============================================================ */

.badge-green {
    display: inline-block;

    background: #ecfdf5;

    color: #047857;

    border: 1px solid #a7f3d0;

    padding: 5px 10px;

    border-radius: 999px;

    font-size: 11px;

    font-weight: 700;

    margin-right: 5px;
}

.badge-blue {
    display: inline-block;

    background: #eff6ff;

    color: #1d4ed8;

    border: 1px solid #bfdbfe;

    padding: 5px 10px;

    border-radius: 999px;

    font-size: 11px;

    font-weight: 700;

    margin-right: 5px;
}

.badge-gray {
    display: inline-block;

    background: #f8fafc;

    color: #475569;

    border: 1px solid #e2e8f0;

    padding: 5px 10px;

    border-radius: 999px;

    font-size: 11px;

    font-weight: 700;
}


/* ============================================================
   RECOMMENDATION
   ============================================================ */

.recommendation {
    background: linear-gradient(
        135deg,
        #ffffff,
        #eff6ff
    );

    border: 1px solid #93c5fd;

    border-radius: 22px;

    padding: 28px;

    margin-top: 12px;

    box-shadow:
        0 12px 35px rgba(37,99,235,0.10);
}

.recommendation-tag {
    color: #2563eb;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.2px;

    margin-bottom: 8px;
}

.recommendation-airline {
    font-size: 29px;

    font-weight: 850;

    color: #0f172a;
}

.recommendation-flight {
    color: #64748b;

    font-size: 14px;
}

.recommendation-price {
    font-size: 32px;

    font-weight: 850;

    color: #1d4ed8;

    text-align: right;
}

.recommendation-route {
    margin-top: 20px;

    font-size: 18px;

    font-weight: 650;

    color: #334155;
}

.reason {
    background: white;

    border: 1px solid #dbeafe;

    border-left: 4px solid #2563eb;

    border-radius: 12px;

    padding: 17px;

    margin-top: 20px;

    color: #334155;

    font-size: 14px;

    line-height: 1.6;
}


/* ============================================================
   FOOTER
   ============================================================ */

.custom-footer {
    text-align: center;

    color: #94a3b8;

    font-size: 12px;

    margin-top: 50px;

    padding-top: 20px;

    border-top: 1px solid #e2e8f0;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .hero {
        padding: 30px 24px;
    }

    .hero-title {
        font-size: 32px;
    }

    .hero-text {
        font-size: 14px;
    }

    .timeline-header {
        align-items: flex-start;

        flex-direction: column;
    }

    .recommendation-route {
        font-size: 15px;
    }

}

</style>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        🤖 AUTONOMOUS AI TRAVEL AGENT
    </div>

    <div class="hero-title">
        ✈️ MakeMyTrip Autonomous<br>
        Web Operations Agent
    </div>

    <div class="hero-text">
        Describe your travel requirements in natural language.
        The autonomous agent understands your intent, operates
        the browser, observes flight results, validates
        constraints and uses AI reasoning to produce an
        explainable recommendation.
    </div>

</div>
""")


# ============================================================
# SEARCH PANEL
# ============================================================

st.html("""
<div class="search-card">

    <div class="search-title">
        🧳 Where do you want to go?
    </div>

    <div class="search-subtitle">
        Tell the agent what you need. No complicated forms —
        simply describe your trip naturally.
    </div>

</div>
""")


travel_request = st.text_area(
    "Travel request",
    placeholder=(
        "Example: Find me a non-stop flight from Mumbai "
        "to Delhi on 26 September 2026 for 2 people "
        "under ₹8,000, preferably after 6 PM."
    ),
    height=110,
    label_visibility="collapsed"
)


search_button = st.button(
    "✈️  Find Flights with AI Agent",
    type="primary",
    use_container_width=True
)


# ============================================================
# AGENT EXECUTION
# ============================================================

if search_button:

    if not travel_request.strip():

        st.warning(
            "Please describe your travel requirements first."
        )

    else:

        with st.spinner(
            "🤖 Autonomous agent is working..."
        ):

            try:

                result = run_agent(
                    travel_request,
                    show_terminal_output=False
                )

                agent_run_success = True

            except Exception as error:

                agent_run_success = False

                st.error(
                    "The autonomous agent encountered an error."
                )

                st.exception(error)


        if agent_run_success:

            st.success(
                "Agent workflow completed successfully."
            )


            # =================================================
            # REAL AGENT EXECUTION TIMELINE
            # =================================================

            execution_steps = result.get(
                "execution_steps",
                []
            )


            step_information = {

                "understand_request": {
                    "icon": "🧠",
                    "title": "Understand Request",
                    "description":
                        "AI interpreted the natural-language travel request."
                },

                "search_website": {
                    "icon": "🌐",
                    "title": "Search Website",
                    "description":
                        "Playwright operated the simulated travel website and searched for flights."
                },

                "recover_search": {
                    "icon": "🔄",
                    "title": "Autonomous Recovery",
                    "description":
                        "The agent detected a search problem and initiated a recovery attempt."
                },

                "validate_flights": {
                    "icon": "✅",
                    "title": "Validate Requirements",
                    "description":
                        "Observed flights were checked against the user's mandatory requirements."
                },

                "analyze_flights": {
                    "icon": "🎯",
                    "title": "AI Preference Reasoning",
                    "description":
                        "AI compared validated flights using the user's soft preferences."
                }

            }


            timeline_html = """
            <div class="agent-timeline">

                <div class="timeline-header">

                    <div>

                        <div class="timeline-title">
                            🤖 Agent Execution Timeline
                        </div>

                        <div class="timeline-subtitle">
                            Actual LangGraph execution path
                        </div>

                    </div>

                    <div class="timeline-status">
                        ✓ COMPLETED
                    </div>

                </div>
            """


            visible_step_number = 0


            for step_name in execution_steps:

                information = step_information.get(
                    step_name
                )

                if not information:
                    continue

                visible_step_number += 1


                timeline_html += f"""
                <div class="timeline-item">

                    <div class="timeline-number">
                        {visible_step_number}
                    </div>

                    <div class="timeline-icon">
                        {information["icon"]}
                    </div>

                    <div class="timeline-content">

                        <div class="timeline-step-title">
                            {information["title"]}
                        </div>

                        <div class="timeline-description">
                            {information["description"]}
                        </div>

                    </div>

                    <div class="timeline-check">
                        ✓
                    </div>

                </div>
                """


            if not execution_steps:

                timeline_html += """
                <div class="timeline-item">

                    <div class="timeline-number">
                        —
                    </div>

                    <div class="timeline-icon">
                        ⚠️
                    </div>

                    <div class="timeline-content">

                        <div class="timeline-step-title">
                            Execution information unavailable
                        </div>

                        <div class="timeline-description">
                            The agent completed, but no execution
                            steps were returned.
                        </div>

                    </div>

                </div>
                """


            timeline_html += """
            </div>
            """


            st.html(
                timeline_html
            )


            # =================================================
            # AI UNDERSTANDING
            # =================================================

            requirements = result.get(
                "requirements",
                {}
            )


            with st.expander(
                "🧠 View AI Understanding"
            ):

                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Origin",
                        requirements.get(
                            "origin",
                            "—"
                        )
                    )


                with col2:

                    st.metric(
                        "Destination",
                        requirements.get(
                            "destination",
                            "—"
                        )
                    )


                with col3:

                    st.metric(
                        "Travel Date",
                        requirements.get(
                            "travel_date",
                            "—"
                        )
                    )


                col1, col2, col3, col4 = st.columns(4)


                with col1:

                    st.metric(
                        "Passengers",
                        requirements.get(
                            "number_of_passengers",
                            "—"
                        )
                    )


                with col2:

                    maximum_price = requirements.get(
                        "maximum_price"
                    )


                    if isinstance(
                        maximum_price,
                        dict
                    ):

                        maximum_price = maximum_price.get(
                            "amount"
                        )


                    if maximum_price is not None:

                        try:

                            budget = (
                                f"₹{int(maximum_price):,}"
                            )

                        except (
                            ValueError,
                            TypeError
                        ):

                            budget = str(
                                maximum_price
                            )

                    else:

                        budget = "—"


                    st.metric(
                        "Maximum Budget",
                        budget
                    )


                with col3:

                    nonstop = requirements.get(
                        "non_stop_required",
                        False
                    )


                    st.metric(
                        "Non-stop",
                        "Required"
                        if nonstop
                        else "Flexible"
                    )


                with col4:

                    st.metric(
                        "Preferred Time",
                        requirements.get(
                            "preferred_departure_time",
                            "—"
                        )
                    )


            # =================================================
            # FLIGHT RESULTS
            # =================================================

            flights = result.get(
                "validated_flights",
                []
            )


            st.html("""
            <h2 style="
                color:#0f172a;
                font-size:28px;
                font-weight:800;
                margin-top:30px;
                margin-bottom:16px;
            ">
                ✈️ Available Flights
            </h2>
            """)


            if flights:

                st.caption(
                    f"{len(flights)} flights satisfy the mandatory requirements."
                )


                for flight in flights:

                    airline = flight.get(
                        "airline",
                        "Unknown Airline"
                    )

                    flight_number = flight.get(
                        "flight_number",
                        "—"
                    )

                    departure = flight.get(
                        "departure",
                        "—"
                    )

                    arrival = flight.get(
                        "arrival",
                        "—"
                    )

                    stops = flight.get(
                        "stops",
                        "Unknown"
                    )

                    flight_date = flight.get(
                        "date",
                        "—"
                    )

                    price = flight.get(
                        "price",
                        0
                    )

                    validation_reason = flight.get(
                        "validation_reason",
                        ""
                    )


                    try:

                        formatted_price = (
                            f"₹{int(price):,}"
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        formatted_price = str(
                            price
                        )


                    st.html(
                        f"""
                        <div class="flight-card">

                            <div style="
                                display:flex;
                                justify-content:space-between;
                                align-items:flex-start;
                                gap:20px;
                            ">

                                <div>

                                    <div class="airline">
                                        ✈️ {airline}
                                    </div>

                                    <div class="flight-number">
                                        Flight {flight_number}
                                    </div>

                                </div>


                                <div>

                                    <div class="flight-price">
                                        {formatted_price}
                                    </div>

                                    <div class="per-passenger">
                                        per passenger
                                    </div>

                                </div>

                            </div>


                            <div style="
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                gap:18px;
                                margin-top:25px;
                                margin-bottom:20px;
                            ">

                                <div style="
                                    text-align:right;
                                    min-width:120px;
                                ">

                                    <div style="
                                        font-size:13px;
                                        color:#64748b;
                                        margin-bottom:4px;
                                    ">
                                        {requirements.get(
                                            'origin',
                                            'Origin'
                                        )}
                                    </div>

                                    <div class="time">
                                        {departure}
                                    </div>

                                </div>


                                <div style="
                                    flex:1;
                                    max-width:220px;
                                    text-align:center;
                                ">

                                    <div style="
                                        color:#94a3b8;
                                        font-size:18px;
                                        letter-spacing:3px;
                                    ">
                                        ─── ✈ ───
                                    </div>

                                </div>


                                <div style="
                                    text-align:left;
                                    min-width:120px;
                                ">

                                    <div style="
                                        font-size:13px;
                                        color:#64748b;
                                        margin-bottom:4px;
                                    ">
                                        {requirements.get(
                                            'destination',
                                            'Destination'
                                        )}
                                    </div>

                                    <div class="time">
                                        {arrival}
                                    </div>

                                </div>

                            </div>


                            <div style="
                                display:flex;
                                justify-content:space-between;
                                align-items:center;
                                flex-wrap:wrap;
                                gap:10px;
                                padding-top:16px;
                                border-top:1px solid #f1f5f9;
                            ">

                                <div>

                                    <span class="badge-green">
                                        ✓ {stops}
                                    </span>

                                    <span class="badge-blue">
                                        📅 {flight_date}
                                    </span>

                                </div>


                                <div style="
                                    color:#059669;
                                    font-size:12px;
                                    font-weight:700;
                                ">
                                    ✓ Meets mandatory requirements
                                </div>

                            </div>


                            {
                                f'''
                                <div style="
                                    margin-top:12px;
                                    color:#64748b;
                                    font-size:12px;
                                ">
                                    <strong>
                                        Validation:
                                    </strong>
                                    {validation_reason}
                                </div>
                                '''
                                if validation_reason
                                else ""
                            }

                        </div>
                        """
                    )


            else:

                st.info(
                    "No flights satisfy the mandatory requirements."
                )


            # =================================================
            # AI RECOMMENDATION
            # =================================================

            decision = result.get(
                "decision",
                {}
            )


            recommended = decision.get(
                "recommended_flight"
            )


            if recommended:

                recommended_number = recommended.get(
                    "flight_number"
                )


                recommended_data = None


                for flight in flights:

                    if (
                        flight.get("flight_number")
                        == recommended_number
                    ):

                        recommended_data = flight

                        break


                if recommended_data:

                    st.html("""
                    <h2 style="
                        color:#0f172a;
                        font-size:28px;
                        font-weight:800;
                        margin-top:35px;
                        margin-bottom:16px;
                    ">
                        🎯 Agent Recommendation
                    </h2>
                    """)


                    recommendation_price = (
                        recommended_data.get(
                            "price",
                            0
                        )
                    )


                    try:

                        formatted_recommendation_price = (
                            f"₹{int(recommendation_price):,}"
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        formatted_recommendation_price = str(
                            recommendation_price
                        )


                    st.html(
                        f"""
                        <div class="recommendation">

                            <div class="recommendation-tag">
                                AI SELECTED FLIGHT
                            </div>


                            <div style="
                                display:flex;
                                justify-content:space-between;
                                align-items:flex-start;
                                gap:20px;
                            ">

                                <div>

                                    <div class="recommendation-airline">
                                        ✈️ {recommended_data.get(
                                            'airline',
                                            'Unknown Airline'
                                        )}
                                    </div>

                                    <div class="recommendation-flight">
                                        Flight {recommended_data.get(
                                            'flight_number',
                                            '—'
                                        )}
                                    </div>

                                </div>


                                <div>

                                    <div class="recommendation-price">
                                        {formatted_recommendation_price}
                                    </div>

                                    <div style="
                                        text-align:right;
                                        color:#64748b;
                                        font-size:12px;
                                    ">
                                        per passenger
                                    </div>

                                </div>

                            </div>


                            <div class="recommendation-route">

                                🛫 {requirements.get(
                                    'origin',
                                    'Origin'
                                )}

                                &nbsp;&nbsp;

                                {recommended_data.get(
                                    'departure',
                                    '—'
                                )}

                                &nbsp;&nbsp; → &nbsp;&nbsp;

                                {recommended_data.get(
                                    'arrival',
                                    '—'
                                )}

                                &nbsp;&nbsp;

                                🛬 {requirements.get(
                                    'destination',
                                    'Destination'
                                )}

                            </div>


                            <div style="
                                margin-top:14px;
                            ">

                                <span class="badge-green">
                                    ✓ {recommended_data.get(
                                        'stops',
                                        'Unknown'
                                    )}
                                </span>

                                <span class="badge-blue">
                                    📅 {recommended_data.get(
                                        'date',
                                        '—'
                                    )}
                                </span>

                                <span class="badge-gray">
                                    ✓ AI verified
                                </span>

                            </div>


                            <div class="reason">

                                <strong>
                                    🧠 Why did the agent select this?
                                </strong>

                                <br><br>

                                {recommended.get(
                                    'reason',
                                    'No explanation available.'
                                )}

                            </div>

                        </div>
                        """
                    )


            # =================================================
            # EXECUTION SUMMARY
            # =================================================

            st.html("""
            <h2 style="
                color:#0f172a;
                font-size:28px;
                font-weight:800;
                margin-top:35px;
                margin-bottom:16px;
            ">
                🔍 Agent Execution Summary
            </h2>
            """)


            observed_flights = result.get(
                "flights",
                []
            )


            retry_count = result.get(
                "retry_count",
                0
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Flights Observed",
                    len(observed_flights)
                )


            with col2:

                st.metric(
                    "Matching Flights",
                    len(flights)
                )


            with col3:

                st.metric(
                    "Recovery Attempts",
                    retry_count
                )


            with col4:

                st.metric(
                    "AI Decision",
                    "Generated"
                    if recommended
                    else "No Match"
                )


            # =================================================
            # TECHNICAL DETAILS
            # =================================================

            with st.expander(
                "🔬 View Agent Decision Data"
            ):

                st.json(
                    decision
                )


            # =================================================
            # ACTUAL EXECUTION DATA
            # =================================================

            with st.expander(
                "⚙️ View Agent Execution Data"
            ):

                st.json(
                    {
                        "execution_steps":
                            result.get(
                                "execution_steps",
                                []
                            ),

                        "retry_count":
                            result.get(
                                "retry_count",
                                0
                            ),

                        "search_error":
                            result.get(
                                "search_error",
                                ""
                            )
                    }
                )


            # =================================================
            # RECOVERY INFORMATION
            # =================================================

            search_error = result.get(
                "search_error",
                ""
            )


            if search_error:

                st.warning(
                    f"Agent recovery information: "
                    f"{search_error}"
                )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="custom-footer">

    <strong style="color:#64748b;">
        MakeMyTrip: Autonomous Web Operations Agent
    </strong>

    <br><br>

    Master's AI / Data Science Project
    • Educational Simulation
    • Autonomous Browser Agent

</div>
""")