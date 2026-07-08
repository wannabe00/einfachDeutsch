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

# Hosts: localhost for dev, plus any comma-separated hosts from the env
# (e.g. the Render domain) for production.
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS += [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]


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
    "allauth.socialaccount.providers.github",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # Local apps
    "apps.accounts",
    "apps.books",
    "apps.vocabulary",
    "apps.grammar",
    "apps.exercises",
    "apps.ai_assistant",
    "apps.recitation",
    "apps.videos",
    "apps.history",
]

SITE_ID = 1

MIDDLEWARE = [
    # CorsMiddleware must come first so CORS headers are added to every response.
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise serves static files in production (must follow SecurityMiddleware).
    "whitenoise.middleware.WhiteNoiseMiddleware",
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


# Postgres (Neon) in production via DATABASE_URL; SQLite locally otherwise.
import dj_database_url  # noqa: E402

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=bool(os.getenv("DATABASE_URL")),
    )
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
STATIC_ROOT = BASE_DIR / "staticfiles"
# WhiteNoise: compressed, hashed static files in production.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---- Django REST Framework ----
# Token auth (Authorization: Token <key>) for the SPA; session auth kept for the
# browsable API/admin. Content endpoints stay public-readable; per-user endpoints
# enforce auth at the view level.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Expiring variant of TokenAuthentication: tokens older than
        # TOKEN_TTL_DAYS are rejected + deleted (stolen tokens stop working).
        "apps.accounts.authentication.ExpiringTokenAuthentication",
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
        # Brute-force guard on login + social code exchange (per IP).
        "login": os.getenv("THROTTLE_LOGIN", "5/min"),
        # One-shot onboarding endpoint (per user, defence in depth).
        "onboarding": os.getenv("THROTTLE_ONBOARDING", "5/min"),
    },
}

# Auth tokens are rejected + deleted after this many days (forces re-login).
TOKEN_TTL_DAYS = int(os.getenv("TOKEN_TTL_DAYS", "30"))

# ---- Auth (allauth + dj-rest-auth), token-based ----
# Accounts are created via Google/GitHub OAuth (see GoogleLogin/GitHubLogin).
# After first sign-in the user completes onboarding (username + password + name)
# and can then log in with either provider or username + password. No email or
# phone verification is used.
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True

# Social login: trust the provider's email (already verified by Google/GitHub),
# create the account automatically, never block on email confirmation.
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    },
    "github": {
        "APP": {
            "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
            "secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
            "key": "",
        },
        "SCOPE": ["read:user", "user:email"],
    },
}

# Where the SPA lives — used to build OAuth callback URLs.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

REST_AUTH = {
    "USE_JWT": False,  # simple DRF token in localStorage — easiest for the SPA
    "SESSION_LOGIN": False,
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",
    "USER_DETAILS_SERIALIZER": "apps.accounts.serializers.UserDetailsSerializer",
    "LOGIN_SERIALIZER": "apps.accounts.serializers.LoginSerializer",
}

# Email: real SMTP when EMAIL_HOST is configured (production), else the dev
# console backend. Only used for password reset (no email verification).
if os.getenv("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@einfachdeutsch.local")

# ---- CORS ----
# Dev: the Vite server (any localhost port). Prod: explicit origins from env
# (comma-separated, e.g. the Vercel domain).
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOWED_ORIGINS += [
    o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
]
# Cross-site POSTs (login/registration) from the SPA domain need CSRF trust.
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]
if DEBUG:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^http://localhost:\d+$",
        r"^http://127\.0\.0\.1:\d+$",
    ]

# ---- Production hardening (only when DEBUG is off) ----
if not DEBUG:
    # Render terminates TLS at the proxy and forwards this header.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True") == "True"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "2592000"))  # 30 days
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# LLM API key (AI features). Gemini is the active provider for the AI
# chat/assistant; empty until configured in .env (then endpoints return 503).
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


# ---- Lesson schedule + streaks (Phase 15, all tunable) ----
# Weekdays new lessons unlock on (Mon=0 … Sun=6). Default Mon/Wed/Fri.
LESSON_UNLOCK_WEEKDAYS = [
    int(d) for d in os.getenv("LESSON_UNLOCK_WEEKDAYS", "0,2,4").split(",") if d != ""
]
STREAK_INITIAL_FREEZE_TOKENS = int(os.getenv("STREAK_INITIAL_FREEZE_TOKENS", "2"))
STREAK_FREEZE_EARN_DAYS = int(os.getenv("STREAK_FREEZE_EARN_DAYS", "14"))
STREAK_FREEZE_MAX = int(os.getenv("STREAK_FREEZE_MAX", "5"))

# ---- Recitation v2 cost control (Phase 16, tunable) ----
RECITATION_DAILY_CAP = int(os.getenv("RECITATION_DAILY_CAP", "5"))
RECITATION_MAX_AUDIO_SECONDS = int(os.getenv("RECITATION_MAX_AUDIO_SECONDS", "120"))
RECITATION_MAX_AUDIO_MB = int(os.getenv("RECITATION_MAX_AUDIO_MB", "10"))

# ---- Video / show suggestions (Phase 17) ----
# Minimum CEFR level at which curated video suggestions unlock (after A2 = B1).
VIDEO_UNLOCK_MIN_LEVEL = os.getenv("VIDEO_UNLOCK_MIN_LEVEL", "B1")


# ---- Cloudinary (profile picture uploads) ----
# Server-side image hosting (the API secret never reaches the frontend). If
# unset, the avatar-upload endpoint returns a graceful 503.
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")
if CLOUDINARY_CLOUD_NAME:
    import cloudinary

    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True,
    )
