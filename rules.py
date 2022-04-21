import numpy as np
import darknet
import Lane.util as util
import time
import math

class Rule():
    def __init__(self, SetStatusObjs = [], StatusLines = [], StatusBoxes = [], objs_disappear = []):

        self.StatusObjs = SetStatusObjs
        self.StatusLines = StatusLines
        self.objs_disappear = objs_disappear
        self.StatusBoxes = StatusBoxes
        self.tweakAngle = None
        self.speed = None
        self.flag = False
        self.time = 0
        self.point_in_lane = 0
        self.fits = None




    def update(self, SetStatusObjs, StatusLines, StatusBoxes, objs_disappear, point_in_lane, fits ):
        self.StatusObjs = SetStatusObjs
        self.StatusLines = StatusLines
        self.StatusBoxes = StatusBoxes
        self.objs_disappear = objs_disappear
        self.point_in_lane = point_in_lane
        self.fits = fits
        # self.fps = fps 
        

    def get_result(self):
        return self.tweakAngle, self.speed

    def handle(self):
        
        if self.flag is not False:
            print(self.StatusObjs, self.StatusLines, self.objs_disappear)
            if (all(np.array(self.StatusLines[-3:]) >= 2) and self.time < 10) or self.time <= 0:
                print("stoped flag handle")
                self.flag = False
                self.tweakAngle = None
                self.speed = None

            if self.flag == 'i12':
                if 'i5' in self.StatusObjs[-1]:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 )
                    y_center = int(( top + bottom ) / 2 )
                    if x_center < 256:
                        self.tweakAngle = util.errorAngle((x_center + 120, y_center)) 
                        self.speed = 5
                        self.time = int(math.sqrt(((25*25 + 180 * 5**2 ) * 250) /(5**4))) - 20
                        # self.time = 
                    # print('i5 after p12')
                    # self.speed = 5
                    # v = self.speed
                    # self.tweakAngle = -25
                    # self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 250) /(v**4))) - 5
            self.time -= 1

        else:
            if 'i10' in self.objs_disappear:
                self.handle_i10()
                self.flag = 'i10'
                # if 'i5' in self.StatusObjs[-1]:
                #     index = list(self.StatusObjs[-1]).index('i5')
                #     bbox_i5 = self.StatusBoxes[-1][index]
                #     left, top, right, bottom = darknet.bbox2points(bbox_i5)
                #     x_center = int(( left + right ) / 2 / 416 * 512)
                #     # x_center = int(( left + right ) / 2)
                #     if x_center > 300 and x_center < 512:
                #         self.tweakAngle = util.errorAngle((x_center + 40, 128))
                #         self.speed = 30
                #         self.time = 15
                # else:
                # self.tweakAngle += 8
                if 'i5' in self.StatusObjs[-1]:
                    print('i5 after p14')
                    # self.tweakAngle += 8
                    # self.speed = 5
                    # v = self.speed
                    # self.tweakAngle = 25
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2)
                    y_center = int(( top + bottom ) / 2 )
                    if x_center >= 256:
                        self.tweakAngle = util.errorAngle((x_center + 35, y_center))
                        self.speed = 5
                        self.time = int(math.sqrt(((25*25 + 180 * 5**2 ) * 250) /(5**4))) - 20
                    # self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 200) /(v**4))) - 15
                else :
                    self.speed = 5
                    v = self.speed
                    self.tweakAngle = 25
                    self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 200) /(v**4))) - 15
                
            if 'i12' in self.objs_disappear:
                self.handle_i12()
                self.flag = 'i12'
                self.tweakAngle = -5
                if 'i5' in self.StatusObjs[-1] or 'pne' in self.StatusObjs[-1]:
                    print('i5 after p12')
                    self.speed = 5
                    v = self.speed
                    self.tweakAngle = -25
                    self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 250) /(v**4))) - 5
                else :
                    print('not i5 and pne after i12')
                    self.speed = 5
                    v = self.speed
                    self.tweakAngle = -23
                    self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 200) /(v**4)))  - 20
            if 'i13' in self.objs_disappear:
                self.handle_i13()
                self.flag = 'i13' 
                if 'i5' in self.StatusObjs[-1]:
                    index = list(self.StatusObjs[-1]).index('i5')
                    bbox_i5 = self.StatusBoxes[-1][index]
                    left, top, right, bottom = darknet.bbox2points(bbox_i5)
                    x_center = int(( left + right ) / 2 )
                    if x_center > 200 and x_center < 412:
                        self.tweakAngle = util.errorAngle((x_center + 35, 128))
                        self.speed = 30
                        self.time = 20
                else:
                    self.speed = -10
                    self.tweakAngle = 0
                    self.time = 7
                # else:
                #     self.tweakAngle = 0
                #     self.speed = 50
                #     self.time = 15



            if 'p19' in self.objs_disappear:
                self.handle_p19()
                self.flag = 'p19'
                # if 'i5' in self.StatusObjs[-1]:
                #     index = list(self.StatusObjs[-1]).index('i5')
                #     bbox_i5 = self.StatusBoxes[-1][index]
                #     left, top, right, bottom = darknet.bbox2points(bbox_i5)
                #     x_center = int(( left + right ) / 2 / 224 * 512)
                #     if x_center > 150 and x_center < 462:
                #         self.tweakAngle = util.errorAngle((x_center + 35, 128))
                #         self.speed = 30
                #         self.time = 17

                # elif all(np.array(self.StatusLines[-3:]) < 1):
                #     self.tweakAngle = -25
                #     self.speed = -2
                #     self.time = 30
                # self.tweakAngle = -2
                if all(np.array(self.StatusLines[-3:]) < 3):
                    y = 20
                    avaiable_fit =  np.poly1d(self.fits[0])
                        # check where do line?
                    # temp_y = 200
                    # temp_x = (np.poly1d(self.fits[-1])(temp_y) + np.poly1d(self.fits[-2])(temp_y)) // 2
                    # self.point_in_lane = (temp_x,temp_y)
                    #     # check where do line?
                    point_x = self.point_in_lane[0]
                    point_y = self.point_in_lane[1]
                    val = point_x - avaiable_fit(point_y)
                        # print(avaiable_fit(point_y))
                        # print(val)
                    # print('x:' ,point_x)
                    # print('y:', point_y)
                    print('available_fit:', avaiable_fit)  
                    print('diem x: ', avaiable_fit(point_y))
                    print("val:", val)   
                    # print("val:", val)
                    if int(val) < 0: #val < 225 
                            # self.tweakAngle += 10
                        print('---loss less----')
                        if 'i5' in self.StatusObjs[-3:] or 'pne' in self.StatusObjs[-3:]:
                            print('i5 after p14')
                            self.speed = 20
                            v = 5
                            self.tweakAngle = -25
                            self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 200) /(v**4))) - 20
                        else:    
                            self.speed = 20
                            v = 5
                            self.tweakAngle = -25
                            # self.time = 9
                            # print(int(math.sqrt(((25*25 + 180 * v**2 ) * 50) /(v**4))))
                            self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 200) /(v**4))) -20
                    else :
                        if 'i5' in self.StatusObjs[-1]:
                            index = list(self.StatusObjs[-1]).index('i5')
                            bbox_i5 = self.StatusBoxes[-1][index]
                            print(bbox_i5)
                            left, top, right, bottom = darknet.bbox2points(bbox_i5)
                            x_center = int(( left + right ) / 2 )
                            if x_center > 150 and x_center < 462:
                                self.tweakAngle = util.errorAngle((x_center + 35, 128))
                                self.speed = 30
                                self.time = 17
                            else :
                                self.speed = 15
                                self.tweakAngle = 0

                else:
                    if 'i5' in self.StatusObjs[-1]:
                            index = list(self.StatusObjs[-1]).index('i5')
                            bbox_i5 = self.StatusBoxes[-1][index]
                            print(bbox_i5)
                            left, top, right, bottom = darknet.bbox2points(bbox_i5)
                            x_center = int(( left + right ) / 2 )
                            if x_center > 150 and x_center < 462:
                                self.tweakAngle = util.errorAngle((x_center + 35, 128))
                                self.speed = 30
                                self.time = 17
                    else:
                                self.tweakAngle = 3
                                self.speed = 30


            if 'p23' in self.objs_disappear:
                self.handle_p23()
                self.flag = 'p23'
                # if 'i5' in self.StatusObjs[-1]:
                #     index = list(self.StatusObjs[-1]).index('i5')
                #     bbox_i5 = self.StatusBoxes[-1][index]
                #     print(bbox_i5)
                #     left, top, right, bottom = darknet.bbox2points(bbox_i5)
                #     x_center = int(( left + right ) / 2 / 224 * 512)
                #     if x_center > 150 and x_center < 462:
                #         self.tweakAngle = util.errorAngle((x_center + 35, 128))
                #         self.speed = 30
                #         self.time = 17
                # self.tweakAngle = 2
                if all(np.array(self.StatusLines[-3:]) < 3):
                    y = 20
                    avaiable_fit =  np.poly1d(self.fits[0])
                    # temp_y = 200
                    # temp_x = (np.poly1d(self.fits[-1])(temp_y) + np.poly1d(self.fits[-2])(temp_y)) // 2
                    # self.point_in_lane = (temp_x,temp_y)
                    #     # check where do line?
                    point_x = self.point_in_lane[0]
                    point_y = self.point_in_lane[1]
                    val = point_x - avaiable_fit(point_y)
                        # print(avaiable_fit(point_y))
                        # print(val)
                    print('x:' ,point_x)
                    print('y:', point_y)
                    print('available_fit:', avaiable_fit)  
                    print('diem x: ', avaiable_fit(point_y))
                    print("val:", val)  
                    # print("val:", val)
                    if int(val) > 0: #val < 225 
                            # self.tweakAngle += 10
                        print('---loss right----')
                        if 'i5' in self.StatusObjs[-1]:
                            index = list(self.StatusObjs[-1]).index('i5')
                            bbox_i5 = self.StatusBoxes[-1][index]
                            print(bbox_i5)
                            left, top, right, bottom = darknet.bbox2points(bbox_i5)
                            x_center = int(( left + right ) / 2 )
                            if x_center > 150 and x_center < 462:
                                self.tweakAngle = util.errorAngle((x_center + 35, 128))
                                self.speed = 30
                                self.time = 17
                        else:    
                            self.speed = 30
                            self.tweakAngle = 25
                            # self.time = 9
                            # print(int(math.sqrt(((25*25 + 180 * v**2 ) * 50) /(v**4))))
                            self.time = int(math.sqrt(((25*25 + 180 * 5**2 ) * 200) /(5**4))) -20
                    else :
                        if 'i5' in self.StatusObjs[-1]:
                            index = list(self.StatusObjs[-1]).index('i5')
                            bbox_i5 = self.StatusBoxes[-1][index]
                            print(bbox_i5)
                            left, top, right, bottom = darknet.bbox2points(bbox_i5)
                            x_center = int(( left + right ) / 2)
                            if x_center > 150 and x_center < 462:
                                self.tweakAngle = util.errorAngle((x_center + 35, 128))
                                self.speed = 30
                                self.time = 17
                        else:
                                self.tweakAngle = 0
                                self.speed = 20
                else:

                    if 'i5' in self.StatusObjs[-1]:
                            index = list(self.StatusObjs[-1]).index('i5')
                            bbox_i5 = self.StatusBoxes[-1][index]
                            print(bbox_i5)
                            left, top, right, bottom = darknet.bbox2points(bbox_i5)
                            x_center = int(( left + right ) / 2 )
                            if x_center > 150 and x_center < 462:
                                self.tweakAngle = util.errorAngle((x_center + 35, 128))
                                self.speed = 30
                                self.time = 17
                    else:
                                self.tweakAngle = 3
                                self.speed = 30

                    # else:
                    #     print('----loss left--- ')
                        
                    #         # self.tweakAngle -= 10
                        
                    #     if 'i5' in self.StatusObjs[-3:] or 'pne' in self.StatusObjs[-3:]:
                    #         print('i5 after p14')
                    #         self.speed = 5
                    #         v = self.speed 
                    #         self.tweakAngle = -25
                    #         self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 200) /(v**4))) -20
                    #     else:
                    #         self.speed = 5
                    #         v = self.speed
                    #         self.tweakAngle = -20
                    #         # print(int(math.sqrt(((25*25 + 180 * v**2 ) * 50) /(v**4)))) 
                    #         self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 200) /(v**4))) -20

                # elif all(np.array(self.StatusLines[-3:]) < 1):
                #     self.tweakAngle = 25
                #     self.speed = -2
                #     self.time = 30

            if 'p14' in self.objs_disappear:
                self.handle_p14()
                self.flag = 'p14'
                if all(np.array(self.StatusLines[-3:]) < 3):
                    y = 20
                    avaiable_fit =  np.poly1d(self.fits[0])
                        # check where do line?
                    # temp_y = 200
                    # temp_x = (np.poly1d(self.fits[-1])(temp_y) + np.poly1d(self.fits[-2])(temp_y)) // 2
                    # self.point_in_lane = (temp_x,temp_y)
                    #     # check where do line?
                    point_x = self.point_in_lane[0]
                    point_y = self.point_in_lane[1]
                    val = point_x - avaiable_fit(point_y)
                        # print(avaiable_fit(point_y))
                        # print(val)
                    print('point_X:', point_x)
                    print('point_y:', point_y)
                    print('available_fit:', avaiable_fit)  
                    print('diem x: ', avaiable_fit(point_y))
                    print("val:", val)
                    if int(val) > 0: #val > 260
                            # self.tweakAngle += 10
                        print('---loss right----')
                        # self.speed = 30
                        if 'i5' in self.StatusObjs[-1]:
                            index = list(self.StatusObjs[-1]).index('i5')
                            bbox_i5 = self.StatusBoxes[-1][index]
                            left, top, right, bottom = darknet.bbox2points(bbox_i5)
                            x_center = int(( left + right ) / 2 )
                            if x_center > 200 and x_center < 412:
                                self.tweakAngle = util.errorAngle((x_center + 35, 128))
                                self.speed = 50
                                # self.time = 20
                                self.time = int(math.sqrt(((25*25 + 180 * 5**2 ) * 200) /(5**4))) - 20
                        else:    
                            self.speed = 50
                            self.tweakAngle = 25
                            # self.time = 9
                            # print(int(math.sqrt(((25*25 + 180 * v**2 ) * 50) /(v**4))))
                            self.time = int(math.sqrt(((25*25 + 180 * 5**2 ) * 200) /(5**4))) - 20
                    else:
                        print('----loss left--- ')
                        # self.speed = 30
                        if 'i5' in self.StatusObjs[-1]:
                            index = list(self.StatusObjs[-1]).index('i5')
                            bbox_i5 = self.StatusBoxes[-1][index]
                            left, top, right, bottom = darknet.bbox2points(bbox_i5)
                            x_center = int(( left + right ) / 2 )
                            if x_center > 200 and x_center < 412:
                                self.tweakAngle = util.errorAngle((x_center + 100, 128))
                                self.speed = 50
                                # self.time = 20
                                self.time = int(math.sqrt(((25*25 + 180 * 5**2 ) * 250) /(5**4))) - 15
                        else:
                            self.tweakAngle = -20
                            self.speed = 60
                            v = 5
                            # print(int(math.sqrt(((25*25 + 180 * v**2 ) * 50) /(v**4)))) 
                            self.time = int(math.sqrt(((25*25 + 180 * v**2 ) * 250) /(v**4))) - 15 + 3
                

    
    def handle_i10(self):
        print("handle_i10")
        self.flag = False
        self.tweakAngle = None
        self.speed = None
    
    def handle_i12(self):
        print("handle_i12")
        self.flag = False
        self.tweakAngle = None
        self.speed = None

    def handle_i13(self):
        print("handle_i13")
        self.flag = False
        self.tweakAngle = None
        self.speed = None

    def handle_p19(self):
        print("handle_p19")
        self.flag = False
        self.tweakAngle = None
        self.speed = None

    def handle_p23(self):
        print("handle_p23")
        self.flag = False
        self.tweakAngle = None
        self.speed = None        

    def handle_p14(self):
        print("handle_p14")
        self.flag = False
        self.tweakAngle = None
        self.speed = None
