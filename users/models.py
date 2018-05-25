from django.db import models


class AppQuerySet(models.QuerySet):
    pass


class AppManager(models.Manager):

    queryset_class = AppQuerySet

    def get_query(self):
        return self.queryset_class(self.model)


class AppModel(models.Model):
    objects = AppManager()

    class Meta:
        abstract = True


class DfTGroup(AppModel):
    name = models.CharField(max_length=50, blank=False, default="None")

    def __str__(self):
        return self.name


class Division(AppModel):
    name = models.CharField(max_length=50, blank=False)
    dft_group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Employee(AppModel):
    first_name = models.CharField(max_length=50, default="First Name")
    last_name = models.CharField(max_length=100, default="Last Name")
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return " ".join([self.first_name, self.last_name])
