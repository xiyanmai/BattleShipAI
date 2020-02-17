import enum
import random


class Orientation(enum.Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'

    @staticmethod
    def from_string(str_orientation: str) -> "Orientation":
        str_orientation = str_orientation.lower().strip()
        if any(letter.isspace() for letter in str_orientation):
            raise ValueError(f'{str_orientation} does not represent an Orientation')
        for ori in Orientation:
            if ori.value.startswith(str_orientation):
                return ori
        raise ValueError(f'{str_orientation} does not represent an Orientation')

    @staticmethod
    def random_orientation() -> "Orientation":

        # Need help here, can not randomly choose from enum
        ori_choice = random.choice([0, 1])
        ori = Orientation[ori_choice]
        return ori


