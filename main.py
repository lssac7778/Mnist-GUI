# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 21:52:56 2019

@author: Isaac
"""
import pygame
import numpy as np
from skimage.transform import resize
from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import time

def printFont(string , color_tuple , size , pos_tuple, screen):
    fontObj = pygame.font.Font('Maplestory Light.ttf' , size)
    textSurfaceObj = fontObj.render(string, True, color_tuple)
    textRectObj = textSurfaceObj.get_rect()    
    textRectObj.center = pos_tuple
    screen.blit(textSurfaceObj, textRectObj)

def Eways(x,y, line_dis):
    dline_dis = 2*line_dis
    result1 = [[x+line_dis, y+line_dis],
              [x-line_dis, y+line_dis],
              [x+line_dis, y-line_dis],
              [x-line_dis, y-line_dis],
              [x, y+line_dis],
              [x, y-line_dis],
              [x+line_dis, y],
              [x-line_dis, y],]
              
    result2 = [[x+dline_dis, y+dline_dis],
              [x-dline_dis, y+dline_dis],
              [x+dline_dis, y-dline_dis],
              [x-dline_dis, y-dline_dis],
              [x, y+dline_dis],
              [x, y-dline_dis],
              [x+dline_dis, y],
              [x-dline_dis, y]]
    
    return result1, result2

def main(predict_number):
    pygame.init() 
    line_dis = 20
    img_width, img_height = 28,28
    extra_wid = 70
    width, height = line_dis*img_width + extra_wid, line_dis*img_height
    pane_array = np.zeros((img_width, img_height))

    screen=pygame.display.set_mode((width, height))
    pygame.display.set_caption('Num_recog')

    BLACK = (0,0,0)
    semiBLACK = (150,150,150)
    WHITE = (255,255,255)
    BLUE = (84, 77, 207)
    PURPLE = (130, 0, 255)
    RED = (255,0,0)
    WRED = (253, 113, 91)
    WBROWN = (255,191,0)
    LEFT = 1

    prediction_flag = 0
    prediction_interval = 50

    num = 0
    LEFTbuttondown = False
    Quit = False
    write_mode = True
    Rects = []
    semiRects = []
    semisemiRects = []
    while not Quit:
        screen.fill(WHITE)
        
        
        # 가로선 긋기
        for i in range(img_height + 1):
            pygame.draw.line(screen, semiBLACK, (0, i*line_dis), (line_dis*img_width, i*line_dis))
        for i in range(img_width + 1):
            pygame.draw.line(screen, semiBLACK, (i*line_dis, 0), (i*line_dis, line_dis*img_height))
    #    for rect in semisemiRects:
    #        pygame.draw.rect(screen, semiBLACK, rect)
        for rect in semiRects:
            pygame.draw.rect(screen, semiBLACK, rect)
        for rect in Rects:
            pygame.draw.rect(screen, BLACK, rect)
            
        # 버튼 그리기 
        pygame.draw.rect(screen, BLACK, pygame.Rect((width - extra_wid + 10,10), (50, 140)))
        printFont('지', WHITE, 32, (width - extra_wid + 35,40), screen)
        printFont('우', WHITE, 32, (width - extra_wid + 35,80), screen)
        printFont('개', WHITE, 32, (width - extra_wid + 35,120), screen)
        # 글자 쓰기
        
        printFont(str(num), BLACK, 32, (width - extra_wid + 35,190), screen)
        
        pygame.display.flip()
        for event in pygame.event.get():
            prediction_flag += 1
            if prediction_flag % prediction_interval==0:
                num = predict_number(pane_array.copy())


        # check if the event is the X button
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                Quit = True
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                x = event.pos[0]
                y = event.pos[1]
                if width - extra_wid + 10 < x and x < width - extra_wid + 60 and 10 < y and y < 140:
                    Rects = []
                    semiRects = []
                    semisemiRects = []
                    pane_array = np.zeros((img_width, img_height))
                    num = 0
                else:
                    LEFTbuttondown = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                LEFTbuttondown = False
                
            if event.type == pygame.MOUSEMOTION and LEFTbuttondown:
                x = event.pos[0]
                y = event.pos[1]

                #num = predict_number(pane_array.copy())
                
                if x < width - extra_wid:
                    x = x - x%line_dis
                    y = y - y%line_dis
                    rect = pygame.Rect((x,y), (line_dis, line_dis))
                    
                    arr_x = int(x/line_dis)
                    arr_y = int(y/line_dis)
                    if write_mode:
                        ways1, ways2 = Eways(x,y, line_dis)
                        Rects.append(rect)
                        pane_array[arr_y][arr_x] = 1
                        #semiRects
                        for way in ways1:
                            semiRects.append(pygame.Rect((way[0],way[1]), (line_dis, line_dis)))
                            
                            temp_x, temp_y = int(way[0]/line_dis), int(way[1]/line_dis)
                            if 0>temp_x or 27<temp_x or 0>temp_y or 27<temp_y:
                                continue
                            if pane_array[temp_y][temp_x]==0:
                                pane_array[temp_y][temp_x] += 0.5
                        # semisemiRects
    #                    for way in ways2:
    #                        semisemiRects.append(pygame.Rect((way[0],way[1]), (line_dis, line_dis)))
    #                        
    #                        temp_x, temp_y = int(way[0]/line_dis), int(way[1]/line_dis)
    #                        if 0>temp_x or 27<temp_x or 0>temp_y or 27<temp_y:
    #                            continue
    #                        if pane_array[temp_y][temp_x]==0:
    #                            pane_array[temp_y][temp_x] += 0.5
                    elif rect in Rects:
                        del Rects[Rects.index(rect)]
                        pane_array[arr_y][arr_x] = 0
            
if __name__ == "__main__":
    from model import *
    predictor = torch_predictor()
    main(predictor)


