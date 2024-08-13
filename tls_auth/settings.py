from django.conf import settings

USER_DATA_EXTRACTOR_CLASS = getattr(
    settings,
    "TLS_AUTH_USER_DATA_EXTRACTOR_CLASS",
    "tls_auth.utils.DefaultUserDataExtractor",
)

# Create user if not exists
AUTOCREATE_USER = getattr(settings, "TLS_AUTH_AUTOCREATE_USER", False)

# Header containing User identifing DN
USER_DN_HEADER = getattr(settings, "TLS_AUTH_REVERSE_PROXY_USER_DN_HEADER", "X-SSL-USER-DN")
# Header containing Issuer DN
ISSUER_DN_HEADER = getattr(settings, "TLS_AUTH_REVERSE_PROXY_ISSUER_DN_HEADER", "X-SSL-ISSUER-DN")
# Forwarded verification result
SUCCESS_HEADER = getattr(settings, "TLS_AUTH_REVERSE_PROXY_SUCCESS_HEADER", "X-SSL-AUTHENTICATED")
