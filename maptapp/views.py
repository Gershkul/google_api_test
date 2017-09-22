from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.conf import settings
from .models import Address
from .fusiontable import Fusiontable
import json

class HomeView(View):
    """
    displays Home Page, connects Google.maps.api and loads styles, js-libraries, connects
    map.js (the script, that displays and manages the main page content), bootstraps data for map.js
    """
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name, {
            'bootstrap': json.dumps(settings.GOOGLE_API_OPTIONS),
            'api_key': settings.GOOGLE_API_OPTIONS.get('api_key')
        })


class MapApiView(View):
    """
    the server part of map.js functionality
    """
    def get(self, request):
        """
        Selects all addresses from the database
        :param request:
        :return address list:
        """
        return JsonResponse({'results': [x.attributes for x in Address.objects.all()]})

    def post(self, request):
        """
        Adds address to database and fusion table
        :param request:
        :return address list or error mesage:
        """
        try:
            address = Address(latLng=request.POST.dict(), api_key=settings.GOOGLE_API_OPTIONS.get('api_key'))
            if not address.is_valid:
                return JsonResponse({
                    'message': 'This place has no address'
                }, status=404)
            fusiontable = Fusiontable(data=address.attributes, options=settings.GOOGLE_API_OPTIONS)
            if not fusiontable.already_exists:
                fusiontable.save()
                address.save()
                return JsonResponse({  # Everything's ok! Return info for displaying
                    'data': [x.attributes for x in Address.objects.all()]
                })
        except:
            return JsonResponse({
                'message': 'Google API is not available, please contact site administrator'
            }, status=404)
        return JsonResponse({
            'message': 'This address already exists'
        }, status=404)

    def delete(self, request):
        """

        :param request:
        :return:
        """
        Address.objects.all().delete()
        Fusiontable(settings.GOOGLE_API_OPTIONS).delete_all()
        return HttpResponse('ok')

