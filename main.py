import os
import json
from typing import TypedDict, List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright
from langgraph.graph import StateGraph, START, END


# ============================================================
# 1. CONFIGURATION
# ============================================================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ============================================================
# 2. AGENT STATE
# ============================================================

class AgentState(TypedDict):

    travel_request: str
    requirements: Dict[str, Any]

    flights: List[Dict[str, Any]]
    validated_flights: List[Dict[str, Any]]

    decision: Dict[str, Any]

    search_error: str
    retry_count: int


# ============================================================
# 3. NODE 1 — UNDERSTAND USER REQUEST
# ============================================================

def understand_request(state: AgentState):

    print("\n" + "=" * 60)
    print("NODE 1: UNDERSTAND REQUEST")
    print("=" * 60)

    response = client.responses.create(

        model="gpt-5.6-luna",

        input=f"""
You are a travel planning AI.

Extract the following information:

- origin
- destination
- travel_date
- number_of_passengers
- maximum_price
- non_stop_required
- preferred_departure_time

Rules:

1. Convert dates to YYYY-MM-DD.
2. Convert prices to numbers.
3. Convert departure preferences to 24-hour time.
4. If a value is not provided, use null.
5. Return ONLY valid JSON.

User request:

{state["travel_request"]}
"""
    )

    requirements = json.loads(
        response.output_text
    )

    print(
        json.dumps(
            requirements,
            indent=2,
            ensure_ascii=False
        )
    )

    return {
        "requirements": requirements
    }


# ============================================================
# 4. NODE 2 — SEARCH WEBSITE
# ============================================================

def search_website(state: AgentState):

    print("\n" + "=" * 60)
    print("NODE 2: SEARCH WEBSITE")
    print("=" * 60)

    requirements = state["requirements"]

    retry_count = state.get(
        "retry_count",
        0
    )

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            page = browser.new_page()

            website_url = "http://localhost:8000"

            if retry_count > 0:

                print(
                    f"Recovery attempt #{retry_count}"
                )

            print(
                f"Opening website: {website_url}"
            )

            page.goto(
                website_url,
                timeout=10000
            )

            print(
                "Website opened."
            )

            # ------------------------------------------------
            # ENTER TRAVEL DETAILS
            # ------------------------------------------------

            page.locator(
                "#from"
            ).fill(
                requirements["origin"]
            )

            page.locator(
                "#to"
            ).fill(
                requirements["destination"]
            )

            page.locator(
                "#date"
            ).fill(
                requirements["travel_date"]
            )

            print(
                "Travel details entered."
            )

            # ------------------------------------------------
            # SEARCH
            # ------------------------------------------------

            page.locator(
                "#searchBtn"
            ).click()

            print(
                "Search button clicked."
            )

            page.wait_for_timeout(
                2500
            )

            # ------------------------------------------------
            # OBSERVE FLIGHTS
            # ------------------------------------------------

            flight_cards = page.locator(
                ".flight-card"
            )

            flights = []

            for i in range(
                flight_cards.count()
            ):

                flight = flight_cards.nth(i)

                airline = flight.locator(
                    ".airline-name"
                ).inner_text()

                flight_number = flight.locator(
                    ".flight-number"
                ).inner_text()

                price_text = flight.locator(
                    ".price-value"
                ).inner_text()

                departure = flight.locator(
                    ".time"
                ).nth(0).inner_text()

                arrival = flight.locator(
                    ".time"
                ).nth(1).inner_text()

                stops = flight.locator(
                    ".nonstop"
                ).inner_text()

                details = flight.locator(
                    ".detail"
                )

                date_text = details.nth(
                    3
                ).inner_text()

                price = int(
                    price_text
                    .replace("₹", "")
                    .replace(",", "")
                )

                flight_date = (
                    date_text
                    .replace(
                        "Date:",
                        ""
                    )
                    .strip()
                )

                stops_clean = (
                    stops
                    .replace(
                        "✓",
                        ""
                    )
                    .strip()
                )

                flights.append({

                    "airline":
                        airline,

                    "flight_number":
                        flight_number,

                    "price":
                        price,

                    "departure":
                        departure,

                    "arrival":
                        arrival,

                    "stops":
                        stops_clean,

                    "date":
                        flight_date

                })

            print(
                f"Flights observed: "
                f"{len(flights)}"
            )

            browser.close()

        # ------------------------------------------------
        # CHECK RESULTS
        # ------------------------------------------------

        if len(flights) == 0:

            raise Exception(
                "No flight results were observed."
            )

        return {

            "flights":
                flights,

            "search_error":
                "",

            "retry_count":
                retry_count

        }

    except Exception as error:

        print(
            "\n⚠ SEARCH OPERATION FAILED"
        )

        print(
            f"Error: {error}"
        )

        return {

            "flights":
                [],

            "search_error":
                str(error),

            "retry_count":
                retry_count

        }


