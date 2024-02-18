"""
Пользователь - имеет логин и пароль, а так же календарь.
у пользователя есть итендифекатор начинающийся с @
"""
import pymongo
import bcrypt
import json
from Calendar import Calendar


class User:
    __identificators = []
    __id = 0
    __id_list = []
    __hash_and_salts = []
    fieldnames_user = ['_id', 'name', 'login', 'identificator', 'job_title', 'password', 'email', 'calendars']
    file_users = "users_data.csv"
    _calendars = dict()
    calendars_db = list()
    _users = list()
    users_db = list()
    __connection_info = "mongodb+srv://krayushkin90:11171990@cluster0.dn7jino.mongodb.net/"

    def __init__(self, login, user_password, name=None, job_title=None, email=None, calendars=None, _user_id=None):
        self._login = login
        self._password = user_password
        self._name = name
        self._email = email
        self._job_title = job_title
        self._identificator = '@' + self._login
        self.__class__.__identificators.append(self._identificator)
        self.__class__.__id = self.__class__.__id + 1
        self._user_id = self.__class__.__id
        self.__class__.__id_list.append(self.__class__.__id)
        self.__hash_and_salted_pass = ''
        self.gen_hashed_pass()
        self._user_dict = dict()
        self._user_calendars = dict()
        self._user_calendars_list = list()
        self.id_calendars = []
        self.opened_calendar = None

    @property
    def name(self):
        """Возвращает имя user"""
        return self._name

    @name.setter
    def name(self, new_name):
        """Изменяет имя user  ====================Добавить update базы и сессии"""
        self._name = new_name

    @property
    def login(self):
        """Возвращает login user"""
        return self._login

    @login.setter
    def login(self, new_login):
        """Изменяет login user ====================Добавить update базы и сессии"""
        self._login = new_login
        self.change_identificator()

    @property
    def job_title(self):
        """Возвращает должность user"""
        return self._job_title

    @job_title.setter
    def job_title(self, new_job_title):
        """Изменяет должность user  ====================Добавить update базы и сессии"""
        self._job_title = new_job_title

    @property
    def user_id(self):
        """Возвращает id user"""
        return self._user_id

    def get_identificator(self):
        """Возвращает идентификатор user"""
        return self._identificator

    @property
    def email(self):
        """Возвращает email адрес user"""
        return self._email

    @email.setter
    def email(self, new_email):
        """Изменяет email адрес user   ====================Добавить update базы и сессии"""
        self._email = new_email

    @email.deleter
    def email(self):
        """Удаляет email адрес user  ====================Добавить update базы и сессии"""
        self._email = ""

    # def change_name(self, new_name):
    #     self._name = new_name
    #     return self._name
    #
    # def change_login(self, new_login):
    #     self._login = new_login
    #     self.change_identificator()
    #     return self._login

    # def change_job_title(self, new_job_title):
    #     self._job_title = new_job_title
    #     return self._job_title

    def change_identificator(self):
        """Корректирует идентификатор после изменения login ====================Добавить update базы и сессии"""
        self._identificator = '@' + self._login
        return self._identificator

    def __str__(self):
        """Текстовое представление экземпляров User"""
        return f'User: {self.get_identificator()}: Name: {self.name}, ID: {self.user_id}, Login: {self.login}, Job title: {self.job_title}, password: {self.__hash_and_salted_pass}'

    def __repr__(self):
        """Представление экземпляров User для debug"""
        return f'User: {self.get_identificator()}, Name: {self.name}, ID: {self.user_id}, Login: {self.login}, Job title: {self.job_title}'

    def __hash__(self):
        """Хэш пароля - не используется, пароль хэшируется с подсолом в другом методе"""
        return hash(self._password)

    def connection_db(self):
        """Вставляет экземпляр User после команды сохранения или при закрытии сессии"""
        try:
            client = pymongo.MongoClient("mongodb+srv://krayushkin90:11171990@cluster0.dn7jino.mongodb.net/")
            db = client.users
            coll = db.new_users
            dict_calendars = []
            for calendar in self.__class__._calendars:
                dict_calendars.append(calendar.calendar_to_dict)
            self._user_dict['calendars'] = dict_calendars
            coll.insert_one(
                {"id": self.user_id, "name": self.name, "login": self.login, "identificator": self.get_identificator(),
                 "job_title": self.job_title, "password": self.__hash_and_salted_pass, "email": self._email,
                 "calendars": self._user_dict['calendars']})

        except ConnectionError:
            print(f'Соединение с БД не достигнуто')

    @staticmethod
    def read_all_users_db():
        """Считывает users из базы данных, например при инициализации ============Добавить update users_db"""
        try:
            client = pymongo.MongoClient(User.__connection_info)
            db = client.calendarwork
            coll = db.users
            for value in coll.find():
                print(f'Считано{value}')
                User.users_db.append(value)
        except ConnectionError:
            print(f'Соединение с БД не достигнуто')

    def gen_hashed_pass(self):
        """Хэширование и засол пароля user ====================Добавить update базы и сессии"""
        # password = userInput
        self.__hash_and_salted_pass = bcrypt.hashpw(self._password.encode(), bcrypt.gensalt())
        self.__class__.__hash_and_salts.append(self.__hash_and_salted_pass)
        # save "__hash_and_salted_pass" in data base

    def check_pass(self, entered_password: str):
        """Проверка соответствия пароля ================добавить из БД"""
        # To check:
        # password = userInput
        # user_pass = str(input("Enter "))  # - для проверки на отладке
        user_pass = entered_password
        valid = bcrypt.checkpw(user_pass.encode(), self.__hash_and_salted_pass)
        print(valid)

    def create_from_json_message(self, json_message):
        """Создает User из переменной текстового формата json ====================Добавить календари и добавление в БД и сессию"""
        import json
        data_json = json.loads(json_message)
        print(data_json)  # закомментировать после отладки
        self._user_id = data_json["_id"]
        self._name = data_json["name"]
        self._login = data_json["login"]
        self._identificator = data_json["identificator"]
        self._job_title = data_json["job_title"]
        self._password = data_json[
            "password"]  # будем считать пока что это стандартный пароль, который user должен поменять на свой
        self._email = data_json["email"]
        return self

    def create_from_json_file(self, json_path):
        """Создает User из файла с json текстом ====================Добавить календари и добавление в БД и сессию"""

        with open(json_path, 'r') as file_from_path:
            data_json = json.load(file_from_path)
            print(data_json)
            self._user_id = data_json["_id"]
            self._name = data_json["name"]
            self._login = data_json["login"]
            self._identificator = data_json["identificator"]
            self._job_title = data_json["job_title"]
            self._password = data_json[
                "password"]  # будем считать пока что это стандартный пароль, который user должен поменять на свой
            self._email = data_json["email"]
            # print(self)  # закомментировать после отладки

    def save_as_json_var(self):
        """Сохраняет User в переменную формата json)    ====================Добавить календари"""
        data_user = {'_id': self._user_id, 'name': self._name, 'login': self._login,
                     'identificator': self._identificator, 'job_title': self._job_title,
                     'password': self._password, 'email': self._email}
        json_mes = json.dumps(data_user, indent=4)
        return json_mes

    def save_as_json_file(self):
        """Сохраняет User в файл формата json)   ====================Добавить календари"""
        data_user = {'_id': self._user_id, 'name': self._name, 'login': self._login,
                     'identificator': self._identificator, 'job_title': self._job_title,
                     'password': self._password, 'email': self._email}
        with open(str(self._user_id) + "-" + str(self._name) + ' -User.json', 'w') as file_json_from_user:
            json.dump(data_user, file_json_from_user, indent=4, ensure_ascii=True)

    def to_dict(self):
        """Преобразует в словарь user c календарями и их событиями"""
        self._user_dict['_id'] = self._user_id
        self._user_dict['name'] = self._name
        self._user_dict['login'] = self._login
        self._user_dict['identificator'] = self._identificator
        self._user_dict['job_title'] = self._job_title
        self._user_dict['password'] = self.__hash_and_salted_pass
        self._user_dict['email'] = self._email
        dict_calendars = []
        for calendar in self.__class__._calendars.values():
            dict_calendars.append(calendar.to_dict())
        self._user_dict['calendars'] = dict_calendars
        # self._user_calendars['calendars'] = self.__class__._calendars
        self.__class__._users.append(self._user_dict)

        return self._user_dict

    def to_dict_db(self):
        """Преобразует в словарь user c id календарями для связи коллекций БД"""
        self._user_dict['_id'] = self._user_id
        self._user_dict['name'] = self._name
        self._user_dict['login'] = self._login
        self._user_dict['identificator'] = self._identificator
        self._user_dict['job_title'] = self._job_title
        self._user_dict['password'] = self.__hash_and_salted_pass
        self._user_dict['email'] = self._email

        self._user_dict['calendars'] = self.id_calendars
        self.__class__.users_db.append(self._user_dict)

        # self._user_calendars['calendars'] = self.__class__._calendars

        return self._user_dict

    def create_calendar(self):
        """Создание календаря экземпляром user  =========Добавить update БД и сессии"""

        new_calendar = Calendar("", "")
        new_calendar.name = input("Введите имя календаря: ")
        new_calendar._owner = self.login
        new_calendar._events = list()
        self.__class__._calendars[new_calendar.get_id()] = new_calendar
        self._user_calendars[new_calendar.get_id()] = new_calendar

        print(self.__class__._calendars)  # - закомментировать после отладки
        # new_user.save_as_json_file()
        self.id_calendars.append(new_calendar.get_id())  # ====================================
        self.calendars_db.append(new_calendar.to_dict_db())  # ====================================
        self._user_calendars_list.append(new_calendar.to_dict_db())
        for user in self.__class__.users_db:
            if user["_id"] == self._user_id:
                user["calendars"].append(new_calendar.get_id())
        return new_calendar

    def add_calendar(self, new):
        """Добавление календаря экземпляром user  =========Добавить update БД и сессии"""
        new_calendar = Calendar("", "")
        new_calendar._id = new.get_id()
        new_calendar.name = new.name
        new_calendar._owner = self.login
        new_calendar._events = new.get_events_dict_self()
        self.__class__._calendars[new_calendar.get_id()] = new_calendar
        self._user_calendars[new_calendar.get_id()] = new_calendar
        self.id_calendars.append(new_calendar._id)  # ==================================
        self.calendars_db.append(new_calendar.to_dict_db())
        self._user_calendars_list.append(new_calendar.to_dict_db())
        # print(self.__class__._calendars)  # - закомментировать после отладки
        # new_user.save_as_json_file()
        for user in self.__class__.users_db:
            if user["_id"] == self._user_id:
                user["calendars"].append(new_calendar.get_id())
        return new_calendar

    def get_user_calendars(self):
        """Возвращает календари экземпляра user"""
        return self._user_calendars

    @staticmethod
    def get_calendars():
        """Возвращает календари класса User"""
        return User._calendars

    def find_calendar_by_owner(self, owner):
        """Находит календари по владельцу"""
        found_calendars = []
        for calendar in self._user_calendars_list:
            if calendar['owner'] == owner:
                found_calendars.append(calendar)
        print(found_calendars)
        return found_calendars

    def m_find_calendar_by_owner(self, owner):
        """Находит календари по владельцу"""
        found_calendars = []
        for calendar in self._user_calendars.values():
            if calendar.get_owner() == owner:
                found_calendars.append(calendar)
        print(found_calendars)
        return found_calendars

    def find_calendar_by_id(self, id_calendar):
        """Находит календари по id"""

        for calendar in self._user_calendars_list:
            if int(calendar['_id']) == int(id_calendar):
                print(calendar)
                return calendar

    def m_find_calendar_by_id(self, id_calendar):
        """Находит календари по id"""

        for calendar in self._user_calendars.values():
            if calendar.get_id() == int(id_calendar):
                return calendar

    def open_calendar(self):
        """Распаковывает календарь для дальнейшей работы"""
        calendars = self.find_calendar_by_owner(self.login)
        # select = input(f"Выберите id календаря для дальнейших действий: ")
        selected_calendar = None
        select = 0
        while selected_calendar is None:
            select = input(f"Выберите id календаря для дальнейших действий или нажмите '0' для выхода: ")
            if int(select) == 0:
                return
            selected_calendar = self.find_calendar_by_id(select)
        self.opened_calendar = Calendar(name=selected_calendar['name'],
                                        owner=selected_calendar['owner'],
                                        _id=selected_calendar['_id'],
                                        _events=selected_calendar['events'])
        return self.opened_calendar

    def m_open_calendar(self):
        """Распаковывает календарь для дальнейшей работы"""
        calendars = self.m_find_calendar_by_owner(self.login)
        # select = input(f"Выберите id календаря для дальнейших действий: ")
        selected_calendar = None
        select = 0
        while selected_calendar is None:
            select = input(f"Выберите id календаря для дальнейших действий или нажмите '0' для выхода: ")
            if int(select) == 0:
                return
            selected_calendar = self.m_find_calendar_by_id(select)
            print(selected_calendar)
        self.opened_calendar = Calendar(name=selected_calendar.name,
                                        owner=selected_calendar.get_owner(),
                                        _id=selected_calendar.get_id(),
                                        _events=selected_calendar.get_events_dict_self())
        return self.opened_calendar

    def update_user(self):
        """Подключается к БД и обновляет user в базе данных"""
        try:
            mongoclient = pymongo.MongoClient(User.__connection_info)
            db = mongoclient.calendarwork
            collection = db.users
            collection.insert_many(User.calendars_db)

        except ConnectionError:
            print(f'Соединение с БД не достигнуто')


