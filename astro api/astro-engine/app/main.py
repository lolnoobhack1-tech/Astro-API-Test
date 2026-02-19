from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

# 1. IMPORT STRICT MODELS FROM models.py
# (Do not define them here again!)
from .models import (
    KundliRequest, 
    KundliResponse, 
    CompatibilityRequest, 
    CompatibilityResponse
)
from .astrology import generate_kundli
from .compatibility import generate_ashta_koota

# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI(
    title="Kundli Astro Engine",
    description="A production-ready Kundli & Compatibility API using Swiss Ephemeris and Parāśara Ashta-Koota",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Kundli Generation Endpoint
# -----------------------------
@app.post(
    "/generate-kundli",
    response_model=KundliResponse,
    status_code=status.HTTP_200_OK
)
async def generate_kundli_api(request: KundliRequest) -> KundliResponse:
    """
    Generate a kundli (astrological chart) based on birth details.
    """
    try:
        return generate_kundli(request)
    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Validation Error", "details": ve.errors()}
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Invalid Input", "message": str(ve)}
        )
    except Exception as e:
        import traceback
        print(f"Error generating kundli: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal Server Error", "message": "Failed to generate kundli"}
        )

# -----------------------------
# Compatibility Endpoint (UPDATED)
# -----------------------------
@app.post(
    "/calculate-compatibility",
    response_model=CompatibilityResponse,
    status_code=status.HTTP_200_OK
)
async def calculate_compatibility_api(request: CompatibilityRequest) -> CompatibilityResponse:
    """
    Calculate Ashta-Koota compatibility.
    Uses strict Enums for Moon Sign and Nakshatra inputs.
    """
    try:
        # 2. UNWRAP THE REQUEST
        # We explicitly extract the fields from the Pydantic model
        # and pass them as strings to the logic function.
        result = generate_ashta_koota(
            bride_moon_sign=request.bride.moon_sign,
            bride_nakshatra=request.bride.nakshatra,
            groom_moon_sign=request.groom.moon_sign,
            groom_nakshatra=request.groom.nakshatra
        )
        return result

    except ValidationError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Validation Error", "details": ve.errors()}
        )
    except ValueError as ve:
        # Catches logical errors (e.g. invalid nakshatra names that slipped through)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Logic Error", "message": str(ve)}
        )
    except Exception as e:
        import traceback
        print(f"Error calculating compatibility: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal Server Error", "message": "Failed to calculate compatibility"}
        )

# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get(
    "/health",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK
)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify API is running.
    """
    try:
        return {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "database": "ok",
                "cache": "ok"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "unhealthy", "error": str(e)}
        )
