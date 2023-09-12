from drf_yasg.utils import swagger_auto_schema
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg import openapi

class BearerTokenAutoSchema(SwaggerAutoSchema):
    def get_security_definitions(self, auto_schema_context):
        security_definitions = super(BearerTokenAutoSchema, self).get_security_definitions(auto_schema_context)
        security_definitions['Bearer'] = openapi.SecurityScheme(
            type=openapi.TYPE_API_KEY,
            in_=openapi.IN_HEADER,
            name='Authorization',
            description="JWT 토큰 키를 입력해주세요!"
        )
        return security_definitions

def admin_login_view_schema():
    return {
        'request_body': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'social_email': openapi.Schema(type=openapi.TYPE_STRING, description='Admin email', example="admin@example.com"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Admin password', example="passwd1234"),
            },
        ),
        'responses': {
            200: openapi.Response(description='Successful Login', schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={'AccessToken': openapi.Schema(type=openapi.TYPE_STRING, example="sampleAccessToken12345")})),
            400: 'INVALID_DATA',
            403: 'NO_PERMISSION',
            401: 'INVALID_USER'
        },
        'operation_description': "Admin login view \n 관리자 아이디로 접속시, users.USER_ROLE이 ADMIN일시 토큰발급"
    }


def admin_main_view_schema():
    return {
        'responses': {
            200: openapi.Response(description='Get reported contents and banned users'),
        },
        'operation_description': "관리자 메인 페이지"
    }

def unban_user_view_schema():
    return {
        'responses': {
            200: "유저 정지 해제 완료.",
            400: "밴 데이터가 없습니다."
        },
        'operation_description': "유저 정지 해제"
    }

def report_detail_view_get_schema():
    return {
        'responses': {
            200: openapi.Response(description='Get report detail'),
        },
        'operation_description': "리폿 상세뷰 가져오기"
    }

def report_detail_view_post_schema():
    return {
        'request_body': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(type=openapi.TYPE_STRING, description='Action to take (무고, 30일 정지, 블랙리스트)'),
                'ban_reason': openapi.Schema(type=openapi.TYPE_STRING, description='밴 사유'),
                'ban_reason_title': openapi.Schema(type=openapi.TYPE_STRING, description='밴 사유 제목'),
            },
            required=['action', 'ban_reason', 'ban_reason_title'],
            example={
                'action': '30일 정지',
                'ban_reason': '비매너 행동으로 다수의 신고가 접수됨',
                'ban_reason_title': '비매너 행동'
            }
        ),
        'responses': {
            200: "신고 처리 완료.",
            400: "유저가 이미 밴 상태입니다..",
        },
        'operation_description': "리폿 처리"
    }

