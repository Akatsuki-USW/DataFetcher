import hashlib
from django.views import View
from django.http import JsonResponse
from .models import Users, Report, Ban, BlackList
from .models import Users
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
class AdminLoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        social_email = data.get('social_email')
        password = data.get('password')

        if not all([social_email, password]):
            return JsonResponse({'message': 'INVALID_DATA'}, status=400)

        try:
            user = Users.objects.get(social_email=social_email)

            if user.role != 'ROLE_ADMIN':
                return JsonResponse({'message': 'NO_PERMISSION'}, status=403)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                payload = {"user_id": user.user_id}
                token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({'AccessToken': token}, status=200)

            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except Users.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

@method_decorator(csrf_exempt, name='dispatch')  #csrf token 비활성화
class AdminMainView(View):
    @authorization
    def get(self, request):
        reported_count = Report.objects.all().count()

        banned_users_count = Ban.objects.filter(is_banned=True).count()

        return JsonResponse({
            'reported_count': reported_count,
            'banned_users_count': banned_users_count
        }, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class ReportDetailView(View):
    @authorization
    def get(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        data = {
            'report_id': report.report_id,
            'created_at': report.created_at,
            'updated_at': report.updated_at,
            'content': report.content,
            'report_target': report.report_target,
            'target_id': report.target_id,
            'ban_id': report.ban.ban_id if report.ban else None,
            'reported_user_id': report.reported_user.user_id if report.reported_user else None,
            'reporter_user_id': report.reporter_user.user_id if report.reporter_user else None
        }
        return JsonResponse(data, status=200)

    def post(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)

        if Ban.objects.filter(banned_user=report.reported_user).exists():
            return JsonResponse({"message": "유저가 이미 밴 상태입니다.."}, status=400)
        if BlackList.objects.filter(
                social_email=hashlib.sha256(report.reported_user.social_email.encode()).hexdigest()).exists():
            return JsonResponse({"message": "유저가 이미 블랙리스트 상태입니다."}, status=400)
        # JSON 데이터를 파싱
        data = json.loads(request.body)
        action = data.get('action')

        # is_checked를 1로
        report.is_checked = '1'
        report.save()

        if action == '무고':
            pass

        elif action == '30일 정지':
            reported_user = report.reported_user
            reported_user.user_status = "BANNED"
            reported_user.save()

            Ban.objects.create(
                ban_started_at=timezone.now(),
                ban_ended_at=timezone.now() + timedelta(days=30),
                content="30일 정지",
                is_banned='1',
                title="30일 정지",
                banned_user=reported_user
            )


        elif action == '블랙리스트':
            hashed_social_email = hashlib.sha256(report.reported_user.social_email.encode()).hexdigest()
            BlackList.objects.create(
                ban_started_at=timezone.now(),
                ban_ended_at=timezone.now() + timedelta(days=365),  # 1년 정지
                social_email=hashed_social_email  # 해시된 값을 저장
            )

        return JsonResponse({"message": "Action applied successfully."}, status=200)