# ============================================================
# 5. NODE 3 — AUTONOMOUS RECOVERY
# ============================================================

def recover_search(state: AgentState):

    print("\n" + "=" * 60)
    print("NODE 3: AUTONOMOUS RECOVERY")
    print("=" * 60)

    retry_count = state.get(
        "retry_count",
        0
    )

    previous_error = state.get(
        "search_error",
        ""
    )

    print(
        f"Previous retry count: {retry_count}"
    )

    if previous_error:

        print(
            f"Previous error: {previous_error}"
        )

    # --------------------------------------------------------
    # RETRY 1
    # --------------------------------------------------------

    if retry_count == 0:

        print(
            "Recovery strategy: Restart browser session"
        )

        print(
            "Agent will retry the complete search operation."
        )

        return {

            "retry_count":
                1,

            "search_error":
                "",

        }

    # --------------------------------------------------------
    # RETRY 2
    # --------------------------------------------------------

    if retry_count == 1:

        print(
            "Recovery strategy: Repeat browser search"
        )

        print(
            "Agent will perform a second recovery attempt."
        )

        return {

            "retry_count":
                2,

            "search_error":
                "",

        }

    # --------------------------------------------------------
    # MAXIMUM RETRIES
    # --------------------------------------------------------

    print(
        "Maximum recovery attempts reached."
    )

    print(
        "Agent will continue to validation."
    )

    return {

        "search_error":
            "Maximum recovery attempts reached."

    }

# ============================================================
# 6. ROUTING DECISION
# ============================================================

def decide_next_step(state: AgentState):

    error = state.get(
        "search_error",
        ""
    )

    retry_count = state.get(
        "retry_count",
        0
    )

    if error:

        if retry_count < 2:

            return "recover_search"

        return "validate_flights"

    return "validate_flights"


# ============================================================
# 7. NODE 4 — VALIDATE HARD REQUIREMENTS
# ============================================================

