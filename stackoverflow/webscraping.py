#!/usr/bin/python3

import sys
import requests
import operator
from lxml.html import fromstring

_skills = [] # empty list

def main(argv):
    
    place_name = None
    pages = 10

    if len(sys.argv) >= 2:
        place_name = sys.argv[1] 

    if len(sys.argv) >= 3:
        pages = int(sys.argv[2])

    last_page = 0
    is_continue = True
    i = 0

    while is_continue:

        if i == 0:
            i = 1
            query = {'d': 20, 'l': place_name, 'u': 'Km' }
        else:
            query = {'d': 20, 'l': place_name, 'u': 'Km', 'pg': i}

        if place_name is None:
            del query['l']

        req = requests.get('https://stackoverflow.com/jobs', params=query)
        html_page = fromstring(req.content)

        # TODO: Calculate pages automatically...
        
        process_page(html_page)
        i += 1

        is_continue = pages >= i

        print(req.url)
        print('Processing page ' + str(i) + ' of ' + str(pages))

    create_file(req.url, place_name)


def get_text(el, class_name):
    els = el.find_class(class_name)
    if els:
        return els[0].text_content()
    else:
        return ''


def get_element(el, class_name):
    return el.find_class(class_name)


def process_page(doc):
    list_result = doc.find_class('listResults')    
    if list_result:
        get_results(list_result)


def get_results(list_result):
    for result in list_result:
        elements = result.find_class('-job js-result')              
        if elements and len(elements) > 0:            
            for el in elements:
                results = el.find_class('grid')                
                if results:
                    for result in results:
                        skills = get_element(result, 'post-tag no-tag-menu')
                        if skills:
                            for skill in skills:
                                populate_skills(skill.text)


def populate_skills(skill_name):
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
