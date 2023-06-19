import json
from django.conf import settings
from getApi.models import Location
from django.utils import timezone

class ConvertCongestionData():

    def __init__(self, data):
        self.data = data

    def handle(self):
        # json으로 변환
        json_data = json.dumps(self.data)

        # json데이터를 db에 저장
        city_data_list = json.loads(json_data)
        #print(city_data_list)
        #중복 데이터는 업데이트함. 없으면 만들고.

        for city_data in city_data_list:
            city_name = city_data['name']
            updated_at = city_data['updated_at']
            # congestion_msg = congestion_data['congestion_msg']
            created_at = timezone.localtime(timezone.now())
            api_id = city_data['api_id']
            location_category_id = city_data['location_category_id']

            _, created = Location.objects.update_or_create(

                name=city_name,
                defaults={'name': city_name,
                          'updated_at': updated_at,
                          'created_at': created_at,
                          'api_id' : api_id,
                          'location_category_id' : location_category_id
                          }
            )
            print(f"{city_name} created: {created}")