def validate_flights(state: AgentState):

    print("\n" + "=" * 60)
    print("NODE 4: VALIDATE HARD REQUIREMENTS")
    print("=" * 60)

    requirements = state["requirements"]

    flights = state["flights"]

    validated_flights = []

    maximum_price = requirements.get(
        "maximum_price"
    )

    non_stop_required = requirements.get(
        "non_stop_required"
    )

    travel_date = requirements.get(
        "travel_date"
    )

    print("\nValidation results:")

    # ========================================================
    # CHECK EACH OBSERVED FLIGHT
    # ========================================================

    for flight in flights:

        reasons = []

        passed = True

        flight_number = flight.get(
            "flight_number",
            "Unknown"
        )

        # ----------------------------------------------------
        # BASIC DATA VALIDATION
        # ----------------------------------------------------

        required_fields = [
            "price",
            "departure",
            "arrival",
            "stops",
            "date"
        ]

        missing_fields = [

            field

            for field in required_fields

            if flight.get(field) in (
                None,
                ""
            )

        ]

        if missing_fields:

            passed = False

            reasons.append(
                "Missing data: "
                + ", ".join(missing_fields)
            )

        # ----------------------------------------------------
        # PRICE VALIDATION
        # ----------------------------------------------------

        if (
            passed
            and
            maximum_price is not None
        ):

            try:

                flight_price = float(
                    flight["price"]
                )

                budget = float(
                    maximum_price
                )

                if flight_price > budget:

                    passed = False

                    reasons.append(
                        "Price exceeds budget"
                    )

                else:

                    reasons.append(
                        "Within budget"
                    )

            except (
                ValueError,
                TypeError
            ):

                passed = False

                reasons.append(
                    "Invalid price data"
                )

        # ----------------------------------------------------
        # NON-STOP VALIDATION
        # ----------------------------------------------------

        if (
            passed
            and
            non_stop_required
        ):

            stops = str(
                flight["stops"]
            ).strip().lower()

            if stops != "non-stop":

                passed = False

                reasons.append(
                    "Not non-stop"
                )

            else:

                reasons.append(
                    "Non-stop"
                )

        # ----------------------------------------------------
        # DATE VALIDATION
        # ----------------------------------------------------

        if (
            passed
            and
            travel_date
        ):

            observed_date = str(
                flight["date"]
            ).strip()

            requested_date = str(
                travel_date
            ).strip()

            if observed_date != requested_date:

                passed = False

                reasons.append(
                    "Wrong date"
                )

            else:

                reasons.append(
                    "Correct date"
                )

        # ----------------------------------------------------
        # FINAL VALIDATION RESULT
        # ----------------------------------------------------

        result = {

            **flight,

            "status":
                "MATCH"
                if passed
                else "REJECTED",

            "validation_reason":
                "; ".join(reasons)

        }

        if passed:

            validated_flights.append(
                result
            )

        # ----------------------------------------------------
        # TERMINAL OUTPUT
        # ----------------------------------------------------

        print(

            f"{flight_number:12}"

            f"₹{flight.get('price', 'N/A'):<10}"

            f"{flight.get('departure', 'N/A'):<10}"

            f"{'✓ MATCH' if passed else '✗ REJECTED'}"

        )

        if reasons:

            print(
                f"    Reason: "
                f"{'; '.join(reasons)}"
            )

    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        f"\nFlights satisfying hard "
        f"requirements: "
        f"{len(validated_flights)}"
    )

    return {

        "validated_flights":
            validated_flights

    }


# ============================================================
# 8. NODE 5 — AI PREFERENCE REASONING
# ============================================================

