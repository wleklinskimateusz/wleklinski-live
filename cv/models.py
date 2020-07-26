from django.db import models

# Create your models here.


class Technology(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    experience = models.IntegerField()

    def __str__(self):
        return self.name


class TechSet(models.Model):
    tech1 = models.ForeignKey(Technology, on_delete=models.CASCADE, related_name='tech1')
    tech2 = models.ForeignKey(Technology, on_delete=models.CASCADE, related_name='tech2', null=True, blank=True)
    tech3 = models.ForeignKey(Technology, on_delete=models.CASCADE, related_name='tech3', null=True, blank=True)

    def __str__(self):
        output = f"{self.tech1}"
        if self.tech2:
            output += f", {self.tech2}"
        if self.tech3:
            output += f", {self.tech3}"
        return output


class WorkExperience(models.Model):
    start = models.DateField()
    end = models.DateField()
    job = models.CharField(max_length=30)
    workplace = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    technologies = models.ForeignKey(TechSet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.job} at {self.workplace}"

    def day_month(self, start):
        if start:
            output = f"{self.start.strftime('%B')}, {self.start.year}"
        else:
            output = f"{self.end.strftime('%B')}, {self.end.year}"
        return output


class PersonalProjects(models.Model):
    project = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    time = models.DateField(null=True, blank=True)
    technologies = models.ForeignKey(TechSet, on_delete=models.CASCADE)

    def __str__(self):
        return self.project


class Education(models.Model):
    university = models.CharField(max_length=20)
    field = models.CharField(max_length=20)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100)
    degree = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.field} in {self.university}"

    def year_month(self, start):
        if start:
            output = f"{self.start.strftime('%B')}, {self.start.year}"
        else:
            output = f"{self.end.strftime('%B')}, {self.end.year}"
        return output


class Hobby(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Skills(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    experience = models.IntegerField()

    def __str__(self):
        return self.name




