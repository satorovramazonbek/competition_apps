from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name
class Participant(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)  # 👈 AVTOMATIK KOD
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.code} - {self.first_name} {self.last_name}"
