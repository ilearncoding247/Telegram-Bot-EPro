#!/usr/bin/env python3
"""
Minimal FastAPI server exposing referral APIs for website integration.

Endpoints:
- GET /api/health
- GET /api/referral/progress?user_id=123  (or ?referral_code=ref_xxx)

Run locally:
  uvicorn api_server:app --host 0.0.0.0 --port 8080 --reload
"""

import os
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from telegramreferralpro.database import Database
from telegramreferralpro.referral_system import ReferralSystem


logger = logging.getLogger(__name__)

# Instantiate shared services once
database = Database()
referral_system = ReferralSystem(database)

app = FastAPI(title="Referral API", version="1.0.0")

# CORS setup: allow configured frontend origin or default to common dev origins
frontend_origin = os.getenv("FRONTEND_ORIGIN")
allowed_origins = [frontend_origin] if frontend_origin else [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/referral/progress")
def get_referral_progress(
    user_id: Optional[int] = Query(default=None, ge=1),
    referral_code: Optional[str] = Query(default=None),
) -> dict:
    """Return referral progress for a given user.

    One of user_id or referral_code must be provided.
    """
    if not user_id and not referral_code:
        raise HTTPException(status_code=400, detail="Provide either user_id or referral_code")

    try:
        resolved_user_id: Optional[int] = user_id

        if resolved_user_id is None and referral_code:
            user = database.get_user_by_referral_code(referral_code)
            if not user:
                raise HTTPException(status_code=404, detail="User not found for referral code")
            # database layer may backfill user_id if encoded in code; otherwise omit
            resolved_user_id = user.get("user_id") if isinstance(user, dict) else None

        if resolved_user_id is None:
            # Fall back to zero progress if user_id cannot be resolved
            progress = {
                "active_referrals": 0,
                "total_referrals": 0,
                "target": referral_system.get_active_referral_target(),
                "remaining": referral_system.get_active_referral_target(),
                "target_reached": False,
                "progress_percentage": 0,
            }
            return {"ok": True, "user_id": None, "progress": progress}

        progress = referral_system.get_referral_progress(resolved_user_id)
        return {"ok": True, "user_id": resolved_user_id, "progress": progress}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching referral progress: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Optional convenience: allow running via `python api_server.py`
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("REFERRAL_API_PORT", os.getenv("PORT", "8080")))
    uvicorn.run("api_server:app", host="0.0.0.0", port=port, reload=True)


