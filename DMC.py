#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import math

class DMC:
    
    dmc = {}
    
    def __init__(self):
        with open('dmc_dict.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.dmc = {rows[0]: [int(rows[1]), int(rows[2]), int(rows[3]), rows[4], rows[0]] for rows in reader}
    
    def get_colour_code(self, colour):
        temp_dist = 99999999
        code = ''
        for key in self.dmc:
            dist = self.euclidean_distance(self.dmc[key], colour)
            if dist < temp_dist:
                code = key
                temp_dist = dist
        return self.dmc[code]
    
    def get_colour_code_corrected(self, colour):
        temp_dist = 99999999
        code = ''
        for key in self.dmc:
            dist = self.euclidean_distance_corrected(self.dmc[key], colour)
            if dist < temp_dist:
                code = key
                temp_dist = dist
        #print(code)
        #return ((self.dmc[code][0],self.dmc[code][1],self.dmc[code][2]))
        return self.dmc[code]
        
    def get_dmc_rgb_triple(self, colour):
        dmc_item = self.get_colour_code_corrected(colour)
        return (dmc_item[0], dmc_item[1], dmc_item[2])
            
    def euclidean_distance(self, c1, c2):
        (r1, g1, b1, name, code) = c1
        r2, g2, b2 = c2
        return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

    def euclidean_distance_corrected(self, c1, c2):
        (r1, g1, b1, name, code) = c1
        (r2, g2, b2) = c2
        return math.sqrt(2 * ((r1-r2)**2) + 4*((g1-g2)**2) + 3*((b1-b2)**2))
        #return ((r1 - r2) * 0.3) ** 2 + ((g1 - g2) * 0.59) ** 2 + ((b1 - b2) * 0.11) ** 2


    
        


    
    

        



    
    