def analyze_flights(state: AgentState):

    print("\n" + "=" * 60)
    print("NODE 5: AI PREFERENCE REASONING")
    print("=" * 60)

    requirements = state[
        "requirements"
    ]

    valid_flights = state[
        "validated_flights"
    ]

    travel_request = state.get(
        "travel_request",
        ""
    )

    # --------------------------------------------------------
    # NO VALID FLIGHTS
    # --------------------------------------------------------

    if not valid_flights:

        print(
            "No flights available for preference reasoning."
        )

        return {

            "decision": {

                "matching_flights": [],

                "recommended_flight":
                    None,

                "reason":
                    "No flights satisfy the mandatory requirements."

            }

        }

    # --------------------------------------------------------
    # PREPARE FLIGHT DATA
    # --------------------------------------------------------

    flight_data = json.dumps(
        valid_flights,
        indent=2,
        ensure_ascii=False
    )

    # --------------------------------------------------------
    # AI PREFERENCE REASONING
    # --------------------------------------------------------

    response = client.responses.create(

        model="gpt-5.6-luna",

        input=f"""
You are the preference-reasoning component
of an autonomous travel agent.

ORIGINAL USER REQUEST:

{travel_request}

EXTRACTED USER REQUIREMENTS:

{json.dumps(
    requirements,
    indent=2
)}

VALIDATED FLIGHTS:

{flight_data}

IMPORTANT:

All flights above have already passed
the mandatory requirements.

Do NOT reject a validated flight because
of a hard requirement.

Your job is to compare the validated flights
using the user's SOFT preferences.

Consider:

1. Preferred departure time
2. Price
3. Departure convenience
4. Any additional preference clearly stated
   in the original user request

If the user says something such as
"preferably after 6 PM", treat that as a
preference, not a mandatory requirement.

Prefer flights that satisfy the soft preference
when practical.

Use ONLY information present in the user request,
requirements, and validated flights.

NEVER invent:
- flight numbers
- prices
- times
- airlines
- routes
- dates

The recommended flight_number MUST exactly match
one of the validated flights.

Return ONLY valid JSON in this format:

{{
    "matching_flights": [
        {{
            "flight_number": "...",
            "reason": "..."
        }}
    ],

    "recommended_flight": {{
        "flight_number": "...",
        "reason": "..."
    }}
}}
"""
    )

    # --------------------------------------------------------
    # PARSE AI RESPONSE
    # --------------------------------------------------------

    try:

        decision = json.loads(
            response.output_text
        )

    except (
        json.JSONDecodeError,
        TypeError
    ):

        print(
            "AI returned invalid JSON."
        )

        # Safe fallback:
        # choose the lowest-priced validated flight.

        fallback = min(
            valid_flights,
            key=lambda flight:
                flight["price"]
        )

        decision = {

            "matching_flights": [

                {
                    "flight_number":
                        flight["flight_number"],

                    "reason":
                        "Validated flight."
                }

                for flight in valid_flights

            ],

            "recommended_flight": {

                "flight_number":
                    fallback["flight_number"],

                "reason":
                    "Fallback recommendation based "
                    "on the lowest validated price "
                    "after AI response validation."
            }

        }

    # --------------------------------------------------------
    # VERIFY AI RECOMMENDATION
    # --------------------------------------------------------

    recommended = decision.get(
        "recommended_flight"
    )

    valid_flight_numbers = {

        flight["flight_number"]

        for flight in valid_flights

    }

    if not recommended:

        print(
            "AI did not provide a recommendation."
        )

        fallback = min(
            valid_flights,
            key=lambda flight:
                flight["price"]
        )

        decision["recommended_flight"] = {

            "flight_number":
                fallback["flight_number"],

            "reason":
                "Fallback recommendation based "
                "on the lowest validated price."
        }

    elif (
        recommended.get("flight_number")
        not in valid_flight_numbers
    ):

        print(
            "AI recommendation failed validation."
        )

        fallback = min(
            valid_flights,
            key=lambda flight:
                flight["price"]
        )

        decision["recommended_flight"] = {

            "flight_number":
                fallback["flight_number"],

            "reason":
                "AI recommendation did not match "
                "a validated flight, so the agent "
                "selected the lowest-priced validated "
                "flight as a safe fallback."
        }

    else:

        print(
            "AI recommendation verified against "
            "validated flight results."
        )

    # --------------------------------------------------------
    # VERIFY MATCHING FLIGHTS
    # --------------------------------------------------------

    matching_flights = (
        decision.get(
            "matching_flights",
            []
        )
    )

    verified_matching = []

    for item in matching_flights:

        flight_number = item.get(
            "flight_number"
        )

        if flight_number in valid_flight_numbers:

            verified_matching.append(
                item
            )

    decision["matching_flights"] = (
        verified_matching
    )

    print(
        "AI preference reasoning completed."
    )

    return {

        "decision":
            decision

    }


# ============================================================
# 9. BUILD LANGGRAPH
# ============================================================

graph_builder = StateGraph(
    AgentState
)

graph_builder.add_node(
    "understand_request",
    understand_request
)

graph_builder.add_node(
    "search_website",
    search_website
)

graph_builder.add_node(
    "recover_search",
    recover_search
)

graph_builder.add_node(
    "validate_flights",
    validate_flights
)

graph_builder.add_node(
    "analyze_flights",
    analyze_flights
)


# ============================================================
# 10. GRAPH FLOW
# ============================================================

graph_builder.add_edge(
    START,
    "understand_request"
)

graph_builder.add_edge(
    "understand_request",
    "search_website"
)

graph_builder.add_conditional_edges(

    "search_website",

    decide_next_step,

    {

        "recover_search":
            "recover_search",

        "validate_flights":
            "validate_flights"

    }

)

graph_builder.add_edge(
    "recover_search",
    "search_website"
)

