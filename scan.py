#!/usr/bin/python
# -*- coding: utf-8 -*-

#Модули
import requests;
import multiprocessing;
import queue;
import time;
import argparse;

#Эту функцию юзают потоки, передаем номер потока, очередь, и урл шо сканим
def Scan(i, DirList, url):
	#Бэзконечный цикл
	while True:
		#Небольгая пауза
		time.sleep(0.1);
		#Если очередь пуста то
		if (DirList.empty() == True):
			#Пишем что такой поток закончил
			print ('Thread %i: Done, exiting...' % i);
			#Обрываем цикл
			break;
		#Берем из очереди диру или файл
		Dir = DirList.get();
		#Делаем запрос, обрезая символ переноса строки
		r = requests.get(url + Dir[:-1]);
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
		#Создаем очередь
		DirList = multiprocessing.JoinableQueue()
		#Открываем файл для чтения
		DirFile = open('dirs.txt', 'r');
		#Проходимся циклом по всем строкам
		for line in DirFile.readlines():
			#Добавляем в очередь ип из списка 
			DirList.put(line);
		print ('Scan starting....');
		#Создаем потоки
		for i in range(int(args.Thread)):
			p = multiprocessing.Process(target=Scan, args=(i, DirList, args.URL));
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
