import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env.local"))

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/databases/")

# MCP Server Configuration
MCP_SERVERS = {
    "email": {
        "name": "email-server",
        "description": "Email data source for OOO summarizer"
    },
    "calendar": {
        "name": "calendar-server", 
        "description": "Calendar data source for OOO summarizer"
    },
    "slack": {
        "name": "slack-server",
        "description": "Slack data source for OOO summarizer"
    },
}

# OOO Period Configuration
DEFAULT_OOO_START = "2024-01-15"
DEFAULT_OOO_END = "2024-01-22"
