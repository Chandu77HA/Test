from django.contrib.messages import constants as messages
import os
from pathlib import Path

from .settings import *
from .settings import BASE_DIR

import os
from pathlib import Path
from llama_index.core import Settings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.llms.together import TogetherLLM
from langchain.embeddings import HuggingFaceEmbeddings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_DIR = os.path.join(BASE_DIR, 'static')


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "doc1"
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project_doc_summary.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project_doc_summary.wsgi.application"

connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
parameters = {pair.split('=')[0]: pair.split(
    '=')[1] for pair in connection_string.split(' ')}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parameters['dbname'],
        "USER": parameters['user'],
        "PASSWORD": parameters['password'],
        "HOST": parameters['host'],
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

STATICFILES_DIRS = [
    BASE_DIR / "static",
    STATIC_DIR,
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# LLM model settings
LLM_MODEL = "togethercomputer/llama-2-70b-chat"
LLM_API_KEY = "96557b956acf6073510ee7e4abadc1c7863626e75278a0eaf9a747875af30604"

# Sentence embedding model
SENTENCE_EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"

# Chunk size for sentence splitter
SPLITTER_CHUNK_SIZE = 1000

# Context window size
CONTEXT_WINDOW_SIZE = 4000
# Initialize the embedding model
embed_model = LangchainEmbedding(
    HuggingFaceEmbeddings(model_name=SENTENCE_EMBEDDING_MODEL))
Settings.embed_model = embed_model

# Initialize the LLM model
llm = TogetherLLM(model=LLM_MODEL, api_key=LLM_API_KEY)
Settings.llm = llm

# Set context window size
Settings.context_window = CONTEXT_WINDOW_SIZE


# It will create a media folder in project directory where media files are stored
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
