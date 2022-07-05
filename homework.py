
from typing import Dict, Type
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MASSAGE = (
        "Тип тренировки: {}; "
        "Длительность: {:.3f} ч.; "
        "Дистанция: {:.3f} км; "
        "Ср. скорость: {:.3f} км/ч; "
        "Потрачено ккал: {:.3f}."
    )

    def get_message(self) -> str:
        data = asdict(self)
        return self.MASSAGE.format(*data.values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_MIN: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('переопределите метод в дочерних классах')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""
    cf_run_1: int = 18
    cf_run_2: int = 20

    def get_spent_calories(self) -> float:
        return (
            (self.cf_run_1 * self.get_mean_speed() - self.cf_run_2)
            * self.weight / self.M_IN_KM * self.duration * self.M_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_sw_1: float = 0.035
    cf_sw_2: int = 2
    cf_sw_3: float = 0.029

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.cf_sw_1 * self.weight + (self.get_mean_speed()
             ** self.cf_sw_2 // self.height) * self.cf_sw_3 * self.weight)
            * self.duration * self.M_IN_MIN
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    cf_sm_1: float = 1.1
    cf_sm_2: int = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.cf_sm_1)
            * self.cf_sm_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        training: Dict[str, Type[Training]] = {
            'SWM': Swimming,
            'RUN': Running,
            'WLK': SportsWalking
        }
        return training[workout_type](*data)
    except KeyError:
        raise "Тренировка не найдена"


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Точка входа."""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        # ('FOO', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
