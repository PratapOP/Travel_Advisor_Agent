import os
import json
import random
from openai import OpenAI
from .prompts import (
    ITINERARY_SYSTEM_PROMPT,
    BUDGET_SYSTEM_PROMPT,
    PACKING_SYSTEM_PROMPT,
    CHAT_SYSTEM_PROMPT
)

def get_openai_client():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    try:
        # Check if the API key is not just a placeholder
        if api_key.startswith('your-') or len(api_key) < 15:
            return None
        return OpenAI(api_key=api_key)
    except Exception:
        return None

def generate_itinerary(source, destination, num_days, budget_amount, interests, travel_style):
    client = get_openai_client()
    
    if client:
        try:
            prompt = ITINERARY_SYSTEM_PROMPT.format(
                source=source,
                destination=destination,
                num_days=num_days,
                budget_amount=budget_amount,
                interests=interests,
                travel_style=travel_style
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=1500
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"OpenAI itinerary generation failed: {e}. Using fallback engine.")
            # Fall through to local fallback generator

    # Heuristic Fallback Generator
    day_plans = []
    interests_list = [i.strip().lower() for i in interests.split(',') if i.strip()]
    
    # Base generic themes
    themes = [
        "Arrival & City Orientation",
        "Historical Landmarks & Culture",
        "Nature Trails & Hidden Gems",
        "Culinary Journey & Local Markets",
        "Scenic Photography & Architecture",
        "Adventure Activities & Sports",
        "Leisure & Souvenir Shopping",
        "Departure Preparation & Final Vistas"
    ]
    
    generic_activities = [
        {"time": "09:00 AM", "activity": "Explore Historical Quarter", "description": "Walk through the old town to discover local architecture and history.", "expense": 15.00, "transport": "Walking"},
        {"time": "11:30 AM", "activity": "Visit Landmark Museum", "description": "Examine art collections and local cultural exhibits.", "expense": 20.00, "transport": "Metro"},
        {"time": "01:30 PM", "activity": "Lunch at traditional restaurant", "description": "Taste local delicacies and street food.", "expense": 25.00, "transport": "Walking"},
        {"time": "03:30 PM", "activity": "Scenic viewpoint exploration", "description": "Take panoramic pictures of the city skyline.", "expense": 0.00, "transport": "Tram"},
        {"time": "06:00 PM", "activity": "Leisure walk at Central Park", "description": "Enjoy the relaxing gardens and local fountains.", "expense": 5.00, "transport": "Walking"},
        {"time": "08:00 PM", "activity": "Fine Dining & Live Music", "description": "Conclude the day with live performance and local drinks.", "expense": 45.00, "transport": "Taxi"}
    ]

    adventure_activities = [
        {"time": "08:30 AM", "activity": "Outdoor Adventure Excursion", "description": "Guided hiking, ziplining, or rock climbing.", "expense": 60.00, "transport": "Shuttle Bus"},
        {"time": "01:00 PM", "activity": "Camp-style lunch", "description": "Traditional outdoor lunch in the wilderness.", "expense": 15.00, "transport": "Walking"},
        {"time": "03:00 PM", "activity": "Kayaking or river rafting session", "description": "Thrilling water sports activity with a certified guide.", "expense": 40.00, "transport": "Walking"},
        {"time": "07:30 PM", "activity": "Barbecue Dinner under the stars", "description": "Relax and recharge by the campfire.", "expense": 30.00, "transport": "Taxi"}
    ]

    culture_activities = [
        {"time": "09:30 AM", "activity": "Heritage Temple/Church Tour", "description": "Appreciate ancient architecture and religious legacy.", "expense": 10.00, "transport": "Walking"},
        {"time": "12:00 PM", "activity": "Local Cooking Workshop", "description": "Learn to cook authentic traditional recipes from local chefs.", "expense": 50.00, "transport": "Metro"},
        {"time": "04:00 PM", "activity": "Artisans Market tour", "description": "Watch craft demonstrations and support local artisans.", "expense": 5.00, "transport": "Walking"},
        {"time": "07:00 PM", "activity": "Traditional Dance/Theatre Show", "description": "Watch a cultural performance depicting local folklore.", "expense": 35.00, "transport": "Taxi"}
    ]

    for d in range(1, num_days + 1):
        day_theme = themes[(d - 1) % len(themes)]
        activities = []
        
        # Decide activity templates based on travel style/interests
        active_pool = generic_activities
        if 'adventure' in travel_style.lower() or 'adventure' in interests_list:
            active_pool = adventure_activities if d % 2 == 0 else generic_activities
        elif 'cultural' in travel_style.lower() or 'history' in interests_list or 'culture' in interests_list:
            active_pool = culture_activities if d % 2 == 0 else generic_activities
            
        # Compile 3-4 activities for the day
        selected_indexes = [0, 1, 2, 3] if len(active_pool) >= 4 else list(range(len(active_pool)))
        for idx in selected_indexes:
            act = active_pool[idx].copy()
            # Scale expenses based on total budget level
            scale = 0.5 if budget_amount < 500 else (1.5 if budget_amount > 2000 else 1.0)
            act['estimated_expense'] = round(act['estimated_expense'] * scale, 2)
            activities.append({
                "time": act['time'],
                "activity": act['activity'],
                "description": f"{act['description']} (Experience in {destination})",
                "estimated_expense": act['estimated_expense'],
                "transportation": act['transport']
            })
            
        day_plans.append({
            "day": d,
            "theme": day_theme,
            "activities": activities
        })
        
    return {
        "destination": destination,
        "days_count": num_days,
        "total_estimated_expense": budget_amount,
        "day_wise_plan": day_plans
    }

