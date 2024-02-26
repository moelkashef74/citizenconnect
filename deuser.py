# delete_all_users.py

from django.contrib.auth import get_user_model

def main():
    User = get_user_model()
    # Get the number of users before deletion
    count = User.objects.count()
    # Delete all users
    User.objects.all().delete()
    # Print the result
    print(f"Deleted {count} users successfully.")

if __name__ == "__main__":
    main()
