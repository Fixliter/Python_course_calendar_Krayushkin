"""
Сущность, отвечающая за хранение и предоставление данных
Оно хранит пользователей, календари и события.
Хранение, в том числе означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

*- Нужно хранить для каждого пользователя все события которые с ним произошли, но ещё не были обработаны.
"""
import asyncio
import csv
from Event import Event
from Calendar import Calendar
from User import User
from threading import Lock, Thread
import pymongo
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
import bcrypt


class SingletonMeta(type):
    """
    Это потокобезопасная реализация класса Singleton с использованием метакласса.
    """
    _instances = {}
    _lock: Lock = Lock()
    """
    Создаем объект-блокировки для синхронизации потоков во время
    первого доступа к Одиночке.
    """

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        # Теперь представьте, что программа была только-только запущена.
        # Объекта-одиночки ещё никто не создавал, поэтому несколько потоков
        # вполне могли одновременно пройти через предыдущее условие и достигнуть
        # блокировки. Самый быстрый поток поставит блокировку и двинется внутрь
        # секции, пока другие будут здесь его ожидать.
        with cls._lock:
            # Первый поток достигает этого условия и проходит внутрь, создавая
            # объект-одиночку. Как только этот поток покинет секцию и освободит
            # блокировку, следующий поток может снова установить блокировку и
            # зайти внутрь. Однако теперь экземпляр одиночки уже будет создан и
            # поток не сможет пройти через это условие, а значит новый объект не
            # будет создан.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Backend(metaclass=SingletonMeta):
    """Класс на основе паттерна Синглтон"""
    _users = dict()
    _users_list = list()
    _instance = None
    __connection_info = "mongodb+srv://krayushkin90:11171990@cluster0.dn7jino.mongodb.net/"
    _statuses = {"1": "Запуск",
                 "2": "Авторизация",
                 "3": "Успешно авторизован",
                 "4": "Загрузка данных",
                 "5": "Данные загружены",
                 "6": "Выбор календаря",
                 "7": "Календарь загружен",
                 "8": "Загрузка событий",
                 "9": "События загружены",
                 "10": "Создание календаря",
                 "11": "Календарь создан",
                 "12": "Добавление события",
                 "13": "Событие добавлено",
                 "14": "Событие принято",
                 "15": "Событие удалено",
                 "16": "Событие отклонено",
                 "17": "Календарь удален",
                 "18": "Данные сохранены",
                 "19": "Сессия закрыта",
                 "20": "Загрузка данных",
                 "21": "Данные загружены",
                 "22": "Подключение к Users",
                 "23": "Users подключены",
                 "24": "Подключение к Calendars",
                 "25": "Calendars подключены",
                 "26": "Подключение к Events",
                 "27": "Events подключены",
                 "28": "Проверка подключения",
                 "29": "Проверка завершена",
                 "30": "Регистрация пользователя",
                 "31": "Регистрация пользователя завершена",
                 "32": "Закрытие сессии",
                 "33": "Обновление данных",
                 "34": "Данные обновлены",
                 "35": "Сохранение данных в csv файл",
                 "36": "Данные в csv файл сохранены",
                 "37": "Сохранение данных из csv в базу данных",
                 "38": "Данные из csv файла сохранены в базу данных",
                 "39": "Сохранение Users в базу данных",
                 "40": "Users сохранены в базу данных",
                 "41": "Сохранение Calendars в базу данных",
                 "42": "Calendars в базу данных сохранены",
                 "43": "Сохранение Events в базу данных",
                 "44": "Events в базу данных сохранены",
                 "45": "Загрузка Users из базы данных",
                 "46": "Users загружены из базы данных",
                 "47": "Загрузка Calendars из базы данных",
                 "48": "Calendars загружены из базы данных",
                 "49": "Загрузка Events из базы данных",
                 "50": "Events загружены из базы данных"

                 }

    def __init__(self, current_user=None):
        # self.__class__.get_users_from_db()
        self.launched_user = ''
        self.current_user = current_user
        self.session_launched = ""
        self.show_status("1")

    @staticmethod
    def show_status(status):
        Backend.status = status
        print(Backend._statuses[str(Backend.status)])
        return Backend.status

    @staticmethod
    def asyncconnect_db():
        """Попытка сделать асинхронное пользование БД, но не доделано"""
        Backend.show_status("20")
        cluster = AsyncIOMotorClient(
            "mongodb+srv://krayushkin90:11171990@cluster0.dn7jino.mongodb.net/?retryWrites=true&w=majority")

        async def users():
            collection = cluster.calendarwork.users
            data_user = await collection.find_one({})
            print(data_user)

        async def calendars():
            collection = cluster.calendarwork.events
            data_calendars = await collection.find_one({})
            print(data_calendars)

        async def events():
            collection = cluster.calendarwork.calendars
            data_events = await collection.find_one({})
            print(data_events)

        async def main():
            await users()
            await calendars()
            await events()

        asyncio.run(main())
        Backend.show_status("21")

    @staticmethod
    def connection_db_check():
        """Подключение и пинг связи с ДБ, возврат ошибки при остутствии пинга или сообщения
        о успешном пинги при его наличии"""
        Backend.show_status("28")
        uri = "mongodb+srv://krayushkin90:11171990@cluster0.dn7jino.mongodb.net/?retryWrites=true&w=majority"
        # # Create a new client and connect to the server
        client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        Backend.show_status("29")

    @staticmethod
    def set_index_db():
        """ Вызывается один раз для установки индексов в целях оптимизации скорости
         поиска по часто запрашиваемым полям"""

        def user_index():
            mongoclient = pymongo.MongoClient(Backend.__connection_info)
            db = mongoclient.calendarwork
            collection = db.users
            collection.create_index([("login", pymongo.ASCENDING)], unique=True)
            collection.create_index([("_id", pymongo.ASCENDING)])
            collection.create_index([("calendars", pymongo.ASCENDING)])

        def calendars_index():
            mongoclient = pymongo.MongoClient(Backend.__connection_info)
            db = mongoclient.calendarwork
            collection = db.calendars
            collection.create_index([("owner", pymongo.ASCENDING)])
            collection.create_index([("_id", pymongo.ASCENDING)])
            collection.create_index([("events", pymongo.ASCENDING)])

        def events_index():
            mongoclient = pymongo.MongoClient(Backend.__connection_info)
            db = mongoclient.calendarwork
            collection = db.events
            collection.create_index([("start_time", pymongo.ASCENDING)])
            collection.create_index([("end_time", pymongo.ASCENDING)])
            collection.create_index([("_id", pymongo.ASCENDING)])
            collection.create_index([("members", pymongo.ASCENDING)])

        user_index()
        calendars_index()
        events_index()

    @staticmethod
    def connection_db_users():
        """Подключение к базе и конкретно к коллекции users"""
        Backend.show_status("22")
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.users
        Backend.show_status("23")
        return collection

    # Можно написать пару wrapper для одного connection_db, но не вижу особых удобств
    @staticmethod
    def connection_db_calendars():
        """Подключение к базе и конкретно к коллекции calendars"""
        Backend.show_status("24")
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.calendars
        Backend.show_status("25")
        return collection

    @staticmethod
    def connection_db_events():
        """Подключение к базе и конкретно к коллекции events"""
        Backend.show_status("26")
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.events
        Backend.show_status("27")
        return collection

    def register_new_user(self):
        """Создания нового экземпляра класса User с проверкой соответствующих
        полей на ввод данных, логин и пароль являются обязательными, логин проверяется на
        наличие в базе, пароль проверяется на пустое значение и наличие пробела"""
        Backend.show_status("30")
        collection = self.connection_db_users()
        new_user = User("", "")
        new_user.name = input("Введите имя пользователя: ")
        new_user.job_title = input("Введите должность: ")
        new_user.email = input("Введите email: ")
        new_user.login = input("Введите login(латинскими): ")
        is_exists = collection.count_documents({"login": new_user.login})
        if is_exists == 0:
            print("Login is available")
        else:
            print("Login is already exist, try to use another one")
            while collection.count_documents({"login": new_user.login}):
                # while new_user.login in self._users.keys():
                print(f"login {new_user.login} уже занят")
                new_user.login = input("Введите другой login: ")
        new_user._password = input("Введите password: ")
        if new_user._password is not None and " " not in new_user._password:
            print(f"Пароль успешно принят")
            new_user.gen_hashed_pass()
        else:
            print("Пароль не введен или содержит пробел, введите пароль в виде букв, чисел и символов без пробелов")
            while new_user._password is not None and " " not in new_user._password:
                print(f"login {new_user.login} уже занят")
                new_user._password = input("Введите password корректно, например 'ABCdef1234@^%': ")

        self.__class__._users[new_user.login] = new_user.to_dict_db()
        User.users_db.append(new_user.to_dict_db())
        User._users.append(new_user.to_dict_db())
        print(self.__class__._users)  # - закомментировать после отладки
        # new_user.save_as_json_file()
        collection = self.connection_db_users()
        collection.insert_one(self.__class__._users[new_user.login])

        Backend.show_status("31")

    def read_user_from_class(self, user):
        """При подключении к User создает словарь с user"""
        self.__class__._users[user.login] = user

    def get_users(self):
        """Возвращает словарь с Users"""
        return self.__class__._users

    @staticmethod
    def get_users_from_db():
        """Возвращает словари users из базы данных"""
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.users
        for user in collection.find():
            Backend._users_list.append(user)
            # print(user)  # после отладки закомментировать
        # print(Backend._users_list)  # после отладки закомментировать
        return Backend._users_list

    def save_data(self, mode):
        """Сохранение данных в соответствующие csv файлы"""
        self.show_status("35")
        if mode.lower() == "u":
            fieldnames = User.fieldnames_user
            file = User.file_users
            # source = self.__class__._users # - содержит Users(calendars(events)))
            source = User.users_db  # - содержит Users(...+_id_calendars)

        elif mode.lower() == 'c':
            fieldnames = Calendar.fieldnames_calendar
            file = Calendar.file_calendar
            source = User.get_calendars()

        elif mode.lower() == 'e':
            fieldnames = Event.fieldnames_event
            file = Event.file_events
            source = Calendar.events_to_db
        else:
            raise ValueError("Неправильно выбран режим сохранения данных")

        with open(file, mode='w', newline='') as file:

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for item in source.values():
                print(f'Записано: {item}')
                # writer.writerow(item.to_dict()) # - требовалось для преобразования к словарю для дальнейшей передачи в csv или json/bson
                writer.writerow(item)
        self.show_status("36")

    @staticmethod
    def save_from_csv_to_db():
        """Сохранение данных из csv в базу данных"""

        def csv_user_data_to_db():
            """Подключается к БД и записывает users в базу данных из csv users_data"""

            try:
                mongoclient = pymongo.MongoClient(Backend.__connection_info)
                db = mongoclient.calendarwork
                collection = db.users
                header = User.fieldnames_user
                with open(User.file_users, "r") as csv_file:
                    reader = csv.DictReader(csv_file)

                    for each in reader:
                        row = {}
                        for field in header:
                            row[field] = each[field]
                        print(row)
                        collection.insert_one(row)

            except ConnectionError:
                print(f'Соединение с БД не достигнуто')

        def csv_calendars_data_to_db():
            """Подключается к БД и записывает calendars в базу данных из csv calendars_data"""
            try:
                mongoclient = pymongo.MongoClient(Backend.__connection_info)
                db = mongoclient.calendarwork
                collection = db.calendars
                header = Calendar.fieldnames_calendar
                with open(Calendar.file_calendar, "r") as csv_file:
                    reader = csv.DictReader(csv_file)

                    for each in reader:
                        row = {}
                        for field in header:
                            row[field] = each[field]
                        print(row)
                        collection.insert_one(row)

            except ConnectionError:
                print(f'Соединение с БД не достигнуто')

        def csv_events_data_to_db():
            """Подключается к БД и записывает events в базу данных из csv events_data"""
            try:
                mongoclient = pymongo.MongoClient(Backend.__connection_info)
                db = mongoclient.calendarwork
                collection = db.events
                header = Event.fieldnames_event
                with open(Event.file_events, "r") as csv_file:
                    reader = csv.DictReader(csv_file)

                    for each in reader:
                        row = {}
                        for field in header:
                            row[field] = each[field]
                        print(row)
                        collection.insert_one(row)

            except ConnectionError:
                print(f'Соединение с БД не достигнуто')

        Backend.show_status("37")

        csv_user_data_to_db()
        csv_calendars_data_to_db()
        csv_events_data_to_db()

        Backend.show_status("38")

    @staticmethod
    def save_users_to_db():
        """Подключается к БД и записывает users в базу данных"""
        Backend.show_status("39")
        try:
            collection = Backend.connection_db_users()
            collection.insert_many(User.users_db)

        except ConnectionError:
            print(f'Соединение с БД не достигнуто')
        Backend.show_status("40")

    @staticmethod
    def save_calendars_to_db():
        """Подключается к БД и записывает calendars в базу данных"""
        Backend.show_status("41")
        try:
            mongoclient = pymongo.MongoClient(Backend.__connection_info)
            db = mongoclient.calendarwork
            collection = db.calendars
            collection.insert_many(User.calendars_db)

        except ConnectionError:
            print(f'Соединение с БД не достигнуто')
        Backend.show_status("42")

    @staticmethod
    def save_events_to_db():
        """Подключается к БД и записывает events в базу данных"""
        Backend.show_status("43")
        try:
            mongoclient = pymongo.MongoClient(Backend.__connection_info)
            db = mongoclient.calendarwork
            collection = db.events
            collection.insert_many(Calendar.events_to_db)

        except ConnectionError:
            print(f'Соединение с БД не достигнуто')
        Backend.show_status("44")

    @staticmethod
    def load_from_db_users():
        Backend.show_status("45")
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.users
        for user in collection.find():
            User.users_db.append(user)
            User._users.append(user)
        print(User.users_db, "\n", User._users)  # после отладки закомменитровать
        Backend.show_status("46")

    @staticmethod
    def load_from_db_calendars():
        Backend.show_status("47")
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.calendars
        for calendar in collection.find():
            User.calendars_db.append(calendar)
            User._calendars[calendar["_id"]] = calendar
            Calendar._calendars_dict[calendar["_id"]] = calendar
            Calendar._id_list.append(calendar["_id"])
        print(User.calendars_db, "\n", User._calendars, "\n",
              Calendar._calendars_dict)  # после отладки закомменитровать
        Backend.show_status("48")

    @staticmethod
    def load_from_db_events():
        Backend.show_status("49")
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.events
        for event in collection.find():
            Calendar._events[event["_id"]] = event
            Calendar.events_to_db.append(event)
            Event._events_db.append(event)
            Event._id_list.append(event["_id"])

        print(Calendar._events, "\n", Calendar.events_to_db, "\n", Event._events_db, "\n",
              Event._id_list)  # после отладки закомменитровать
        Backend.show_status("50")

    @staticmethod
    def asyncload_db():
        """Попытка сделать асинхронную выгрузку данных с БД для дальнейшей работы"""
        Backend.show_status("4")
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork

        async def users():
            collection = db.users
            for user in collection.find():
                User.users_db.append(user)
                User._users.append(user)
            print(User.users_db, "\n", User._users)  # после отладки закомменитровать

        async def calendars():
            collection = db.calendars
            for calendar in collection.find():
                User.calendars_db.append(calendar)
                User._calendars[calendar["_id"]] = calendar
                Calendar._calendars_dict[calendar["_id"]] = calendar
                Calendar._id_list.append(calendar["_id"])
            print(User.calendars_db, "\n", User._calendars, "\n",
                  Calendar._calendars_dict)

        async def events():
            collection = db.events
            for event in collection.find():
                Calendar._events[event["_id"]] = event
                Calendar.events_to_db.append(event)
                Event._events_db.append(event)
                Event._id_list.append(event["_id"])

        async def main_load():
            await users()
            await calendars()
            await events()

        asyncio.run(main_load())
        Backend.show_status("5")

    @staticmethod
    def asyncsave_db():
        """Попытка сделать асинхронное сохранение данных в БД, например при закрытии сессии"""

        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork

        async def users():
            """Подключается к БД и записывает users в базу данных"""
            Backend.show_status("39")
            try:
                collection = Backend.connection_db_users()
                collection.insert_many(User.users_db)

            except ConnectionError:
                print(f'Соединение с БД не достигнуто')
            Backend.show_status("40")

        async def calendars():
            """Подключается к БД и записывает calendars в базу данных"""
            Backend.show_status("41")
            try:
                # mongoclient = pymongo.MongoClient(Backend.__connection_info)
                # db = mongoclient.calendarwork
                collection = db.calendars
                collection.insert_many(User.calendars_db)

            except ConnectionError:
                print(f'Соединение с БД не достигнуто')
            Backend.show_status("42")

        async def events():
            """Подключается к БД и записывает events в базу данных"""
            Backend.show_status("43")
            try:
                # mongoclient = pymongo.MongoClient(Backend.__connection_info)
                # db = mongoclient.calendarwork
                collection = db.events
                collection.insert_many(Calendar.events_to_db)

            except ConnectionError:
                print(f'Соединение с БД не достигнуто')
            Backend.show_status("44")

        async def main_save():
            await users()
            await calendars()
            await events()

        asyncio.run(main_save())
        Backend.show_status("18")

    def find_user_by_login(self, login):
        return self.connection_db_users().find_one({"login": login})

    def find_users_by_id(self):
        pass

    def find_users_by_ident(self):
        pass

    @staticmethod
    def check_pass_user(login, entered_password: str):
        """Проверка соответствия пароля, смотрит в выгруженном листе users"""
        # To check:
        # password = userInput
        # user_pass = str(input("Enter "))  # - для проверки на отладке
        user_pass = entered_password
        Backend.get_users_from_db()
        for user in Backend._users_list:
            if login == user["login"]:
                valid = bcrypt.checkpw(user_pass.encode(), user["password"])
                print(valid)
                return valid

    @staticmethod
    def check_pass_user_direct_in_db(login, entered_password: str):
        """Проверка соответствия пароля, смотрит в базе напрямую"""
        user_pass = entered_password
        mongoclient = pymongo.MongoClient(Backend.__connection_info)
        db = mongoclient.calendarwork
        collection = db.users
        for user in collection.find({"login": login}):
            valid = bcrypt.checkpw(user_pass.encode(), user["password"])
            print(valid)
            return valid

    def launch_session(self, login, password):
        """Запуск сессии, ввод логина и пароля, поверка данных, вызов User"""
        Backend.show_status("1")
        Backend.show_status("2")
        if not self.check_pass_user_direct_in_db(login, password):
            print(f"Введеный пароль неверный для login: {login}")
            while self.check_pass_user_direct_in_db(login, password):
                password = input(f"Попробуйте еще раз ввести верный пароль для login {login}: ")
        Backend.show_status("3")
        Backend.show_status("4")
        self.asyncload_db()
        self.get_users_from_db()
        for user in Backend._users_list:
            if login == user["login"]:
                self.launched_user = user
                self.current_user = User(login=user["login"],
                                         user_password=password,
                                         name=user["name"],
                                         job_title=user["job_title"],
                                         email=user["email"],
                                         calendars=user["calendars"],
                                         _user_id=user["_id"])
                Backend.show_status("5")
        self.choose_calendar(self.current_user.login)

    def choose_calendar(self, user_login):
        """Выбор календаря для текущей работы"""
        Backend.show_status("6")
        # print(self.connection_db_users().find_one({"login": user_login}, {"id": 0, "calendars": 1}))
        print(self.current_user.get_user_calendars())
        calendar_open_id = int(input(f"Выберите календарь, указав номер _id : "))
        calendar_open = self.connection_db_calendars().find_one({"_id": calendar_open_id})
        # print(calendar_open)
        # print(calendar_open_id, type(calendar_open_id))
        # print(self.current_user.get_identificator())

        calendar_current = Calendar(self.current_user.get_identificator(),
                                    calendar_open["name"],
                                    _id=calendar_open_id,
                                    _events=calendar_open["events"])
        Backend.show_status("7")
        calendar_current.start_calendar()
        return calendar_current

    def close_session(self):
        Backend.show_status("32")
        self.update_all()
        # self.save_users_to_db()
        # self.save_calendars_to_db()
        # self.save_events_to_db()
        # self.asyncsave_db()
        self.save_data("u")
        self.save_data("c")
        self.save_data("e")
        self.current_user = None
        Backend.show_status("18")
        Backend.show_status("19")

    def update_user(self, _id=None, new_login=None, new_hpassword=None, new_name=None, new_email=None,
                    new_job_title=None,
                    new_calendars=None):
        Backend.show_status("33")
        collection = self.connection_db_users()
        if _id is not None:
            current = {"_id": _id}
        else:
            current = {"_id": self.current_user.user_id}
        if new_login is not None:
            collection.update_one(current, {"$set": {"login": new_login}})
            collection.update_one(current, {"$set": {"identificator": "@" + new_login}})

        if new_hpassword is not None:
            collection.update_one(current, {"$set": {"password": new_hpassword}})
        if new_name is not None:
            collection.update_one(current, {"$set": {"name": new_name}})
        if new_email is not None:
            collection.update_one(current, {"$set": {"email": new_email}})
        if new_job_title is not None:
            collection.update_one(current, {"$set": {"job_title": new_job_title}})
        if new_calendars is not None:
            collection.update_one(current, {"$set": {"calendars": new_calendars}})
        self.load_from_db_users()

        Backend.show_status("34")

    def update_calendar(self, id_cal=None, new_name=None, events=None):
        Backend.show_status("33")
        collection = self.connection_db_calendars()
        current = {"_id": id_cal}
        if new_name is not None:
            collection.update_one(current, {"$set": {"name": new_name}})
        if events is not None:
            collection.update_one(current, {"$set": {"events": events}})
        self.load_from_db_calendars()

        Backend.show_status("34")

    def update_event(self, id_event=None, new_title=None, new_periodic=None, new_start=None, new_end=None,
                     new_duration=None, new_descr=None, new_members=None):
        Backend.show_status("33")
        collection = self.connection_db_events()
        current = {"_id": id_event}
        if new_title is not None:
            collection.update_one(current, {"$set": {"title": new_title}})
        if new_periodic is not None:
            collection.update_one(current, {"$set": {"periodic": new_periodic}})
        if new_start is not None:
            collection.update_one(current, {"$set": {"start_time": new_start}})
            collection.update_one(current, {"$set": {"duration": new_start}})
        if new_end is not None:
            collection.update_one(current, {"$set": {"end_time": new_end}})
            collection.update_one(current, {"$set": {"duration": new_start}})
        if new_descr is not None:
            collection.update_one(current, {"$set": {"descr": new_descr}})
        if new_members is not None:
            collection.update_one(current, {"$set": {"members": new_members}})
        self.load_from_db_events()
        Backend.show_status("34")

    def update_all(self):
        self.update_user()
        self.update_calendar()
        self.update_event()

    # Скрипт подключения Python c MongoDB
    # python -m pip install "pymongo[srv]"
    # from pymongo.mongo_client import MongoClient
    # from pymongo.server_api import ServerApi
    # uri = "mongodb+srv://krayushkin90:<password>@cluster0.dn7jino.mongodb.net/?retryWrites=true&w=majority"
    # # Create a new client and connect to the server
    # client = MongoClient(uri, server_api=ServerApi('1'))
    # # Send a ping to confirm a successful connection
    # try:
    #     client.admin.command('ping')
    #     print("Pinged your deployment. You successfully connected to MongoDB!")
    # except Exception as e:
    #     print(e)
    # Для  Compass:
    # mongodb+srv://krayushkin90:<password>@cluster0.dn7jino.mongodb.net/

    #
    # {'_id': self._user_id, 'name': self._name, 'login': self._login,
    #  'identificator': self.__identificator, 'job_title': self._job_title,
    #  'password': self._password, 'email': self._email}

    # @staticmethod
    # def save_data_event():
    #     with ((((open("events_saved_data.txt", "w", newline="") as f)))):
    #         w = csv.DictWriter(f, ["_id", "title", "periodic", "organizer", "start_time", "end_time", "descr"])
    #         w.writeheader()
    #         {'_id': self.__id, 'title': self._title, 'periodic': self._periodic,
    #          'organizer': self._organizer, 'start_time': self._start_time.strftime('%d/%m/%Y, %H:%M:%S'),
    #          'end_time': self._end_time.strftime('%d/%m/%Y, %H:%M:%S'),
    #          'descr': self._description}
    #         routs = Interface.manager.get_routs()
    #         for event in events:
    #             for r in routs[point]:
    #                 data = dict()
    #                 data["_id"],
    #                 data["title"] = r.get_points()
    #                 data["periodic"] =
    #                 data["organizer"].get_name()
    #                 data["start_time"] =
    #                 data["end_time"].get_name()
    #                 data["descr"],
    #                 data["end"] = r.get_timings()
    #                 w.writerow(data)

    # def save_data(self):
    #     with open(self.file, mode='w', newline='') as file:
    #         fieldnames = ['Login', 'Password', 'Id']
    #         writer = csv.DictWriter(file, fieldnames=fieldnames)
    #         writer.writeheader()
    #         for user in self._users:
    #             writer.writerow({'Login': user.get_name(), 'Password': user.get_password(), 'Id': user.get_id()})
    #
    # def load_data(self):
    #     try:
    #         with open(self.file, mode='r') as file:
    #             reader = csv.DictReader(file)
    #             self._users = []
    #             for row in reader:
    #                 login = row['Login']
    #                 password_hash = row['Password']
    #                 user_id = row['Id']
    #                 self._users.append(User(login, password_hash, user_id))
    #     except FileNotFoundError:
    #         pass

    # ===========Для message добавления в событие или удаление из события
    # import smtplib
    # fromaddr = "someone@some.com"
    # toaddrs = ["recipient@other.com"]
    # amount = 123.45
    # msg = f"""From: {fromaddr}
    # Pay {amount} bitcoin or else. We're watching.
    # """
    # server = smtplib.SMTP('localhost')
    # serv.sendmail(fromaddr, toaddrs, msg)
    # serv.quit()
    # ===========


