"""Django settings for einfachDeutsch."""

import os
from pathlib import Path

from dotenv import load_dotenv

# BASE_DIR points at the backend/ directory (the folder containing manage.py).
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from backend/.env (git-ignored).
load_dotenv(BASE_DIR / ".env")

# Off unless .env says DEBUG=True, so a missing variable never exposes debug
# pages in production.
DEBUG = os.getenv("DEBUG", "False") == "True"

# The real key lives in backend/.env (and the host's env) and is never
# committed. The insecure fallback only works with DEBUG on: anyone knowing
# the key could forge password-reset links.
SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY or SECRET_KEY.startswith("django-insecure"):
    if not DEBUG:
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured("Set a long random SECRET_KEY in the environment.")
    SECRET_KEY = "django-insecure-dev-only-key-change-me-via-dotenv"

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
    "apps.talk",
    "apps.videos",
    "apps.history",
    "apps.curriculum",
]

SITE_ID = 1

MIDDLEWARE = [
    # CorsMiddleware must come first so CORS headers are added to every response.
    "corsheaders.middleware.CorsMiddleware",
    # Right after CORS, so even a refused oversized request carries CORS headers.
    "config.middleware.RequestSizeLimitMiddleware",
    "config.middleware.ApiSecurityHeadersMiddleware",
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
        "DIRS": [BASE_DIR / "templates"],  # project overrides (e.g. the reset e-mail)
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
    # JSON only in production: the HTML "browsable API" would show every
    # endpoint's name and docs to anyone (kept locally for development).
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"]
    + ([] if not DEBUG else ["rest_framework.renderers.BrowsableAPIRenderer"]),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # Expiring variant of TokenAuthentication: tokens older than
        # TOKEN_TTL_DAYS are rejected + deleted (stolen tokens stop working).
        "apps.accounts.authentication.ExpiringTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    # Anti-abuse: a request ceiling per anonymous IP and per signed-in user.
    # This is the real spam/DDoS guard (the frontend guest cap is just UX).
    # AI endpoints add their own tighter per-user caps (see ai_assistant.throttles).
    # How many proxies in front of us append to X-Forwarded-For (Render's: 1).
    # Throttles then use the address our own proxy saw, not the client-written
    # part of the header, which anyone can fake to dodge every limit. 0 locally.
    # Check it with /api/accounts/client-ip/ (staff) after a hosting change.
    "NUM_PROXIES": int(os.getenv("NUM_PROXIES", "0" if DEBUG else "1")),
    # Fail closed: a view must say AllowAny to be public (books, grammar, words,
    # stats and the auth endpoints do).
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.getenv("THROTTLE_ANON", "120/min"),
        "user": os.getenv("THROTTLE_USER", "600/min"),
        # Per signed-in user, to protect the limited free Gemini quota.
        "ai_burst": os.getenv("THROTTLE_AI_BURST", "12/min"),
        "ai_daily": os.getenv("THROTTLE_AI_DAILY", "120/day"),
        # Brute-force guard on login + social code exchange (per IP).
        "login": os.getenv("THROTTLE_LOGIN", "5/min"),
        # One-shot onboarding endpoint (per user, defence in depth).
        "onboarding": os.getenv("THROTTLE_ONBOARDING", "5/min"),
        # Reset e-mails and reset attempts (per IP), so nobody can flood an inbox.
        "password_reset": os.getenv("THROTTLE_PASSWORD_RESET", "5/hour"),
        # Placement test submissions (each asks Gemini), per user.
        "placement": os.getenv("THROTTLE_PLACEMENT", "5/day"),
        # Password changes and 2FA changes (each checks the password), per user,
        # so a stolen token can't guess the password.
        "password_change": os.getenv("THROTTLE_PASSWORD_CHANGE", "5/hour"),
        # Avatar uploads (Cloudinary), per user.
        "uploads": os.getenv("THROTTLE_UPLOADS", "10/hour"),
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

# Where the frontend lives; used to build OAuth callback URLs.
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

REST_AUTH = {
    "USE_JWT": False,  # A plain DRF token in localStorage is simplest for the SPA.
    # A password change must prove the current password; without this a stolen
    # token alone could change it and take the account over.
    "OLD_PASSWORD_FIELD_ENABLED": True,
    "SESSION_LOGIN": False,
    "TOKEN_MODEL": "rest_framework.authtoken.models.Token",
    "USER_DETAILS_SERIALIZER": "apps.accounts.serializers.UserDetailsSerializer",
    "LOGIN_SERIALIZER": "apps.accounts.serializers.LoginSerializer",
    "PASSWORD_RESET_SERIALIZER": "apps.accounts.serializers.PasswordResetSerializer",
    "PASSWORD_RESET_CONFIRM_SERIALIZER": "apps.accounts.serializers.PasswordResetConfirmSerializer",
}
# The reset e-mail's subject; allauth would otherwise prefix the Sites domain.
ACCOUNT_EMAIL_SUBJECT_PREFIX = "einfachDeutsch: "

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
    # Fail fast instead of hanging until the web worker is killed.
    EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", "10"))
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
    # A year: browsers only accept "preload" (below) with at least that.
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


# LLM API key (AI features). Gemini is the active provider for the AI
# chat/assistant; empty until configured in .env (then endpoints return 503).
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Azure Speech (free F0 tier) speaks the Hören recordings when set; else Gemini does.
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "")


