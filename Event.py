"""
Описывает некоторое "событие" - промежуток времени с присвоенными характеристиками
У события должно быть описание, название и список участников
Событие может быть единожды созданным
Или периодическим (каждый день/месяц/год/неделю)

Каждый пользователь ивента имеет свою "роль"
организатор умеет изменять названия, список участников, описание, а так же может удалить событие
участник может покинуть событие

запрос на хранение в json
Уметь создавать из json и записывать в него

Иметь покрытие тестами
Комментарии на нетривиальных методах и в целом документация
"""
import datetime
import datetime as dt
import json


class Event:
    _id_list = []
    __id = 0
    __item = None
    _events_db = []
    file_events = "events_data.csv"
    fieldnames_event = ['_id', 'title', 'periodic', 'organizer', 'start_time', 'end_time', 'duration', 'descr',
                        'members']
    _periodic_dict = {"1": "Ежегодно",
                      "2": "Ежемесячно",
                      "3": "Еженедельно",
                      "4": "Ежедневно",
                      "5": "Разовое"}

    def __init__(self):
        self._title = ''
        self._description = ''
        self._periodic = {}
        self._members = []
        self._organizer = ''
        self.__class__.__id += 1
        self.__class__._id_list.append(self.__class__.__id)
        self.__id = self.__class__.__id
        _y, _m, _d = (str(dt.datetime.today())).split(sep="-")
        _d, _t = str(_d).split(sep=" ")
        _h, _min, _s = str(_t).split(sep=":")
        _initial_date = dt.datetime(year=int(_y), month=int(_m), day=int(_d), hour=int(_h), minute=int(_min))
        self._start_time = _initial_date
        self._end_time = dt.datetime(year=int(_y), month=int(_m), day=int(_d), hour=int(_h), minute=int(_min))
        self._duration = self._end_time - self._start_time
        self._event_dict = dict()

    def __str__(self):
        """Строковое представление события"""
        return f'Event[ {self._title} is organized by {self._organizer} {self._periodic} with members {self._members} at {self._start_time} up to {self._end_time}, duration is {str(self._duration)}: {self._description}'

    def __repr__(self):
        """Представление события во время отладки"""
        return f'Event: ID: {self.__id}, title: {self._title}, organizer: {self._organizer}, periodic: {self._periodic}, members: {self._members}, start_time: {self._start_time}, end_time: {self._end_time}, duration: {str(self._duration)},'

    @property
    def title(self):
        """Возвращает название мероприятия"""
        return self._title

    @title.setter
    def title(self, new_title):
        """Изменяет название мероприятия =======Добавить update сессии и БД"""
        self._title = new_title

    @property
    def description(self):
        """Возвращает описание мероприятия"""
        return self._description

    @description.setter
    def description(self, new_description):
        """Изменяет описание мероприятия =======Добавить update сессии и БД"""
        self._description = new_description

    @property
    def members(self):
        """Возвращает список участников мероприятия"""
        return self._members

    @members.setter
    def members(self, new_members):
        """Изменяет список участников =======Добавить update сессии и БД"""
        self._members = new_members

    @members.deleter
    def members(self):
        """Удаляет всех участников =======Добавить update сессии и БД"""
        self._members = []

    def add_member(self, new_member):
        """Добавляет участника мероприятия =======Добавить update сессии и БД"""
        self._members.append(new_member)

    def _del_member(self):
        """Удаляет участника мероприятия, например при отклонении события
         =======Добавить update сессии и БД"""
        pass

    def get_id(self):
        """Возвращает ID мероприятия"""
        return self.__id

    def get_organizer(self):
        """Возвращает организатора события"""
        return self._organizer

    @property
    def start(self):
        """Возвращает время начала мероприятия"""
        return self._start_time

    @start.setter
    def start(self, new_start_time):
        """Изменяет время начала мероприятия =======Добавить update сессии и БД"""
        self._start_time = datetime.datetime.strptime(new_start_time, '%Y/%m/%d, %H:%M')
        self.update_duration()

    @property
    def end(self):
        """Возвращает время окончания мероприятия"""
        return self._end_time

    @end.setter
    def end(self, new_end_time):
        """Изменяет время окончания мероприятия =======Добавить update сессии и БД"""
        self._end_time = datetime.datetime.strptime(new_end_time, '%Y/%m/%d, %H:%M')
        self.update_duration()

    @property
    def periodic(self):
        """Возвращает периодичность мероприятия"""
        return self._periodic

    @periodic.setter
    def periodic(self, new_periodic):
        """Изменяет периодичность мероприятия =======Добавить update сессии и БД"""
        self._periodic = new_periodic

    def set_periodic(self):

        periodic = input(f'Выберите периодичность события:\n'
                         f'"1" - Ежегодно\n'
                         f'"2" - Ежемесячно\n'
                         f'"3" - Еженедельно\n'
                         f'"4" - Ежедневно\n'
                         f'"5" - Разовое\n'
                         f'Ваш выбор: ')
        while periodic not in (1, 2, 3, 4, 5, 0):
            periodic = input(f'Вы ввели неверный номер периодичности, повторите набор, либо наберите "0" для выхода:\n'
                             f'"1" - Ежегодно\n'
                             f'"2" - Ежемесячно\n'
                             f'"3" - Еженедельно\n'
                             f'"4" - Ежедневно\n'
                             f'"5" - Разовое\n'
                             f'Ваш выбор: ')

        self._periodic = self.__class__._periodic_dict[periodic]

    def to_dict(self):
        """Преобразует событие к словарю, например для записи в БД или json/bson"""
        self._event_dict['_id'] = self.get_id()
        self._event_dict['title'] = self.title
        self._event_dict['periodic'] = self.periodic
        self._event_dict['organizer'] = self.get_organizer()
        self._event_dict['start_time'] = self.start
        self._event_dict['end_time'] = self.end
        self._event_dict['duration'] = str(self.duration)
        self._event_dict['descr'] = self.description
        self._event_dict['members'] = self.members


        return self._event_dict

    def create_from_json_message(self, json_message):
        """Создает Event из переменной текстового формата json"""
        import json
        data_json = json.loads(json_message)
        print(data_json)  # закомментировать после отладки
        self.__id = data_json["_id"]
        self._title = data_json["title"]
        self._periodic = data_json["periodic"]
        self._organizer = data_json["organizer"]
        _y, _m, _d = (str(data_json["start_time"])).split(sep="/")
        _d, _t = str(_d).split(sep=", ")
        _h, _min = str(_t).split(sep=":")
        start = dt.datetime(year=int(_y), month=int(_m), day=int(_d), hour=int(_h), minute=int(_min))
        self._start_time = start
        _y, _m, _d = (str(data_json["end_time"])).split(sep="/")
        _d, _t = str(_d).split(sep=", ")
        _h, _min = str(_t).split(sep=":")
        end = dt.datetime(year=int(_y), month=int(_m), day=int(_d), hour=int(_h), minute=int(_min))
        self._end_time = end
        if self.check_sequence_dates(self._start_time, self._end_time):
            raise ValueError(f'В {json_message} сообщении дата начала события позже окончания')
        self._duration = data_json["duration"]
        self._description = data_json["descr"]
        self._members = data_json["members"]

        # print(data_json["start_time"])
        # print(data_json["end_time"])
        return self

    def create_from_json_file(self, json_path):
        """Создает Event из файла с json текстом"""

        with open(json_path, 'r') as file_from_path:
            data_json = json.load(file_from_path)
            print(data_json)
            self.__id = data_json["_id"]
            self._title = data_json["title"]
            self._periodic = data_json["periodic"]
            self._organizer = data_json["organizer"]
            _y, _m, _d = (str(data_json["start_time"])).split(sep="/")
            _d, _t = str(_d).split(sep=", ")
            _h, _min = str(_t).split(sep=":")
            start = dt.datetime(year=int(_y), month=int(_m), day=int(_d), hour=int(_h), minute=int(_min))
            self._start_time = start
            _y, _m, _d = (str(data_json["end_time"])).split(sep="/")
            _d, _t = str(_d).split(sep=", ")
            _h, _min = str(_t).split(sep=":")
            end = dt.datetime(year=int(_y), month=int(_m), day=int(_d), hour=int(_h), minute=int(_min))
            self._end_time = end
            if self.check_sequence_dates(self._start_time, self._end_time):
                raise ValueError(f'В {json_path} файле дата начала события позже окончания')
            self._duration = data_json["duration"]
            self._description = data_json["descr"]
            self._members = data_json["members"]
            # print(self)  # закомментировать после отладки

    def save_as_json_var(self):
        """Сохраняет Event в переменную формата json)"""
        data_event = {'_id': self.__id, 'title': self._title, 'periodic': self._periodic,
                      'organizer': self._organizer, 'start_time': self._start_time.strftime('%Y/%m/%d, %H:%M'),
                      'end_time': self._end_time.strftime('%Y/%m/%d, %H:%M'), '_duration': str(self._duration),
                      'descr': self._description, 'members': self._members}
        json_mes = json.dumps(data_event, indent=4)
        return json_mes

    def save_as_json_file(self):
        """Сохраняет Event в файл формата json)"""
        data_event = {'_id': self.__id, 'title': self._title, 'periodic': self._periodic,
                      'organizer': self._organizer, 'start_time': self._start_time.strftime('%Y/%m/%d, %H:%M'),
                      'end_time': self._end_time.strftime('%Y/%m/%d, %H:%M'), 'duration': str(self._duration),
                      'descr': self._description, 'members': self._members}
        with open(str(self.__id) + str(self._title) + ' -event.json', 'w') as file_json_from_event:
            json.dump(data_event, file_json_from_event, indent=4, ensure_ascii=True)

    @property
    def duration(self):
        """Производит расчет и возвращает продолжительность события"""
        self._duration = self._end_time - self._start_time
        return self._duration

    @staticmethod
    def check_sequence_dates(start, end):
        return end > start

    def update_duration(self):
        """Производит расчет продолжительности события без вывода"""
        self._duration = self._end_time - self._start_time

    def message_to_members_add(self):
        """Отправляет сообщение участникам события о добавлении в событие"""
        pass

    def message_to_members_cancel(self):
        """Отправляет сообщение участникам события об отмене события"""
        pass

    def message_to_members_change_time(self):
        """Отправляет сообщение участникам события об изменении времени начала события"""
        pass

    def message_to_members_change_periodic(self):
        """Отправляет сообщение участникам события об изменении периодичности события"""
        pass

    def message_to_organizer_cancel_participation(self):
        """Отправляет сообщение организатору об отклонении события участником"""
        pass


