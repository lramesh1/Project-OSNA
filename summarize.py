"""
sumarize.py
"""

from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
import pickle
import string
import re
import requests
import numpy as np


def print_genders(tweets):
    counts = Counter([t['gender'] for t in tweets])
    print('%.2f of accounts are labeled with gender' %
          ((counts['male'] + counts['female']) / sum(counts.values())))
    print('gender counts:\n', counts)

def main():

    Y=[]
    print("Here is the summary!!!")
    tweets = pickle.load(open('tweets.pkl', 'rb'))
    tweets_gender = pickle.load(open('tweets_gender.pkl', 'rb'))
    print("number of messages collected: %d" %len(tweets))
    print("*************************************************")
    print("Number of communities and members:")
    comp = pickle.load(open('comp.pkl', 'rb'))
    count = 1
    for i in comp:
        print('community %d  has %d members' %(count,len(i)))
        count+=1
        Y.append(len(i))
    print("number of users collected: %d" %np.sum(Y))
    print("average number of users per community: %d" %np.mean(Y))
    print("communities in a glimpse:")
    N = len(Y)
    X = range(N)
    width = 1 / 1.5
    plt.bar(X, Y, width, color="green", align='center')
    plt.show()
    print("graph displayed and closed!!")
    print("*************************************************")
    male = pickle.load(open('male.pkl', 'rb'))
    female = pickle.load(open('female.pkl', 'rb'))
    unknown = pickle.load(open('unknown.pkl', 'rb'))
    users = len(male)+len(female)+len(unknown)
    print("number of users collected: %d" %users)
    print_genders(tweets_gender)
    print("here is a glimpse of gender classification:")
    labels = 'male', 'female', 'unknown'
    sizes = [len(male), len(female), len(unknown)]
    colors = ['lightskyblue', 'lightcoral', 'lightgreen']
    plt.pie(sizes, labels=labels, colors=colors,autopct='%1.1f%%', startangle=90)
    plt.show()
    print("graph displayed and closed!!")
    print("Thak you!!")


if __name__ == '__main__':
    main()