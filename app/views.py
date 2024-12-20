# app/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse
from .models import TelegramToken
import json
from django.views.decorators.csrf import csrf_exempt

def login_with_telegram_view(request):
    # Если пользователь уже авторизован – показываем профиль
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})
    else:
        # Генерируем новый токен
        ttoken = TelegramToken.objects.create()
        bot_username = "your_telegram_bot_username"  # Замените на имя вашего бота
        telegram_link = f"https://t.me/{bot_username}?start={ttoken.token}"
        return render(request, 'login.html', {
            'telegram_link': telegram_link,
            'token': ttoken.token
        })

def check_status_view(request):
    token_str = request.GET.get('token')
    try:
        ttoken = TelegramToken.objects.get(token=token_str)
    except TelegramToken.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Token not found'})

    if ttoken.completed and ttoken.user:
        # Авторизуем пользователя
        login(request, ttoken.user)
        return JsonResponse({'status': 'completed', 'username': ttoken.user.username})
    else:
        return JsonResponse({'status': 'pending'})

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if 'message' in data and 'text' in data['message']:
            text = data['message']['text']
            from_user = data['message']['from']
            telegram_id = from_user['id']
            telegram_username = from_user.get('username', '')

            if text.startswith('/start '):
                token_str = text.split(' ')[1]
                # Проверяем токен
                try:
                    ttoken = TelegramToken.objects.get(token=token_str)
                except TelegramToken.DoesNotExist:
                    return HttpResponse("Token not found", status=200)

                # Если нет user – создаём
                if not ttoken.user:
                    username = f"tg_{telegram_id}"
                    user, created = User.objects.get_or_create(username=username)
                    ttoken.user = user
                
                ttoken.telegram_id = telegram_id
                ttoken.telegram_username = telegram_username
                ttoken.completed = True
                ttoken.save()

        return HttpResponse("OK", status=200)
    else:
        return HttpResponse("Only POST allowed", status=405)