graph_builder.add_edge(
    "validate_flights",
    "analyze_flights"
)

graph_builder.add_edge(
    "analyze_flights",
    END
)


agent = graph_builder.compile()


# ============================================================
# 11. REUSABLE AGENT FUNCTION
# ============================================================

def run_agent(
    travel_request: str,
    show_terminal_output: bool = True
):

    """
    Run the complete autonomous travel agent.

    Also records the actual LangGraph nodes
    executed during the workflow.

    Returns:
        Complete final LangGraph state plus
        execution timeline.
    """

    initial_state = {

        "travel_request":
            travel_request,

        "requirements":
            {},

        "flights":
            [],

        "validated_flights":
            [],

        "decision":
            {},

        "search_error":
            "",

        "retry_count":
            0
    }

    # --------------------------------------------------------
    # EXECUTION TIMELINE
    # --------------------------------------------------------

    execution_steps = []

    final_state = initial_state.copy()

    # --------------------------------------------------------
    # STREAM LANGGRAPH EXECUTION
    # --------------------------------------------------------

    for update in agent.stream(
        initial_state,
        stream_mode="updates"
    ):

        if not isinstance(update, dict):
            continue

        for node_name, node_output in update.items():

            # Record the actual node executed.
            execution_steps.append(
                node_name
            )

            # Merge the node output into
            # the current final state.
            if isinstance(
                node_output,
                dict
            ):

                final_state.update(
                    node_output
                )

    # --------------------------------------------------------
    # ADD EXECUTION TIMELINE
    # --------------------------------------------------------

    final_state[
        "execution_steps"
    ] = execution_steps

    return final_state
# ============================================================
# 12. TERMINAL MODE
# ============================================================

def terminal_mode():

    print("\n")

    print("=" * 60)

    print(
        " MAKE MY TRIP: AUTONOMOUS WEB OPERATIONS AGENT"
    )

    print("=" * 60)

    travel_request = input(
        "\nWhat flight are you looking for?\n> "
    )

    final_state = run_agent(
        travel_request
    )

    # --------------------------------------------------------
    # FINAL DECISION REPORT
    # --------------------------------------------------------

    print("\n")

    print("=" * 60)

    print(
        "              AGENT DECISION REPORT"
    )

    print("=" * 60)

    valid_flights = final_state[
        "validated_flights"
    ]

    decision = final_state[
        "decision"
    ]

    recommended = decision.get(
        "recommended_flight"
    )

    print(
        "\nFlight        Price       Departure      Status"
    )

    print(
        "-" * 60
    )

    for flight in valid_flights:

        print(

            f"{flight['flight_number']:12}"

            f"₹{flight['price']:<10,}"

            f"{flight['departure']:<15}"

            f"✓ MATCH"

        )

    print(
        "-" * 60
    )

    # --------------------------------------------------------
    # RECOMMENDED FLIGHT
    # --------------------------------------------------------

    if recommended:

        recommended_number = (
            recommended[
                "flight_number"
            ]
        )

        recommended_data = None

        for flight in valid_flights:

            if (
                flight["flight_number"]
                == recommended_number
            ):

                recommended_data = flight

                break

        print(
            "\nRecommended Flight:"
        )

        print(
            f"✈ {recommended_number}"
        )

        if recommended_data:

            print(
                f"Airline: "
                f"{recommended_data['airline']}"
            )

            print(
                f"Price: "
                f"₹{recommended_data['price']:,}"
            )

            print(
                f"Departure: "
                f"{recommended_data['departure']}"
            )

            print(
                f"Arrival: "
                f"{recommended_data['arrival']}"
            )

            print(
                f"Stops: "
                f"{recommended_data['stops']}"
            )

        print(
            "\nAI Reason:"
        )

        print(
            recommended["reason"]
        )

    else:

        print(
            "\nNo suitable flight found."
        )

    print("\n")

    print("=" * 60)

    print(
        "           AGENT WORKFLOW COMPLETED"
    )

    print("=" * 60)


# ============================================================
# 13. PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    terminal_mode()