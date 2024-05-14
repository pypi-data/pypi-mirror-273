import random
import string

from django.conf import settings
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


def generate_random_password():
    # Ensure at least one digit and one punctuation
    characters = [random.choice(string.digits), random.choice(string.punctuation)]

    # Fill the string to reach 16 characters
    while len(characters) < 16:
        characters.append(random.choice(string.ascii_letters + string.digits + string.punctuation))

    # Shuffle the list to avoid predictable placement of digit and punctuation
    random.shuffle(characters)
    return "".join(characters)


class Command(createsuperuser.Command):
    help = "Create a superuser, and allow password to be provided"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--auto",
            dest="auto",
            default=False,
            action="store_true",
            help="Get admin user details from settings",
        )
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Specifies the password for the superuser.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        email = options["email"]
        database = options["database"]

        if password and not username:
            raise CommandError("--username is required if specifying --password")

        users = []
        if options.get("auto"):
            default_password = password
            admins = getattr(settings, "ADMINS", None)
            if not admins:
                raise CommandError("--auto requires one or more ADMINS to be configured in settings.")
            for adminuser in admins:
                username, email, *password = adminuser
                password = password[0] if password else default_password or None
                users.append((username, email, password or generate_random_password()))

        else:
            users.append((username, email, password))

        default_manager = self.UserModel._default_manager.db_manager(database)  # noqa W0212
        for username, email, password in users:
            if default_manager.filter(username=username).exists():
                self.stdout.write(f"User {username} exists, skipping")
                continue
            options |= {
                "username": username,
                "email": email,
                "password": password,
                "interactive": False,
            }
            super().handle(*args, **options)
            if password:
                user = default_manager.get(username=username)
                user.set_password(password)
                user.save()
