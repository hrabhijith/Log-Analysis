# !/usr/bin/env python3
# !/usr/bin/python -3.5.2

import psycopg2
import datetime
import sys

DBNAME = 'news'

now = datetime.datetime.now()


def dbConnect():
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    return db


def firstQuery():
    db = dbConnect()
    c = db.cursor()
    print("Scanning log data, please wait!\n")
    c.execute('''select a.title, count(l.path) as num
                from articles as a left join log as l
                on a.slug = replace(l.path, '/article/','')
                group by a.title
                order by num desc
                limit 3''')
    result = c.fetchall()
    db.close()
    return result


a = firstQuery()


def firstQueryResult():
    print("Here is the report on: \n")
    print("1. Most popular three articles of all time as of %s. \n" %
          now.strftime("%Y-%m-%d %H:%M"))

    for ab in a:
        print("--The article with the title: " + "\"" +
              str(ab[0]) + "\"" + " has got " + str(ab[1]) + " views." + '\n')


firstQueryResult()


def secondQuery():
    db = dbConnect()
    c = db.cursor()
    print("Scanning log data, please wait!\n")
    c.execute('''select a.name, b.view_count
                from authors as a join auth_log as b
                on a.id = b.author_id
                order by b.view_count desc
                limit 3''')
    result = c.fetchall()
    db.close()
    return result


b = secondQuery()


def secondQueryResult():
    print("Here is the report on: \n")
    print("2. Most popular article authors of all time as of %s. \n" %
          now.strftime("%Y-%m-%d %H:%M"))

    for ab in b:
        print("--The author: " + "\"" +
              str(ab[0]) + "\"" + " has got " + str(ab[1]) +
              " views for their article." + '\n')


secondQueryResult()


def thirdQuery():
    db = dbConnect()
    c = db.cursor()
    print("Scanning log data, please wait!\n")
    c.execute('''select to_char(date_all::date, 'FMMonth DD, YYYY')
                as date_all,
                round(percent_error,2) as percent_error
                from error_percentage
                where percent_error > 1''')
    result = c.fetchall()
    db.close()
    return result


c = thirdQuery()


def thirdQueryResult():
    print("Here is the report on: \n")
    print("3. Days which had more than 1 percent of" +
          " requests which lead to errors as of %s. \n" %
          now.strftime("%Y-%m-%d %H:%M"))

    for ab in c:
        print("--This day: " + "\"" +
              str(ab[0]) + "\"" + " has observed " + str(ab[1]) + "%" +
              " of request errors." + '\n')


thirdQueryResult()
