import os
from django.contrib.auth.models import User
from django.db import IntegrityError

USERNAME = "admin"
EMAIL = "admin@example.com"
# Obtener la contraseña de la variable de entorno, que configuraste en Render
PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'defaultsecurepassword') 

def create_or_update_superuser():
    print("Iniciando verificación/creación de Superusuario...")
    try:
        if not User.objects.filter(username=USERNAME).exists():
            # Crear si no existe
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            print(f"Superusuario '{USERNAME}' creado exitosamente con la contraseña de Render.")
        else:
            # Actualizar la contraseña si ya existe
            user = User.objects.get(username=USERNAME)
            user.set_password(PASSWORD)
            user.save()
            print(f"Superusuario '{USERNAME}' actualizado exitosamente.")

    except IntegrityError:
        # Esto maneja si el usuario ya existe pero el filtro no lo detectó por alguna razón
        print(f"Advertencia: El superusuario '{USERNAME}' ya existe. La contraseña fue actualizada.")
    except Exception as e:
        print(f"Error fatal al crear/actualizar superusuario: {e}")

# Llamar a la función
create_or_update_superuser()