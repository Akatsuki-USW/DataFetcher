
import json

from getApi.models import Congestion, Location
from django.db.models import Max
from datetime import datetime


class ConvertCongestionData():

    def __init__(self, data):
        self.data = data

    def handle(self):
        # 데이터베이스에 저장할 데이터 리스트
        json_data = json.dumps(self.data)

        # json데이터를 db에 저장
        congestion_data_list = json.loads(json_data)
        print(congestion_data_list)

        # 새로운 데이터를 추가할 때 사용할 id값을 찾.
        max_congestion_id = Congestion.objects.aggregate(Max('congestion_id'))['congestion_id__max'] or 0
        # 데이터베이스에 저장
        date_format = '%Y-%m-%d %H:%M:%S'


        for congestion_data in congestion_data_list:
            congestion_level = congestion_data['congestion_level']
            location_id = congestion_data['location_id']  # Location 인스턴스 대신 location_id 값을 변수에 저장
            location_inst = Location.objects.filter(location_id=location_id).first()  # location_id 값을 가진 첫번째 Location 인스턴스 가져오기
            #observed_at = congestion_data['observed_at']
            observed_at = datetime.strptime(congestion_data['observed_at'], date_format)

            _, created = Congestion.objects.update_or_create(
                congestion_id=max_congestion_id + 1,
                #location_id= location_id,
                location_id=location_inst.pk, # id는 django가 자동으로 하기때문에 pk를 사용해야한다고 함.
                congestion_level = congestion_level,
                #congestion_msg = congestion_msg,
                defaults={'congestion_level': congestion_level,
                          #'congestion_msg': congestion_msg,
                          'observed_at' : observed_at
                          # 크리에이트는 지우면 실행이 될거같기도 하고?
                          }
            )
            print(f"{congestion_level} created: {created}")
            max_congestion_id += 1


