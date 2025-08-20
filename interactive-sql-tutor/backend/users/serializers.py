from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    """
    This serializer handles user registration by validating and saving user input.

    Features:
    1. Requires `email`, `name`, `password`, `verify_password`, and `role` fields.
    2. Ensures password and verify_password match.
    3. Prevents duplicate registration using the same email.
    4. Delegates user creation to the custom User model's create_user method.

    Fields:
        - password: Write-only field, with a minimum length of 6 characters.
        - verify_password: Write-only field used to confirm password match.

    Methods:
        - validate: Confirms password and verify_password match.
        - create: Removes verify_password, checks for duplicate email, and creates the user.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    verify_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'verify_password', 'role']
    
    def validate(self, data):
        """
        Ensures the password and verify_password fields match.

        Raises:
            serializers.ValidationError: If passwords do not match.
        """
        if data['password'] != data['verify_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Creates a new user instance after validation.

        Steps:
        1. Remove the verify_password field since it is not part of the model.
        2. Check if the email already exists in the database.
           - If it does, raise a validation error.
        3. Call the custom create_user method from the UserManager to create the user.

        Returns:
            User: The newly created user instance.
        """
        validated_data.pop('verify_password') # No need to store to table
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("Email is already in use.")
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that extends the default TokenObtainPairSerializer.

    Purpose:
    - Adds additional user information to both the JWT payload and the response body.

    Enhancements:
    - Injects 'user_id', 'name', and 'role' into:
        1. The refresh/access token payload (via `get_token`)
        2. The response body returned after login (via `validate`)
    
    This makes it easier for the frontend to access user details immediately after login,
    without needing to decode the JWT manually.

    Example Response:
    {
        "refresh": "<token>",
        "access": "<token>",
        "user_id": 3,
        "name": "Thomas",
        "role": "Student",
        "email": "thomas@example.com",
        "profile_info": "I love SQL and biophysics."
    }
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.user_id
        token['name'] = user.name
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.user_id
        data['name'] = self.user.name
        data['role'] = self.user.role
        data['email'] = self.user.email
        data['profile_info'] = self.user.profile_info
        return data

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information, including optional password change.

    Features:
    - Allows users to update their name, profile_info, and optionally change their password.
    - Supports password confirmation through the `verify_password` field.
    - Validates that both password fields match before allowing update.
    - Automatically hashes the password before saving using `set_password`.
    - Excludes `verify_password` from the actual database update, as it's used only for validation.

    Fields:
        name (str): Updated display name of the user.
        profile_info (str): Additional user profile details.
        password (str, write-only, optional): New password to be set.
        verify_password (str, write-only, optional): Confirmation field that must match the password.

    Example Input:
        {
            "name": "Updated Name",
            "profile_info": "I like SQL.",
            "password": "newpassword123",
            "verify_password": "newpassword123"
        }

    Example Output:
        {
            "name": "Updated Name",
            "profile_info": "I like SQL."
        }

    Notes:
    - If `password` and `verify_password` are omitted, the password remains unchanged.
    - Passwords must match if either field is provided.
    - `verify_password` is only used for validation and will not be stored.
    """
    password = serializers.CharField(write_only=True, required=False)
    verify_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['name', 'profile_info', 'password', 'verify_password']

    def validate(self, data):
        password = data.get('password')
        verify = data.get('verify_password')
        # Ensure that if either password field is provided, both must match
        if password or verify:
            if password != verify:
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data):
        # Remove 'verify_password' from data since it's not stored
        validated_data.pop('verify_password', None)

        # If a password is provided, hash it before saving
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
            
        # Continue with the standard update for other fields
        return super().update(instance, validated_data)