from django.db import models
import uuid
from django.core.validators import MinValueValidator

class RoleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    character_name = models.CharField(max_length=255, unique=False, default="Extra")
    pay = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    movie = models.ForeignKey('movies_api.MovieModel', on_delete=models.CASCADE, null=False, blank=False)
    actor = models.ForeignKey('actors_api.ActorModel', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = "roles"

        def __str__(self) -> str:
            return self.movie + self.actor