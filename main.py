# -*- coding: utf-8 -*-
import time
import psutil
import threading
from datetime import datetime
from openpyxl.styles import Alignment, Font
from openpyxl import load_workbook
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
        time.sleep(2)
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
        time.sleep(2)
        while check_py():
            time_end = time_start = datetime.now()
            time.sleep(2)
            while check_device():
                time.sleep(30)
                time_end = datetime.now()
            if time_end > time_start and (time_end.second - time_start.second) > 5:
                result = time_end - time_start
                print(f'Работал в пайчарме {result.seconds}')
                making_note(
                    day=time_end.day,
                    full_data=time_end.date(),
                    time_of_start=time_start.time(),
                    time_of_end=time_end.time(),
                    proc='paycharm',
                    second=result.seconds
                    )


def get_time_video():
    """Записывает историю при просмотре обучающего
    видео юзером"""
    while True:
        time.sleep(1)
        time_end = time_start = datetime.now()
        while check_video():
            time.sleep(1)
            time_end = datetime.now()
        if time_end > time_start and (time_end.second - time_start.second) > 5:
            result = time_end - time_start
            print(f'Смотрел обучающий видос {result.seconds} секунд')
            making_note(
                day=time_end.day,
                full_data=time_end.date(),
                time_of_start=time_start.time(),
                time_of_end=time_end.time(),
                proc='watch_video',
                second=result.seconds
            )


def making_note(day, full_data, time_of_start, time_of_end, proc, second, thins=None, wb=None):
    """Выполняет запись в таблицу XL
    :param: Day
    :param: full_Data
    :param: time_start
    :param: time_end
    :param: second
    """
    filename = 'timer.xlsx'
    font = Font(
        name='Calibri',
        size=20,
        bold=True,
        italic=False,
        strike=False,
        color='FF000000'
    )
    alignment = Alignment(
        horizontal='general',
        vertical='center',
        text_rotation=0,
        wrap_text=False,
        shrink_to_fit=False,
        indent=0
    )

    wb = load_workbook(filename, read_only=False, keep_links=True, keep_vba=False)
    sheet = str(datetime.now().month)
    try:
        ws = wb[sheet]
        ws.append([day, full_data, time_of_start, time_of_end, proc, second])
    except Exception:
        ws = wb.create_sheet(sheet)
        ws.append(['DAY', 'FULL_DATA', 'TIME_OF_START', 'TIME_OF_END', 'PROC', 'SECOND'])
        ws.append([day, full_data, time_of_start, time_of_end, proc, second])
        columns = ['A', 'B', 'C', 'D', 'E', 'F']
        for column in columns:
            col = ws.column_dimensions[column]
            col.width = 35
            col.alignment = Alignment(horizontal='center')
        row = ws.row_dimensions[1]
        row.font = font
        row.height = 25
        row.alignment = alignment
    finally:
        wb.save(filename)
        wb.close()


def main():
    task = threading.Thread(target=get_time_video)
    task.start()
    get_time_proc()


if __name__ == '__main__':
    main()