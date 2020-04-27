#!/usr/bin/python3

import sys
import requests
import operator
import re
from lxml.html import fromstring

_skills = [] # empty list
_num_jobs_expected = 0
_place_name = None
_usa_states = ["AK", "AL", "AR", "AS", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "GU", "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MP", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UM", "UT", "VA", "VI", "VT", "WA", "WI", "WV", "WY"]
_canada_provinces = ["AB", "BC", "MB", "NB", "NL", "NT", "NS", "NU", "ON", "PE", "QC", "SK", "YT"]

def main(argv):
    
    global _place_name   
    global _num_jobs_expected

    if len(sys.argv) >= 2:
        _place_name = sys.argv[1] 

    is_continue = True
    i = 0
    
    while is_continue:

        if i == 0:
            i = 1
            query = {'d': 20, 'l': _place_name, 'u': 'Km' }
        else:
            query = {'d': 20, 'l': _place_name, 'u': 'Km', 'pg': i}

        if _place_name is None:
            del query['l']

        req = requests.get('https://stackoverflow.com/jobs', params=query)
        html_page = fromstring(req.content)

        if _num_jobs_expected == 0:
            _num_jobs_expected = get_num_jobs(html_page)        

        if _num_jobs_expected > 0:
            process_page(html_page)
            i += 1
        
        print(req.url)
        print('Jobs to be processed: ' + str(_num_jobs_expected))
        is_continue = _num_jobs_expected - 1 > 0

    create_file(req.url, _place_name)

def get_num_jobs(page):
    
    regex = r"\d+"
    elements = page.find_class('description fc-light fs-body1')    
    if (elements is not None):
        for el in elements:  
            matches = re.findall(regex, el.text.replace(',',''), re.DOTALL)
            if matches is not None and len(matches) > 0:
                return int(matches[0])
    return 0


def get_text(el, class_name):
    els = el.find_class(class_name)
    if els:
        return els[0].text_content()
    else:
        return ''

def process_page(doc):
    list_result = doc.find_class('listResults')    
    if list_result is not None:
        process_results(list_result)


def process_results(list_result):
    if list_result is not None:
        for x in list_result:
            process_listed_jobs(x)


def process_listed_jobs(elements):   
    if elements is not None:
        for el in elements:
            grids = el.find_class('grid--cell fl1')
            if len(grids) > 0:
                process_job_skills(grids)           


def process_job_skills(elements):
    global _num_jobs_expected
    if elements is not None:
        for x in elements:           
            if is_place(x):                              
                _num_jobs_expected -= 1                  
                skills = x.find_class('post-tag no-tag-menu')
                if len(skills) > 0:                     
                    for skill in skills:
                        count_skills(skill.text)
        

def is_place(element):
    
    global _place_name
    global _usa_states

    if _place_name is None:
        return True

    company_location = element.find_class('fc-black-700 fs-body1 mb4')

    if len(company_location) > 0 and len(company_location[0]) > 1:        
        city_place = company_location[0][1].text.split(',')
        if len (city_place) > 1:
            if is_country('usa', _usa_states, city_place[1].strip()):
                return True
            if is_country('canada', _canada_provinces, city_place[1].strip()):
                return True
            return city_place[1].strip().lower() == _place_name.lower()
        else:
            return city_place[0].strip().lower() == _place_name.lower()

    return False


def is_country(country_name, country_states_provinces, value):
    global _place_name
    if country_name.lower() == _place_name.lower() and value in country_states_provinces:
        return True
    return False


def count_skills(skill_name):
    global _skills
    skill = next((x for x in _skills if x.name == skill_name), None)
    if skill is not None:
        index = _skills.index(skill)
        _skills[index].count += 1
    else:
        _skills.append(Skill(skill_name, 1))

        
def create_file(url, place_name):
    global _skills

    if place_name is None:
        place_name = 'stackoverflow'

    with open(place_name + '-skill.txt', mode='wt', encoding='utf-8') as f:
        f.write(url)
        f.write('\n')
        _skills.sort(key=operator.attrgetter('count'), reverse=True)
        for skill in _skills:
            f.write('\n' + skill.name + ': ' + str(skill.count))

        
class Skill:
    def __init__(self, name, count):
        self.name = name
        self.count = count      

if __name__ == "__main__":
    main(sys.argv)
