class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.interested_trip_ids = []

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def interested_trip_ids(self):
        return self._interested_trip_ids

    @interested_trip_ids.setter
    def interested_trip_ids(self, value):
        self._interested_trip_ids = value

    def add_interested_trip(self, trip_id):
        self.interested_trip_ids.append(trip_id)

    def __str__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Interested Trip IDs: {self.interested_trip_ids}"
