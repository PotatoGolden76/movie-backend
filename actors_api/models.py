from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class ActorModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    age = models.IntegerField(null=False, blank=True)
    birthDate = models.DateTimeField(null=False, blank=False)
    deathDate = models.DateTimeField(null=False, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = "actors"
        ordering = ['-age']

        def __str__(self) -> str:
            return self.title