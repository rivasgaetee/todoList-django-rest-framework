import json
from jose import jwt
from urllib.request import urlopen
from django.conf import settings
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User


def get_token_auth_header(request):
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise exceptions.AuthenticationFailed('Authorization header is expected')

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')
    elif len(parts) == 1:
        raise exceptions.AuthenticationFailed('Token not found')
    elif len(parts) > 2:
        raise exceptions.AuthenticationFailed('Authorization header must be Bearer token')

    token = parts[1]
    return token


def jwt_decode_token(token):
    try:
        jsonurl = urlopen(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
    except Exception as e:
        raise exceptions.AuthenticationFailed(f'Unable to fetch JWKS: {str(e)}')

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
            break

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.AUTH0_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token is expired')
        except jwt.JWTClaimsError:
            raise exceptions.AuthenticationFailed('Incorrect claims, please check the audience and issuer')
        except Exception:
            raise exceptions.AuthenticationFailed('Unable to parse authentication token')

    raise exceptions.AuthenticationFailed('Unable to find appropriate key')


class Auth0JSONWebTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = get_token_auth_header(request)
        try:
            payload = jwt_decode_token(token)
            print(payload)
            user, created = User.objects.get_or_create(username=payload['sub'], defaults={
                'email': payload.get('email', ''),
                'first_name': payload.get('name', '')
            })
            return user, token
        except exceptions.AuthenticationFailed as e:
            raise e
        except Exception:
            raise exceptions.AuthenticationFailed('Unable to parse authentication token')
