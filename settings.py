ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "qanita-syafika-myportofolio.pws.cs.ui.ac.id",
    "*.pws.cs.ui.ac.id",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

CSRF_TRUSTED_ORIGINS = [
    "https://qanita-syafika-myportofolio.pws.cs.ui.ac.id",
    "https://*.pws.cs.ui.ac.id",
]