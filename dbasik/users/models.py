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


class Organisation(AppModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DfTGroup(AppModel):
    name = models.CharField(max_length=50, blank=False, default="None")

    def __str__(self):
        return self.name


class DfTDivision(AppModel):
    name = models.CharField(max_length=50, blank=False)
    dft_group = models.ForeignKey(DfTGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Role(AppModel):
    name = models.CharField(max_length=50)


class Employee(AppModel):
    first_name = models.CharField(max_length=50, default="First Name")
    last_name = models.CharField(max_length=100, default="Last Name")
    organisation = models.ManyToManyField(Organisation)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=12)
    landline = models.CharField(max_length=25)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([self.first_name, self.last_name])
