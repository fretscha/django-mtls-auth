import logging

from django.contrib.auth import authenticate, get_user_model, login
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .settings import AUTOCREATE_USER, ISSUER_DN_HEADER, SUCCESS_HEADER, USER_DN_HEADER
from .utils import get_user_data_extractor_class

User = get_user_model()
logger = logging.getLogger(__name__)


class MTLSAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            logger.debug("User already authenticated, skipping MTLS authentication")
            return None

        user_dn = request.headers.get(USER_DN_HEADER)
        issuer_dn = request.headers.get(ISSUER_DN_HEADER)
        success = request.headers.get(SUCCESS_HEADER)
        userdata_extractor = get_user_data_extractor_class()()

        if user_dn and success == "SUCCESS":
            logger.info(f"Attempting MTLS authentication for user_dn: {user_dn}")
            if self.verify_valid(user_dn, issuer_dn):
                user_data = userdata_extractor.get_userdata(user_dn)
                if AUTOCREATE_USER:
                    user, created = User.objects.get_or_create(username=user_data.get("username"), defaults=user_data)
                    if created:
                        logger.info(f"Created new user: {user.username}")
                        user.set_unusable_password()
                        user.save()
                else:
                    user = authenticate(request, username=user_data["username"])

                if user is not None:
                    login(request, user)
                    logger.info(f"Successfully authenticated user: {user.username}")
                    return None
                else:
                    logger.warning(f"Invalid user for user_dn: {user_dn}")
                    return JsonResponse({"error": "Invalid user"}, status=401)
            else:
                logger.error(f"Invalid MTLS certificate for user_dn: {user_dn}")
                return JsonResponse({"error": "invalid MTLS certificate"}, status=401)
        else:
            logger.debug("MTLS authentication headers not present, falling back to traditional authentication")
            return None

    def verify_valid(self, user_dn, issuer_dn):
        logger.debug(f"Verifying user {user_dn} with issuer {issuer_dn}")
        return True
