from .rpg_exceptions import GameObject
from ..game.utils import load_datas, file_paths
from ..game.language_manager import status_dict

class Status(GameObject) :
    nb_status = 0
    def __init__(self, name, reversible = False, once = False, duration = -1, strengh = 1, idu = 0, applied = 0):
        Status.nb_status +=1
        self.id = Status.nb_status*100 if idu == 0 else idu
        super().__init__(name if strengh == 1 else self._set_strname(name, strengh))
        self.status = name
        self.duration = duration
        self.strengh = strengh
        self.effect, self.rate, self.buff = self._set_effect_rate_buff()
        self.reversible = reversible
        self.once = once
        self.applied = applied

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _set_strname(name, strengh):
        if strengh < 1:
            return f"{status_dict['status.strengh.slight']} {name}"
        else:
            return f"{status_dict['status.strengh.serious']} {name}"

    def _set_effect_rate_buff(self):
        status_table = load_datas(file_paths['status'])['status_table']
        for stat in status_table :
            if status_dict[stat['status']] == self.status :
                return stat['effect'], stat['rate']*self.strengh, stat['type']

    def get_status_effect(self) :
        if self.once and self.applied :
            return False, False
        elif self.duration != 0 :
            self.duration -= 1
            return self.effect, self.rate
        else :
            return False, False

    def reverse_effect(self):
        if self.reversible :
            return self.effect, self.applied
        else :
            return False, False

    def apply_effect(self, value):
        self.applied += value

    def to_dict(self):
        return {
            "class" : self.__class__.__name__,
            "name": self.status,
            "duration": self.duration,
            "strengh": self.strengh,
            "idu" : self.id,
            "reversible" : self.reversible,
            "once" : self.once,
            "applied" : self.applied
        }

    @staticmethod
    def from_dict(data) :
        class_name = data['class']
        status_attributes = {k: v for k, v in data.items() if k != 'class'}
        return STATUS_CLASSES[class_name](**status_attributes)

    def __hash__(self):
        """
        Defines an hash to the object.
        :return: object's name to garanty the object's hash
        """
        return hash(self.id)

    def __eq__(self, other):
        """
        Defines how 2 objects of the class can be considered as equals.
        :param other: the class of any object to compare
        :return: True if both objects are the same class and the same id, else false
        """
        return isinstance(other, Status) and self.id == other.id


STATUS_CLASSES = {
    "Status" : Status,
}