from flask import Flask, render_template, redirect, url_for
from flask_frozen import Freezer
import sys

app = Flask(__name__.split('.')[0])
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)

import urllib2
import json
import datetime
from functools import partial
import re

API_BASE = "http://iati-datastore.herokuapp.com/api/1/access/activity.json?%s&offset=%s"

@app.route("/")
def index():
    return render_template('index.html')

def get_title(title):
    if type(title)==dict:
        return title["text"]
    elif type(title)==unicode:
        return title
    return title[0]["text"]

def getDate(date):
    if date.get("iso-date"):
        return date["iso-date"]
    return date.get("text")

def isCorrectType(type, activity_date):
    if activity_date.get('type')==type:
        return activity_date
    return False    

def getBestDate(activity_dates, startend):
    if startend == "start":
        start_actual=filter(partial(isCorrectType, 'start-actual'), activity_dates)
        start_planned=filter(partial(isCorrectType, 'start-planned'), activity_dates)
        if start_actual:
            return (getDate(start_actual[0]), "actual")
        elif start_planned:
            return (getDate(start_planned[0]), "planned")
        else:
            return ("Unknown", "unknown")
    elif startend == "end":
        end_actual=filter(partial(isCorrectType, 'end-actual'), activity_dates)
        end_planned=filter(partial(isCorrectType, 'end-planned'), activity_dates)
        if end_actual:
            return (getDate(end_actual[0]), "actual")
        elif end_planned:
            return (getDate(end_planned[0]), "planned")
        else:
            return ("Unknown", "unknown")
    return ("", "")

def makeList(var):
    if type(var)==dict:
        return [var]
    else:
        return var

def datetimeformat(value, format='%Y-%m-%dT%H:%M:%S'):
    try:
        return datetime.datetime.strptime(value, format)
    except ValueError:
        return value
    except TypeError:
        return "Unknown"

def makeIdentifierSafe(identifier):
    identifier = re.sub("/", "___", identifier)
    identifier = re.sub(":", ">>>", identifier)
    return identifier

def reverseSafeIdentifier(identifier):
    identifier = re.sub("___", "/", identifier)
    identifier = re.sub(">>>", ":", identifier)
    return identifier

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.globals.update(get_title=get_title)
app.jinja_env.globals.update(makeList=makeList)
app.jinja_env.globals.update(getDate=getDate)
app.jinja_env.globals.update(getBestDate=getBestDate)
app.jinja_env.globals.update(makeIdentifierSafe=makeIdentifierSafe)

@app.route("/projects/<iati_identifier>/")
def show_project(iati_identifier=None):
    iati_identifier = reverseSafeIdentifier(iati_identifier)
    project_data = projects[iati_identifier]['iati-activity']
    return render_template('project.html', project=project_data)

@app.route("/projects/")
def show_projects():
    projects_data = projects
    return render_template('projects.html', projects=projects_data)

@app.route("/pledges/")
def show_pledges():
    return render_template('pledges.html')

def get_projects():
    offset = 0
    newdata = []
    while True:
        print "Requesting", API_BASE % ("recipient-country=PH&limit=50", offset)
        try:
            req = urllib2.Request((API_BASE % ("recipient-country=PH&limit=50", offset)))
            out = urllib2.urlopen(req).read()
            print "Retrieved, loading data"
            data = json.loads(out)
            for d in data['iati-activities']:
                newdata.append((d['iati-activity']['iati-identifier'], d))
            offset+=50
        except urllib2.HTTPError:
            break
        except Exception:
            pass
        if offset >50:
            break
    return dict(newdata)

if __name__ == '__main__':
    projects = get_projects()
    print "Site ready."
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        if len(sys.argv)>2:
            freezer.freeze()
            freezer.serve()
        else:
            freezer.freeze()
    else:
        app.run(port=8000, debug=True)
