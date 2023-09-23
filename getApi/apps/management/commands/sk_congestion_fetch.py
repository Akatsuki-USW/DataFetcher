import requests
from django.core.management import BaseCommand
import django_secrets
from getApi.models import Location, Congestion
import datetime

class Command(BaseCommand):
    help = "sk_congestion_fetch"

    def handle(self, *args, **options):
        base_url = "https://apis.openapi.sk.com/puzzle/place/congestion/rltm/pois"
        headers = {
            "accept": "application/json",
            "appkey": django_secrets.SK_API_KEY
        }

        def get_level_mapping(congestion_level):
            if 1 <= congestion_level <= 2:
                return 1
            elif 3 <= congestion_level <= 4:
                return 2
            elif 5 <= congestion_level <= 9:
                return 3

        allowed_api_ids = [387701,6967166,192300]
        locations = Location.objects.filter(api_id__in=allowed_api_ids)

        for location in locations:
            poiId = location.api_id
            if poiId is not None:
                url = f"{base_url}/{poiId}"
                response = requests.get(url, headers=headers)
                sk_congestion_data = response.json()
                print(sk_congestion_data)

                try:
                    if sk_congestion_data['status']['code'] == '00':
                        content = sk_congestion_data['contents']
                        rltm_list = content['rltm']

                        for rltm in rltm_list:
                            congestion_level = rltm['congestionLevel']
                            mapped_level = get_level_mapping(congestion_level)
                            observed_at = rltm['datetime']
                            observed_at = datetime.datetime.strptime(observed_at, '%Y%m%d%H%M%S')

                            congestion = Congestion(
                                location_id=location.pk,
                                observed_at=observed_at,
                                congestion_level=mapped_level
                            )
                            congestion.save()

                            # Update the location's realtime_congestion_level
                            location.realtime_congestion_level = mapped_level
                            location.save(update_fields=['realtime_congestion_level'])

                            print(f"Location {location.name}: CongestionLevel {congestion_level} updated.")
                    else:
                        print(f"Error with SK API: {sk_congestion_data['status']['message']}")
                except KeyError as e:
                    print(f"Unexpected JSON format (KeyError): {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