def generate_budget(destination, num_days, budget_amount, travel_style):
    client = get_openai_client()
    
    if client:
        try:
            prompt = BUDGET_SYSTEM_PROMPT.format(
                destination=destination,
                num_days=num_days,
                budget_amount=budget_amount,
                travel_style=travel_style
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.5,
                max_tokens=500
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"OpenAI budget generation failed: {e}. Using fallback calculation.")
            
    # Deterministic budget splitter
    total = float(budget_amount)
    
    # standard percentage splits based on style
    if 'luxury' in travel_style.lower():
        accommodation = total * 0.50
        food = total * 0.20
        transport = total * 0.15
        emergency = total * 0.15
    elif 'budget' in travel_style.lower():
        accommodation = total * 0.35
        food = total * 0.25
        transport = total * 0.25
        emergency = total * 0.15
    else: # Moderate/Adventure
        accommodation = total * 0.40
        food = total * 0.25
        transport = total * 0.20
        emergency = total * 0.15
        
    return {
        "total_cost": round(total, 2),
        "accommodation_cost": round(accommodation, 2),
        "food_budget": round(food, 2),
        "transport_budget": round(transport, 2),
        "emergency_reserve": round(emergency, 2)
    }

def generate_packing(destination, num_days, interests):
    client = get_openai_client()
    
    if client:
        try:
            prompt = PACKING_SYSTEM_PROMPT.format(
                destination=destination,
                num_days=num_days,
                interests=interests
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.5,
                max_tokens=600
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"OpenAI packing list generation failed: {e}. Using fallback lists.")

    # Fallback lists based on inputs
    weather_items = [
        "Light jacket", 
        "Comfortable walking shoes", 
        "Umbrella or raincoat", 
        "Sunglasses & Sunscreen"
    ]
    if num_days > 5:
        weather_items.extend(["Extra underwear layers", "Hat / Cap"])
        
    destination_items = [
        "Universal plug adapter", 
        "Phone charger & power bank", 
        "Reusable water bottle",
        f"Offline navigation map of {destination}"
    ]
    
    medical_items = [
        "Pain relief tablets (Ibuprofen/Paracetamol)", 
        "Band-aids & antiseptic wipes", 
        "Anti-diarrhea tablets",
        "Personal prescription medicines",
        "Motion sickness pills"
    ]
    
    travel_documents = [
        "Passport (with at least 6 months validity)", 
        "Printed flight tickets & boarding passes", 
        "Hotel reservation slips", 
        "Travel Insurance documents",
        "Local currency cash & international credit cards"
    ]
    
    return {
        "weather_items": weather_items,
        "destination_items": destination_items,
        "medical_items": medical_items,
        "travel_documents": travel_documents
    }

