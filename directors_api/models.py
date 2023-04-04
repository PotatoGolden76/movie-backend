from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class DirectorModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    age = models.IntegerField(null=False, blank=True,
                              validators=[MinValueValidator(15)])
    birthDate = models.DateTimeField(null=False, blank=False)
    deathDate = models.DateTimeField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = "directors"
        ordering = ['-age']

        def __str__(self) -> str:
            return self.title