import os
import argparse

parser = argparse.ArgumentParser(description='A tutorial of argparse')
parser.add_argument('-n', '--name', nargs='?', default='Некто', help="Вот твоё имя")
parser.add_argument('-p', '--path', help="Вот путь к твоему файлу")
parser.add_argument('-nQ', '--noQ', action="store_true", help="У матросов, как грится, нет вопросов")
args = parser.parse_args()
print(f'Привет {args.name}!')
print(args)

if os.path.exists(args.path):
    if args.noQ:
        os.remove(args.path)
        exit(0)
    else:
        ag = input(f'\n{args.name}, ты хочешь удалить зис файл??? ').capitalize()
        if ag[0] == 'Д':
            os.remove(args.path)
        else:
            print('Ладненько, не двигаюсь...')
else:
    print("\nУверен,что он в этом измерении?..")