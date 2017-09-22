from django.db.models import *
import googlemaps

class Address(Model):
    lat = DecimalField(max_digits=20, decimal_places=16, blank=False, null=False)
    lng = DecimalField(max_digits=20, decimal_places=16)
    address = CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'addresses'

    def __init__(self, *args, **kwargs):
        lat_lng = kwargs.get('latLng')
        if lat_lng:
            lat = lat_lng.get('lat')
            lng = lat_lng.get('lng')
            kwargs.update({
                'address': self.__get_address(lat, lng, kwargs.get('api_key')),
                'lat': lat,
                'lng': lng
            })
            del kwargs['latLng']
            del kwargs['api_key']
        super(Address, self).__init__(*args, **kwargs)

    @staticmethod
    def __get_address(lat, lng, api_key):
        """
        defines address by provided coordinates via google maps reverse geocode service.
        :param lat:
        :param lng:
        :param api_key:
        :return string or None:
        """
        gmaps = googlemaps.Client(key=api_key)
        result = gmaps.reverse_geocode((lat, lng))
        return result[0].get('formatted_address') if len(result) else None

    @property
    def attributes(self):
        """
        is used for suitable displaying of this data in visual tables
        :return dict:
        """
        return {
            'id': self.id,
            'lat': self.lat,
            'lng': self.lng,
            'address': self.address
        }

    @property
    def is_valid(self):
        """
        :return bool True if Address.address is not empty:
        """
        return bool(self.address)
