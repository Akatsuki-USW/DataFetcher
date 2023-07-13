from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
import requests
import xmltodict
from getApi.apps import congestion_convert
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "seoul_locationName_fetch.py"
    def handle(self, *args, **options):
        apikey = '6f6169666c61736838387a74747569'
        pk_values = ['강남 MICE 관광특구', '동대문 관광특구', '명동 관광특구', '이태원 관광특구', '잠실 관광특구', '종로·청계 관광특구',
                     '홍대 관광특구', '광화문·덕수궁', '보신각', '서울 암사동 유적', '창덕궁·종묘', '가산디지털단지역', '강남역', '건대입구역',
                     '고덕역', '고속터미널역', '교대역', '구로디지털단지역', '구로역', '군자역', '남구로역', '대림역', '동대문역', '뚝섬역',
                     '미아사거리역', '발산역', '북한산우이역', '사당역', '삼각지역', '서울대입구역', '선릉역', '성신여대입구역', '수유역',
                     '신논현역·논현역', '신도림역', '신림역', '신촌·이대역', '양재역', '역삼역', '연신내역', '오목교역·목동운동장', '왕십리역',
                     '이태원역', '장지역', '장한평역', '천호역', '총신대입구(이수)역', '충정로역', '합정역', '혜화역', '홍대입구역(2호선)',
                     '회기역', '4·19 카페거리', '가락시장', '가로수길', '광장(전통)시장', '김포공항', '낙산공원·이화마을', '노량진',
                     '덕수궁길·정동길', '방배역 먹자골목', '서촌', '성수카페거리', '수유리 먹자골목', '쌍문동 맛집거리', '압구정로데오거리',
                     '연남동', '영등포 타임스퀘어', '용리단길', '이태원 앤틱가구거리', '인사동·익선동', '창동 신경제 중심지', '청담동 명품거리',
                     '해방촌·경리단길', 'DDP(동대문디자인플라자)', 'DMC(디지털미디어시티)', '강서한강공원', '고척돔', '광나루한강공원', '난지한강공원',
                     '노들섬', '뚝섬한강공원', '망원한강공원', '불광천', '서울광장', '서울대공원', '서울숲공원', '아차산', '양화한강공원', '응봉산',
                     '이촌한강공원', '잠실한강공원', '잠원한강공원', '청계산', '용산역', '북촌한옥마을', '여의도', '외대앞', '청량리 제기동 일대 전통시장',
                     '광화문광장', '국립중앙박물관·용산가족공원', '남산공원', '반포한강공원', '북서울꿈의숲', '어린이대공원', '여의도한강공원', '월드컵공원',
                     '잠실종합운동장','청와대']

        city_data_list = []

        # lvl을 숫자로 매핑
        congestion_mapping = {
            '여유': 'RELAX',
            '보통': 'NOMAL',
            '약간 붐빔': 'BUZZING',
            '붐빔': 'BUZZING'
        }
        date_format = '%Y-%m-%d %H:%M:%S'

        def get_data(city_name):
            url = f'http://openapi.seoul.go.kr:8088/{apikey}/xml/citydata/1/5/{city_name}'
            response = requests.get(url)

            # xml을 딕셔너리로 변환
            congestion_data = xmltodict.parse(response.content)

            # 데이터 추출. 먼저 지역이름, 혼잡도, apiId
            area_data = congestion_data['SeoulRtd.citydata']['CITYDATA']['LIVE_PPLTN_STTS']['LIVE_PPLTN_STTS']
            area_name = congestion_data['SeoulRtd.citydata']['CITYDATA']['AREA_NM']
            api_id = congestion_data['SeoulRtd.citydata']['CITYDATA']['AREA_CD']
            # POI 제거
            api_id = api_id.lstrip('POI')

            observed_at = make_aware(parse_datetime(area_data['PPLTN_TIME']))
            observed_at_str = observed_at.strftime(date_format)



            return {
                'name': area_name,
                'api_id': api_id,
                'updated_at': observed_at_str,
                'created_at': observed_at_str,
                'location_category_id': 2
            }

        with ThreadPoolExecutor(max_workers=5) as executor:
            city_data_list = list(executor.map(get_data, pk_values))

        congestion_converter = congestion_convert.ConvertCongestionData(city_data_list)
        congestion_converter.handle()
