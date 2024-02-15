# delete_superuser.py

from django.contrib.auth import get_user_model

def main():
    User = get_user_model()
    try:
        superuser = User.objects.get(email="mhmdalsyd2015@gmail.com")
        superuser.delete()
        print("Superuser deleted successfully.")
    except User.DoesNotExist:
        print("Superuser with email 'mhmdalsyd2015@gmail.com' does not exist.")

if __name__ == "__main__":
    main()
