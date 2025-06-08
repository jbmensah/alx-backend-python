from django.core.management.base import BaseCommand
from chats.models import CustomUser, Conversation, Message

class Command(BaseCommand):
    help = "Seed database with test users, a conversation, and messages"

    def handle(self, *args, **options):
        # Create or get user narkie
        u1, created = CustomUser.objects.get_or_create(
            username='narkie',
            defaults={
                'email': 'narkie@example.com',
                'first_name': 'Narkie',
                'last_name': 'Nartey',
                'phone_number': '0244-123456',
            }
        )
        if created:
            # Hash the password properly
            u1.set_password('password123')
            u1.save()

        # Create or get user ewuradwoa
        u2, created = CustomUser.objects.get_or_create(
            username='ewuradwoa',
            defaults={
                'email': 'ewuradwoa@example.com',
                'first_name': 'Ewuradwoa',
                'last_name': 'Andoh Biney Mensah',
                'phone_number': '0245-123456',
            }
        )
        if created:
            u2.set_password('password123')
            u2.save()

        # Create a conversation
        conv, _ = Conversation.objects.get_or_create(
            name='Demo Chat',
            is_group=False
        )
        conv.participants.set([u1, u2])

        # Create messages
        Message.objects.get_or_create(
            conversation=conv,
            sender=u1,
            message_body='Hello Narkie!',
        )
        Message.objects.get_or_create(
            conversation=conv,
            sender=u2,
            message_body='Hey Ewuradwoa!',
        )

        self.stdout.write(self.style.SUCCESS("✅ Seed data loaded successfully."))
