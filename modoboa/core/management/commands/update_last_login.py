"""Management command to update last-login timestamp of a user, which will get called as
postlogin-script from dovecot after imap-/pop3-login, see https://wiki.dovecot.org/PostLoginScripting"""

from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management import BaseCommand, CommandError

from modoboa.core.models import User


class Command(BaseCommand):

    help = "Update login-timestamp of user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            help="username who's login-timestamp should get updated"
        )

    def handle(self, *args, **options):
        username = options['user']
        try:
            user = User.objects.get(username)
        except ObjectDoesNotExist:
            raise CommandError("username {} not found".format(username))
        except MultipleObjectsReturned:
            raise CommandError("username {} found multiple times".format(username))
        except Exception as e:
            raise CommandError("username {} not found: {}".format(username, e))
        update_last_login(sender=None, user=user)
