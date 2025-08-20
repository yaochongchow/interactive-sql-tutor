from django.db import models
from users.models import User

# Create your models here.
class Topic(models.Model):
    """
    Represents a topic or category to which SQL problems can be assigned.

    Fields:
        topic_id (AutoField): The primary key, automatically incremented.
        name (CharField): The unique name of the topic (e.g., "JOIN", "GROUP BY").
        description (TextField): A description or explanation of the topic.

    Meta:
        db_table: Specifies the underlying database table name as "Topic".
        managed: Set to False, indicating that Django will not manage the creation or migration of this table.
                 This assumes the table is created manually via raw SQL or externally.

    Example:
        Topic(topic_id=1, name="Aggregation", description="Problems related to GROUP BY and aggregate functions")
    """
    topic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "Topic"
        managed = False  # Set to True if you want Django to manage the table creation

    def __str__(self):
        return self.name


class SQLProblem(models.Model):
    """
    Represents a SQL problem in the platform, including its content, difficulty, and topic.

    Fields:
        problem_id (AutoField): The primary key, auto-incremented.
        title (CharField): The title of the problem (e.g., "Find Top Sales").
        description (TextField): A detailed problem description with input/output expectations.
        difficulty_level (CharField): The difficulty of the problem, with four allowed values: 
            'Easy', 'Medium', 'Hard', 'Expert'.
        last_modified (DateTimeField): Automatically updated timestamp when the problem is modified.
        topic (ForeignKey): A foreign key linking to the Topic model, indicating the category this problem belongs to.

    Meta:
        db_table: Explicitly maps the model to the "SQLProblem" table in the database.
        managed: Set to False, meaning Django will not manage (create/migrate) this table.
                Use this if the table is created manually via SQL DDL scripts.

    Example:
        SQLProblem(
            problem_id=1,
            title="Find Top Seller",
            description="Write a query to find the employee with the highest sales...",
            difficulty_level="Medium",
            topic=some_topic_instance
        )
    """
    problem_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=10,
        choices=[
            ('Easy', 'Easy'),
            ('Medium', 'Medium'),
            ('Hard', 'Hard'),
            ('Expert', 'Expert')
        ]
    )
    last_modified = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    class Meta:
        db_table = "SQLProblem"
        managed = False  

    def __str__(self):
        return self.title

class Hint(models.Model):
    """
    Represents a hint associated with a specific SQL problem.

    Each hint provides an optional clue or guidance to help users solve the problem.
    Multiple hints can be associated with the same problem, ordered by `hint_order`.

    Fields:
        hint_id (AutoField): Primary key, auto-incremented unique ID for the hint.
        problem (ForeignKey): A reference to the related SQLProblem.
                              Deleting the problem will also delete its hints.
        hint_text (TextField): The actual hint content shown to the user.
        hint_order (IntegerField): The order in which the hint should be displayed (e.g., 1, 2, 3...).

    Meta:
        db_table: Maps the model to the "Hint" table in the database.
        managed: Set to False to indicate that the table is manually created via SQL DDL.

    Example:
        Hint(
            hint_id=1,
            problem=some_problem_instance,
            hint_text="Start by grouping the data by department.",
            hint_order=1
        )
    """
    hint_id = models.AutoField(primary_key=True)
    problem = models.ForeignKey(SQLProblem, on_delete=models.CASCADE)
    hint_text = models.TextField()
    hint_order = models.IntegerField(default=1)

    class Meta:
        db_table = "Hint"
        managed = False

class Attempt(models.Model):
    """
    Represents a user's attempt at solving a specific SQL problem.

    This model tracks submission details such as score, time taken, status, and hint usage.

    Fields:
        attempt_id (AutoField): Primary key, unique ID for each attempt.
        user (ForeignKey): Reference to the User who made the attempt.
        problem (ForeignKey): Reference to the SQLProblem being attempted.
        submission_date (DateTimeField): Timestamp when the attempt was submitted (auto-set).
        score (DecimalField): Score earned in the attempt (e.g., 100.00), with 2 decimal places.
        time_taken (IntegerField): Optional. Time taken to submit in seconds.
        status (CharField): Status of the attempt. Options include:
            - 'Completed': User submitted and passed the problem.
            - 'In Progress': User is still working on it.
            - 'Failed': User submitted but failed.
            - 'Abandoned': User started but didn’t finish or gave up.
        hints_used (IntegerField): The number of hints used during the attempt.

    Meta:
        db_table: Maps the model to the "Attempt" table in the database.
        managed: False to indicate Django won't create or manage this table.
        indexes: Adds a compound index on (user, problem) to optimize lookup queries.

    Example:
        Attempt(
            attempt_id=42,
            user=some_user,
            problem=some_problem,
            score=80.5,
            status='Completed',
            time_taken=120,
            hints_used=1
        )
    """
    attempt_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)
    problem = models.ForeignKey(SQLProblem, db_column='problem_id', on_delete=models.CASCADE, related_name='attempts')
    submission_date = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    time_taken = models.IntegerField(null=True, blank=True, help_text="Time taken in seconds")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Completed', 'Completed'),
            ('In Progress', 'In Progress'),
            ('Failed', 'Failed'),
            ('Abandoned', 'Abandoned'),
        ]
    )
    hints_used = models.IntegerField(default=0)

    class Meta:
        db_table = 'Attempt'
        managed = False
        indexes = [
            models.Index(fields=['user', 'problem'], name='idx_user_problem')
        ]

    def __str__(self):
        return f"Attempt {self.attempt_id} - User {self.user_id} - Problem {self.problem_id}"