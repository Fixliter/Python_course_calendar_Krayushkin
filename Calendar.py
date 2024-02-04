"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
"""
import calendar
import datetime

from Event import Event
import datetime as dt
import calendar
import numpy as np
from datetime import timedelta


class Calendar:
    _owner = []
    _id_list = []
    __id = 0
    _events = dict()
    fieldnames_calendar = ['_id', 'owner', 'name', 'events']
    file_calendar = "calendar_data.csv"
    _calendars_dict = dict()
    events_to_db = list()

    def __init__(self, owner, name, _id=None, _events=None):
        self._owner = owner
        self._name = name
        self.__class__.__id += 1
        self.__class__._id_list.append(self.__class__.__id)
        self.__id = self.__class__.__id
        self._calendar_dict = dict()
        self._calendar_dict_db = dict()
        self._events = []
        self._events_d = dict()
        self.to_dict()
        self.__class__._calendars_dict[self.__id] = self
        self._id_events = []
        self.stage = None

    def __str__(self):
        """Текстовое представление экземпляра класса Календарь"""
        return f"Calendar: ID: {self.__id}, Name: {self._name}, owner: {self._owner}, events: {self._events_d}"

    def __repr__(self):
        """Представление экземпляра класса Календарь для отладки"""
        return f"Calendar: ID: {self.__id}, Name: {self._name}, owner: {self._owner}, events: {self._events_d}"

    def start_calendar(self):
        """Запуск выбранного календаря, инициализация, приветствие ==========Доделать"""

        print(f'Приветствую, {self._owner}!')
        self.stage = str(input(f'Выберите опцию для работы:'
                               f'"1" - Добавить(создать) событие,'
                               f'"2" - Удалить событие,'
                               f'"3" - Редактировать событие,'
                               f'"4" - Найти события по временному интервалу,'
                               f'"5" - Найти события по названию,'))
        match self.stage:
            case "1":
                self.add_event()
            case "2":
                self.del_event()

    def get_owner(self):
        """Возвращает владельца календаря"""
        return self._owner

    def get_id(self):
        """Возвращает ID календаря"""
        return self.__id

    @property
    def name(self):
        """Возвращает название календаря"""
        return self._name

    @name.setter
    def name(self, new_name):
        """Изменяет название календаря   ====Добавить update сессии и БД"""
        self._name = new_name
        self.__class__._calendars_dict[self.__id]._name = new_name

    def add_event(self):
        """Добавляет событие в календарь"""
        new_event = Event()
        new_event.title = input("Введите название мероприятия: ")
        # new_event.periodic = input("Введите периодичность мероприятия: ").capitalize()
        new_event.set_periodic()
        new_event._organizer = self._owner

        new_event.start = input("Введите начало мероприятия в формате YYYY/mm/dd, H:M : ")
        new_event.end = input("Введите окончание мероприятия в формате: YYYY/mm/dd, H:M : ")
        while not new_event.check_sequence_dates(new_event.start, new_event.end):
            print("Пожалуйста, введите дату и время окончания события позже, чем начало события")
            new_event.start = input("Введите начало мероприятия в формате YYYY/mm/dd, H:M : ")
            new_event.end = input("Введите окончание мероприятия в формате: YYYY/mm/dd, H:M : ")

        new_event.description = input("Введите описание мероприятия с указанием цели и темы: ")
        new_event.members = input("добавьте идентификаторы участников в строчку через '/': ").strip().split("/")
        new_event.to_dict()
        self.__class__._events[new_event.get_id()] = new_event
        self._events_d[new_event.get_id()] = new_event.to_dict()
        # self.__class__.__events.append(new_event)
        self._events.append(new_event)
        self._id_events.append(new_event.get_id())
        self.events_to_db.append(new_event.to_dict())
        return new_event

    def del_event(self, _id_event=None):
        if _id_event is None:
            del_event = str(input(f"Выберите id события для удаления: \n"
                                  f"{self._events_d}"))
        else:
            del_event = str(_id_event)
        self.__class__._events.pop(del_event)
        self._events_d.pop(del_event)
        for event in self._events:
            if event["_id"] == del_event:
                self._events.remove(event)
        for id_event in self._id_events:
            if id_event == del_event:
                self._id_events.remove(id_event)
        for event_d in self.events_to_db:
            if event_d["_id"] == del_event:
                self.events_to_db.remove(event_d)
        return del_event

    def add_event_from_json_message(self, message):
        """Добавляет событие в календарь из json переменной, например при инициализации"""
        new_event = Event()
        new_event.create_from_json_message(message)
        new_event.to_dict()
        self.__class__._events[new_event.get_id()] = new_event
        self._events_d[new_event.get_id()] = new_event.to_dict()
        self._id_events.append(new_event.get_id())
        self._events.append(new_event)
        self.events_to_db.append(new_event.to_dict())
        return new_event

    def add_event_from_json_file(self, json_file):
        """Добавляет событие в календарь из json файла, например при инициализации"""
        new_event = Event()
        new_event.create_from_json_file(json_file)
        new_event.to_dict()
        self.__class__._events[new_event.get_id()] = new_event
        self._events_d[new_event.get_id()] = new_event.to_dict()
        self._events.append(new_event)
        self._id_events.append(new_event.get_id())
        self.events_to_db.append(new_event.to_dict())

        return new_event

    def get_events_list(self):
        """Возвращает лист событий экземпляра календаря"""
        return self._events

    def get_events_dict(self):
        """Возвращает словарь событий экземпляра календаря"""
        for event in self._events:
            return event.to_dict()

    def get_events_dict_class(self):
        """Возвращает словарь событий класса календаря"""
        return self.__class__._events

    # def get_events_dict_class_self(self):
    #     """Возвращает словарь событий класса календаря"""
    #     return self.__events

    def get_events_dict_self(self):
        """Возвращает словарь событий экземпляра календаря"""
        return self._events_d

    def get_calendar_dict(self):
        """Возвращает словарь экземпляра календаря ===================Проверить"""
        self.to_dict()
        return self._calendar_dict

    def to_dict(self):
        """Преобразование в словарь экземпляра календаря со списком событий"""
        self._calendar_dict['_id'] = self.get_id()
        self._calendar_dict['name'] = self.name
        self._calendar_dict['owner'] = self.get_owner()
        self._calendar_dict["events"] = self._events

        return self._calendar_dict

    def to_dict_db(self):
        """Преобразование в словарь экземпляра календаря со списком id событий"""
        self._calendar_dict_db['_id'] = self.get_id()
        self._calendar_dict_db['name'] = self.name
        self._calendar_dict_db['owner'] = self.get_owner()
        self._calendar_dict_db["events"] = self._id_events

        return self._calendar_dict_db

    def get_id_events(self):
        return self._id_events

    def accept_event_and_message(self):
        """Принятие события участником"""
        pass

    def find_events_by_date(self, t1: str, t2: str):
        """Поиск события по дате"""
        found_events = list()
        t1time = dt.datetime.strptime(t1, '%Y/%m/%d, %H:%M')
        t2time = dt.datetime.strptime(t2, '%Y/%m/%d, %H:%M')
        print(t1time, t2time)
        print(t1time.time(), t2time.time())
        event_count = 0
        for event in self.events_to_db:
            print(event["start_time"].time())
            if event["periodic"] == "Разовое":
                if t2time >= event["start_time"] >= t1time:
                    found_events.append(event)
                    event_count += 1
            if (event["periodic"] == "Ежедневно" and
                    (
                    ( t2time.date() > event["start_time"].date() and
                      t2time - t1time >= datetime.timedelta(hours=24) or
                      t2time - t1time < datetime.timedelta(hours=24) and
                      t2time.time() > event["start_time"].time() > t1time.time()
                    )
                    or
                    ( t2time.date() == event["start_time"].date() and
                      t2time.time() >= event["start_time"].time()
                    )
                    )
                ):
                found_events.append(event)
                event_count += 1
            # if event["periodic"] == "Еженедельно" and
            if (
                    (event["periodic"] == "Еженедельно") and
                    (t2time.date() >= event["start_time"].date() and
                            (  (t1time.year < event["start_time"].year) or
                               (t1time.year >= event["start_time"].year) and
                               (
                                       (t1time.isocalendar().week < event["start_time"].isocalendar().week <= t2time.isocalendar().week) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t1time.isocalendar().week < t2time.isocalendar().week and t2time.isoweekday() < event["start_time"].isoweekday() and t1time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() == event["start_time"].isoweekday() and t2time.time() >= event["start_time"].time()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t2time - t1time >= datetime.timedelta(days=7)) or  #t1time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() > event["start_time"].isoweekday() > t1time.isoweekday()) or  #t1time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() >= event["start_time"].isoweekday() > t1time.isoweekday() and t2time.time() >= event["start_time"].time()) or  #t1time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() > event["start_time"].isoweekday() >= t1time.isoweekday() and t1time.time() <= event["start_time"].time()) or  #t1time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t1time.isoweekday() == event["start_time"].isoweekday() and t1time.time() <= event["start_time"].time())
                               )
                            ) and
                            (  #(t2time.year > event["start_time"].year) or
                               (
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t1time.isocalendar().week < t2time.isocalendar().week and t2time.isoweekday() < event["start_time"].isoweekday() and t1time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t1time.isoweekday() == event["start_time"].isoweekday() and t1time.time() <= event["start_time"].time() and t2time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t1time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() == event["start_time"].isoweekday() and t2time.time() >= event["start_time"].time() and t2time.isoweekday() < event["start_time"].isoweekday()) or
                                       (t2time.isocalendar().week >= event["start_time"].isocalendar().week and t2time - t1time >= datetime.timedelta(days=7)) or
                                       (t2time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() > event["start_time"].isoweekday() > t1time.isoweekday()) or
                                       (t2time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() >= event["start_time"].isoweekday() > t1time.isoweekday() and t2time.time() >= event["start_time"].time()) or
                                       (t2time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() > event["start_time"].isoweekday() >= t1time.isoweekday() and t1time.time() <= event["start_time"].time()) or
                                       (t2time.isocalendar().week >= event["start_time"].isocalendar().week and t2time.isoweekday() == event["start_time"].isoweekday() and t2time.time() > event["start_time"].time())
                               )
                            )
                    )
            ):
                found_events.append(event)
                event_count += 1
            # if (
            #         (event["periodic"] == "Ежемесячно") and
            #         (t2time.date() >= event["start_time"].date() and
            #            (
            #              (t1time.month < event["start_time"].month) or
            #              (
            #                      t1time.month == event["start_time"].month and
            #                 (
            #                         (t1time.isocalendar().week < event["start_time"].isocalendar().week) or
            #                         (t1time.isocalendar().week == event["start_time"].isocalendar().week and t1time.isoweekday() < event["start_time"].isoweekday()) or
            #                         (t1time.isocalendar().week == event["start_time"].isocalendar().week and t1time.isoweekday() == event["start_time"].isoweekday() and t1time.time() <= event["start_time"].time())
            #                 )
            #              )
            #            ) and
            #                 (
            #                    (t2time.month > event["start_time"].month) or
            #                    (
            #                            t2time.month == event["start_time"].month and
            #                         (t2time.isocalendar().week > event["start_time"].isocalendar().week) or
            #                         (t2time.isocalendar().week == event["start_time"].isocalendar().week and t2time.isoweekday() > event["start_time"].isoweekday()) or
            #                         (t2time.isocalendar().week == event["start_time"].isocalendar().week and t2time.isoweekday() == event["start_time"].isoweekday() and t2time.time() > event["start_time"].time())
            #                    )
            #                 )
            #         )
            #
            # ):
            #     found_events.append(event)
            #     event_count += 1
            # if (
            #         (event["periodic"] == "Ежегодно") and
            #         (t2time.date() > event["start_time"].date() and
            #           (
            #             (t1time.year < event["start_time"].year) or
            #             (
            #                     t1time.year == event["start_time"].year and
            #                  (
            #
            #                              (t1time.month < event["start_time"].month) or
            #                              (
            #                                      t1time.month == event["start_time"].month and
            #                               (
            #                                       (t1time.isocalendar().week < event["start_time"].isocalendar().week) or
            #                                       (t1time.isocalendar().week == event["start_time"].isocalendar().week and t1time.isoweekday() < event["start_time"].isoweekday()) or
            #                                       (t1time.isocalendar().week == event["start_time"].isocalendar().week and t1time.isoweekday() == event["start_time"].isoweekday() and t1time.time() <= event["start_time"].time())
            #                               )
            #                              )
            #
            #                  )
            #             )
            #           ) and
            #                  (
            #                      (t2time.year > event["start_time"].year) or
            #                      (
            #                              t2time.year == event["start_time"].year and
            #                      (
            #                              (t2time.month > event["start_time"].month) or
            #                              (
            #                                t2time.month == event["start_time"].month and
            #                               (t2time.isocalendar().week > event["start_time"].isocalendar().week) or
            #                               (t2time.isocalendar().week == event["start_time"].isocalendar().week and t2time.isoweekday() > event["start_time"].isoweekday()) or
            #
            #                               (t2time.isocalendar().week == event["start_time"].isocalendar().week and t2time.isoweekday() == event["start_time"].isoweekday() and t2time.time() > event["start_time"].time())
            #                              )
            #
            #                      )
            #                      )
            #                  )
            #
            #
            #         )
            #
            # ):
            #     found_events.append(event)
            #     event_count += 1

            # found_events.append(event)
        print(f"Найдено {event_count} событий(ие) за период {t1} - {t2}")
        for event in found_events:
            print(f'{event["periodic"]}')
        # ts2 = t2time
        # ttt = dt.datetime.strptime("2024/10/12, 00:00", '%Y/%m/%d, %H:%M')
        # print(ts2)
        # print(ttt)
        # while t1time.date != ts2.date:
        #     ts2 = ts2 - timedelta(days=1)
        #     # print(ts2)
        #     if ts2.isoweekday() == ttt.isoweekday():
        #         print("FOUND")
        #         continue
        return found_events

        # 2024/01/18, 00:50
    @staticmethod
    def get_week_of_month(date):
        calendar.setfirstweekday(0)
        date_to = datetime.datetime.strptime(date, '%Y/%m/%d, %H:%M')
        year = date_to.year
        month = date_to.month
        day = date_to.day
        x = np.array(calendar.monthcalendar(int(year), int(month)))
        # print(x)
        week_of_month = np.where(x == day)[0][0] + 1
        return week_of_month

    def find_events_by_title(self):
        """Поиск события по наименованию"""
        pass

    def find_events_by_id(self):
        """Поиск события по id"""
        pass


if __name__ == '__main__':
    g = Calendar("Антон", "Личный")
    message1 = """{
            "_id": 1,
            "title": "Meeting Congratulation",
            "periodic": "Разовое",
            "organizer": "Shella",
            "start_time": "2024/09/28, 00:20",
            "end_time": "2024/09/28, 00:29",
            "duration": "0:09:00",
            "descr": "Wow, amazing!",
            "members": ["@triko", "@gangsta", "@rooney", "@bertha", "@shon"]
        }"""

    message2 = """{
        "_id": 2,
        "title": "Meeting 1234",
        "periodic": "Ежедневно",
        "organizer": "Bobby",
        "start_time": "2024/03/18, 01:50",
        "end_time": "2024/03/18, 02:59",
        "duration": "1:09:00",
        "descr": "Let's do it quickly",
        "members": ["@triko", "@gangsta", "@rooney"]
    }"""

    message3 = """{
        "_id": 3,
        "title": "Meeting WorkHardPlanning",
        "periodic": "Еженедельно",
        "organizer": "Bibi",
        "start_time": "2024/10/12, 02:20",
        "end_time": "2024/10/12, 03:29",
        "duration": "1:09:00",
        "descr": "Every week of a common meeting",
        "members": ["@triko", "@gangsta", "@rooney", "@bertha", "@shon", "@abdalmanah"]
    }"""

    message4 = """{
        "_id": 4,
        "title": "Meeting CEO",
        "periodic": "Ежемесячно",
        "organizer": "Tom",
        "start_time": "2024/06/18, 00:10",
        "end_time": "2024/06/18, 00:29",
        "duration": "0:09:00",
        "descr": "Important!",
        "members": ["@triko", "@gangsta", "@rooney"]
    }"""

    message5 = """{
        "_id": 5,
        "title": "Meeting Year kick-off",
        "periodic": "Ежегодно",
        "organizer": "CEO Miri",
        "start_time": "2024/07/28, 02:20",
        "end_time": "2024/07/28, 10:29",
        "duration": "8:09:00",
        "descr": "Let's see what we achieved",
        "members": ["@triko", "@gangsta", "@rooney", "@bertha", "@shon", "@abdalmanah", "@vinimimi"]
    }"""
    g.add_event_from_json_message(message1)
    g.add_event_from_json_message(message2)
    g.add_event_from_json_message(message3)
    g.add_event_from_json_message(message4)
    g.add_event_from_json_message(message5)
    # g.add_event()
    print(g.to_dict_db())
    print(g.get_events_list(), "self._events")
    print(g.get_calendar_dict(), "self._calendar_dict")
    print(g.get_events_dict(), "self._event_dict")
    print(g.get_events_dict_class(), "self.__class__.__events")
    print(g.get_events_dict_self(), "self._events_d")
    print(g.events_to_db)
    print(g.get_week_of_month("2024/03/04, 00:00"))
    print(g.find_events_by_date(t1="2024/10/13, 00:00", t2="2025/10/11, 20:59"))

    #
    # f = Calendar("Vika", "Work")
    # f.add_event()
    # print(f.get_events_list(), "self._events")
    # print(f.get_calendar_dict(), "self._calendar_dict")
    # print(f.get_events_dict(), "self._event_dict")
    # print(f.get_events_dict_class(), "self.__class__.__events")
    # print(f.get_events_dict_class_self(), "self.__events")
    # print(f.get_events_dict_self(), "self._events_d")
    # g.start_calendar()
