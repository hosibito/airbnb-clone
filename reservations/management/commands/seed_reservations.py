import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django_seed import Seed

from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

NAME = "Reservation"


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
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                # 왜인지 장고에서 랜덤초이스가 안된다. 일일이 지정해줘야함
                "check_in": lambda x: datetime.now(),
                "check_out":
                    lambda x: datetime.now() + timedelta(days=random.randint(3, 25)),
                "guest": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
            }
        )
        seeder.execute()

        self.stdout.write(
            self.style.SUCCESS(f"{number} {NAME} created!!")
        )
