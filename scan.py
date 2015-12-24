#!/usr/bin/python
# -*- coding: utf-8 -*-

#Модули
import requests;
import multiprocessing;
import queue;
import time;
import argparse;
import random;

#Эту функцию юзают потоки, передаем номер потока, очередь, и урл шо сканим
def Scan(i, DirList, url, agent):
	#Бэзконечный цикл
	while True:
		#Небольшая случайная пауза
		time.sleep(random.randint(0, 3));
		#Если очередь пуста то
		if (DirList.empty() == True):
			#Пишем что такой поток закончил
			print ('Thread %i: Done, exiting...' % i);
			#Обрываем цикл
			break;
		#Берем из очереди диру или файл
		Dir = DirList.get();
		#Заголовки
		headers = {'User-Agent': 'none',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language':'en-US,en;q=0.5'}
		#Берем случайный юзерагент
		headers['User-Agent'] = random.choice(agent);
		#Делаем запрос, обрезая символ переноса строки +заголовки
		r = requests.get(url + Dir[:-1], headers=headers);
		#Если файл или дира есть то
		if (r.status_code == requests.codes.ok):
			#Выводим их
			print ("%s - [OK] -Thread %i" % (url + Dir[:-1], i));
			#Ждем завершения
		DirList.task_done();


def Main():
	#Создаем парсер
	parse = argparse.ArgumentParser(description='Сканер дир вебсерва');
	#Добавляем опцию, урл вебсерва
	parse.add_argument('-u', action='store', dest='URL', help='Url, который бум сканить (http://192.168.100.236/)');
	#Добавляем опцию, количества потоков
	parse.add_argument('-t', action='store', dest='Thread', help='Количество потоков');
	#Получаем аргументы
	args = parse.parse_args();
	#Если аргументов нет то
	if (args.URL == None) or (args.Thread == None):
		#Выводим хэлп
		print (parse.print_help());
		#Выход
		exit();
	else:
		#Список для потоков
		jobs = [];
		#Список агентов
		agents = [];
		#Создаем очередь
		DirList = multiprocessing.JoinableQueue()
		#Открываем файл для чтения
		DirFile = open('dirs.txt', 'r');
		#Проходимся циклом по всем строкам
		for line in DirFile.readlines():
			#Добавляем в очередь ип из списка 
			DirList.put(line);
		#Открываем файл для чтения юзерагентов
		UserAgentFile = open('agents.txt', 'r');
		#Проходимся циклом по всем строкам
		for UserAgent in UserAgentFile.readlines():
			#Добавляем в список
			agents.append(UserAgent);
		print ('Scan starting....');
		#Создаем потоки
		for i in range(int(args.Thread)):
			p = multiprocessing.Process(target=Scan, args=(i, DirList, args.URL, agents));
			jobs.append(p);
			p.start();
		#Ждем их завершения
		for p in jobs:
			p.join();
		#Очередь тоже ждем
		DirList.join()
		print ('Scan done....');
#Запуск главной функции
if __name__=="__main__":
	Main();
