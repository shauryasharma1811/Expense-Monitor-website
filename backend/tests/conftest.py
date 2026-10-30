import pytest
from app.auth.auth import login_attempts, revoked_tokens

@pytest.fixture(autouse=True)
def reset_auth_state():
    login_attempts.clear()
    revoked_tokens.clear()
    yield
    login_attempts.clear()
    revoked_tokens.clear()
