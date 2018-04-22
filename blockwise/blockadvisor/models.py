from django.db import models

# Create your models here.
from django.urls import reverse
import uuid

# Create your models here.

class Crime(models.Model):

    neighborhood_cluster = models.CharField(null=True, blank=True, max_length=20, help_text="Enter a neighborhood cluster",default="000")
    census_tract = models.CharField(null=True, blank=True, max_length=20, help_text="Enter a census tract",default="000")
    offense_group = models.CharField(null=True, blank=True, max_length=26, help_text="Enter an offense group")
    longitude = models.CharField(null=True, blank=True, max_length=120, help_text="Enter a longitude",default="000")
    end_date = models.CharField(null=True, blank=True, max_length=22, help_text="Enter an end date",default="000")
    offense_text = models.CharField(null=True, blank=True, max_length=100, help_text="Enter offense text")
    shift = models.CharField(null=True, blank=True, max_length=8, help_text="Enter a shift",default="000")
    yblock = models.CharField(null=True, blank=True, max_length=20, help_text="Enter a yblock",default="000")
    district = models.CharField(null=True, blank=True, max_length=10, help_text="Enter a district",default="000")
    ward = models.CharField(null=True, blank=True, max_length=5, help_text="Enter a ward",default="000")
    year = models.CharField(null=True, blank=True, max_length=20, help_text="Enter a year",default="000")
    offense_key = models.CharField(null=True, blank=True, max_length=100, help_text="Enter an offense key")
    bid = models.CharField(null=True, blank=True, max_length=50, help_text="Enter a BID",default="000")
    sector = models.CharField(null=True, blank=True, max_length=15, help_text="Enter a sector",default="000")
    psa = models.CharField(null=True, blank=True, max_length=3, help_text="Enter a psa",default="000")
    ucrrank = models.CharField(null=True, blank=True, max_length=2, help_text="Enter a ucr rank",default="000")
    block_group = models.CharField(null=True, blank=True, max_length=20, help_text="Enter a block group",default="000")
    voting_precinct = models.CharField(null=True, blank=True, max_length=20, help_text="Enter a voting precinct",default="000")
    xblock = models.CharField(null=True, blank=True, max_length=20, help_text="Enter an xblock",default="000")
    block = models.CharField(null=True, blank=True, max_length=120, help_text="Enter a block",default="000")
    start_date = models.CharField(null=True, blank=True, max_length=22, help_text="Enter a start date",default="000")
    cnn = models.CharField(null=True, blank=True, max_length=10, help_text="Enter a cnn",default="000")
    offense = models.CharField(null=True, blank=True, max_length=100, help_text="Enter an offense")
    anc = models.CharField(null=True, blank=True, max_length=5, help_text="Enter an anc",default="000")
    report_date = models.CharField(null=True, blank=True, max_length=22, help_text="Enter a report date",default="000")
    method = models.CharField(null=True, blank=True, max_length=6, help_text="Enter a method",default="000")
    location = models.CharField(null=True, blank=True, max_length=120, help_text="Enter a location",default="000")
    latitude = models.CharField(null=True, blank=True, max_length=120, help_text="Enter a latitude",default="000")

    
    def __str__(self):
        return self.offense

class Location(models.Model):
    business_name = models.CharField(max_length=200)
    street_name = models.CharField(max_length=300, help_text="Enter a street name",default="Add street name")
    street_number = models.IntegerField(default=0)
    address = models.CharField(max_length=300, help_text="Enter an address",default="Add an address")
    accept_pickup = models.CharField(max_length=50, null=True)
    categories = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=100, help_text="Enter a city", null=True)
    location_id = models.IntegerField(default=0)
    price_range = models.CharField(max_length=50, null=True)
    rank = models.IntegerField(default=0)
    reservation_available = models.CharField(max_length=50, null=True)
    review_count = models.IntegerField(default=0)
    state = models.CharField(max_length=50, help_text="Enter a state", null=True)
    url = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=20, help_text="Enter a zip code",null = True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse('location-detail', args=[str(self.id)])

class LocationInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True) 
    
    def __str__(self):
        return '{0} ({1})'.format(self.id,self.location.business_name)

