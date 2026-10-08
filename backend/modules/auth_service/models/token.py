import uuid

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models


class RefreshToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="refresh_tokens")
    jti = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    crated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = "refresh_tokens"
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["jti", "is_active"]),
        ]

    def __str__(self):
        return f"Refresh token for user {self.user.email}"
