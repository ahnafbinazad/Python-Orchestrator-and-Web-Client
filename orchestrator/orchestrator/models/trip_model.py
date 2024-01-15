class Trip:
    def __init__(self, trip_id, user_id, username, location, date, weather=None):
        self.trip_id = trip_id
        self.user_id = user_id
        self.username = username
        self.location = location
        self.date = date
        self.weather = weather

    @property
    def trip_id(self):
        return self._trip_id

    @trip_id.setter
    def trip_id(self, value):
        self._trip_id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        self._weather = value

    def __str__(self):
        return f"Trip ID: {self.trip_id}, User ID: {self.user_id}, Username: {self.username}, Location: {self.location}, Date: {self.date}, Weather: {self.weather}"

