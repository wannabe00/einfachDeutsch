"""
Django settings for the German Learning Platform.

Brick 0.1 — base project configuration. DRF + CORS are wired in brick 0.2.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# BASE_DIR points at the backend/ directory (the folder containing manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from backend/.env (git-ignored).
load_dotenv(BASE_DIR / ".env")

# A safe, obviously-insecure default is used for local dev only.
# The real key lives in backend/.env and is never committed.
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-dev-only-key-change-me-via-dotenv",
)

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # required by allauth
    # Third-party
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # Local apps
    "apps.accounts",
    "apps.books",
    "apps.vocabulary",
    "apps.grammar",
    "apps.exercises",
    "apps.ai_assistant",
]

SITE_ID = 1

MIDDLEWARE = [
    # CorsMiddleware must come first so CORS headers are added to every response.
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # allauth requires its middleware after AuthenticationMiddleware.
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---- Django REST Framework ----
# Token auth (Authorization: Token <key>) for the SPA; session auth kept for the
# browsable API/admin. Content endpoints stay public-readable; per-user endpoints
# enforce auth at the view level.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    # Anti-abuse: a request ceiling per anonymous IP and per signed-in user.
    # This is the real spam/DDoS guard (the frontend guest cap is just UX).
    # AI endpoints add their own tighter per-user caps (see ai_assistant.throttles).
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.getenv("THROTTLE_ANON", "120/min"),
        "user": os.getenv("THROTTLE_USER", "600/min"),
        # Protect the (free, limited) Gemini quota — per signed-in user.
        "ai_burst": os.getenv("THROTTLE_AI_BURST", "12/min"),
        "ai_daily": os.getenv("THROTTLE_AI_DAILY", "120/day"),
    },
}

# ---- Auth (allauth + dj-rest-auth), token-based ----
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
# Mandatory email verification: registration sends a confirmation link and does
# not return a token; login is blocked until the email is verified (see
# LoginSerializer). In dev the link prints to the runserver terminal (console
# email backend); production wires real SMTP (Phase 12).
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_REQUIRED = True  # required by allauth when verification is mandatory
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_ADAPTER = "apps.accounts.adapter.AccountAdapter"

# Where the SPA lives — used to build the email-confirmation link.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

REST_AUTH = {
    "USE_JWT": False,  # simple DRF token in localStorage — easiest for the SPA
    "SESSION_LOGIN": False,
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",
    "REGISTER_SERIALIZER": "apps.accounts.serializers.RegisterSerializer",
    "USER_DETAILS_SERIALIZER": "apps.accounts.serializers.UserDetailsSerializer",
    "LOGIN_SERIALIZER": "apps.accounts.serializers.LoginSerializer",
}

# Dev email backend — verification/reset links print to the runserver terminal.
# Production should set a real SMTP backend.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ---- CORS ----
# Allow the Vite dev server to call the API during development.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# In local dev, accept any localhost port (Vite may pick an alternate port).
# Production keeps the explicit allow-list above only.
if DEBUG:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://localhost:\d+$",
        r"^http://127\.0\.0\.1:\d+$",
    ]


# LLM API keys (AI features). Empty until configured in .env.
# Gemini is the active provider for the AI chat/assistant.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")  # legacy / optional
