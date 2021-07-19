import random

from django.core.management.base import BaseCommand
from django_seed import Seed

from reviews import models as reviews_mosels
from rooms import models as room_models
from users import models as user_models

NAME = "Review"


class Command(BaseCommand):  # 노트 9 참조
    help = f"{NAME} 더미데이터 생성"

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            default=1,
            type=int,
            help=f'{NAME}을/를 number 만큼 생성합니다.',
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reviews_mosels.Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "cleanliness": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "check_in": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
                "user": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
            }
        )
        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(f"{number} {NAME} created!!")
        )
