from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """
    Custom user manager for handling user creation and superuser creation.

    Methods:
    - create_user: Creates and saves a regular user with the given email, name, and password.
    - create_superuser: Creates and saves a superuser with staff and admin permissions.
    """
    def create_user(self, email, name, password=None):
        """
        Creates a regular user.

        Steps:
        1. Check if the email is provided.
           - If not, raise a ValueError with message 'Email is required'.
        2. Normalize the email address.
        3. Create a user instance with the provided email and name.
        4. Hash the password and save the user to the database.

        Parameters:
            email (str): The user's email address.
            name (str): The user's full name.
            password (str, optional): The user's plain text password.

        Returns:
            User: The newly created user instance.
        """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None):
        """
        Creates a superuser with elevated permissions.

        Steps:
        1. Create a regular user using create_user.
        2. Set is_staff and is_superuser flags to True.
        3. Save the user to the database.

        Parameters:
            email (str): The superuser's email address.
            name (str): The superuser's full name.
            password (str, optional): The superuser's plain text password.

        Returns:
            User: The newly created superuser instance.
        """
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using email as the unique identifier instead of username.

    Fields:
        user_id (AutoField): Primary key for the user.
        name (CharField): The user's full name.
        email (EmailField): Unique email address used for authentication.
        password (CharField): Hashed password.
        role (CharField): The role of the user (Student, Instructor, or Admin).
        date_joined (DateTimeField): Timestamp of when the user registered.
        is_staff (BooleanField): Allows access to Django admin site.
        is_active (BooleanField): Indicates whether the user account is active.
        is_superuser (BooleanField): Indicates if the user has all permissions.

    Configuration:
        USERNAME_FIELD: Uses 'email' as the login identifier.
        REQUIRED_FIELDS: 'name' is required when creating a superuser.
        db_table: Uses 'user' as the database table name.
        managed: Set to False to prevent Django from creating or modifying the table.

    Returns:
        str: The user's email when the object is printed.
    """
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_info = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('Student', 'Student'), ('Instructor', 'Instructor'), ('Admin', 'Admin')], default='Student')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        # NOTE:
        # This model is linked to a pre-existing table in the database that was created manually (e.g., via raw SQL).
        # - `managed = False` tells Django not to create, modify, or delete this table during migrations.
        # - `db_table = "user"` explicitly specifies the table name to ensure Django maps the model correctly.
        #
        # IMPORTANT: Always include both settings when working with externally managed tables
        # to avoid migration conflicts, accidental table creation, or schema mismatches.
        db_table = "User"
        managed = False
    
    def __str__(self):
        return self.email
    
    @property
    def id(self):
    # This property is added to provide compatibility with Django and third-party packages (like SimpleJWT)
    # which expect the primary key of the user model to be named 'id' by default.
    # Since our custom user model uses 'user_id' as the primary key, we alias it here as 'id'.
        return self.user_id 