import json
from getApi.models import Location, LocationCategory
from django.utils import timezone

class ConvertCongestionData():

    def __init__(self, data):
        self.data = data

    def handle(self):
        # json으로 변환
        json_data = json.dumps(self.data)

        # json데이터를 db에 저장
        city_data_list = json.loads(json_data)
        #중복 데이터는 업데이트함. 없으면 만들고.
        location_category = LocationCategory.objects.get(location_category_id=2)

        for city_data in city_data_list:
            city_name = city_data['name']
            updated_at = city_data['updated_at']
            created_at = timezone.now()
            api_id = city_data['api_id']


            defaults = {
                'name': city_name,
                'updated_at': updated_at,
                'api_id': api_id,
                'location_category_id': location_category
            }

            _, created = Location.objects.update_or_create(
                name=city_name, location_category_id=location_category, defaults=defaults)

