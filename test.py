import jwt

message = {
  "jti": "609a5872-4545-44d5-81dc-adb1561923fa",
  "exp": 1586938102,
  "nbf": 0,
  "iat": 1586937802,
  "iss": "http://192.168.0.33:8180/auth/realms/test",
  "aud": "account",
  "sub": "78c5cfa9-3e79-4079-9fe7-5ef3eeb0ce5b",
  "typ": "Bearer",
  "azp": "kong",
  "auth_time": 0,
  "session_state": "908d939f-700e-42de-bdab-3e178694a042",
  "acr": "1",
  "realm_access": {
    "roles": [
      "offline_access",
      "uma_authorization"
    ]
  },
  "resource_access": {
    "account": {
      "roles": [
        "manage-account",
        "manage-account-links",
        "view-profile"
      ]
    }
  },
  "scope": "profile email",
  "email_verified": 1,
  "preferred_username": "demouser",
  "email": "demouser@gmail.com"
}

"""
Encode the message to JWT(JWS).
"""
public_key = "b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs2iY+UNfz035EspzTZUeSai+FbBQC487BLsWC/BA+d5b1UFVs0k1erXnqrFBWjKzgn10r3fMfPlPn8ffK8iEuvBEoJ5vnRaHRqjhIi1DZ+h1o5sC9qhty0p5k+Nu9i0rV/CpY6PkAQw/e7kXBMWhK8zM/TAsA0GQUOaZDm/4WeNUq2roMAX+fAJZfMFiI2/WRvBQKcTY1SB6wJhC9c5QhBgWs83XR9EGP6BxyzvJMroR0kMyb+B7ITWbzpKXuUWbhsxRWm0Mz2nwHo9jsREC03wN0CnD+vocCnKjLv/4Bqy9igwKBT2bpAssR0Y7p3v1QZmSO3D4OxUhhkoWBZBCyQIDAQAB'"

# public_key = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs2iY+UNfz035EspzTZUeSai+FbBQC487BLsWC/BA+d5b1UFVs0k1erXnqrFBWjKzgn10r3fMfPlPn8ffK8iEuvBEoJ5vnRaHRqjhIi1DZ+h1o5sC9qhty0p5k+Nu9i0rV/CpY6PkAQw/e7kXBMWhK8zM/TAsA0GQUOaZDm/4WeNUq2roMAX+fAJZfMFiI2/WRvBQKcTY1SB6wJhC9c5QhBgWs83XR9EGP6BxyzvJMroR0kMyb+B7ITWbzpKXuUWbhsxRWm0Mz2nwHo9jsREC03wN0CnD+vocCnKjLv/4Bqy9igwKBT2bpAssR0Y7p3v1QZmSO3D4OxUhhkoWBZBCyQIDAQAB'
# public_key = 'secret'
# You can also load an octet key in the same manner as the RSA.
# signing_key = jwk_from_dict({'kty': 'oct', 'k': '...'})

compact_jws = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJmRkI1N182S1RmN3RETkp4bWNnb0FfeHUzNzhRTWhtS3ktU2dyclpZWGw4In0.eyJqdGkiOiI2MDlhNTg3Mi00NTQ1LTQ0ZDUtODFkYy1hZGIxNTYxOTIzZmEiLCJleHAiOjE1ODY5MzgxMDIsIm5iZiI6MCwiaWF0IjoxNTg2OTM3ODAyLCJpc3MiOiJodHRwOi8vMTkyLjE2OC4wLjMzOjgxODAvYXV0aC9yZWFsbXMvdGVzdCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI3OGM1Y2ZhOS0zZTc5LTQwNzktOWZlNy01ZWYzZWViMGNlNWIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJrb25nIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiOTA4ZDkzOWYtNzAwZS00MmRlLWJkYWItM2UxNzg2OTRhMDQyIiwiYWNyIjoiMSIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInByZWZlcnJlZF91c2VybmFtZSI6ImRlbW91c2VyIiwiZW1haWwiOiJkZW1vdXNlckBnbWFpbC5jb20ifQ.imH3oybqi4eqJVwNO7Hzfi057Gi3Kjc7kYe7IWhqdq4FSTEVdcg3YRptw-D8-BW1NDdv3Nn-0ZXOmi4BVqwVabIAQasLAxVg8lmqoCGGTVNpQIt8ntmuUeP4bu0K-YpThHaM_w3DxBzS3grI4laNle1nqu-mo9jEyz8d-'
print(compact_jws)
"""
Decode the JWT with verifying the signature.
"""

# Load a public key from PEM file corresponding to the signing private key.
# with open('rsa_public_key.json', 'r') as fh:
#     verifying_key = jwk_from_dict(json.load(fh))

message_received = jwt.decode(compact_jws, public_key, algorithms='RS256')
print(message_received)
"""
Successfuly retrieved the `message` from the `compact_jws`
"""
# assert message == message_received