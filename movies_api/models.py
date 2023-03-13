from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class MovieModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    releaseDate = models.DateTimeField(null=False, blank=False)
    language = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(default=1,
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    director = models.ForeignKey('directors_api.DirectorModel', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "movies"
        ordering = ['-releaseDate']

        def __str__(self) -> str:
            return self.title