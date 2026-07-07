from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import yaml
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Default configuration
config = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000"
}

# YAML configuration
if os.path.exists("config.development.yaml"):
    with open("config.development.yaml") as f:
        yaml_config = yaml.safe_load(f)
        if yaml_config:
            config.update(yaml_config)

# .env configuration
if os.getenv("APP_DEBUG") is not None:
    config["debug"] = os.getenv("APP_DEBUG").lower() in ["true", "1", "yes", "on"]

if os.getenv("APP_LOG_LEVEL"):
    config["log_level"] = os.getenv("APP_LOG_LEVEL")

if os.getenv("APP_API_KEY"):
    config["api_key"] = os.getenv("APP_API_KEY")

if os.getenv("NUM_WORKERS"):
    config["workers"] = int(os.getenv("NUM_WORKERS"))

# OS environment variables
if os.getenv("APP_WORKERS"):
    config["workers"] = int(os.getenv("APP_WORKERS"))

@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    result = config.copy()

    for item in set:
        if "=" not in item:
            continue

        key, value = item.split("=", 1)

        if key in ["port", "workers"]:
            result[key] = int(value)

        elif key == "debug":
            result[key] = value.lower() in ["true", "1", "yes", "on"]

        else:
            result[key] = value

    result["api_key"] = "****"

    return result