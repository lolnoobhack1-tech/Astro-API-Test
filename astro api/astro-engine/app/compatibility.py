"""
Parāśara Ashta-Koota Compatibility Engine (Strict Classical)
------------------------------------------------------------
This module implements the orthodox 36-point matchmaking system 
derived directly from the Brihat Parāśara Hora Shastra.

Corrections implemented:
1. Vashya: Strictly one-directional (Groom -> Bride) + Identity.
2. Graha Maitri: Full 5-tier scoring (5, 4, 3, 2, 0).
3. Gana: Classical point allocation (Same=6, D-M=5, M-R=1, D-R=0).
"""

from typing import Dict, Any, List

# ==========================================
# 1. ASTROLOGICAL CONSTANTS
# ==========================================

RASHI_ORDER: List[str] = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

NAKSHATRA_ORDER: List[str] = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula",
    "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

VARNA_ORDER: List[str] = ["Shudra", "Vaishya", "Kshatriya", "Brahmin"]

VARNA_BY_RASHI: Dict[str, str] = {
    "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya",
    "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya",
    "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra",
    "Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin"
}

# Vashya Map: Key = Controller, Value = List of Controlled Signs
# (Standard Parāśara Table)
VASHYA: Dict[str, List[str]] = {
    "Aries": ["Leo", "Scorpio"], 
    "Taurus": ["Cancer", "Libra"],
    "Gemini": ["Virgo"], 
    "Cancer": ["Scorpio", "Pisces"],
    "Leo": ["Libra"], 
    "Virgo": ["Pisces", "Gemini"],
    "Libra": ["Virgo", "Capricorn"], 
    "Scorpio": ["Cancer"],
    "Sagittarius": ["Pisces"], 
    "Capricorn": ["Aries", "Aquarius"],
    "Aquarius": ["Aries"], 
    "Pisces": ["Capricorn"]
}

# Planetary Friendships (Naisargika Maitri)
GRAHA_MAITRI_FRIEND: Dict[str, List[str]] = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"]
}

GRAHA_NEUTRAL: Dict[str, List[str]] = {
    "Sun": ["Mercury"],
    "Moon": ["Mars", "Jupiter", "Venus", "Saturn"], 
    "Mars": ["Venus"],
    "Mercury": ["Mars", "Jupiter", "Saturn"],
    "Jupiter": ["Saturn"],
    "Venus": ["Mars", "Jupiter"],
    "Saturn": ["Jupiter"]
}

RASHI_LORD: Dict[str, str] = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

# Gana Classification
GANA: Dict[str, str] = {
    "Ashwini": "Deva", "Bharani": "Manushya", "Krittika": "Rakshasa",
    "Rohini": "Manushya", "Mrigashira": "Deva", "Ardra": "Manushya",
    "Punarvasu": "Deva", "Pushya": "Deva", "Ashlesha": "Rakshasa",
    "Magha": "Rakshasa", "Purva Phalguni": "Manushya", "Uttara Phalguni": "Manushya",
    "Hasta": "Deva", "Chitra": "Rakshasa", "Swati": "Deva",
    "Vishakha": "Rakshasa", "Anuradha": "Deva", "Jyeshtha": "Rakshasa",
    "Mula": "Rakshasa", "Purva Ashadha": "Manushya", "Uttara Ashadha": "Manushya",
    "Shravana": "Deva", "Dhanishta": "Rakshasa", "Shatabhisha": "Rakshasa",
    "Purva Bhadrapada": "Manushya", "Uttara Bhadrapada": "Manushya", "Revati": "Deva"
}

YONI: Dict[str, str] = {
    "Ashwini": "Horse", "Bharani": "Elephant", "Krittika": "Sheep",
    "Rohini": "Serpent", "Mrigashira": "Deer", "Ardra": "Dog",
    "Punarvasu": "Cat", "Pushya": "Sheep", "Ashlesha": "Cat",
    "Magha": "Rat", "Purva Phalguni": "Rat", "Uttara Phalguni": "Cow",
    "Hasta": "Buffalo", "Chitra": "Tiger", "Swati": "Buffalo",
    "Vishakha": "Tiger", "Anuradha": "Deer", "Jyeshtha": "Deer",
    "Mula": "Dog", "Purva Ashadha": "Monkey", "Uttara Ashadha": "Mongoose",
    "Shravana": "Monkey", "Dhanishta": "Lion", "Shatabhisha": "Horse",
    "Purva Bhadrapada": "Lion", "Uttara Bhadrapada": "Cow",
    "Revati": "Elephant"
}

