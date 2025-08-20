from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer
from .serializers import CustomTokenObtainPairSerializer
from .serializers import UserUpdateSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

@api_view(['POST'])
def register_user(request):
    """
    This endpoint allows a new user to register by providing required fields:
    - email
    - name
    - password
    - verify_password
    - role (optional, defaults to 'Student' if not provided)

    Steps:
    1. Initialize the RegisterSerializer with incoming request data.
    2. Validate the data using the serializer.
       - If invalid (e.g., passwords don't match, email already exists), return HTTP 400 with error messages.
    3. If valid, save the new user to the database.
    4. Return a success message with HTTP status 201 (Created).

    Endpoint: POST /api/auth/registor
    Parameters:
        request (Request): The incoming HTTP POST request containing user registration data.

    Returns:
        Response:
            - 201 CREATED with success message if registration succeeds.
            - 400 BAD REQUEST with validation errors if registration fails.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT access and refresh tokens.

    This view uses the CustomTokenObtainPairSerializer to:
    - Authenticate users using email and password.
    - Return both access and refresh tokens.
    - Include additional user information in the response and token payload, such as:
        - user_id
        - name
        - role

    Endpoint: POST /api/auth/login
    Request Body:
        {
            "email": "user@example.com",
            "password": "your_password"
        }

    Successful Response:
        {
            "refresh": "<token>",
            "access": "<token>",
            "user_id": 3,
            "name": "Thomas",
            "role": "Student",
            "email": "thomas@example.com",
            "profile_info": "I love SQL and biophysics."
        }

    This enhanced response allows frontend applications to retrieve key user info
    without needing to decode the JWT manually.
    """
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    """
    Allows authenticated users to log out by blacklisting their refresh token.

    Steps:
    1. Requires the user to be authenticated (access token in header).
    2. Accepts a refresh token in the POST body.
    3. Attempts to blacklist the given refresh token.
       - If successful, returns HTTP 205 (Reset Content).
       - If the token is invalid or missing, returns HTTP 400.

    Endpoint: POST /api/auth/logout/
    Request data: { "refresh": "<refresh_token>" }
    Response: { "message": "Logout successful." }

    Notes:
    - Requires `rest_framework_simplejwt.token_blacklist` app to be enabled.
    - Only refresh tokens can be blacklisted (not access tokens).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(APIView):
    """
    API endpoint that allows authenticated users to update their profile information.

    Features:
    - Requires the user to be authenticated (`IsAuthenticated`).
    - Supports updating profile fields such as `name`, `profile_info`, and optionally `password`.
    - Validates that `password` and `verify_password` match before allowing password updates.
    - Performs a partial update, meaning users can update one or more fields without submitting all fields.

    Methods:
        PUT /api/auth/update/

    Request Body Example:
        {
            "name": "Updated Name",
            "profile_info": "New profile info",
            "password": "newpassword123",
            "verify_password": "newpassword123"
        }

    Success Response:
        HTTP 200 OK
        {
            "message": "Profile updated successfully."
        }

    Failure Response:
        HTTP 400 Bad Request
        {
            "password": ["Passwords do not match."]
        }

    Notes:
    - The update is performed on the currently logged-in user (`request.user`).
    - Password change is optional; if not provided, the password remains unchanged.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user  # Get the currently authenticated user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)