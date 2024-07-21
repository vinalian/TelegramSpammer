from ..models import Account
from django.shortcuts import render
import requests

__all__ = [
    'start_auth', 'confirm_code'
]


def start_auth(request, account_id):
    account_data = Account.objects.get(id=account_id)
    account_data.is_active = False
    account_data.save()

    data = {
        'account_id': str(account_data.id),
        'phone_number': account_data.phone_number,
        'api_id': account_data.api_id,
        'api_hash': account_data.api_hash,
        'name': account_data.name,
        'session_string': account_data.session_string
    }
    resp = requests.post('http://spammer:7777/authorize_account', json=data)
    if resp.status_code != 200:
        return render(request, 'admin/api/account/start_auth.html', {'text': 'Ошибка при авторизации!'})

    json_resp = resp.json()
    send = 0
    timeout = None
    if json_resp.get('status') == 'code_send':
        text = 'Код отправлен!'
        send = 1
        phone_code_hash = json_resp.get('phone_code_hash')
        timeout = json_resp.get('timeout')
        account_data.phone_code_hash = phone_code_hash
        account_data.save()

    elif json_resp.get('status') == 'error':
        text = json_resp.get('data')

    elif json_resp.get('status') == 'authorized':
        text = 'Аккаунт успешно авторизован!'
        session_string = json_resp.get('session_string')
        account_data.session_string = session_string
        account_data.save()

    else:
        account_data.phone_code_hash = None
        account_data.session_string = None
        account_data.save()
        text = 'Неизвестная ошибка!'

    return render(request, 'admin/api/account/start_auth.html', {
        'text': text,
        'send': send,
        'account_id': str(account_data.id),
        'account_name': account_data.name,
        'timeout': timeout
    })


def confirm_code(request):
    import uuid
    if request.method == "POST":
        activation_code = request.POST.get('activation_code')
        account_id = request.POST.get('account_id')
        account_data = Account.objects.get(id=uuid.UUID(account_id))
        data = {
            'account_id': str(account_data.id),
            'phone_code': activation_code,
            'phone_number': account_data.phone_number,
            'api_id': account_data.api_id,
            'api_hash': account_data.api_hash,
            'phone_code_hash': account_data.phone_code_hash,
            'session_string': account_data.session_string,
            'name': account_data.name,
        }
        resp = requests.post('http://spammer:7777/authorize_account', json=data)
        if resp.status_code != 200:
            return render(request, 'admin/api/account/confirm_code.html',
                          {
                              'text': 'Ошибка при подтверждении кода!',
                              'account_id': account_id
                          })

        json_resp = resp.json()
        if json_resp.get('status') == 'error':
            text = json_resp.get('data')
        elif json_resp.get('status') == 'authorized':
            text = 'Аккаунт успешно авторизован!'
            session_string = json_resp.get('session_string')
            account_data.session_string = session_string
            account_data.is_active = True
            account_data.save()
        else:
            account_data.phone_code_hash = None
            account_data.session_string = None
            account_data.save()
            text = 'Неизвестная ошибка!'

        return render(request, 'admin/api/account/confirm_code.html', {
            'text': text,
            'account_id': account_id
        })
