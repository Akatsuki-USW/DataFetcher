from concurrent.futures import ThreadPoolExecutor

from django.core.management.base import BaseCommand
import requests
import xmltodict
from getApi.models import Location
from getApi.apps import congestion_convert, realtime_convert
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        apikey = '6f6169666c61736838387a74747569'
        pk_values = ['강남 MICE 관광특구', '동대문 관광특구', '명동 관광특구', '이태원 관광특구', '잠실 관광특구', '종로·청계 관광특구', '홍대 관광특구', '경복궁·서촌마을',
                     '광화문·덕수궁', '창덕궁·종묘', '가산디지털단지역', '강남역', '건대입구역', '고속터미널역', '교대역', '구로디지털단지역', '서울역', '선릉역', '신도림역',
                     '신림역', '신촌·이대역', '역삼역', '연신내역', '용산역', '왕십리역', 'DMC(디지털미디어시티)', '창동 신경제 중심지', '노량진', '낙산공원·이화마을',
                     '북촌한옥마을', '가로수길', '성수카페거리', '수유리 먹자골목', '쌍문동 맛집거리', '압구정로데오거리', '여의도', '영등포 타임스퀘어', '인사동·익선동',
                     '국립중앙박물관·용산가족공원', '남산공원', '뚝섬한강공원', '망원한강공원', '반포한강공원', '북서울꿈의숲', '서울대공원', '서울숲공원', '월드컵공원',
                     '이촌한강공원', '잠실종합운동장', '잠실한강공원']
        city_data_list = []
        realtime_congestions =  []

        # lvl을 숫자로 매핑
        congestion_mapping = {
            '여유': 'RELAX',
            '보통': 'NOMAL',
            '약간 붐빔': 'BUZZ',
            '붐빔': 'VERY_BUZZ'
        }
        date_format = '%Y-%m-%d %H:%M:%S'

        def get_data(city_name):
            url = f'http://openapi.seoul.go.kr:8088/{apikey}/xml/citydata/1/5/{city_name}'
            response = requests.get(url)

            # xml을 딕셔너리로 변환
            congestion_data = xmltodict.parse(response.content)

            # 데이터 추출 . 먼저 지역이름, 혼잡도, 혼잡도 메세지만 가져옴
            area_data = congestion_data['SeoulRtd.citydata']['CITYDATA']['LIVE_PPLTN_STTS']['LIVE_PPLTN_STTS']
            area_name = congestion_data['SeoulRtd.citydata']['CITYDATA']['AREA_NM']
            congestion_level = area_data['AREA_CONGEST_LVL']

            observed_at = parse_datetime(area_data['PPLTN_TIME'])
            observed_at_str = observed_at.strftime(date_format)

            # location_id 값 찾기
            location = Location.objects.get(name=area_name)
            location_id = location.location_id

            # 혼잡도를 숫자로 매핑하기.
            if congestion_level in congestion_mapping:
                congestion_level_mapped = congestion_mapping[congestion_level]
            else:
                congestion_level_mapped = None

            return {
                'location_id': location_id,  # location_id 추가
                'congestion_level': congestion_level_mapped,
                'observed_at': observed_at_str,
            }

        with ThreadPoolExecutor(max_workers=5) as executor:
            realtime_congestions = list(executor.map(get_data, pk_values))

        print(realtime_congestions)

        realtime_converter = realtime_convert.ConvertCongestionData(realtime_congestions)
        realtime_converter.handle()