YONI_ENEMIES = {
    ("Rat", "Cat"), ("Cat", "Rat"),
    ("Lion", "Elephant"), ("Elephant", "Lion"),
    ("Dog", "Deer"), ("Deer", "Dog"),
    ("Monkey", "Sheep"), ("Sheep", "Monkey"),
    ("Mongoose", "Serpent"), ("Serpent", "Mongoose"),
    ("Cow", "Tiger"), ("Tiger", "Cow"),
    ("Horse", "Buffalo"), ("Buffalo", "Horse"),
    ("Rat", "Lion"), ("Lion", "Rat")
}

NADI: Dict[str, str] = {
    "Ashwini": "Adi", "Bharani": "Madhya", "Krittika": "Antya",
    "Rohini": "Adi", "Mrigashira": "Madhya", "Ardra": "Antya",
    "Punarvasu": "Adi", "Pushya": "Madhya", "Ashlesha": "Antya",
    "Magha": "Antya", "Purva Phalguni": "Adi", "Uttara Phalguni": "Madhya",
    "Hasta": "Antya", "Chitra": "Adi", "Swati": "Madhya", "Vishakha": "Antya",
    "Anuradha": "Adi", "Jyeshtha": "Madhya", "Mula": "Antya",
    "Purva Ashadha": "Adi", "Uttara Ashadha": "Madhya", "Shravana": "Antya",
    "Dhanishta": "Adi", "Shatabhisha": "Madhya",
    "Purva Bhadrapada": "Adi", "Uttara Bhadrapada": "Madhya", "Revati": "Antya"
}

# ==========================================
# 2. CORE LOGIC
# ==========================================

def get_friendship_status(planet1: str, planet2: str) -> str:
    """Helper to determine Naisargika Maitri status (Friend, Neutral, Enemy)"""
    if planet2 in GRAHA_MAITRI_FRIEND.get(planet1, []):
        return "Friend"
    elif planet2 in GRAHA_NEUTRAL.get(planet1, []):
        return "Neutral"
    else:
        return "Enemy"