def run_chat_agent(chat_history, user_profile):
    """
    chat_history is a list of dicts: [{'role': 'user'|'assistant', 'content': '...'}]
    user_profile is a Profile model or dict of preferences
    """
    client = get_openai_client()
    
    # Setup profile preferences context
    if isinstance(user_profile, dict):
        travel_style = user_profile.get('travel_style', 'Leisure')
        budget_pref = user_profile.get('budget_preference', 'Moderate')
        interests = user_profile.get('interests', 'General')
    else:
        travel_style = user_profile.travel_style
        budget_pref = user_profile.budget_preference
        interests = user_profile.interests
        
    system_prompt = CHAT_SYSTEM_PROMPT.format(
        travel_style=travel_style,
        budget_preference=budget_pref,
        interests=interests
    )
    
    if client:
        try:
            messages = [{"role": "system", "content": system_prompt}]
            # map roles from Django model to OpenAI roles
            for msg in chat_history:
                role = "user" if msg['role'] == 'user' else "assistant"
                messages.append({"role": role, "content": msg['content']})
                
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=600
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI Chat execution failed: {e}. Operating in rule-based chat fallback.")

    # Rule-Based Fallback Conversational Engine
    # Get last message
    last_msg = ""
    if chat_history:
        last_msg = chat_history[-1]['content'].lower()
        
    # Heuristic response construction
    response = ""
    medical_keyword = False
    
    if "hello" in last_msg or "hi" in last_msg or "hey" in last_msg:
        response = f"Hello! I am your Travel Adviser Agent. How can I assist you with your upcoming trips today? I can help you compile detailed itineraries, segment budgets, prepare packing checklists, or lookup local emergency numbers."
    elif "itinerary" in last_msg or "plan" in last_msg or "days" in last_msg:
        response = f"I'd love to help you build an itinerary! To get started, please use our **Itinerary Planner** section to specify your source, destination, duration, and budget. Alternatively, tell me: Where are you traveling to, and for how many days?"
    elif "budget" in last_msg or "cost" in last_msg or "money" in last_msg or "price" in last_msg:
        response = f"Setting a clear budget is key! Under your current profile, you prefer a **{budget_pref}** budget style. I can generate accommodation, transport, food, and emergency splits. Would you like me to suggest budget estimations for a specific city?"
    elif "pack" in last_msg or "clothing" in last_msg or "documents" in last_msg:
        response = f"Packing checklist recommendations: For a standard trip, you should always pack a universal power adapter, emergency medical kit (paracetamol, bandages), hotel printouts, and weather-appropriate clothes. You can view a fully generated list under the **Packing Assistant** section!"
    elif "emergency" in last_msg or "police" in last_msg or "help" in last_msg or "embassy" in last_msg or "ambulance" in last_msg:
        response = f"If you are facing an urgent situation, please check our **Emergency Assistant** tool immediately for city-specific contact numbers for Police, Ambulance, and Embassy services. Stay safe!"
    elif "medical" in last_msg or "health" in last_msg or "vaccin" in last_msg or "sick" in last_msg or "ill" in last_msg or "doctor" in last_msg or "fitness" in last_msg:
        medical_keyword = True
        response = f"Regarding health and medical guidance: Before you travel, always ensure you have active travel insurance, complete any recommended vaccinations (e.g. Hepatitis, Yellow Fever depending on destination), pack critical prescription medications in your carry-on, and carry a basic first-aid kit."
    elif "pose" in last_msg or "camera" in last_msg or "photo" in last_msg or "picture" in last_msg:
        response = f"To capture the best travel memories, try our **Photo Pose Assistant**! It provides recommendations for Solo, Couple, Family, and Adventure poses. For example, for adventure, try a 'candid action walking shot' or a 'silhouette pose' at sunset."
    else:
        response = f"That sounds like an exciting travel idea! Based on your profile ({travel_style} traveler, interested in {interests}), I suggest researching local attractions, reviewing budget estimates, and checking weather patterns for your destination. What details would you like to explore next?"

    # Append disclaimer if talking about medical topics
    if medical_keyword or "medical" in last_msg or "health" in last_msg or "vaccin" in last_msg or "sick" in last_msg:
        response += "\n\n**Disclaimer: Not a substitute for professional medical advice.**"
        
    return response
