from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jose import jwt
from urllib.request import urlopen
from django.conf import settings
import json


class Auth0JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self.get_token_auth_header(request)
        if token is None:
            return None

        try:
            payload = self.decode_jwt(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('token is expired')
        except jwt.JWTClaimsError:
            raise AuthenticationFailed('incorrect claims, please check the audience and issuer')
        except Exception:
            raise AuthenticationFailed('Unable to parse authentication token')

        return (payload, token)

    def get_token_auth_header(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        if not auth:
            raise AuthenticationFailed('Authorization header is expected')

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must start with Bearer')
        elif len(parts) == 1:
            raise AuthenticationFailed('Token not found')
        elif len(parts) > 2:
            raise AuthenticationFailed('Authorization header must be Bearer token')

        token = parts[1]
        return token

    def decode_jwt(self, token):
        jsonurl = urlopen("https://{}/.well-known/jwks.json".format(settings.AUTH0_DOMAIN))
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        return jwt.decode(
            token,
            rsa_key,
            algorithms=['RS256'],
            audience=settings.AUTH0_AUDIENCE,
            issuer="https://{}/".format(settings.AUTH0_DOMAIN)
        )
