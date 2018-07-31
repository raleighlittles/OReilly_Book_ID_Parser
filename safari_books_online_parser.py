#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 19:59:03 2018

@author: Raleigh Littles
"""

import requests
import re


def retrieve_page_contents(url):
    r = requests.get(url)
    if r.status_code < 300:
        return (r.content.decode())
    
    print("Current url: {0} returned invalid status code.".format(url))
    raise ValueError('Invalid server response.')
    

def parse_contents_into_list(text):
    """
    Turns the text of a page into a list of book IDs.
    """
    
    regex_string = "/library/cover/[\d]{2,}"
    
    book_id_matches = re.findall(regex_string, text)
    
    book_ids = [match.split('/')[-1] for match in book_id_matches]
    print("Current page found {0} book ids.".format(len(book_ids)))
    return book_ids

def write_id_list_to_txt_file(id_list, filename):
    with open(filename + ".txt", 'a') as txt_file_handler:
        txt_file_handler.write("\n".join([str(book_id) for book_id in id_list]))
        
    txt_file_handler.close()
        

url_dict = {'math_and_science': 'https://www.safaribooksonline.com/topics/math-science',
            'web_development': 'https://www.safaribooksonline.com/topics/web-development',
            'computer_networking': 'https://www.safaribooksonline.com/topics/computer-networking',
            'software_development': 'https://www.safaribooksonline.com/topics/software-development',
            'databases': 'https://www.safaribooksonline.com/topics/databases'}



for topic, url in url_dict.items():
    # don't expect to see a topic with more than 100 pages of books in it
    book_list_for_topic = []
    for page_number in range(0, 100):
        try:
            page_content = retrieve_page_contents(url + "?page={0}".format(page_number))
            
        except ValueError:
            continue
        finally:
            book_list = parse_contents_into_list(page_content)
            book_list_for_topic.extend(book_list)
    print("{0} book ids found for topic: {1}".format(len(book_list_for_topic), topic))
    write_id_list_to_txt_file(book_list_for_topic, topic)
        
        
        
        
    