def generate_ashta_koota(
    bride_moon_sign: str,
    bride_nakshatra: str,
    groom_moon_sign: str,
    groom_nakshatra: str
) -> Dict[str, Any]:
    
    # --- Input Validation ---
    if bride_nakshatra not in NAKSHATRA_ORDER or groom_nakshatra not in NAKSHATRA_ORDER:
        raise ValueError(f"Invalid Nakshatra: {bride_nakshatra} or {groom_nakshatra}")
    if bride_moon_sign not in RASHI_ORDER or groom_moon_sign not in RASHI_ORDER:
        raise ValueError(f"Invalid Moon Sign: {bride_moon_sign} or {groom_moon_sign}")

    score = 0
    breakdown = {}

    # Indices
    b_nak_idx = NAKSHATRA_ORDER.index(bride_nakshatra)
    g_nak_idx = NAKSHATRA_ORDER.index(groom_nakshatra)
    
    r1_idx = RASHI_ORDER.index(bride_moon_sign)
    r2_idx = RASHI_ORDER.index(groom_moon_sign)

    # Lords
    l1 = RASHI_LORD[bride_moon_sign]
    l2 = RASHI_LORD[groom_moon_sign]

    # --- 1. VARNA (1 Point) ---
    b_varna = VARNA_ORDER.index(VARNA_BY_RASHI[bride_moon_sign])
    g_varna = VARNA_ORDER.index(VARNA_BY_RASHI[groom_moon_sign])
    
    # Groom should be equal or higher
    breakdown["Varna"] = 1 if g_varna >= b_varna else 0
    score += breakdown["Varna"]

    # --- 2. VASHYA (2 Points) - STRICT PARĀŚARA ---
    # Rule: If Groom's sign controls Bride's sign, it is auspicious.
    # Logic: Groom=Controller, Bride=Controlled.
    # We check if Bride is in Groom's Vashya list.
    
    if bride_moon_sign == groom_moon_sign:
        breakdown["Vashya"] = 2 # Identity Identity
    elif bride_moon_sign in VASHYA.get(groom_moon_sign, []):
        breakdown["Vashya"] = 2 # Groom controls Bride (Classical requirement)
    else:
        breakdown["Vashya"] = 0 # No mutual credit in strict Parāśara
        
    score += breakdown["Vashya"]

    # --- 3. TARA (3 Points) ---
    # Count from Bride to Groom
    count = (g_nak_idx - b_nak_idx) % 27
    tara_val = count % 9
    # Bad Taras: 1(Janma/0), 3(Vipat/2), 5(Pratyak/4), 7(Naidhana/6)
    if tara_val in [0, 2, 4, 6]:
        breakdown["Tara"] = 0
    else:
        breakdown["Tara"] = 3
    score += breakdown["Tara"]

    # --- 4. YONI (4 Points) ---
    y1, y2 = YONI[bride_nakshatra], YONI[groom_nakshatra]
    # Simple Enemy Check (Binary 0 or 4 as per simplified requirement, 
    # though intermediate points exist in some texts, 0/4 is defensible)
    if (y1, y2) in YONI_ENEMIES or (y2, y1) in YONI_ENEMIES:
        breakdown["Yoni"] = 0
    else:
        breakdown["Yoni"] = 4
    score += breakdown["Yoni"]

    # --- 5. GRAHA MAITRI (5 Points) - FULL 5-TIER LADDER ---
    
    if l1 == l2:
        breakdown["Graha Maitri"] = 5
        lords_are_friendly = True # For Bhakoot Exception
    else:
        # Determine relationship directions
        # Status of L2 towards L1 (Groom's lord towards Bride's lord)
        rel_2_to_1 = get_friendship_status(l1, l2)
        # Status of L1 towards L2 (Bride's lord towards Groom's lord)
        rel_1_to_2 = get_friendship_status(l2, l1)
        
        # Determine if Lords are generally "friendly" for Bhakoot cancellation
        # We consider them friendly if they get >= 4 points
        lords_are_friendly = False

        if rel_2_to_1 == "Friend" and rel_1_to_2 == "Friend":
            breakdown["Graha Maitri"] = 5
            lords_are_friendly = True
        elif (rel_2_to_1 == "Friend" and rel_1_to_2 == "Neutral") or \
             (rel_2_to_1 == "Neutral" and rel_1_to_2 == "Friend"):
            breakdown["Graha Maitri"] = 4
            lords_are_friendly = True
        elif rel_2_to_1 == "Neutral" and rel_1_to_2 == "Neutral":
            breakdown["Graha Maitri"] = 3
        elif (rel_2_to_1 == "Neutral" and rel_1_to_2 == "Enemy") or \
             (rel_2_to_1 == "Enemy" and rel_1_to_2 == "Neutral"):
            breakdown["Graha Maitri"] = 2
        else:
            # Mutual Enemy OR Friend/Enemy (Strict Parāśara often treats F/E harshly)
            breakdown["Graha Maitri"] = 0
            
    score += breakdown["Graha Maitri"]

    # --- 6. GANA (6 Points) - CLASSICAL ALLOCATION ---
    g1, g2 = GANA[bride_nakshatra], GANA[groom_nakshatra]
    
    if g1 == g2:
        breakdown["Gana"] = 6
    else:
        # Create set for easier comparison
        pair = {g1, g2}
        if pair == {"Deva", "Manushya"}:
            breakdown["Gana"] = 5 # Classical score
        elif pair == {"Manushya", "Rakshasa"}:
            breakdown["Gana"] = 1 # Classical score (Avoids 0)
        else:
            # Deva/Rakshasa
            breakdown["Gana"] = 0 
            
    score += breakdown["Gana"]

    # --- 7. BHAKOOT (7 Points) ---
    dist = (r2_idx - r1_idx) % 12
    
    # Bad Positions: 2/12 (1,11), 5/9 (4,8), 6/8 (5,7)
    is_bhakoot_dosha = dist in [1, 11, 4, 8, 5, 7]

    # Bhakoot Parihara (Exception): Cancel Dosha if Lords are Friendly
    if is_bhakoot_dosha:
        if lords_are_friendly:
            breakdown["Bhakoot"] = 7
        else:
            breakdown["Bhakoot"] = 0
    else:
        breakdown["Bhakoot"] = 7
        
    score += breakdown["Bhakoot"]

    # --- 8. NADI (8 Points) ---
    # Strict: No exceptions implemented without Pada data
    if NADI[bride_nakshatra] == NADI[groom_nakshatra]:
        breakdown["Nadi"] = 0
    else:
        breakdown["Nadi"] = 8
    score += breakdown["Nadi"]

    # --- Result ---
    return {
        "total_gunas": int(score),
        "max_gunas": 36,
        "breakdown": breakdown,
        "verdict": "Good" if score >= 18 else "Low"
    }
