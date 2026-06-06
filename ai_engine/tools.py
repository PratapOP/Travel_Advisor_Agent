"""
LangChain tool definitions for the Travel Advisor Agent.
Each tool represents a specialized travel planning capability.
"""
import json
import logging

from langchain_core.tools import tool

from .client import get_llm
from .prompts import (
    BUDGET_PROMPT,
    EMERGENCY_PROMPT,
    HOTEL_PROMPT,
    ITINERARY_PROMPT,
    MEDICAL_PROMPT,
    PACKING_PROMPT,
    TOURISM_PROMPT,
)

logger = logging.getLogger('ai_engine')


@tool
def generate_itinerary(
    destination: str,
    start_date: str,
    end_date: str,
    num_days: int,
    num_travelers: int = 1,
    budget_tier: str = "mid_range",
    interests: str = "",
    special_requirements: str = "",
) -> str:
    """Generate a detailed day-by-day travel itinerary for a destination.

    Args:
        destination: The travel destination (city/country).
        start_date: Trip start date (YYYY-MM-DD).
        end_date: Trip end date (YYYY-MM-DD).
        num_days: Total number of days.
        num_travelers: Number of people traveling.
        budget_tier: One of budget, mid_range, luxury, ultra_luxury.
        interests: Comma-separated interests like adventure, culture, food.
        special_requirements: Any accessibility or dietary needs.
    """
    llm = get_llm(temperature=0.7)
    prompt = ITINERARY_PROMPT.format(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        num_days=num_days,
        num_travelers=num_travelers,
        budget_tier=budget_tier,
        interests=interests or "general sightseeing",
        special_requirements=special_requirements or "none",
    )
    response = llm.invoke(prompt)
    return response.content


@tool
def recommend_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    budget_range: str = "$100-$200 per night",
    preferences: str = "",
    star_rating: str = "3-4 stars",
) -> str:
    """Recommend hotels and accommodations for a destination.

    Args:
        destination: The travel destination.
        check_in: Check-in date (YYYY-MM-DD).
        check_out: Check-out date (YYYY-MM-DD).
        budget_range: Price range per night.
        preferences: Specific preferences (pool, gym, central location, etc.).
        star_rating: Preferred star rating range.
    """
    llm = get_llm(temperature=0.7)
    prompt = HOTEL_PROMPT.format(
        destination=destination,
        check_in=check_in,
        check_out=check_out,
        budget_range=budget_range,
        preferences=preferences or "central location, good reviews",
        star_rating=star_rating,
    )
    response = llm.invoke(prompt)
    return response.content


@tool
def estimate_budget(
    destination: str,
    num_days: int,
    num_travelers: int = 1,
    budget_tier: str = "mid_range",
) -> str:
    """Estimate the total trip budget with a detailed breakdown.

    Args:
        destination: The travel destination.
        num_days: Trip duration in days.
        num_travelers: Number of travelers.
        budget_tier: One of budget, mid_range, luxury, ultra_luxury.
    """
    llm = get_llm(temperature=0.5)
    prompt = BUDGET_PROMPT.format(
        destination=destination,
        num_days=num_days,
        num_travelers=num_travelers,
        budget_tier=budget_tier,
    )
    response = llm.invoke(prompt)
    return response.content


@tool
def suggest_packing_list(
    destination: str,
    num_days: int,
    climate: str = "",
    trip_purpose: str = "leisure",
    activities: str = "",
) -> str:
    """Generate a smart packing list based on destination and trip details.

    Args:
        destination: The travel destination.
        num_days: Trip duration in days.
        climate: Expected weather/climate.
        trip_purpose: Purpose of trip (leisure, business, adventure, etc.).
        activities: Specific planned activities.
    """
    llm = get_llm(temperature=0.6)
    prompt = PACKING_PROMPT.format(
        destination=destination,
        num_days=num_days,
        climate=climate or "check local forecast",
        trip_purpose=trip_purpose,
        activities=activities or "general sightseeing",
    )
    response = llm.invoke(prompt)
    return response.content


@tool
def get_tourism_info(destination: str) -> str:
    """Get comprehensive tourism information about a destination including attractions, culture, and tips.

    Args:
        destination: The travel destination (city or country).
    """
    llm = get_llm(temperature=0.6)
    prompt = TOURISM_PROMPT.format(destination=destination)
    response = llm.invoke(prompt)
    return response.content


@tool
def get_emergency_info(destination: str) -> str:
    """Get emergency and safety information for a destination including emergency numbers and embassy info.

    Args:
        destination: The country or destination.
    """
    llm = get_llm(temperature=0.3)
    prompt = EMERGENCY_PROMPT.format(destination=destination)
    response = llm.invoke(prompt)
    return response.content


@tool
def get_medical_info(
    destination: str,
    health_info: str = "",
) -> str:
    """Get medical and health travel information including vaccinations and health risks.

    Args:
        destination: The country or destination.
        health_info: Any relevant traveler health information.
    """
    llm = get_llm(temperature=0.3)
    prompt = MEDICAL_PROMPT.format(
        destination=destination,
        health_info=health_info or "no specific health conditions reported",
    )
    response = llm.invoke(prompt)
    return response.content


# Collect all tools for the agent
ALL_TOOLS = [
    generate_itinerary,
    recommend_hotels,
    estimate_budget,
    suggest_packing_list,
    get_tourism_info,
    get_emergency_info,
    get_medical_info,
]
