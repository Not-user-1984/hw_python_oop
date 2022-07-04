from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.distance = distance
        self.duration = duration
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_MIN = 60

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
        pass

    def get__info_name(self) -> str:
        """Получить название тренировки."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.get__info_name(),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_cal_1 = 18
    coeff_cal_2 = 20

    def get__info_name(self) -> str:
        """Получить название тренировки."""
        return 'Running'

    def get_spent_calories(self) -> float:
        return ((self.coeff_cal_1 * self.get_mean_speed() - self.coeff_cal_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.M_IN_MIN
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_1: float = 0.035
    coeff_2: int = 2
    coeff_3: float = 0.029

    def get__info_name(self) -> str:
        """Получить название тренировки."""
        return 'SportsWalking'

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.coeff_1
                * self.weight
                + (self.get_mean_speed()
                 ** self.coeff_2
                 // self.height)
                * self.coeff_3
                * self.weight)
                * self.duration
                * self.M_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_1_: float = 1.1
    coeff_2_: int = 2
    LEN_STEP: float = 1.38

    def get__info_name(self) -> str:
        """Получить название тренировки."""
        return 'Swimming'

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
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.coeff_1_)
            * self.coeff_2_ * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_training: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    return dict_training[workout_type](*data)


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
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