if __name__ == '__main__':
    first_user = User("Batman", "123456788q", "Dmitriy Blinov", "accountant", "blinov.d.@lol.com")
    second_user = User("Pacman", "353353535q", "Vasiliy Krasin", "engineer", "krasin.v.@lol.com")
    third_user = User("Mona", "asdfgh123", "Anna Mosina", "assistant", "mosina.a.@lol.com")
    f = first_user.create_calendar()
    f1 = first_user.create_calendar()
    s = second_user.create_calendar()
    t = third_user.create_calendar()
    message1 = """{
        "_id": 1,
        "title": "Meeting CEO",
        "periodic": {"1": "Monthly"},
        "organizer": "Batman",
        "start_time": "2024/01/18, 00:50",
        "end_time": "2024/01/18, 00:59",
        "duration": "0:09:00",
        "descr": "Let's do it quickly",
        "members": ["@triko", "@gangsta", "@rooney"]
    }"""
    message2 = """{
        "_id": 2,
        "title": "Meeting Celebrating",
        "periodic": {"1": "Weekly"},
        "organizer": "Pacman",
        "start_time": "2024/01/18, 00:50",
        "end_time": "2024/01/18, 00:59",
        "duration": "0:09:00",
        "descr": "Let's do it quickly",
        "members": ["@triko", "@gangsta", "@rooney"]
    }"""
    message3 = """{
        "_id": 3,
        "title": "Meeting",
        "periodic": {"1": "Monthly"},
        "organizer": "Mona",
        "start_time": "2024/01/18, 00:50",
        "end_time": "2024/01/18, 00:59",
        "duration": "0:09:00",
        "descr": "Let's do it quickly",
        "members": ["@triko", "@gangsta", "@rooney"]
    }"""
    f.add_event_from_json_message(message1)
    s.add_event_from_json_message(message2)
    t.add_event_from_json_message(message3)
    first_user.to_dict_db()
    print(first_user)
    second_user.to_dict_db()
    print(second_user)
    third_user.to_dict_db()
    print(third_user)
    print(User._users)
    print(first_user._user_calendars)
    print(second_user._user_calendars)
    print(third_user._user_calendars)
    first_user.get_user_calendars()
    second_user.get_user_calendars()
    third_user.get_user_calendars()
    print(f.__dict__)
    print(first_user.__dict__)
    print(User.users_db)
    print(first_user.id_calendars)
    print(first_user.calendars_db)
    # print(first_user._user_calendars_list)
    # first_user.find_calendar_by_id(2)
    # first_user.find_calendar_by_owner('Batman')
    # first_user.m_find_calendar_by_owner('Batman')
    # print(first_user.open_calendar())
    print(first_user.m_open_calendar())
    # print(first_user.m_find_calendar_by_id(2))

    # ====================================================
    # first_user.check_auth()
    # m = first_user.save_as_json_var()
    # print(m)
    # new_user = User("", "")
    # new_user.create_from_json_message(m)
    # print(new_user)
    # new_user.save_as_json_file()
    # one_more = User("", "")
    # one_more.create_from_json_file("1-Dmitriy Blinov -User.json")
    # print(one_more, 'this is a new one')
    # =============Проверка связи================
    # first_user.connection_db()
    # second_user.connection_db()
    # third_user.connection_db()
    # User.read_all_users_db()

    # ==================================================================================================
    # # Хэширование пароля
    # import bcrypt
    #
    # password = input()
    # hashAndSalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # # save "hashAndSalt" in data base
    # # To check:
    # # password = userInput
    # valid = bcrypt.checkpw(password.encode(), hashAndSalt)
