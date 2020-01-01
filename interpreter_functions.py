import nltk
import subprocess
import re
import os
import requests
import csv
from owlready2 import *
from bs4 import BeautifulSoup
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
# from Detect_uncertain.reduceUncertain import *
import Detect_uncertain.reduceUncertain
def set():
    global object_caption  # say that it is global
    print(object_caption)

def splitAndSet(raw_input, slpitter):
    try:
        data_list = raw_input.split(slpitter)
        reduceUncertain.text_input = data_list[0]
        reduceUncertain.object_caption = data_list[1]
        reduceUncertain.distance_to_object = data_list[2]
    except:
        print("splitter error!")

def filterPos(input_list, category):
    p = []
    for i in input_list:
        for j in range(len(i)):
            if i[j][1] == category:
                p.append(i[j][0])
    return p


def filterChunk(result, category):
    for r in result:
        if type(r) == nltk.tree.Tree:
            if r.label() == category:
                command = ' '.join([x[0] for x in r.leaves()])
                return command


def getUncertain(command):
    uncertain = ""
    for r in command:
        if 'IN' in r or 'JJ' in r or 'RBR' in r or 'NN' in r or 'JJR' in r or 'RB' in r or 'JJS' in r or 'JJ' in r or 'NNS' in r:
            uncertain = r[0]
            # break
    return uncertain


def getObject(command_object):
    obj = ""
    for r in command_object:
        if 'NN' in r or 'JJ' in r:
            obj = r[0]
            break
    return obj


def getUncertainVelocity(command):
    u_velocity = ""
    for r in command:
        if 'RBR' in r or 'RBS' in r or 'RB' in r or 'NN' in r or 'JJR' in r or 'JJS' in r or 'JJ' in r:
            u_velocity = r[0]
        else:
            u_velocity = "[default]"
    return u_velocity


def getMultiplier(command_list, word):
    multipliers = ["very", "much", "really", "pretty", "more", "little", "bare", "baby"]
    try:
        multiplier = command_list[command_list.index(word) - 1]
    except:
        multiplier = ""

    if multiplier in multipliers:
        return multiplier
    else:
        return 0


def superlativeOrComparative(tagged_command1, tagged_command2, word):
    if word[-3:] == 'est':
        return "Superlative"
    elif word[-2:] == 'er':
        return "Comparative"
    else:
        tagged_command = tagged_command1 + tagged_command2
        for r in tagged_command:
            if 'JJS' in r or 'RBS' in r:
                if word == r[0]:
                    return "Superlative"
            elif 'JJR' in r or 'RBR' in r:
                if word == r[0]:
                    return "Comparative"
            else:
                return "Base"


def calculateDistanceToTravel(raw_distance, multiplier, uncertain_distance_numeric):
    return raw_distance * (1 + multiplier) * (1 - uncertain_distance_numeric)


# web scrapper
def webCrawlThis(word):
    result = requests.get("http://localhost/Godrone/Uncerain.html")
    src = result.content
    soup = BeautifulSoup(src)

    if soup.find("td", text=word):
        body = soup.find("td", text=word).find_next_sibling("td")
        body1 = soup.find("td", text=word).find_previous_sibling("td")
        outfile = open("C:/Users/Admin/Desktop/Out.txt", "w+")
        if outfile.write(body1.text + " " + word + " " + body.text):
            print("Found something from web!")
        outfile.close()

        path = "java -jar C:/Users/Admin/PycharmProjects/untitled1/ontologyStore/dist/ontologyStore.jar"
        if javaShortRun(path):
            print("Stored the value on Ontology")
    else:
        print("Crawler could not able to find the word on web!")


def filterNumeric(value_str):
    num_decimal = re.compile(r'[^\d.]+')
    filtered_decimal = num_decimal.sub('', value_str)
    return filtered_decimal


# Refered http://bit.ly/34KLLVE
def getBaseFormat(word, postition):
    result = requests.get("http://localhost/Godrone/wordPosition.html")
    src = result.content
    soup = BeautifulSoup(src)

    if postition == "Comparative":
        # return re.sub('er$', '', word)
        body = soup.find("td", text=word).find_previous_sibling("td")
        return body.text
    elif postition == "Superlative":
        # return re.sub('est$', '', word)
        body = soup.find("td", text=word).find_previous_sibling("td")
        body1 = soup.find("td", text=body).find_previous_sibling("td")
        return body1.text
    elif postition == "Base":
        return word
    else:
        return "none"

# Run java file without getting the console output to a string
def javaShortRun(path):
    try:
        if subprocess.call(path, shell=True):
            print("Perfect Java shortrun")
    except:
        print("Java shotrun failed")

# Run java file with args[]
def javaRun(path, argument):
    try:
        s = subprocess.check_output(path + argument, shell=True)
        s = filterNumeric(s.decode("utf-8"))

        # check for empty string
        if not s:
            return 0
        else:
            return float(s) / 100.0

    except:
        return -1