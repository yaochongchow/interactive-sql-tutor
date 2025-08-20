from django.db import models

class SQLProblem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    solution = models.TextField()

    def __str__(self):
        return self.title