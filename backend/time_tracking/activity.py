class Activity():
    def __init__(self, name):
        self.name = name
        self.time_entries = []

    def add_time_entry(self, time_entry):
        self.time_entries.append(time_entry)

    def time_entries_to_json(self,):
        return [time_entry.serialize() for time_entry in self.time_entries]

    def serialize(self):
        return {
            'name': self.name,
            'time_entries': self.time_entries_to_json()
        }

    def __str__(self):
        return f'{self.serialize()}'
