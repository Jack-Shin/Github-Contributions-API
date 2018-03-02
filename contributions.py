from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask import Flask
import datetime

app = Flask(__name__)

@app.route("/contributions/daily/<uname>")
def contributions(uname):
  
  return getContributionsJSON(uname)

@app.route("/contributions/weekly/<uname>")
def contributionsWeekly(uname):
  rects = getContributionsElement(uname)
  sun = 0
  mon = 0 
  tue = 0
  wed = 0
  thu = 0
  fri = 0
  sat = 0

  for rect in rects:
    dt = rect.get('data-date')
    count = int(rect.get('data-count'))
    year, month, day = (int(x) for x in dt.split('-'))
    ans = datetime.date(year, month, day)
    dayOfWeek = ans.strftime("%A")

    if dayOfWeek == "Sunday":
      sun += count
    elif dayOfWeek == "Monday":
      mon += count
    elif dayOfWeek == "Tuesday":
      tue += count
    elif dayOfWeek == "Wednesday":
      wed += count
    elif dayOfWeek == "Thursday":
      thu += count
    elif dayOfWeek == "Friday":
      fri += count
    elif dayOfWeek == "Saturday":
      sat += count
    
  json = "{ "\
            "\"Sunday\" : \"%s\", "\
            "\"Monday\" : \"%s\", "\
            "\"Tuesday\" : \"%s\", "\
            "\"Wednesday\" : \"%s\", "\
            "\"Thursday\" : \"%s\", "\
            "\"Friday\" : \"%s\", "\
            "\"Saturday\" : \"%s\""\
          " }" % (str(sun), str(mon), str(tue), str(wed), str(thu), str(fri), str(sat))

  return json

@app.route('/contributions/monthly/<uname>')
def contributionsMonthly(uname):
  rects = getContributionsElement(uname)

  m_jan = 0
  m_feb = 0
  m_mar = 0
  m_apr = 0
  m_may = 0
  m_jun = 0
  m_jul = 0
  m_aug = 0
  m_sep = 0
  m_oct = 0
  m_nov = 0
  m_dec = 0

  for rect in rects:
    dt = rect.get('data-date')
    count = int(rect.get('data-count'))
    month = dt.split('-')[1]
    if month == "01":
      m_jan += count
    elif month == "02":
      m_feb += count
    elif month == "03":
      m_mar += count
    elif month == "04":
      m_apr += count
    elif month == "05":
      m_may += count
    elif month == "06":
      m_jun += count
    elif month == "07":
      m_jul += count
    elif month == "08":
      m_aug += count
    elif month == "09":
      m_sep += count
    elif month == "10":
      m_oct += count
    elif month == "11":
      m_nov += count
    elif month == "12":
      m_dec += count

  json = "{ "\
            "\"January\" : \"%s\", "\
            "\"Febuary\" : \"%s\", "\
            "\"March\" : \"%s\", "\
            "\"April\" : \"%s\", "\
            "\"May\" : \"%s\", "\
            "\"June\" : \"%s\", "\
            "\"July\" : \"%s\","\
            "\"August\" : \"%s\","\
            "\"September\" : \"%s\","\
            "\"October\" : \"%s\","\
            "\"November\" : \"%s\","\
            "\"December\" : \"%s\","\
          " }" % (str(m_jan), str(m_feb), str(m_mar), str(m_apr), str(m_may), str(m_jun), str(m_jul), str(m_aug), str(m_sep), str(m_oct), str(m_nov), str(m_dec))

  return json


def getContributionsJSON(uname):
  rects = getContributionsElement(uname)

  json = "["
  for rect in rects:
    if rect.get('data-count') != "0":
      json += "\n    {\n        \"date\" : \"%s\",\n        \"count\" : \"%s\"\n    }," % (rect.get('data-date'), rect.get('data-count'))
    
  json = json[:-1]
  json += "\n]"
  return json

def getContributionsElement(uname):
  url = 'https://github.com/' + uname

  html = urlopen(url)
  soup = BeautifulSoup(html, 'html.parser')

  rects = soup.find_all("rect")
  return rects

if __name__ == "__main__":
  app.debug = False
  app.run(host="0.0.0.0")
