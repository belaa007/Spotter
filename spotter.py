#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import Queue
import time
import sys
import traceback
import subprocess
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
    output = {}
    pings_arr = pings.split('\n')
    for i in range(len(rv)):
        pings_line = pings_arr[i].split(' ')
        output[pings_line[0]] = (pings_line[3])[1:]
    print output
    return output


######....BOTTLE LOGIC....######

# egy cim pingelese
# bemeneti formatum: "<ip>"
# pl: localhost:8080/ping/"gmail.com"

@route('/ping/<ip>')
def thread_ping(ip):

# cim konvertalasa

    add = loads(ip)

# id generalasa a cimhez

    qid = id(add)

# pingelsi keres feladasa a poolba

    put(add, qid)

# visszateresi ertek tipusanak beallitsa

    response.content_type = 'application/json'

# visszateres JSON formatumban: "<atlag ms-ben>"

    return dumps(get(qid))


# tobb cim pingelese
# bemeneti formatum: ["<ip1>","<ip2>",...] - tomb
# pl: http://localhost:8080/fping/%5B%22gmail.com%22,%22hotmail.com%22,%22index.hu%22%5D

@route('/fping/<ips>')
def single_fping(ips):

# visszateresi ertek tipusanak beallitsa

    response.content_type = 'application/json'

# a bemeno adatokra lefuttatott fping fuggveny eremenyenek visszaadasa standard json formatumban: {"<ip1>":"<ping1>", "<ip2>":"<ping2>",...} - szotar

    return dumps(fping(ips))



#######....MAIN PROGRAM....######
# szalak inditasa

start_threads()

# alkalmazas futtatasa

run(host='0.0.0.0', port=8080, debug=True, server='cherrypy')

# szalak leallitasa, ha kilepunk

stop_threads()


			
