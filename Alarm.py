from functools import total_ordering


@total_ordering
class Alarm:
    def __init__(self, level, type):
        self.level = level
        self.type = type
    def __lt__(self, other):
        return (self.level, self.type) < (other.level, other.type)
    def __eq__(self, other):
        return self.level == other.level and self.type == other.type
    def __str__(self):
        return f'{self.type} {self.level}'
    def __repr__(self):
        return f'Alarm({self.level}, {self.type})'
    def serialize(self):
        return {'level': self.level,'type': self.type}
    @classmethod
    def deserializer(cls, obj):
        return cls(obj['level'], obj['type'])