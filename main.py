# -*- coding: utf-8 -*-

import string
import pyperclip
from twitter_scraper import get_tweets
import nltk
from nltk.tag import pos_tag
from random import randint
import markovify

## Vars
greetings = ['Bonkour', 'Henlo']
prenoun = ['les', 'le']
end = ['auf Widerzeighn', 'Guten Byebye', 'oui oui out']
unicodeA = ['á', 'Á', 'ą́', 'Ą́', 'ắ', 'Ắ']
unicodeE = ['é', 'É', 'ḗ', 'Ḗ', 'ę́', 'Ę́']
unicodeI = ['í', 'Í', 'ḯ', 'Ḯ', 'ī́', 'Ī́']
unicodeO = ['ó', 'Ó', 'ṍ', 'Ṍ', 'ǿ', 'Ǿ']
unicodeU = ['ú', 'Ú', 'ų́', 'Ų́', 'ứ', 'Ứ']

## Chances
unicode_chance = 5
capital_chance = 50

## Selected Users
selected_users = ['realdonaldtrump', 'officialmcrich', 'COOLPOP59', 
            'Juliadante34', 'spunkymunkeymus', 'NelsonMandela', 'Bible_Time', 
            'Simonblox']

## Twitter Pages
twitter_pages = 5

## Menu Options
menu_options = ['Custom Sentence', 'Random Tweet [select user]', 'Random Tweet [random user]', 
                    'AutoGen Tweet [select user]', 'AutoGen Tweet [random user]', 'Exit']

### Main Menu
def print_title():
    print("\nRoddy Speak - For Twitter\n")

def main_menu_print():
    print("### Main Menu")
    for index, option in enumerate(menu_options):
        print(str(index + 1) + ": " + str(option))

def main_menu():
    print_title()
    main_menu_print()
    choice = 0
    while (int(choice) < 1) or (int(choice) > len(menu_options)):
        choice = input("Select Choice [1-" + str(len(menu_options)) + "]\n-> ")
    return choice

### User Selection
def print_user(user):
    print("Twitter User: " + user + "\n")

def custom_user():
    user = ""
    while (user == "") or (" " in user):
        user = input("Enter the Twitter Handle\n-> ")
    print_user(user)
    return user

def random_user():
    user = selected_users[randint(0, len(selected_users)-1)]
    print_user(user)
    return user

### Sentence Selection
def print_sentence(title, sentence):
    print("\n" + title + ":\n" + sentence)

def custom_sentence():
    sentence = ""
    while " " not in sentence:
        sentence = input("Enter a Sentence:\n-> ")
    print_sentence("Custom Sentence", sentence)
    return sentence

def random_tweet(user):
    sentence = ""
    while " " not in sentence:
        tweets = []
        for tweet in get_tweets(selected_users[randint(0, len(selected_users)-1)], pages=twitter_pages):
            tweets.append(str(tweet['text']))
        sentence = str(tweets[randint(0, len(tweets)-1)])
    print_sentence("Random Tweet", sentence)
    return sentence

def generated_tweet(user):
    sentence = ""
    while " " not in sentence:
        tweets = '\n'.join([t['text'] for t in get_tweets(str(user), pages=5)])
        text_model = markovify.Text(tweets)
        sentence = text_model.make_short_sentence(200)
    print_sentence("Generated Tweet", sentence)
    return sentence

### Roddy Time
def prepend_nouns(sentence):
    split_sentence = pos_tag(sentence.split())
    nouns = [word for word,pos in split_sentence if pos == 'NNP']
    for s in nouns:
        sentence = sentence.replace(str(s), str(prenoun[randint(0,len(prenoun)-1)] + " " + str(s)), 1)
    return sentence

def tailends(sentence):
    sentence = greetings[randint(0, len(greetings)-1)] + ", " + sentence + ", " + end[randint(0, len(end)-1)]
    return sentence

def random_uppercase(sentence):
    for i in range(0,len(sentence)):
        if (randint(1, capital_chance) == 1):
            sentence = sentence[:i] + sentence[i].upper() + sentence[i + 1:]
    return sentence

def random_unicode(sentence):
    s = ""
    for word in sentence.split():
        if "com" not in word:
            for l in range(0, len(word)-1):
                if (word[l].lower() in ('a', 'e', 'i', 'o', 'u')) and (randint(1, unicode_chance) == 1):
                    if (word[l] == 'a'):
                        word = word[:l] + unicodeA[randint(0, len(unicodeA)-1)] + word[l + 1:]
                    if (word[l] == 'e'):
                        word = word[:l] + unicodeE[randint(0, len(unicodeE)-1)] + word[l + 1:]
                    if (word[l] == 'i'):
                        word = word[:l] + unicodeI[randint(0, len(unicodeI)-1)] + word[l + 1:]
                    if (word[l] == 'o'):
                        word = word[:l] + unicodeO[randint(0, len(unicodeO)-1)] + word[l + 1:]
                    if (word[l] == 'u'):
                        word = word[:l] + unicodeU[randint(0, len(unicodeU)-1)] + word[l + 1:]
        s = s + word + " "
    return s

### MAIN
def main():
    running = True
    user = ""
    sentence = ""
    while running:
        selection = int(main_menu())
        if selection == 1:
            sentence = custom_sentence()
        elif selection == 2:
            user = custom_user()
            sentence = random_tweet(user)
        elif selection == 3:
            user = random_user()
            sentence = random_tweet(user)
        elif selection == 4:
            user = custom_user()
            sentence =generated_tweet(user)
        elif selection == 5:
            user = random_user()
            sentence =generated_tweet(user)
        elif selection == 6:
            running = False
        sentence = random_unicode(random_uppercase(tailends(prepend_nouns(sentence))))
        print_sentence("Roddified Sentence", sentence)

main()


