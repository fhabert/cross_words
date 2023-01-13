import numpy as np
import random
from bs4 import BeautifulSoup
import requests
import text

class MotsCroises(object):
    def __init__(self, dim, words):
        self.dim = dim
        self.words = words
        self.init_words = 5
        self.limit = 29
        self.mat = [[0 for _ in range(self.dim[1])] for _ in range(self.dim[0])]
        self.words_pos_h = []
        self.words_pos_v = []
        self.def_h = []
        self.def_v = []
        self.count_h = 0
        self.count_v = 0
        pass
    
    def print_table(self):
        for i in range(len(self.mat)):
            print("-" * (len(self.mat[0])*2+1))
            for j in range(len(self.mat[0])):
                print("|", end="")
                if self.mat[i][j] == 0:
                    print(" ", end="")
                else:
                    print(self.mat[i][j], end="")
            print("|")
        pass

    def first_words(self):
        for word in self.words[0:self.init_words]:
            pos = [random.randint(0, self.dim[0]-1), random.randint(0, self.dim[1]-1)]
            dir = random.randint(0,1)
            while not self.check_validity(word[0], dir, pos):
                pos = [random.randint(0, self.dim[0]-1), random.randint(0, self.dim[1]-1)]
                dir = random.randint(0,1)
            if dir:
                count = 0
                for letter in word[0]:
                    self.mat[pos[0]][pos[1]+count] = letter
                    count += 1
                self.count_h += 1
                self.words_pos_h.append([pos, self.count_h])
                self.def_h.append(word[1])
            else:
                count = 0
                for letter in word[0]:
                    self.mat[pos[0]+count][pos[1]] = letter
                    count += 1
                self.count_v += 1
                self.words_pos_v.append([pos, self.count_v])
                self.def_v.append(word[1])
        pass
    
    def insert_words(self):
        for word in self.words[self.init_words:self.limit]:
            # If 1 then write the word horizontally, if 0 write it vertically
            no_loop = False
            for _ in range(2):
                for i in range(self.dim[0]):
                    for j in range(self.dim[1]):
                        if not no_loop:
                            pos = [i, j]
                            if i % 2 == 0:
                                dir = 0
                            else:
                                dir = 1
                            no_loop = self.check_validity(word[0], dir, pos)

            if no_loop:
                if dir:
                    count = 0
                    for letter in word[0]:
                        self.mat[pos[0]][pos[1]+count] = letter
                        count += 1
                    self.count_h += 1
                    self.words_pos_h.append([pos, self.count_h])
                    self.def_h.append(word[1])
                else:
                    count = 0
                    for letter in word[0]:
                        self.mat[pos[0]+count][pos[1]] = letter
                        count += 1
                    self.count_v += 1
                    self.words_pos_v.append([pos, self.count_v])
                    self.def_v.append(word[1])
        pass

    def check_validity(self, word, dir, pos):
        if dir:
            check = 0
            same_letters = []
            for i in range(len(word)):
                if pos[1]+i < self.dim[1]-1 and (self.mat[pos[0]][pos[1]+i] == 0 or self.mat[pos[0]][pos[1]+i] == word[i]):
                    check += 1
                if pos[1]+i < self.dim[1]-1 and self.mat[pos[0]][pos[1]+i] == word[i]:
                    same_letters.append((pos[0], pos[1]+i))
            free_around_f = False
            free_around_e = False
            check_along = True
            if check:
                for i in range(len(word)):
                    if pos[1]-1 > 0 and pos[0]-1 > 0 and pos[0]+1 <= self.dim[0]-1 and (self.mat[pos[0]][pos[1]-1] == 0) and (self.mat[pos[0]-1][pos[1]] == 0) and (self.mat[pos[0]+1][pos[1]] == 0):
                        free_around_f = True
                    if pos[1]+len(word) <= self.dim[1]-1 and pos[0]-1 > 0 and pos[0]+1 <= self.dim[0]-1 and (self.mat[pos[0]][pos[1]+len(word)] == 0) and (self.mat[pos[0]-1][pos[1]+len(word)] == 0) and (self.mat[pos[0]+1][pos[1]+len(word)] == 0):
                        free_around_e = True
                    if i > 0 and i < len(word) and (pos[0],pos[1]+i) not in same_letters and pos[0]-1 > 0 and pos[0]+1 <= self.dim[0]-1 and pos[1]+i <= self.dim[1]-1 and (self.mat[pos[0]-1][pos[1]+i] != 0 or self.mat[pos[0]+1][pos[1]+i] != 0):
                        check_along = False
            if check == len(word) and free_around_f and free_around_e and check_along:
                return True
            return False
        else:
            check = 0
            same_letters = []
            for i in range(len(word)):
                if pos[0]+i < self.dim[0]-1 and (self.mat[pos[0]+i][pos[1]] == 0 or self.mat[pos[0]+i][pos[1]] == word[i]):
                    check += 1
                if pos[0]+i < self.dim[0]-1 and self.mat[pos[0]+i][pos[1]] == word[i]:
                    same_letters.append((pos[0]+i, pos[1]))
            free_around_f = False
            free_around_e = False
            check_along = True
            if check:
                for i in range(len(word)):
                    if pos[1]-1 > 0 and pos[1]+1 < self.dim[1]-1 and pos[0]-1 >=0 and (self.mat[pos[0]][pos[1]-1] == 0) and (self.mat[pos[0]][pos[1]+1] == 0) and (self.mat[pos[0]-1][pos[1]] == 0):
                        free_around_f = True
                    if pos[0]+len(word) <= self.dim[0]-1 and pos[1]-1 > 0 and pos[1]+1 <= self.dim[1]-1 and (self.mat[pos[0]+len(word)][pos[1]] == 0) and (self.mat[pos[0]+len(word)][pos[1]-1] == 0) and (self.mat[pos[0]+len(word)][pos[1]+1] == 0):
                        free_around_e = True
                    if i > 0 and i < len(word) and (pos[0]+i,pos[1]) not in same_letters and pos[1]-1 > 0 and pos[1]+1 <= self.dim[0]-1 and pos[0]+i <= self.dim[0]-1 and (self.mat[pos[0]+i][pos[1]-1] != 0 or self.mat[pos[0]+i][pos[1]+1] != 0):
                        check_along = False
            if check == len(word) and free_around_f and free_around_e and check_along:
                return True
            return False
    

