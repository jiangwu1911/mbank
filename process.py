import socket
import json
import thread
import sqlite3
import re
import datetime
import sys
import os
import csv
from optparse import OptionParser

HOST = '0.0.0.0'
PORT = 5000

def connect_db():
    return sqlite3.connect('mbank.db')

def disconnect(conn):
    conn.close()

def create_table(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS session')
    cur.execute('CREATE TABLE session(sid TEXT, cst TEXT, start TEXT, \
                 end TEXT, duration INT)')
    cur.execute('CREATE UNIQUE INDEX session_index_01 ON session(sid)')
    cur.execute('DROP TABLE IF EXISTS flow')
    cur.execute('CREATE TABLE flow(sid TEXT, cst TEXT, \
                 flow TEXT, start TEXT, end TEXT, duration INT, retvalue TEXT)')
    cur.execute('CREATE INDEX flow_index_01 ON flow(sid, flow)')


def format_time(stime):
    t =  datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S,%f')
    return t.strftime("%Y-%m-%d %H:%M:%S.%f")

def flow_begin(db, m):
    cur = db.cursor()
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = memory")
    cur.execute("INSERT INTO flow VALUES('%s', '%s', '%s', '%s', '%s', %d, '%s')" %
                (m(2), m(3), m(5), format_time(m(1)), '', 0, ''))
    # if already have session begin record, will raise exception
    try:
        cur.execute("INSERT INTO session VALUES('%s', '%s', '%s', '%s', %d)" %
                    (m(2), m(3), format_time(m(1)), '', 0))
    except:
        pass
    db.commit()

def flow_end(db, m):
    cur = db.cursor()
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = memory")
    cur.execute("SELECT start FROM flow WHERE sid='%s' AND flow='%s'" % (m(2), m(5)))
    row = cur.fetchone()
    if row:
        t_start = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
        t_end = datetime.datetime.strptime(m(1), '%Y-%m-%d %H:%M:%S,%f')
        d = t_end - t_start
        duration = d.seconds * 1000 + d.microseconds/1000
        cur.execute("UPDATE flow SET end='%s', duration=%d WHERE sid='%s' AND flow='%s'"
                    % (format_time(m(1)), duration, m(2), m(5)))
    else:
        print "Found a flow end without start record, sid=%s, flow=%s" % (m(2), m(5))

    cur.execute("SELECT start FROM session WHERE sid='%s'" % (m(2)))
    row = cur.fetchone()
    if row:
        t_start = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
        t_end = datetime.datetime.strptime(m(1), '%Y-%m-%d %H:%M:%S,%f')
        d = t_end - t_start
        duration = d.seconds * 1000 + d.microseconds/1000
        cur.execute("UPDATE session SET end='%s', duration=%d WHERE sid='%s'"
                    % (format_time(m(1)), duration, m(2)))
    else:
        print "Found a flow end without session start record, sid=%s, flow=%s" % (m(2), m(5))
    db.commit()

def process(filename, db):
    p_date = '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) '
    p_session = '\[sid:(.*),cst:(.*),hst:(.*)\] '
    r_flow_begin = re.compile(p_date + p_session + 'begin flow (.*)')
    r_flow_end = re.compile(p_date + p_session + 'flow (.*) end (.*)')

    with open(filename) as f:
        for line in f:
            m1 = re.search(r_flow_begin, line)
            if m1: 
                flow_begin(db, m1.group)
                next
            m2 = re.search(r_flow_end, line)
            if m2:
                flow_end(db, m2.group)
                next

def output_to_csv(filename, db, table):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        cur = db.cursor()
        cur.execute("SELECT * FROM " + table)
        for row in cur.fetchall():
            writer.writerow(row)

if __name__ == '__main__':
    VERSION = "0.1"
    usage = "Usage: python " + sys.argv[0] + " -i <input_dir> -o output_dir"
    parser = OptionParser(usage, version = VERSION)

    parser.add_option("-i", "--input", action="store", type="string", dest="input", 
                      help="Input dir.")
    parser.add_option("-o", "--output", action="store", type="string", dest="output",
                      help="Output dir..")

    options, args = parser.parse_args()
    if options.input==None or options.output==None:
        print usage
        sys.exit(-1)

    db = connect_db()
    create_table(db)

    for file in os.listdir(options.input):
        filename = os.path.join(options.input, file)
        process(filename, db)

    output_to_csv(options.output+"/session.csv", db, "session")
    output_to_csv(options.output+"/flow.csv", db, "flow")
    disconnect(db)
