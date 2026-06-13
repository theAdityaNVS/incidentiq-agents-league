"""Vercel serverless entrypoint — exposes the FastAPI ASGI app.

Vercel's @vercel/python runtime serves the module-level `app` (ASGI). The IncidentIQ
app runs in local reasoning mode on Vercel (no Azure needed at runtime; azure imports are
lazy and only used by Foundry mode).
"""

import os
import sys

# Make the src/ package importable on the serverless filesystem.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from incidentiq.api import app  # noqa: E402  (path set above)
