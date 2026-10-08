from django.core.management import BaseCommand
from django.db import connection

from modules.event.models.event import CategoryEvent, EventTag
from modules.place.models.place import CategoryPlace, PlaceTag
from modules.route.models.route import CategoryRoute


class Command(BaseCommand):
    """Команда заполняет тегами и категориями бд"""
    help = 'Команда заполняющая бд тегами и категориями'


    CategoryPlace.objects.all().delete()
    CategoryEvent.objects.all().delete()
    CategoryRoute.objects.all().delete()
    EventTag.objects.all().delete()
    PlaceTag.objects.all().delete()

    with connection.cursor() as cursor:
        cursor.execute("ALTER SEQUENCE place_categoryplace_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE place_placetag_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE event_categoryevent_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE event_eventtag_id_seq RESTART WITH 1;")
        cursor.execute("ALTER SEQUENCE route_categoryroute_id_seq RESTART WITH 1;")

    
    def _create_tags_categories(self):
        """Метод заполнения дб тегами и категориями"""
        categories_place = [{'value': 'Еда и напитки', 'icon': None},
                        {'value': 'Культура, искусство и история','icon': None},
                        {'value': 'Парки, набережные и природа', 'icon': None},
                        {'value': 'Покупки и развлечения', 'icon': None},
                        {'value': 'Спорт и активный отдых', 'icon': None},
                        {'value': 'Другое', 'icon': None}]
        
        categories_route = [{'value': 'Исторический', 'icon': None},
                        {'value': 'Гастрономический','icon': None},
                        {'value': 'Архитектурный', 'icon': None},
                        {'value': 'Спортивный', 'icon': None},
                        {'value': 'На природе', 'icon': None},
                        {'value': 'Развлекательный', 'icon': None},
                        {'value': 'Другое', 'icon': None}]

        categories_event = [{'value': 'Искусство, сцена и кино','icon': None},
                        {'value': 'Образование и бизнес','icon': None},
                        {'value': 'Еда и гастрономия','icon': None},
                        {'value': 'Спорт и активность','icon': None},
                        {'value': 'Городские и тематические фестивали','icon': None},
                        {'value': 'Другое','icon': None}]
        tags_place = [{'value': 'Молодёжное'},
                        {'value': 'Для встреч и общения'},
                        {'value': 'С игровой зоной'},
                        {'value': 'С развлекательной программой'},
                        {'value': 'Фотозона'},
                        {'value': 'Популярная локация'},
                        {'value': 'Студенческие цены'},
                        {'value': 'С коворкинг-зоной'},
                        {'value': 'С возможностью активного отдыха'},
                        {'value': 'Тематическое пространство'}]
        tags_event = [{'value': 'Молодёжное'},
                        {'value': 'Семейное'},
                        {'value': 'Детское'},
                        {'value': 'Для подростков'},
                        {'value': 'Для старшего поколения'},
                        {'value': 'Бесплатное'},
                        {'value': 'По регистрации'},
                        {'value': 'По приглашению'}]
        
        sync_map = [
            (CategoryPlace, categories_place),
            (CategoryEvent, categories_event),
            (CategoryRoute, categories_route),
            (EventTag, tags_event),
            (PlaceTag, tags_place),
        ]

        for model, data in sync_map:
            for i, item in enumerate(data, start=1):
                model.objects.create(id=i, value=item["value"])

    def handle(self, *args, **options):
        return self._create_tags_categories()
