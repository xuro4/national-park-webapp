from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.postgres.fields import ArrayField


# ------------------------------- PARKS (OVERARCHING INFO)----------------------------------
# ------------------------------------------------------------------------------------------
# Model with Attributes for each park
class Park(models.Model):
    name = models.CharField(max_length=100, blank=False)
    states = models.CharField(null=True, max_length=100, blank=False)
    slug = models.SlugField(default=None, blank=False)
    geometry = geomodels.PointField(null=True, blank=True, default=None)
    desc = models.TextField(default=None, blank=False)
    designation = models.CharField(max_length=255, default=None, null=True)

    class Meta:
        # order of drop-down list items
        ordering = ('name',)

# --------------------------- END PARKS (OVERARCHING INFO)----------------------------------


# --------------------------------- NEWS & CURRENT INFO ------------------------------------
# ------------------------------------------------------------------------------------------
# Model with Attributes for each Alert, with a foreignkey tying each alert to a specific park
class Alert(models.Model):
    title = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    desc = models.TextField(null=True, blank=False)
    url = models.CharField(default=None, max_length=200, blank=False)

    class Meta:
        # order of drop-down list items
        ordering = ('park',)


# Refer to above
class Event(models.Model):
    title = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    date_start = models.DateField(null=True, blank=False)
    date_end = models.DateField(null=True, blank=False)
    times = ArrayField(models.CharField(max_length=255), blank=True)
    desc = models.TextField(null=True, blank=False)
    reg_required = models.BooleanField(null=True, blank=False)
    reg_info = models.TextField(null=True, blank=False)

    class Meta:
        # order of drop-down list items
        ordering = ('date_start',)


class Articles(models.Model):
    title = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    url = models.CharField(default=None, max_length=200, blank=False)
    img = models.CharField(blank=False, max_length=200, default=None)
    desc = models.TextField(null=True, blank = False)

    class Meta:
        # order of drop-down list items
        ordering = ('park',)


class NewsReleases(models.Model):
    title = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    url = models.CharField(default=None, max_length=200, blank=False)
    img = models.CharField(blank=False, max_length=200, default=None)
    abstract = models.TextField(null=True, blank=False)
    date = models.DateField(null=True, blank=False)

    class Meta:
        # order of drop-down list items
        ordering = ('date',)

# ----------------------------- END NEWS & CURRENT INFO ------------------------------------


# --------------------------------- EDUCATIONAL CONTENT ------------------------------------
# ------------------------------------------------------------------------------------------
class LessonPlans(models.Model):
    title = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    url = models.CharField(default=None, max_length=200, blank=False)
    duration = models.IntegerField(null=True, blank=False)
    desc = models.TextField(null=True, blank=False)
    subject = models.CharField(max_length=255, blank=False)
    grade_level = models.CharField(max_length=255, blank=False)

    class Meta:
        # order of drop-down list items
        ordering = ('park',)


class People(models.Model):
    title = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    url = models.CharField(default=None, max_length=200, blank=False)
    desc = models.TextField(null=True, blank=False)
    img = models.CharField(blank=False, max_length=200, default=None)

    class Meta:
        # order of drop-down list items
        ordering = ('park',)


class Places(models.Model):
    title = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    url = models.CharField(default=None, max_length=200, blank=False)
    desc = models.TextField(null=True, blank=False)
    img = models.CharField(blank=False, max_length=200, default=None)

    class Meta:
        # order of drop-down list items
        ordering = ('park',)

# ----------------------------- END EDUCATIONAL CONTENT ------------------------------------


# --------------------------------- VISITING INFORMATION -----------------------------------
# ------------------------------------------------------------------------------------------
class VisitorCenters(models.Model):
    name = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    url = models.CharField(default=None, max_length=200, blank=False)
    desc = models.TextField(default=None, blank=False)
    directions = models.TextField(default=None, blank=False)
    direction_url = models.CharField(default=None, max_length=200, blank=False)
    geometry = geomodels.PointField(blank=True, null=True, default=None)

    class Meta:
        # order of drop-down list items
        ordering = ('name',)


class Campgrounds(models.Model):
    name = models.CharField(max_length=255, blank=False)
    park = models.ForeignKey(Park, on_delete=models.CASCADE, default=None)
    reserve_url = models.CharField(default=None, max_length=200, blank=False)
    desc = models.TextField(default=None, blank=False)
    reg_overview = models.TextField(default=None, blank=False)
    weather = models.TextField(default=None, blank=False)
    campsites = models.IntegerField(default=0, blank=True)

    internet_info = models.TextField(default=None, blank=False)
    rv_info = models.TextField(default=None, blank=False)
    ada_info = models.TextField(default=None, blank=False)
    wheelchair_info = models.TextField(default=None, blank=False)
    cell_info = models.TextField(default=None, blank=False)
    additional_info = models.TextField(default=None, blank=False)


    firewood = models.BooleanField(default=None, blank=True)
    ice = models.BooleanField(default=None, blank=True)
    food_storage = models.BooleanField(default=None, blank=True)
    internet = models.BooleanField(default=None, blank=True)
    cellphone = models.BooleanField(default=None, blank=True)

    geometry = geomodels.PointField(null=True, blank=True, default=None)

    class Meta:
        # order of drop-down list items
        ordering = ('name',)

# ----------------------------- END VISITING INFORMATION -----------------------------------
