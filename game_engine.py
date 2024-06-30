# -*- coding: utf-8 -*-
import csv
import json
import datetime
import re
from decimal import Decimal

REMAINING_TIME = '1234567890.0987654321'
FIELD_NAMES = ['current_location', 'current_experience', 'current_date']


class Game:
    """
    Консольная игра с 'переходами' из комнаты в комнату, где есть монстры и двери в другие комнаты
    Каждый 'переход' снимает определенное количество времени
    Каждое сражение с монстрами так же снимает определенное количество времени и даёт определенное количество опыта
    Карта записана в файле map_for_game.json
    """

    def __init__(self):
        self.remaining_time = REMAINING_TIME
        self.field_names = FIELD_NAMES
        self.experience = Decimal(0)
        self.time = Decimal(0)
        self.re_experience = r'exp(\d+)'
        self.re_time = r'tm(\d.+)'
        self.exp_for_win = Decimal(280)
        self.map = None
        self.object_in_location = []
        self.location_name = []
        self.writer = None
        self.result_the_game = []
        self.mobs = []
        self.location_to_move = []

    def read_map(self):
        """
        Считывание карты

        :return: None
        """
        with open('map_for_game.json', mode='r') as game_map:
            self.map = json.load(game_map)
            self.object_in_location.extend(self.map['Location_0_tm0'])
            self.location_name.extend(self.map.keys())

    def create_file(self):
        """
        Создание файла результата

        :return: None
        """
        with open('game_result.csv', mode='w', newline='') as created_file:
            self.writer = csv.writer(created_file)
            self.writer.writerow(self.field_names)

    def write_result_in_file(self):
        """
        Запись результатов в файл результата

        :return: None
        """
        with open('game_result.csv', mode='a', newline='') as resulted_file:
            self.writer = csv.writer(resulted_file)
            self.result_the_game.extend([self.location_name[0], self.experience, datetime.datetime.now()])
            self.writer.writerow(self.result_the_game)

    def create_location(self):
        """
        Создание локации

        :return: None
        """
        for object in self.object_in_location:
            if isinstance(object, str):
                self.mobs.append(object)
            elif isinstance(object, dict):
                self.location_to_move.append(list(object.keys())[0])

    def print(self):
        """
        Отображение текущей позиции в терминале

        :return: None
        """
        print(f'\nВы находитесь в {self.location_name[0]}\n'
              f'У вас {self.experience} опыта и осталось {datetime.timedelta(seconds=float(self.remaining_time))}\n'
              f'Прошло уже {datetime.timedelta(seconds=float(self.time))}\n'
              f'Внутри вы видите:')
        for mob in self.mobs:
            print(f'-- Монстра {mob}')
        for location in self.location_to_move:
            print(f'-- Вход в локацию {location}')

    def user_input(self):
        """
        Реализация взаимодействия с пользователем

        :return: вывод текущего состояния в терминал
        """
        while True:
            self.print()
            choice = input('Выберите действие: \n'
                           '1. Атаковать монстра\n'
                           '2. Перейти в другую локацию\n'
                           '3. Выйти из игры\n'
                           'Ваш выбор: ')
            if choice == '1':
                if not self.mobs:
                    print('Нет монстров для атаки!')
                    continue
                else:
                    for index, monster in enumerate(self.mobs):
                        print(f'-- {index + 1}. {monster[1]}')
                    selected_mob = input('Какого монстра выбираете?: ')
                    if selected_mob.isalpha():
                        print('Необходимо вводить цифры!')
                        continue
                    elif int(selected_mob) > len(self.mobs):
                        print('Такого монстра не существует!')
                        continue
                    else:
                        selected_mob = self.mobs[int(selected_mob) - 1]
                        plus_exp = re.search(self.re_experience, selected_mob)
                        self.experience += Decimal(plus_exp[1])
                        plus_time = re.search(self.re_time, selected_mob)
                        self.time += Decimal(plus_time[1])
            elif choice == '2':