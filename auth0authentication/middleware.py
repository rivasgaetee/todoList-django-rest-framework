import json
from jose import jwt
from urllib.request import urlopen
from django.conf import settings
from django.http import JsonResponse

def get_token_auth_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    if not auth:
        raise ValueError("Authorization header is expected")

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise ValueError("Authorization header must start with Bearer")
    elif len(parts) == 1:
        raise ValueError("Token not found")
    elif len(parts) > 2:
        raise ValueError("Authorization header must be Bearer token")

    token = parts[1]
    return token

def jwt_decode_token(token):
    jsonurl = urlopen(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    return jwt.decode(
        token,
        rsa_key,
        algorithms=["RS256"],
        audience=settings.AUTH0_AUDIENCE,
        issuer=f"https://{settings.AUTH0_DOMAIN}/"
    )

class Auth0Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            token = get_token_auth_header(request)
            print(f"Token: {token}")
            payload = jwt_decode_token(token)
            print(f"Payload: {payload}")
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'token is expired'}, status=401)
        except jwt.JWTClaimsError:
            return JsonResponse({'message': 'incorrect claims, please check the audience and issuer'}, status=401)
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({'message': 'Unable to parse authentication token.'}, status=401)

        request.user = payload
        response = self.get_response(request)
        return response