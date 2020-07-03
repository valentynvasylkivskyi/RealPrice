from django.core.mail import send_mail
from django.conf import settings
from myapp.models import Product

product = Product.objects.get(id=19)

def email():
    subject = '-17% Apple iPhone Xr 64Gb Black (MRY42)'
    message = 'Изменена стоимость товара - Apple iPhone Xr 64Gb Black (MRY42). Цена упала на 17%'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    for user in product.users.all():
        recipient_list.append(user.email)
    send_mail( subject, message, email_from, recipient_list )
    return 'Успешно отправлено на email {}'.format(recipient_list)

email()