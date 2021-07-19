import random

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from rooms import models as room_models
from users import models as user_models

NAME = "Rooms"


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
        all_users = user_models.User.objects.all()  # All()로 가져오면 안된다.(ex:유저10000명...)
        all_roomtypes = room_models.RoomType.objects.all()
        seeder.add_entity(room_models.Room, number, {
            # "name": lambda x: seeder.faker.address(),  # 너무긴 이름이 와서 정제된 가짜 데이터를 넣음
            "name": lambda x: seeder.faker.sentence(),
            "host": lambda x: random.choice(all_users),  # foreignKey 는 자동으로 못넣어준다.
            "room_type": lambda x: random.choice(all_roomtypes),
            "price": lambda x: random.randint(20, 300),  # 음수나 너무큰 범위의 숫자 제한
            "gueste": lambda x: random.randint(1, 10),
            "beds": lambda x: random.randint(1, 5),
            "bedrooms": lambda x: random.randint(1, 5),
            "baths": lambda x: random.randint(1, 5),
        })
        created_room = seeder.execute()  # seeder.execute() 된곳에 포토를 추가하기위해 받아옴.
        # print(created_room.values())
        # dict_values([[15, 16, 17, 18, 19, 20]]) pk값을 리턴한다. 결과값이지저분하다.
        # from django.contrib.admin.utils import flatten
        created_room_pk_clean = flatten(list(created_room.values()))  # 지저분하지 않게 해준다.
        # print(created_room_pk_clean)  # [15, 16, 17, 18, 19, 20] 만들어진 룸 아이디

        all_amenities = room_models.Amenity.objects.all()
        all_facilities = room_models.Facility.objects.all()
        all_house_rules = room_models.HouseRule.objects.all()

        for pk in created_room_pk_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(1, random.randint(5, 14)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 32)}.webp",
                )

            for ame in all_amenities:  # manytomany가 너무 많으면... 문제다른방식 사용할것
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(ame)
            for faci in all_facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(faci)
            for hr in all_house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(hr)

        self.stdout.write(
            self.style.SUCCESS(f"{number} {NAME} created!!")
        )
