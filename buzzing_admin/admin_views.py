import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .swagger import (
    admin_login_view_schema,
    admin_main_view_schema,
    unban_user_view_schema,
    report_detail_view_get_schema,
    report_detail_view_post_schema
)
from .models import Users, Report, Ban, BlackList,Spot,Comment
import jwt
import bcrypt
from django_secrets import JWT_SECRET_KEY, ALGORITHM
import json
from django.views.decorators.csrf import csrf_exempt #csrf token 비활성화
from django.utils.decorators import method_decorator  #csrf token 비활성화
from utils import authorization
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta


@method_decorator(csrf_exempt, name='dispatch')  #csrf token 비활성화
class AdminLoginView(APIView):
    @swagger_auto_schema(**admin_login_view_schema())
    def post(self, request):
        data = json.loads(request.body)
        social_email = data.get('social_email')
        password = data.get('password')

        if not all([social_email, password]):
            return Response({'message': 'INVALID_DATA'}, status=400)

        try:
            user = Users.objects.get(social_email=social_email)

            if user.role != 'ROLE_ADMIN':
                return Response({'message': 'NO_PERMISSION'}, status=403)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                payload = {"user_id": user.user_id}
                token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
                return Response({'AccessToken': token}, status=200)

            return Response({'message': 'INVALID_USER'}, status=401)

        except Users.DoesNotExist:
            return Response({'message': 'INVALID_USER'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')  # csrf token 비활성화
class AdminMainView(APIView):
    @swagger_auto_schema(**admin_main_view_schema())
    @authorization
    def get(self, request):
        #커서 페이징
        cursor_id = request.GET.get('cursor_id')
        if cursor_id:
            reported_contents = Report.objects.filter(is_checked=0, report_id__gt=cursor_id).order_by('report_id')[:10]
        else:
            reported_contents = Report.objects.filter(is_checked=0).order_by('report_id')[:10]

        reported_data = []
        for report in reported_contents:
            content_data = {
                'report_id': report.report_id,
                'report_content': report.content,  # 신고 사유
            }
            if report.report_target == 'SPOT':
                spot = Spot.objects.get(pk=report.target_id)
                content_data['title'] = spot.title
                content_data['content'] = spot.content
            elif report.report_target == 'COMMENT':
                comment = Comment.objects.get(pk=report.target_id)
                content_data['content'] = comment.content
            reported_data.append(content_data)

        # 정지된 유저와 블랙리스트 유저 정보 가져오기
        banned_users = Ban.objects.filter(is_banned=True)
        banned_data = []
        for ban in banned_users:
            banned_data.append({
                'ban_id': ban.ban_id,
                'title': ban.title,
                'banned_user_nickname': ban.banned_user.nickname,
                'ban_started_at': ban.ban_started_at,
                'ban_ended_at': ban.ban_ended_at,
                'banned_user_id': ban.banned_user_id
            })

        # 블랙리스트 유저 정보 가져오기, ++++++ 밴 테이블에 블랙리스트를 추가 후 블랙리스트 하는것이기 때문에 밴만 조회하면 될듯
        # blacklisted_users = BlackList.objects.all()
        # blacklist_data = []
        # for user in blacklisted_users:
        #     blacklist_data.append({
        #         'black_list_id': user.black_list_id,
        #         'ban_started_at': user.ban_started_at,
        #         'ban_ended_at': user.ban_ended_at,
        #         'social_email': user.social_email
        #     })

        return Response({
            'reported_contents': reported_data,
            'banned_users': banned_data,
            #'blacklisted_users': blacklist_data
        }, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class UnbanUserView(APIView):
    @swagger_auto_schema(**unban_user_view_schema())
    @authorization
    def post(self, request, user_id):
        try:
            ban_data = Ban.objects.get(banned_user_id=user_id, is_banned=1)

            ban_data.is_banned = None
            ban_data.save()

            user = Users.objects.get(pk=user_id)
            user.user_status = "NORMAL"
            user.save()

            return Response({"message": "유저 정지 해제 완료."}, status=200)

        except Ban.DoesNotExist:
            return Response({"message": "밴 데이터가 없습니다."}, status=400)
        except Users.DoesNotExist:
            return Response({"message": "해당 유저가 존재하지 않습니다."}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ReportDetailView(APIView):
    @swagger_auto_schema(**report_detail_view_get_schema())
    @authorization
    def get(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        data = {
            'report_id': report.report_id,
            'created_at': report.created_at,
            'content': report.content,
            'reported_user_nickname': report.reported_user.nickname if report.reported_user else None,
            'reporter_user_nickname': report.reporter_user.nickname if report.reporter_user else None
        }
        if report.report_target == 'SPOT':
            spot = get_object_or_404(Spot, pk=report.target_id)
            data['title'] = spot.title
            data['content'] = spot.content
            data['spot_content'] = spot.content
        elif report.report_target == 'COMMENT':
            comment = get_object_or_404(Comment, pk=report.target_id)
            data['content'] = comment.content
        return Response(data, status=200)

    @swagger_auto_schema(**report_detail_view_post_schema())
    @authorization
    def post(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)

        if Ban.objects.filter(banned_user=report.reported_user).exists():
            return Response({"message": "유저가 이미 밴 상태입니다.."}, status=400)
        if BlackList.objects.filter(
                social_email=hashlib.sha256(report.reported_user.social_email.encode()).hexdigest()).exists():
            return Response({"message": "유저가 이미 블랙리스트 상태입니다."}, status=400)
        data = json.loads(request.body)
        action = data.get('action')
        ban_reason = data.get('ban_reason')  # 정지 사유
        ban_reason_title = data.get('ban_reason_title')  # 정지 사유 제목

        # is_checked를 1로
        report.is_checked = 1
        report.save()

        if action == '무고':
            pass

        elif action == '30일 정지':
            reported_user = report.reported_user
            reported_user.user_status = "BANNED"
            reported_user.save()
            #신고처리 시 그 게시글 삭제.
            if report.report_target == 'SPOT':
                Spot.objects.filter(pk=report.target_id).delete()
            elif report.report_target == 'COMMENT':
                Comment.objects.filter(pk=report.target_id).delete()

            Ban.objects.create(
                ban_started_at=timezone.now(),
                ban_ended_at=timezone.now() + timedelta(days=30),
                content=ban_reason,  # 정지 사유
                is_banned='1',
                title=ban_reason_title,  # 정지 사유 제목
                banned_user=reported_user
            )

        elif action == '블랙리스트':
            reported_user = report.reported_user
            reported_user.user_status = "BLACKLIST"
            reported_user.save()
            #신고처리시 그 게시글 삭제
            if report.report_target == 'SPOT':
                Spot.objects.filter(pk=report.target_id).delete()
            elif report.report_target == 'COMMENT':
                Comment.objects.filter(pk=report.target_id).delete()

            Ban.objects.create(
                ban_started_at=timezone.now(),
                ban_ended_at=timezone.now() + timedelta(days=365),  # 1년 정지
                content=ban_reason,  # 정지 사유
                is_banned='1',
                title=ban_reason_title,  # 정지 사유 제목
                banned_user=reported_user
            )

            hashed_social_email = hashlib.sha256(report.reported_user.social_email.encode()).hexdigest()
            BlackList.objects.create(
                ban_started_at=timezone.now(),
                ban_ended_at=timezone.now() + timedelta(days=365),  # 1년 정지
                social_email=hashed_social_email
            )

        return Response({"message": "신고 처리 완료."}, status=200)