import requests, bs4, re, sys
from datetime import datetime

def main():
    page = None
    if len(sys.argv) < 2:
        print('Input person you want to find: ', end = '')
        page = download_page(get_arguments())
    else:
        page = download_page('_'.join(sys.argv[1:]))

    if is_this_page_about_person(page):
        print('=-' * 20)
        print(get_person_name(page))
        print('Born: ' + str(get_born_date(page)[0]))

        if get_died_date(page) != None:
            print('Died: ' + str(get_died_date(page)[0]) + ' at the age of ' + str(int(get_died_date(page)[0])-int(get_born_date(page)[0])))

        else:
            today = datetime.now()
            print('Alive, is ' + str(today.year - int(get_born_date(page)[0])))

    else:
        print('Person has not been found.')


def get_arguments():
    arguments = input()
    return arguments

def download_page(name):
    res = requests.get('https://en.wikipedia.org/wiki/' + name)
    return res.text


def is_this_page_about_person(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    ths = soup.findAll('th')
    thContent = re.compile(r'>(.*)<')

    for th in ths[:50]:
        if thContent.findall(str(th))[0] == 'Born':
            return True

        elif thContent.findall(str(th))[0] == 'Date of birth':
            return True
    
    return False

def get_person_name(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    nameDiv = soup.find_all('h1')
    nameRegex = re.compile(r'>(.*)<')
    name = nameRegex.findall(str(nameDiv[0]))
    return name[0]

def get_born_date(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    trs = soup.findAll('tr')
    bornTr = 0
    nameRegex = re.compile(r'>(Born|Date of birth)<')
    for tr in trs[:50]:
        if len(nameRegex.findall(str(tr))):
            break
        bornTr += 1

    return get_date_str(str(trs[bornTr]))
    

def get_died_date(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    trs = soup.findAll('tr')
    diedTr = 0
    nameRegex = re.compile(r'>(Died)<')
    for tr in trs[:50]:
        if len(nameRegex.findall(str(tr))):
            return get_date_str(str(trs[diedTr]))
        diedTr += 1

    return None

def get_date_str(div):
    dateRegex = re.compile(r'\d\d\d\d')
    date = dateRegex.findall(str(div))
    if not date:
        return None
    else:
        return date


main()

