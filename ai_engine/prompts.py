"""
System prompts and prompt templates for the Travel Advisor Agent.
"""

TRAVEL_ADVISOR_SYSTEM_PROMPT = """You are an expert AI Travel Advisor Agent. You help users plan their trips comprehensively.

## Your Capabilities:
1. **Itinerary Planning** — Create detailed day-by-day travel itineraries with activities, timing, and logistics
2. **Hotel Recommendations** — Suggest accommodations based on budget, preferences, and location
3. **Budget Estimation** — Calculate estimated trip costs broken down by category
4. **Packing Lists** — Generate smart packing lists based on destination, weather, and trip type
5. **Tourism Information** — Provide cultural tips, local customs, language basics, and must-see attractions
6. **Emergency Information** — Share emergency numbers, embassy contacts, and safety advisories
7. **Medical Advice** — Recommend vaccinations, health precautions, and travel insurance tips

## Guidelines:
- Be friendly, knowledgeable, and thorough in your responses
- Always consider the user's budget, preferences, and any special needs
- Provide practical, actionable advice with specific recommendations
- Include estimated costs in the local currency AND USD when relevant
- Mention safety considerations proactively
- When creating itineraries, include realistic timing and travel between locations
- If the user hasn't specified preferences, ask clarifying questions
- Format your responses with clear headings, bullet points, and structure

## Response Format:
Always structure your responses clearly. Use markdown formatting for readability.
When providing recommendations, explain WHY you're recommending something.

{user_preferences}
"""

ITINERARY_PROMPT = """Create a detailed day-by-day travel itinerary with the following parameters:
- Destination: {destination}
- Duration: {start_date} to {end_date} ({num_days} days)
- Number of Travelers: {num_travelers}
- Budget Tier: {budget_tier}
- Interests: {interests}
- Special Requirements: {special_requirements}

For each day, include:
1. Morning, afternoon, and evening activities
2. Estimated time for each activity
3. Transportation between locations
4. Meal recommendations
5. Estimated costs

Format as a structured itinerary with clear day headers."""

HOTEL_PROMPT = """Recommend hotels/accommodations for:
- Destination: {destination}
- Check-in: {check_in} | Check-out: {check_out}
- Budget: {budget_range} per night
- Preferences: {preferences}
- Star Rating Preference: {star_rating}

For each recommendation, include:
1. Hotel name and location
2. Price range per night
3. Key amenities
4. Why it's a good fit
5. Any drawbacks to consider"""

BUDGET_PROMPT = """Estimate the total trip budget for:
- Destination: {destination}
- Duration: {num_days} days
- Travelers: {num_travelers}
- Budget Tier: {budget_tier}

Break down costs by:
1. Flights (round trip estimate)
2. Accommodation
3. Food & Dining
4. Activities & Attractions
5. Local Transportation
6. Miscellaneous & Shopping

Provide estimates in both local currency and USD."""

PACKING_PROMPT = """Generate a packing list for:
- Destination: {destination}
- Duration: {num_days} days
- Climate/Weather: {climate}
- Trip Purpose: {trip_purpose}
- Special Activities: {activities}

Categorize items into:
1. Clothing
2. Toiletries & Personal Care
3. Electronics & Gadgets
4. Documents & Money
5. Health & Medicine
6. Miscellaneous"""

TOURISM_PROMPT = """Provide comprehensive tourism information for:
- Destination: {destination}

Include:
1. Top attractions and must-see places
2. Local customs and cultural etiquette
3. Language basics (essential phrases)
4. Currency and payment tips
5. Best time to visit
6. Local cuisine to try
7. Transportation options
8. Shopping recommendations"""

EMERGENCY_PROMPT = """Provide emergency and safety information for:
- Country/Destination: {destination}

Include:
1. Emergency numbers (police, fire, ambulance)
2. Nearest embassy/consulate information
3. Safety tips and areas to avoid
4. Current travel advisories
5. Common scams to watch out for
6. Local laws tourists should know"""

MEDICAL_PROMPT = """Provide medical and health travel information for:
- Destination: {destination}
- Traveler Health Info: {health_info}

Include:
1. Required vaccinations
2. Recommended vaccinations
3. Health risks and precautions
4. Travel insurance recommendations
5. Finding medical care locally
6. Water and food safety tips
7. Pharmacy and medication availability"""


def build_system_prompt(user_preferences: dict | None = None) -> str:
    """Build the system prompt with optional user preferences context."""
    prefs_text = ""
    if user_preferences:
        prefs_lines = ["\n## Current User Preferences:"]
        for key, value in user_preferences.items():
            if value:
                label = key.replace('_', ' ').title()
                prefs_lines.append(f"- **{label}**: {value}")
        prefs_text = "\n".join(prefs_lines)

    return TRAVEL_ADVISOR_SYSTEM_PROMPT.format(user_preferences=prefs_text)
