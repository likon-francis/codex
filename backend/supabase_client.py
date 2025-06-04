import os
from typing import Optional

try:
    from supabase import create_client, Client
except Exception:  # ImportError etc.
    create_client = None
    Client = None


def get_supabase_client() -> Optional['Client']:
    """Create a Supabase client using environment variables."""
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    if not url or not key:
        return None
    if create_client is None:
        raise RuntimeError('supabase-py is not installed')
    return create_client(url, key)