def find_size(li):
    min_s = 0
    for item in li:
        length = len(item[0])
        if length > min_s:
            min_s = length
    return min_s


def get_words():
    link = "https://www.recy.net/lexique.php"
    webpage_source = requests.get(link)
    webpage = webpage_source.content
    eco = BeautifulSoup(webpage, "html.parser")
    website = eco.find_all("p", {"class": "txt"})
    content = []
    limit = 35
    for element in website:
        if len(content) < limit:
            link = element.find("b")
            name = link.text
            definition = element.text.split(":")[1].split(".")[0]
            text = name.split(":")
            content.append([text[0].split(" ")[0], definition])
    return content

# ["ecologie", "foret", "aventure", "ruisseau", "chemin", "eolienne", "solaire", "nature"]
# list_mots = ['Association', 'Bactérie', 'Biodiversité', 'Biotope', 'Bordereau', 'Boue', 'Centrale', 'Charbon', 'Chaufferie', 'Combustibles', 'Compétition', 'Compostage', 'Débit', 'Déchet', 'Déclaration', 'Décomposeur', 'Dépôt', 'Développement', 'Directive', 'Eau', 'Éco-Emballages', 'Écocitoyen', 'Écologie', 'Écosystème', 'Effet', 'Effluent', 'Energie', 'Étude', 'Fiche']
# list_mots = get_words()

def initiliaze_game(list_mots=None):
    if list_mots == None:
        list_mots = text.main_text
    random.shuffle(list_mots)
    min_size = find_size(list_mots)
    print(min_size)
    threshold_rows, theshold_col = 5, 5
    dim = (min_size+threshold_rows, min_size+theshold_col)
    mots = MotsCroises(dim, list_mots)
    mots.first_words()
    print(mots.mat)
    mots.insert_words()
    print(mots.mat)
    # mots.print_table()
    return mots

# initiliaze_game()