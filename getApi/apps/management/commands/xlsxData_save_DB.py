import pandas as pd
from getApi.models import Location, LocationCategory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'xlsxData_dave_DB'

    def handle(self, *args, **options):
        file_path = '/Users/jh_jo/Desktop/location_data/location_data-2.xlsx'

        data = pd.read_excel(file_path, engine='openpyxl')

        for index, row in data.iterrows():
            try:
                location = Location.objects.get(name=row['name']) #이름으로 찾기했는데 id로 하는게 좋을듯합니다.
                location_category = LocationCategory.objects.get(location_category_id=row['location_category_id'])
                #포링키 연결
                if location.location_category_id != location_category.location_category_id:
                    location.location_category_id = location_category
                    location.save()
                else:
                   pass

            except Exception as e:
                print(f"error: {str(e)}")
