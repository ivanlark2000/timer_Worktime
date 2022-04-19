# -*- coding: utf-8 -*-
import time
import psutil
from datetime import datetime
from pynput.mouse import Controller
from pynput import keyboard


def check_device():
    """Проверяет общую активность устройств в случае
    активности выводит True,
    если девайсы не используются выводит False """
    def check_mouse():
        """Проверяет активность мыши и возвращает
        True или False"""
        mouse = Controller()
        check = mouse.position
        time.sleep(30)
        if mouse.position != check:
            return True
        else:
            return False

    def check_keyBoard():
        """Проверяет активность клавиатуры
        и возвращает True или False"""
        with keyboard.Events() as events:
            event = events.get(5.0)
            if event is None:
                return False
            else:
                return True

    if check_mouse():
        return True
    elif check_keyBoard():
        return True
    else:
        return False


def check_py():
    """Проверяем активность процесса пйчарма"""
    for proc in psutil.process_iter():
        if proc.name() == 'pycharm.sh':
            return True
        else:
            continue


def check_video():
    """Проверяем активность процесса видеоплейера"""
    try:
        for proc in psutil.process_iter():
            if proc.name() == 'totem':
                for totem in proc.as_dict()['open_files']:
                    path = totem.path
                    if path.startswith('/home/ivan/Видео/Лекции') \
                            and proc.cpu_percent(interval=1) > 0:
                        return True
        return False
    except Exception:
        return False


def get_time_proc():
    """Записывает историю по работе юзера в приложении"""
    while True:
        time_end = time_start = datetime.now()
        while check_py():
            while check_device():
                time_end = datetime.now()
            if time_end > time_start:
                result = time_end - time_start
                print(f'Работал в пайчарме {result.seconds}')


def get_time_video():
    """Записывает историю при просмотре обучающего
    видео юзером"""
    while True:
        time.sleep(1)
        time_end = time_start = datetime.now()
        while check_video():
            time.sleep(1)
            time_end = datetime.now()
        if time_end > time_start:
            result = time_end - time_start
            print(f'Смотрел обучающий видос {result.seconds} секунд')


def main():
    while True:
        if check_device():
            print('Приступайте к работе')
        else:
            print('Молодец! Вы успешно работаете.')


if __name__ == '__main__':
    main()
