# Every Platform-layer model must be imported here so it registers on
# Base.metadata as soon as anything imports app.platform — this is what
# alembic/env.py relies on for autogenerate to see every table. Neither
# SQLAlchemy nor Alembic prescribes this specific pattern (confirmed
# against their official docs), but centralizing it here means adding a
# new Platform model can never again silently produce an empty migration
# the way forgetting a one-off import in env.py already did once.
from app.platform.users.models import User  # noqa: F401
