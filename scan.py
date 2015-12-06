#!/usr/bin/python
# -*- coding: utf-8 -*-

#Модули
import requests;

DirsFile = open("dirs.txt", 'r');
DirsList = [line.strip() for line in DirsFile];

for Dir in DirsList:
	r = requests.get('http://192.168.100.236/' + Dir);
	if (r.status_code == requests.codes.ok):
		print ("%s - [OK]" % Dir);
