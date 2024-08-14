from django.contrib.auth import authenticate, get_user_model, login
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from .settings import AUTOCREATE_USER, ISSUER_DN_HEADER, SUCCESS_HEADER, USER_DN_HEADER
from .utils import get_user_data_extractor_class

User = get_user_model()


class MTLSAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip middleware if the user is already authenticated
        if request.user.is_authenticated:
            return None

        # Check for authentication headers
        user_dn = request.headers.get(USER_DN_HEADER)
        issuer_dn = request.headers.get(ISSUER_DN_HEADER)
        success = request.headers.get(SUCCESS_HEADER)
        userdata_extractor = get_user_data_extractor_class()()

        if user_dn and success == "SUCCESS":
            # Authenticate the user based on the headers
            if self.verify_valid(user_dn, issuer_dn):
                user_data = userdata_extractor.get_userdata(user_dn)
                if AUTOCREATE_USER:
                    # Check if the user exists, create if it doesn't
                    user, created = User.objects.get_or_create(username=user_data.get("username"), defaults=user_data)

                    if created:
                        # Optionally set additional fields or defaults
                        user.set_unusable_password()  # If no password is needed
                        user.save()
                else:
                    # Authenticate user
                    user = authenticate(request, username=user_data["username"])
                if user is not None:
                    login(request, user)
                    return None
                else:
                    return JsonResponse({"error": "Invalid user"}, status=401)
            else:
                return JsonResponse({"error": "invalid MTLS certificate"}, status=401)
        else:
            # Fallback to traditional username/password authentication
            return None

    def verify_valid(self, user_dn, issuer_dn):
        print(f"Verifying user {user_dn} with issuer {issuer_dn}")
        return True
