from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

# class ExperienceTags(models.Model):
#     exptagid = models.AutoField(primary_key=True)
#     exp_tag = models.CharField(max_length=200, blank=True, null=True)
#
#     def __str__(self):
#         return f"{str(self.exptagid)}. {self.exp_tag}"
#
#     class Meta:
#         db_table = 'ExperienceTags'


class Experience(models.Model):
    expid = models.AutoField(primary_key=True)
    exptag = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(blank=True, null=True,upload_to="exp_images")

    def __str__(self):
        return f"{str(self.expid)}"

    class Meta:
        db_table = 'Experience'


class LocationCountry(models.Model):
    countryid = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{str(self.countryid)}. {self.country_name} - {self.country_code}"

    class Meta:
        db_table = 'LocationCountry'


class LocationCity(models.Model):
    cityid = models.AutoField(primary_key=True)
    country = models.ForeignKey(LocationCountry,on_delete=models.PROTECT, null=True)
    city_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{str(self.cityid)}. {self.city_name}"

    class Meta:
        db_table = 'LocationCity'



class HotelInfo(models.Model):
    hotelid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True,blank=True)
    location_street = models.CharField(max_length=200, blank=True, null=True)
    # location_city = models.CharField(max_length=200, blank=True, null=True)
    location_city = models.ForeignKey(LocationCity,on_delete=models.PROTECT, null=True)
    # location_country = models.CharField(max_length=200, blank=True, null=True)
    location_country = models.ForeignKey(LocationCountry,on_delete=models.PROTECT, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=200, blank=True, null=True)
    experiances_tags = models.ManyToManyField(Experience)

    def __str__(self):
        return f"{str(self.hotelid)}. {self.name}"

    def clean(self):
        if self.location_country and self.location_city:
            if self.location_city.country != self.location_country:
                raise ValidationError(_("county and city are mis-matched" ))

    def save(self, *args, **kwargs):
        if self.location_country is None:
            self.location_country = self.location_city.country
        self.full_clean()
        super().save(*args,**kwargs)

    @property
    def location(self):
        return f"{self.location_street}, {self.location_city.city_name}, {self.location_country.country_name}"

    @property
    def experiences_list(self):
        return ", ".join([str(ex.exptag) for ex in self.experiances_tags.all()])


    class Meta:
        db_table = 'HotelInfo'


class HotelReservationItem(models.Model):
    reservationItemId = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelInfo, on_delete=models.PROTECT, null=True, related_name='hotel_reservation')
    reservation_item = models.CharField(max_length=200, blank=True, null=True)
    priceinfo_usd = models.DecimalField(decimal_places=2,max_digits=10, blank=True, null=True)
    priceinfo_lkr = models.DecimalField(decimal_places=2,max_digits=10, blank=True, null=True)

    def __str__(self):
        return f"{str(self.reservationItemId)}. {self.reservation_item} - {self.hotel}"

    class Meta:
        db_table = 'HotelReservationItem'


class HotelAmenities(models.Model):
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelInfo, on_delete=models.PROTECT, null=True, related_name='amenities')
    item_name  = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{str(self.id)}. {self.item_name} - {self.hotel}"

    class Meta:
        db_table = 'HotelAmenities'


class HotelImages(models.Model):
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelInfo, on_delete=models.PROTECT, null=True,related_name='hotel_image')
    image  = models.ImageField(max_length=200, blank=True, null=True,upload_to="hotel_images")

    def __str__(self):
        return f"{str(self.id)}. {self.hotel}"

    class Meta:
        db_table = 'HotelImages'



class GuestInfo(models.Model):
    guestid  = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contactNumber = models.CharField(max_length=200, blank=True, null=True)
    country = models.ForeignKey(LocationCountry,on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{str(self.guestid)}. {self.name} - {self.email}"

    class Meta:
        db_table = 'GuestInfo'


class BookingStatus(models.Model):
    id  = models.AutoField(primary_key=True)
    statusId  = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{str(self.statusId)}. {self.status}"

    class Meta:
        db_table = 'BookingStatus'


class BookingInfo(models.Model):
    bookingid = models.AutoField(primary_key=True)
    guest = models.ForeignKey(GuestInfo, on_delete=models.PROTECT, null=True)
    reservationItem = models.ForeignKey(HotelReservationItem, on_delete=models.PROTECT, null=True)
    checkIn = models.DateTimeField(blank=True, null=True)
    checkOut = models.DateTimeField(blank=True, null=True)
    booking_type  = models.CharField(max_length=200, blank=True, null=True)
    is_paid  = models.BooleanField(blank=True, null=True)
    status  = models.ForeignKey(BookingStatus, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{str(self.bookingid)}. {self.guest}"

    class Meta:
        db_table = 'BookingInfo'





