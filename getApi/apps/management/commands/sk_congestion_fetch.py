import requests
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = "https://apis.openapi.sk.com/puzzle/pois"

        headers = {
            "accept": "application/json",
            "appkey": "KQvy4uZEmI6dMMXosdQwZ8iUdvg4STIR74FxzDcg"
        }

        response = requests.get(url, headers=headers)
        sk_location_name_data = response.json()
        for location in sk_location_name_data['contents']:
            print(location['poiName'])