if __name__ == '__main__':
    # import pymongo
    #
    # client = pymongo.MongoClient("mongodb+srv://krayushkin90:11171990@cluster0.dn7jino.mongodb.net/")
    # db = client.events
    # coll = db.new_events
    # coll.insert_one({"ID": 1, "Name": 'Common meeting'})

    # _y, _m, _d = (str(dt.datetime.today())).split(sep="-")
    # _d, _t = str(_d).split(sep=" ")
    # _h, _min, _s = str(_t).split(sep=":")
    # _initial_date = dt.datetime(year=int(_y), month=int(_m),day=int(_d),hour=int(_h), minute=int(_min))
    # print(_y,"\n", _m,"\n", _d, "\n", _h, "\n", _min)
    # print(_initial_date)
    k = Event()
    # print(type(k.start), k.end)
    # k.start = "2024/01/18, 0:50"
    # k.end = "2024/01/18, 0:59"
    # print(type(k.start), k.end)
    # print(k.duration, type(k.duration))
    # print(k.save_as_json_var())
    # k.save_as_json_file()
    # k.create_from_json_file("1 event.json")
    # message = """{
    #     "_id": 1,
    #     "title": "Meeting CEO",
    #     "periodic": {"1": "Monthly"},
    #     "organizer": "Tom",
    #     "start_time": "2024/01/18, 00:50",
    #     "end_time": "2024/01/18, 00:59",
    #     "duration": "0:09:00",
    #     "descr": "Let's do it quickly",
    #     "members": ["@triko", "@gangsta", "@rooney"]
    # }"""
    # k.create_from_json_message(message)
    # print(k)
