import requests
from django.core.management import BaseCommand
from getApi.models import Location, LocationCategory
import datetime
import json
import pandas as pd

class Command(BaseCommand):
    help = "sk_locationName_fetch"

    def handle(self, *args, **options):
        url = "https://apis.openapi.sk.com/puzzle/pois"
        #location_data_list = [] json파일을 만들기위한 빈 리스트.
        headers = {
            "accept": "application/json",
            "appkey": "KQvy4uZEmI6dMMXosdQwZ8iUdvg4STIR74FxzDcg"
        }

        response = requests.get(url, headers=headers)

        sk_location_name_data = response.json()
        for location_data in sk_location_name_data['contents']:
            poi_name = location_data['poiName']
            poiId = location_data['poiId']
            print(poi_name)
            print(poiId)

            # sk는 api2로함. 카테고리는 sql에서 수정해야해서 디폴드2

            location_category_id = 2

            updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # LocationCategory 모델에서 해당 location_category_id로 인스턴스를 가져옴
            location_category = LocationCategory.objects.get(
                location_category_id=location_category_id
            )

            _, created = Location.objects.update_or_create(
                name=poi_name,
                defaults={
                    'name': poi_name,
                    'api_id': poiId,
                    'updated_at': updated_at,
                    'created_at': updated_at,
                    'location_category_id': location_category  # 이 부분을 location_category로 수정
                }
            )
            #Json파일 추출하기위함.
            # location_data_list.append({
            #     'name': poi_name,
            #     'api_id': api_id,
            #     'updated_at': updated_at,
            #     'created_at': updated_at,
            #     'location_category_id': location_category.location_category_id
            # })
        # with open('location_data.json', 'w') as json_file:
        #     json.dump(location_data_list, json_file, ensure_ascii=False)



