ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "qanita-syafika-myportofolio.pws.cs.ui.ac.id",
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "http://qanita-syafika-myportofolio.pws.cs.ui.ac.id",
    "https://qanita-syafika-myportofolio.pws.cs.ui.ac.id",
]