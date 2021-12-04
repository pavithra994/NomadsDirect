from rest_framework import serializers

from app_nomand.models import Experience, HotelInfo, HotelReservationItem, BookingInfo, GuestInfo, HotelImages, \
    LocationCountry, LocationCity


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

class LocationCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCountry
        fields = "__all__"

class LocationCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationCity
        fields = "__all__"


class ExperienceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['expid','exptag']


class FeaturedHotelsSerializer(serializers.ModelSerializer):
    location_city = LocationCitySerializer(read_only=True)
    location_country = LocationCountrySerializer(read_only=True)
    class Meta:
        model = HotelInfo
        fields = ['hotelid','name','description','location_street','location_city','location_country']


class SearchHotelsSerializer(serializers.ModelSerializer):
    location_city = LocationCitySerializer(read_only=True)
    location_country = LocationCountrySerializer(read_only=True)
    experiances_tags = ExperienceTagSerializer(many=True,read_only=True)
    class Meta:
        model = HotelInfo
        fields = ['hotelid','name','description','location_street','location_city','location_country','experiances_tags']


class HotelReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReservationItem
        fields = ['reservationItemId','reservation_item','priceinfo_usd','priceinfo_lkr',]


class HotelImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImages
        fields = ['image',]


class HotelInfoSerializer(serializers.ModelSerializer):
    location_city = LocationCitySerializer(read_only=True)
    location_country = LocationCountrySerializer(read_only=True)
    experiances_tags = ExperienceTagSerializer(many=True,read_only=True)
    hotel_reservation = HotelReservationItemSerializer(many=True,read_only=True)
    # # SlugRelatedField won't work: error FileNotFoundError: [Errno 2] No such file or directory:
    # hotel_image = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image')
    hotel_image = HotelImagesSerializer(many=True, read_only=True)

    def to_representation(self, data):
        data = super(HotelInfoSerializer,self).to_representation(data)
        data['hotel_image'] = [val['image'] for val in data.get("hotel_image")]

        return data

    class Meta:
        model = HotelInfo
        fields = ['hotelid','name','description','location_street','location_city','location_country','experiances_tags','hotel_reservation','hotel_image']


class BookingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingInfo
        fields = '__all__'


class GuestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestInfo
        fields = '__all__'



