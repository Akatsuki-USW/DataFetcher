import requests
from django.core.management import BaseCommand
from getApi.models import Location, Congestion
import datetime

class Command(BaseCommand):
    help = "sk_congestion_fetch"

    def handle(self, *args, **options):
        base_url = "https://apis.openapi.sk.com/puzzle/congestion/rltm/pois"
        headers = {
            "accept": "application/json",
            "appkey": "KQvy4uZEmI6dMMXosdQwZ8iUdvg4STIR74FxzDcg"
        }

        def get_level_mapping(congestion_level):
            if 1 <= congestion_level <= 3:
                return 'RELEX'
            elif 4 <= congestion_level <= 6:
                return 'NORMAL'
            elif 7 <= congestion_level <= 9:
                return 'BUZZ'

        #객체 가져오기
        locations = Location.objects.all()

        #Location에서 api_id 값을 사용하여 SK API를 호출
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
                            observed_at = rltm['datetime']
                            observed_at = datetime.datetime.strptime(observed_at, '%Y%m%d%H%M%S')

                            # Congestion 생성하거나 업데이트
                            _, created = Congestion.objects.update_or_create(
                                location_id=location.pk,
                                observed_at=observed_at,
                                defaults={
                                    'congestion_level': get_level_mapping(congestion_level)
                                }
                            )
                            print(f"Location {location.name}: CongestionLevel {congestion_level} updated.")
                    else:
                        print(f"Error with SK API: {sk_congestion_data['status']['message']}")
                except KeyError as e:
                    print(f"Unexpected JSON format (KeyError): {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

