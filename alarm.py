from functools import total_ordering

@total_ordering
class Alarm:
    def __init__(self, level, alarmType):
        self.level = level
        self.alarmType = alarmType
    def __lt__(self, other):
        return (self.level, self.alarmType) < (other.level, other.alarmType)
    def __eq__(self, other):
        return self.level == other.level and self.alarmType == other.alarmType
    def __str__(self):
        return f'{self.alarmType} {self.level}'
    def __repr__(self):
        return f'Alarm({self.level}, {self.alarmType})'
    def serialize(self):
        return {'level': self.level,'alarmType': self.alarmType}
    @classmethod
    def deserializer(cls, obj):
        return cls(obj['level'], obj['alarmType'])
