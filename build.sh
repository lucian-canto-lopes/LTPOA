#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# O tráfego da aplicação usa a URL pooled. Para as migrações, quando o Neon
# disponibilizar a URL direta, ela evita limitações de sessão do PgBouncer.
if [[ -n "${DATABASE_URL_UNPOOLED:-}" ]]; then
  export DATABASE_URL="$DATABASE_URL_UNPOOLED"
fi

python manage.py collectstatic --no-input
python manage.py migrate

# No plano gratuito do Render não há Shell. Se as três variáveis abaixo forem
# cadastradas no ambiente, garante um superusuário no primeiro deploy e atualiza
# sua senha nos deploys seguintes sem exibi-la nos logs.
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" && -n "${DJANGO_SUPERUSER_EMAIL:-}" && -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]]; then
  python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']
email = os.environ['DJANGO_SUPERUSER_EMAIL']
password = os.environ['DJANGO_SUPERUSER_PASSWORD']
user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
user.email = email
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.set_password(password)
user.save()
print('Administrador configurado com sucesso.')
"
fi
