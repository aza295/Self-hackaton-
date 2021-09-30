from django.core.mail import send_mail


def send_activation_code(email,activation_code):
    activation_url = f'http://localhost:8000/registration/activate/{activation_code}'
    message = f"""
    Спасибо за регистрацию,
    Пожалуйста, Активируйте ваш аккаунт.
    Ссылка на активацию: {activation_url}
"""
    send_mail(
        'Активируйте ваш аккаунт',
        message,
        'q@gmial.com',
        [email, ],
        fail_silently=False
    )

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
