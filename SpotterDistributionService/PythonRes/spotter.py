#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import Queue
import time
import sys
import traceback
import subprocess
import urllib2
import datetime
from bottle import route, run, response
from json import loads, dumps
from random import shuffle

# threadpool otlet: code.activestate.com/recipes/302746-simplest-useful-i-hope-thread-pool-example/
# bottle otlet: bottlepy.org/docs/dec/index.html

######....THREAD LOGIC....######
# Globalis valtozok
# bemeneti adatsor

Qin = Queue.Queue()

# kimeneti hibasor

Qerr = Queue.Queue()

# kimeneti szotar

Dout = {}

# pool

Pool = []

# frissitesi idokoz (s)

freq = 900 #15 perc


# Hibakezeles - uzenet

def err_msg():
    trace = sys.exc_info()[2]
    try:
        exc_value = str(sys.exc_value)
    except:
        exc_value = ''
    return (str(traceback.format_tb(trace)), str(sys.exc_type),
            exc_value)


# Hibakezeles - hibak kiolvasasa

def get_errors():
    try:
        while 1:
            yield Qerr.get_nowait()
    except Queue.Empty:
        pass


# Pool - fofolyamat

def process_queue():
    flag = 1
    while flag != 0:
        try:
            (flag, t) = Qin.get()  # itt blockol, amig nem erkezik keres
            if flag == 1:
                item = t[0]  # adat kiolvasasa
                qid = t[1]  # id kiolvasasa
                newdata = ping(item)  # pingeles
                Dout[qid] = newdata  # eredmeny szotarba helyezese
        except:
            Qerr.put(err_msg())  # hiba eseten a hibasorba irja a hibat


# Szalak inditasa - amount-al allithato

def start_threads(amount=10):
    for i in range(amount):
        thread = threading.Thread(target=process_queue)
        thread.start()
        Pool.append(thread)


# Uj lekerdezes hozzaadasa a sorhoz

def put(data, qid, flag=1):
    Qin.put([flag, [data, qid]])


# Qid-nek megfelelo valasz kiolvasasa es torlese a szotarbol (memoria optimalizacio), ha cachelni szeretnenk nem kell torolni

def get(qid):
    resp = None
    while resp == None:  # amig nincs meg a valaszunk, addig kerdezzuk, esetleg wait-el lassitani lehet, ha tulsagosan leterheli a servert
        resp = Dout.get(qid)
    del Dout[qid]  # kitoroljuk a valaszt
    return resp


# Szalak leallitasa - vegigiteral a Pool-on es egyesevel stop uzenetet kuld a szalaknak, majd megvarja, mig mind leall

def stop_threads():
    for i in range(len(Pool)):
        Qin.put((0, None))  # 0-flag==stop jelzes
    while Pool:
        time.sleep(1)  # adunk egy kis idot, hogy lealljanak
        for (index, the_thread) in enumerate(Pool):
            if the_thread.isAlive():
                continue
            else:
                del Pool[index]  # kitoroljuk a
            break


######....PING LOGIC....######
# egy ip pingelese

def ping(ip):

# pingeles lefuttatasa

    p1 = subprocess.Popen(['ping', '-c', '1', ip],
                          stdout=subprocess.PIPE)

# utolso sor levagasa

    p2 = subprocess.Popen(['tail', '-1'], stdin=p1.stdout,
                          stdout=subprocess.PIPE)

# atlag kinyerese

    p3 = subprocess.Popen(['awk', '{print $4}'], stdin=p2.stdout,
                          stdout=subprocess.PIPE)

#

    p4 = subprocess.Popen(['cut', '-d', '/', '-f', '2'],
                          stdin=p3.stdout, stdout=subprocess.PIPE)

# csovezetekek lezarasa

    p3.stdout.close()
    p2.stdout.close()
    p1.stdout.close()

    (output, err) = p4.communicate()

# az eredmeny visszaadasa

    return output.split('\n')[0]


# tobb ip pingelese

def fping(ips):

# IP tomb betoltese

    rv = loads(ips)

# IP cimek osszekeverese

    shuffle(rv)

# tomeges pingeleshez hasznalt fping parancs parameterezese

    array = ['fping', '-e']

# tomeges pingeleshez hasznalt ipcimek hozzaadasa a parancshoz

    for x in rv:
        array.append(x)

# tomeges pingeles lefuttatasa csovezetekkel visszaterve

    p1 = subprocess.Popen(array, stdout=subprocess.PIPE)
    (pings, err) = p1.communicate()
    #output={}
	output = []
    pings_arr = pings.split('\n')
    for i in range(len(rv)):
		tdict={}
        pings_line = pings_arr[i].split(' ')
		tdict["ip"]=pings_line[0]
		tdict["avg"]= (pings_line[3])[1:]
        #output[pings_line[0]] = (pings_line[3])[1:]
		output.append(tdict)
	fdict={}
	fdict["result"]=output
    print fdict
    return fdict


######....BOTTLE LOGIC....######

# egy cim pingelese
# bemeneti formatum: "{"ip":"<ip>"}"
# pl: localhost:8080/ping/{"ip":"gmail.com"}

@route('/ping/<ip>')
def thread_ping(ip):

# cim konvertalasa

    param = loads(ip)
	add=param["ip"]

# id generalasa a cimhez

    qid = id(add)

# pingelesi keres feladasa a poolba

    put(add, qid)

# visszateresi ertek tipusanak beallitsa

    response.content_type = 'application/json'

# visszateres JSON formatumban: {"ip":"<ip>", "avg":"<atlag ms-ben>"}
	
	dict = {}
	dict["ip"]=ip
	dict["avg"]=get(qid)

    #return dumps(get(qid))
	return dumps(dict)


# tobb cim pingelese
# bemeneti formatum: ["<ip1>","<ip2>",...] - tomb
# pl: http://localhost:8080/fping/%5B%22gmail.com%22,%22hotmail.com%22,%22index.hu%22%5D

@route('/fping/<ips>')
def single_fping(ips):

# visszateresi ertek tipusanak beallitsa

    response.content_type = 'application/json'

# a bemeno adatokra lefuttatott fping fuggveny eremenyenek visszaadasa standard json formatumban: [{"ip1":"<ip1>", "avg":"<atlag ms-ben>"},{"ip2":"<ip2>", "avg":"<atlag ms-ben>"}]

    return dumps(fping(ips))

#######....SERVICE UPDATE LOGIC....######
def update():
	f = open('config.txt','r')
	sv = f.readline()
	hn = f.readline()
	ip = f.readline()
	urllib2.urlopen('http://'+sv+'/'+hn+'/'+ip).read()

class UpdateTimer(threading.Thread):
	def __init__(self):
		super(UpdateTimer, self).__init__()
		self.time=datetime.datetime.now()
		self.shutdown= False
	def run(self):
		while self.shutdown== False:
			now = datetime.datetime.now()
			delta = now-self.time
			diff = delta.total_seconds()
			if diff<freq:
				time.sleep(freq-diff)
			else:
				update()
				self.time=datetime.datetime.now()
		

#######....MAIN PROGRAM....######
# szalak inditasa

start_threads()

timer = UpdateTimer()
timer.start()

# alkalmazas futtatasa

run(host='0.0.0.0', port=8080, debug=True, server='cherrypy')

# szalak leallitasa, ha kilepunk
timer.shutdown= True
stop_threads()


			
