from django.db import models


class GetInTouch(models.Model):
    full_name = models.CharField(max_length=55)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    user_data = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name
