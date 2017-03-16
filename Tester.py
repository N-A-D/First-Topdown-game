'''
Created on Mar 15, 2017

@author: Austin
'''
from os import listdir
from os import path
from os.path import isfile, join


onlyfiles = [f for f in listdir(path.dirname("img\\Player animations\\handgun\\idle\\")) if isfile(join(path.dirname('img\\Player animations\\handgun\\idle\\'), f))]
print(len(onlyfiles))
onlyfiles.reverse()
for file in onlyfiles:
    print(file)
    
    
    
list = []
        for name in PLAYER_RIFLE_ANIMATIONS['idle']:
            image = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, name)), (TILESIZE, TILESIZE)).convert_alpha()
            list.append(image)
        PLAYER_RIFLE_ANIMATIONS['idle'] = list
        
        list = []
        for name in PLAYER_RIFLE_ANIMATIONS['melee']:
            image = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, name)), (TILESIZE, TILESIZE)).convert_alpha()
            list.append(image)
        PLAYER_RIFLE_ANIMATIONS['melee'] = list
        
        list = []
        for name in PLAYER_RIFLE_ANIMATIONS['move']:
            image = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, name)), (TILESIZE, TILESIZE)).convert_alpha()
            list.append(image)
        PLAYER_RIFLE_ANIMATIONS['move'] = list
        
        list = []
        for name in PLAYER_RIFLE_ANIMATIONS['reload']:
            image = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, name)), (TILESIZE, TILESIZE)).convert_alpha()
            list.append(image)
        PLAYER_RIFLE_ANIMATIONS['reload'] = list
        
        list = []
        for name in PLAYER_RIFLE_ANIMATIONS['shoot']:
            image = pg.transform.smoothscale(pg.image.load(path.join(self.img_folder, name)), (TILESIZE, TILESIZE)).convert_alpha()
            list.append(image)
        PLAYER_RIFLE_ANIMATIONS['shoot'] = list

        self.player_animations['rifle'] = PLAYER_RIFLE_ANIMATIONS
