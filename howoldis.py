import requests, bs4, re, sys
from datetime import date, datetime

def main():
    if len(sys.argv) < 2:
        print('Input person you want to find: ', end = '')
        page = download_page(get_arguments())
    else:
        page = download_page('_'.join(sys.argv[1:]))

    if is_this_page_about_person(page):
        print('=-' * 20)
        print(get_person_name(page))
        print('Born: ' + format_date(get_born_date(page)))

        if get_died_date(page) != None:
            print('Died: ' + format_date(get_died_date(page)) + ' at the age of ' + get_age(get_born_date(page), get_died_date(page)))

        else:
            today = datetime.now()
            today_date = (today.year, today.month, today.day)
            print('Alive, is ' + get_age(get_born_date(page), today_date))

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
    th_content = re.compile(r'>(.*)<')

    for th in ths[:50]:
        if th_content.findall(str(th))[0] == 'Born':
            return True

        elif th_content.findall(str(th))[0] == 'Date of birth':
            return True
    
    return False

def get_person_name(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    name_div = soup.find_all('h1')
    name_regex = re.compile(r'>(.*)<')
    name = name_regex.findall(str(name_div[0]))
    return name[0]

def get_born_date(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    trs = soup.findAll('tr')
    born_tr = 0
    name_regex = re.compile(r'>(Born|Date of birth)<')
    for tr in trs[:50]:
        if len(name_regex.findall(str(tr))):
            break
        born_tr += 1

    return get_date_str(str(trs[born_tr]))
    

def get_died_date(page):
    soup = bs4.BeautifulSoup(page, features = 'html.parser')
    trs = soup.findAll('tr')
    died_tr = 0
    name_regex = re.compile(r'>(Died)<')
    for tr in trs[:50]:
        if len(name_regex.findall(str(tr))):
            return get_date_str(str(trs[died_tr]))
        died_tr += 1

    return None

def get_date_str(div):
    date_regex = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
    date = date_regex.findall(str(div))
    if not date:
        return None
    else:
        return date[0]

def format_date(date):
    year, month, day = date
    beauty_date = str(int(day))
    beauty_date += get_ordinal(int(day)) + ' '
    beauty_date += get_month_name(int(month)) + ' '
    beauty_date += year

    return beauty_date

def get_ordinal(day):
    if day == 1:
        return 'st'
    elif day == 2:
        return 'nd'
    elif day == 3:
       return 'rd'
    elif day > 20 & day%10 == 1:
        return 'st'
    elif day > 20 & day%10 == 2:
        return 'nd'
    elif day > 20 & day%10 == 3:
        return 'rd'
    else:
        return 'th'

def get_month_name(month):
    month_names = {1 : 'January', 
                   2 : 'February',
                   3 : 'March',
                   4 : 'April',
                   5 : 'May',
                   6 : 'June',
                   7 : 'July',
                   8 : 'August',
                   9 : 'September',
                   10 : 'October',
                   11 : 'November',
                   12 : 'December'}
    return month_names[month]

def get_age(born, died):
    born_year, born_month, born_day = born
    died_year, died_month, died_day = died
    
    if int(died_month) < int(born_month):
        return str(int(died_year)-int(born_year) - 1)
    elif int(died_month) == int(born_month) & int(died_day) < int(born_day):
        return str(int(died_year)-int(born_year) - 1)
    else:
        return str(int(died_year)-int(born_year))


main()