if __name__ == '__main__':
    Back = Backend()
    # Для проверки добавления данных и регистрации
    # Back.register_new_user()
    # Back.register_new_user()
    # first_user = User("Buggy", "123456788q", "Ivan Borisov", "CEO", "irborisov.d.@trk.com")
    # second_user = User("Krispi", "353353535q", "Klim Gagarin", "CFO", "kgagarin@trk.com")
    # third_user = User("Dona", "asdfgh123", "Fola Brasa", "klerk", "worker@trk.com")
    # g = first_user.create_calendar()
    # g.name = "Рабочий"
    # message1 = """{
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
    # g.add_event_from_json_message(message1)

    # f = first_user.create_calendar()
    # f.name = "Личный"
    # message1 = """{
    #     "_id": 23322,
    #     "title": "Meeting CFO",
    #     "periodic": {"1": "Daily"},
    #     "organizer": "Bob",
    #     "start_time": "2024/01/18, 10:50",
    #     "end_time": "2024/01/18, 10:59",
    #     "duration": "0:09:00",
    #     "descr": "Let's do it",
    #     "members": ["@triko", "@gangsta", "@rooney", "gigig"]
    # }"""
    # f.add_event().create_from_json_message(message1)
    #
    # c = second_user.create_calendar()
    # c.name = "Рабочий"
    # message1 = """{
    #     "_id": 23,
    #     "title": "Meeting Kick-off",
    #     "periodic": {"1": "Onetime"},
    #     "organizer": "Marly",
    #     "start_time": "2024/01/22, 10:50",
    #     "end_time": "2024/01/22, 10:59",
    #     "duration": "0:09:00",
    #     "descr": "Let's go",
    #     "members": ["@triko", "@gangsta", "@rooney", "gigig", "hilo"]
    # }"""
    # c.add_event().create_from_json_message(message1)
    #
    # b = third_user.create_calendar()
    # b.name = "Private"
    # message1 = """{
    #     "_id": 1111,
    #     "title": "Meeting Celebration",
    #     "periodic": {"1": "Onetime"},
    #     "organizer": "Katy",
    #     "start_time": "2024/01/22, 10:50",
    #     "end_time": "2024/01/22, 10:59",
    #     "duration": "0:09:00",
    #     "descr": "Let's go",
    #     "members": ["@triko", "@gangsta", "@rooney", "gigig", "hilo"]
    # }"""
    # b.add_event().create_from_json_message(message1)
    # print(first_user)
    # print(second_user)
    # print(third_user)

    # print(g, "Календарь")
    # first_user.
    # Back.read_user_from_class(first_user)
    # Back.read_user_from(second_user)
    # Back.read_user_from(third_user)
    # print(Back.get_users(), "written")
    # Back.save_data("u")
    # Back.save_from_csv_to_db()
    # first_user.to_dict_db()
    # # print(first_user)
    # second_user.to_dict_db()
    # # print(second_user)
    # third_user.to_dict_db()
    # # print(third_user)
    # print(User._users)
    # print(User.users_db)
    # print(User.calendars_db)
    # print(g.events_to_db)
    # print(g.__dict__)
    # Back.save_users_to_db()
    # Back.save_calendars_to_db()
    # Back.save_events_to_db()
    # Back.connection_db()
    # print(Back.get_users_from_db())

    # Back.set_index_db()

    # print(Back.asyncconnect_db())
    print(Back._users_list)
    # print(Back.users_db)

    # Проверка загрузки данных
    # Back.load_from_db_users()
    # Back.load_from_db_calendars()
    # Back.load_from_db_events()
    # Back.asyncload_db()

    # # Проверка проверки пароля
    # Back.check_pass_user("Buggy", "123456788q")
    # Back.check_pass_user("Buggy", "123456788q2222")
    # Back.check_pass_user_direct_in_db("Krispi", "353353535q")
    # Back.check_pass_user_direct_in_db("Krispi", "353353535q222")

    # Back.launch_session("Buggy", "123456788q")
    # Проверка update
    # Back.update_user(_id=2, new_login="KurlaKu")

    # Back.find_user_by_login("Dona")
    Back.connection_db_check()