# ---- Streaks (every day counts; a missed day uses a freeze) ----
STREAK_INITIAL_FREEZE_TOKENS = int(os.getenv("STREAK_INITIAL_FREEZE_TOKENS", "2"))
STREAK_FREEZE_EARN_DAYS = int(os.getenv("STREAK_FREEZE_EARN_DAYS", "14"))
STREAK_FREEZE_MAX = int(os.getenv("STREAK_FREEZE_MAX", "5"))

# ---- Talk to AI cost control ----
# Talk to AI: live voice conversations per premium user per day.
TALK_DAILY_CAP = int(os.getenv("TALK_DAILY_CAP", "5"))
# Talk to AI minutes per premium user per calendar month (priced into $2.99/mo).
TALK_MONTHLY_MINUTES = int(os.getenv("TALK_MONTHLY_MINUTES", "60"))

# ---- AI-written history lessons (premium) ----
# Most lessons one user may have the AI write per day.
HISTORY_AI_DAILY_LIMIT = int(os.getenv("HISTORY_AI_DAILY_LIMIT", "5"))
# Optional last-resort picture source for history lessons (free key from pexels.com).
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# ---- Video / show suggestions ----
# Minimum CEFR level at which curated video suggestions unlock (after A2 = B1).
VIDEO_UNLOCK_MIN_LEVEL = os.getenv("VIDEO_UNLOCK_MIN_LEVEL", "B1")


# ---- Learning path: energy + premium ----
# Free tier energy: bar size, and hours to regenerate +1. Premium = unlimited.
ENERGY_MAX = int(os.getenv("ENERGY_MAX", "3"))
ENERGY_REFILL_HOURS = int(os.getenv("ENERGY_REFILL_HOURS", "4"))
# Length of the premium free trial, in days.
PREMIUM_TRIAL_DAYS = int(os.getenv("PREMIUM_TRIAL_DAYS", "7"))

# ---- Level checkpoint exam ----
# Share of a level's lessons that must be completed before the exam unlocks,
# the score needed to pass (and be promoted), and how many questions it samples.
EXAM_UNLOCK_RATIO = float(os.getenv("EXAM_UNLOCK_RATIO", "0.9"))
EXAM_PASS_THRESHOLD = float(os.getenv("EXAM_PASS_THRESHOLD", "0.8"))
EXAM_QUESTION_COUNT = int(os.getenv("EXAM_QUESTION_COUNT", "12"))


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


# The cache holds the rate-limit counters, so it lives in the database: shared by
# every server process (and serverless instance) and kept across restarts. The
# table is made by a migration (accounts 0012).
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    }
}

# A password-reset link works for one hour (Django's default is three days).
PASSWORD_RESET_TIMEOUT = 60 * 60
# Only the admin uses sessions (the app signs in with tokens): log staff out
# after a working day instead of two weeks.
SESSION_COOKIE_AGE = 8 * 60 * 60

# ---- Admin ----
# A secret path in production (e.g. "manage-7f3k9q/"), so bots scanning for
# /admin/ find nothing. Must end with "/".
ADMIN_URL = os.getenv("ADMIN_URL", "admin/").strip("/") + "/"
# Staff need two-factor login on to use the admin (off locally with DEBUG).
ADMIN_REQUIRE_2FA = os.getenv("ADMIN_REQUIRE_2FA", str(not DEBUG)) == "True"

# ---- Cost guards (site-wide, on top of the per-user throttles) ----
# Daily caps for the whole site, per paid AI service: calls of "text" (Gemini
# chat, grading, reports, history lessons, placement), "transcribe" (the mic),
# "talk" (live voice sessions), and characters of "speech" (read-aloud). Over
# the cap a feature answers 503 until tomorrow. AI_DISABLED switches features
# off at once (comma-separated), e.g. "talk,speech".
AI_DAILY_CAPS = {
    "text": int(os.getenv("AI_CAP_TEXT", "2000")),
    "transcribe": int(os.getenv("AI_CAP_TRANSCRIBE", "500")),
    "talk": int(os.getenv("AI_CAP_TALK", "60")),
    "speech": int(os.getenv("AI_CAP_SPEECH_CHARS", "15000")),
}
AI_DISABLED = {f.strip() for f in os.getenv("AI_DISABLED", "").split(",") if f.strip()}

# Request bodies: JSON/form data held in memory is capped at 1 MB (the longest
# legitimate body is a Talk transcript, ~120 KB), and the whole request at 6 MB
# (an avatar or a minute of audio), refused before it is read.
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024
MAX_REQUEST_BYTES = int(os.getenv("MAX_REQUEST_BYTES", str(6 * 1024 * 1024)))


# ---- Monitoring ----
# Logs go to stdout, where the host keeps them. The "security" logger records
# sign-ins, password and 2FA changes, account deletion and AI caps being hit.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"plain": {"format": "%(levelname)s %(name)s: %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "plain"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {"security": {"handlers": ["console"], "level": "INFO", "propagate": False}},
}

# Error tracking (sentry.io), on when SENTRY_DSN is set. No personal data: no
# cookies, headers with credentials or user details; no performance tracing.
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
if SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=os.getenv("SENTRY_ENVIRONMENT", "production" if not DEBUG else "development"),
        send_default_pii=False,
        traces_sample_rate=0,
    )
