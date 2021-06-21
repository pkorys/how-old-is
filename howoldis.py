import requests, bs4, re, sys
from datetime import datetime

def main():
    page = None
    if len(sys.argv) < 2:
        print('Input person you want to find: ', end = '')
        page = downloadPage(getArguments())
    else:
        page = downloadPage('_'.join(sys.argv[1:]))

    if isThisPageAboutPerson(page):
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        print(getPersonName(page))
        print('Born: ' + str(getBornDate(page)[0]))

        if getDiedDate(page) != None:
            print('Died: ' + str(getDiedDate(page)[0]) + ' at the age of ' + str(int(getDiedDate(page)[0])-int(getBornDate(page)[0])))

        else:
            today = datetime.now()
            print('Alive, is ' + str(today.year - int(getBornDate(page)[0])))

    else:
        print('Person has not been found.')


def getArguments():
    arguments = input()
    return arguments

def downloadPage(name):
    res = requests.get('https://en.wikipedia.org/wiki/' + name)
    return res.text


def isThisPageAboutPerson(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    dateDiv = soup.select('#mw-content-text > div.mw-parser-output > table.infobox.biography.vcard > tbody > tr:nth-child(3) > td')
    return len(dateDiv) > 0

def getPersonName(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    nameDiv = soup.find_all('h1')
    nameRegex = re.compile(r'>(.*)<')
    name = nameRegex.findall(str(nameDiv[0]))
    return name[0]

def getBornDate(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    bornDiv = soup.select('#mw-content-text > div.mw-parser-output > table.infobox.biography.vcard > tbody > tr:nth-child(3) > td')
    return getDateStr(bornDiv)
    

def getDiedDate(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    diedDiv = soup.select('#mw-content-text > div.mw-parser-output > table.infobox.biography.vcard > tbody > tr:nth-child(4) > td')
    return getDateStr(diedDiv)

def getDateStr(div):
    dateRegex = re.compile(r'\d\d\d\d')
    date = dateRegex.findall(str(div))
    if len(date) == 0:
        return None
    else:
        return date

main()

