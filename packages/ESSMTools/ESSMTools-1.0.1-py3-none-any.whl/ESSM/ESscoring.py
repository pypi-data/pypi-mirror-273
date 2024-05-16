#!/usr/bin/env python
# coding: utf-8

# In[4]:


import geopandas as gpd
import pandas as pd
import os
import numpy as np
from tqdm import tqdm


# ## data

# In[45]:


# change path to relative path - only for publishing
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

path = "./sampleData/ES_scoring/Mireuksan_sample.shp"
sample_data = gpd.read_file(path)


# ## Scoring

# In[31]:


def Scoring(park, score, weight, i):
    sco = (score*weight*park['Own_Area'][i] / park['Cell_Area'][i])
    
    #print("줄:" + str(i) + ", weight:" + str(weight) + ", score: " + str(sco))
    return sco



# In[43]:


def ESScoring(park, togiWe, imsangWe, GuktoWe):
    """
    This function calculates various Ecosystem Scores (ES score) based on three data sources:
    Land Cover Classification (토지피복분류도), Forest Classification (임상도), and National Environment Assessment Map (국토환경성평가지도).
    
    Requirements:
    Input dataframe must have those attributes (columns):
    1) Cell_ID (int): Unique ID of each cell that includes multiple or one polygon.
    2) Cell_Area (float): Area of each cell (grid) that includes multiple or one polygon.
    3) Own_Area (float): Area of each polygon that is included in one cell (grid)
    4) L3_CODE (str): Attribute of Land cover classification (str)
    5) STORUNST, FROR_CD, FRTP_CD, KOFTR_GROU, DMCLS_CD, AGCLS_CD, DNST_CD, HEIGHT: Attributes of Forest classification map (str)
    6) gridcode (str): Attributes of National Environment Assessment Map (str)

    Parameters:
    park (DataFrame): A pandas DataFrame (or geodataframe with geometry) containing 3 data sources
    togiWe (float): Weight for land cover classification.
    imsangWe (float): Weight for forest classification.
    GuktoWe (float): Weight for national environment assessment map.

    Returns:
    DataFrame: The input DataFrame with additional columns for different Ecosystem Scores (ES score).

    The function initializes lists for different ES scores and iterates through each polygon. For example, based on the land cover
    classification (L3_CODE), it allocate designated scores to each polygon based on weight and area, and add 10 types of scores in the ends with new columns.
    The scores are categorized into four groups:
    
    1. Supply scores:
        - Sup_ForestP
        - Sup_MedHurb
        - Sup_Water
    
    2. Regulation scores:
        - Reg_Erosion
        - Reg_Bio
    
    3. Cultural scores:
        - Cul_Landscape
        - Cul_Recre
        - Cul_heritage
    
    4. Support scores:
        - Support_Habitat
        - Support_BioDiv
    
    Examples
    --------
    >>> sampleScored = ScoringByPark(sample_data.copy(), togiWe = 0.5, imsangWe = 0.5, GuktoWe = 1)
    """

    togiWeight = togiWe #토지피복분류도 가중치
    imsangWeight = imsangWe #임상도 가중치
    GuktoWeight = GuktoWe #국토환경성평가지도 가중치

    
    
    Sup_ForestP = []
    Sup_MedHurb = []
    Sup_Water =[]
    #Reg_Carbon = []
    Reg_Erosion = []
    #Reg_WaterQ = []
    Reg_Bio = []
    #Reg_HeatIs = []
    Cul_Landscape = []
    Cul_Recre = []
    Cul_heritage = []
    Support_Habitat = []
    Support_BioDiv = []


    for i in tqdm(range(len(park))):

        Sup_ForestP.append(0)
        Sup_MedHurb.append(0)
        Sup_Water.append(0)
        #Reg_Carbon.append(0)
        Reg_Erosion.append(0)
        #Reg_WaterQ.append(0)
        Reg_Bio.append(0)
        #Reg_HeatIs.append(0)
        Cul_Landscape.append(0)
        Cul_Recre.append(0)
        Cul_heritage.append(0)
        Support_Habitat.append(0)
        Support_BioDiv.append(0)

        # 토지피복분류도
        if park['L3_CODE'][i] == '111':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '112':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '121':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '131':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '132':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '141':
            Cul_Landscape[i] += Scoring(park, 2, togiWeight, i)
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 3, togiWeight, i)
        elif park['L3_CODE'][i] == '151':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '152':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '153':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '154':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '155':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '161':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '162':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '163':
            Cul_heritage[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '211':
            Sup_ForestP[i] += Scoring(park, 6, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 8, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 2, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 4, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 4, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 6, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 4, togiWeight, i)
        elif park['L3_CODE'][i] == '212':
            Sup_ForestP[i] += Scoring(park, 6, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 4, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 8, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 2, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 4, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 4, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 4, togiWeight, i)
        elif park['L3_CODE'][i] == '221':
            Sup_ForestP[i] += Scoring(park, 6, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 8, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 2, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 4, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 4, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 6, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 4, togiWeight, i)
        elif park['L3_CODE'][i] == '222':
            Sup_ForestP[i] += Scoring(park, 6, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 4, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 8, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 2, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 4, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 4, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 4, togiWeight, i)
        elif park['L3_CODE'][i] == '231':
            Sup_ForestP[i] += Scoring(park, 8, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 4, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 5, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 4, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 4, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 6, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 4, togiWeight, i)
        elif park['L3_CODE'][i] == '241':
            Sup_ForestP[i] += Scoring(park, 8, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 7, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 6, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 6, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 7, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 6, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 6, togiWeight, i)
        elif park['L3_CODE'][i] == '251':
            Sup_ForestP[i] += Scoring(park, 5, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 7, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 6, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 5, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 7, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 6, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 6, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, togiWeight, i)
        elif park['L3_CODE'][i] == '252':
            Sup_ForestP[i] += Scoring(park, 6, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 7, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 6, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 6, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 6, togiWeight, i)
        elif park['L3_CODE'][i] == '311':
            Sup_ForestP[i] += Scoring(park, 10, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 4, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 9, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 10, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 9, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 9, togiWeight, i)
        elif park['L3_CODE'][i] == '321':
            Sup_ForestP[i] += Scoring(park, 10, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 2, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 8, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 8, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 10, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 6, togiWeight, i)
        elif park['L3_CODE'][i] == '331':
            Sup_ForestP[i] += Scoring(park, 10, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 3, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 9, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 10, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 10, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 9, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 9, togiWeight, i)
        elif park['L3_CODE'][i] == '411':
            Sup_ForestP[i] += Scoring(park, 6, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 4, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 9, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 9, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 8, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 8, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 8, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 8, togiWeight, i)
        elif park['L3_CODE'][i] == '421':
            Sup_ForestP[i] += Scoring(park, 2, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 7, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 6, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 5, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 8, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 4, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, togiWeight, i)
        elif park['L3_CODE'][i] == '422':
            Sup_ForestP[i] += Scoring(park, 2, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 7, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 6, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 5, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 2, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 4, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 8, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 9, togiWeight, i)
        elif park['L3_CODE'][i] == '423':
            Sup_ForestP[i] += Scoring(park, 4, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 8, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 6, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 5, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, togiWeight, i)
        elif park['L3_CODE'][i] == '511':
            Sup_ForestP[i] += Scoring(park, 1, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 10, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 8, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 10, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 9, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 8, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, togiWeight, i)
        elif park['L3_CODE'][i] == '521':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 9, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 8, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 6, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, togiWeight, i)
        elif park['L3_CODE'][i] == '522':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 5, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 4, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, togiWeight, i)
        elif park['L3_CODE'][i] == '611':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 2, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 3, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 8, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 9, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 9, togiWeight, i)
        elif park['L3_CODE'][i] == '612':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 7, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 2, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 3, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 7, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, togiWeight, i)
        elif park['L3_CODE'][i] == '613':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 2, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 3, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 6, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, togiWeight, i)
        elif park['L3_CODE'][i] == '621':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 1, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 4, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 3, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, togiWeight, i)
        elif park['L3_CODE'][i] == '622':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 1, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 7, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 2, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, togiWeight, i)
        elif park['L3_CODE'][i] == '623':
            Sup_ForestP[i] += Scoring(park, 1, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 1, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 4, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 5, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 3, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '711':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 10, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 10, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 7, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 9, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '712':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 10, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 10, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 7, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 9, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, togiWeight, i)
        elif park['L3_CODE'][i] == '721':
            Sup_ForestP[i] += Scoring(park, 0, togiWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, togiWeight, i)  
            Sup_Water[i] += Scoring(park, 5, togiWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, togiWeight, i)
            Reg_Bio[i] += Scoring(park, 10, togiWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, togiWeight, i)
            Cul_Recre[i] += Scoring(park, 7, togiWeight, i)  
            Cul_heritage[i] += Scoring(park, 9, togiWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, togiWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, togiWeight, i)
            
        #print("Reg_Bio 점수: " + str(i) + "번째: " + str(Reg_Bio[i]) + ", 가중치: " + str(togiWeight))


        # 임상도 - 숫자형인지 object형인지 확인해야 함. 또한 elif인지 그냥 if인지도.
        # Stocked or Unstocked (입목존재)
        if park['STORUNST'][i] == '1':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 10, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['STORUNST'][i] == '2':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 0, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 0, imsangWeight, i)
        elif park['STORUNST'][i] == '0':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        # Forest Origin (임종)
        if park['FROR_CD'][i] == '1':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['FROR_CD'][i] == '2':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i)
        elif park['FROR_CD'][i] == '0':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)

        # Forest Type (임상) 
        if park['FRTP_CD'][i] == '1':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['FRTP_CD'][i] == '2':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['FRTP_CD'][i] == '3':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 4, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i)
        elif park['FRTP_CD'][i] == '4':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 1, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, imsangWeight, i)
        elif park['FRTP_CD'][i] == '5':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)

        # Kind of Tree (수종그룹)
        if park['KOFTR_GROU'][i] == '11':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '12':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '13':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '14':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '15':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '16':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '17':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '18':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '19':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '20':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '21':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '10':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 6, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '31':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '32':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '33':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '34':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '35':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '36':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '37':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '38':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '39':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '40':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '41':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '42':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '43':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '44':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '45':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '46':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '47':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '48':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '49':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '30':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '61':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '62':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '63':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '64':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '65':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '66':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '67':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '68':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '60':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 8, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '77':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 4, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '78':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 2, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 1, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '81':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 8, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 0, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 0, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '82':
            Sup_ForestP[i] += Scoring(park, 0, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 8, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 2, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 0, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 3, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 0, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 0, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '83':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 2, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 0, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 5, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '91':
            Sup_ForestP[i] += Scoring(park, 0, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 0, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 0, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 0, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 0, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 0, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '92':
            Sup_ForestP[i] += Scoring(park, 0, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 8, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 2, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 3, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '93':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 2, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 1, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 2, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '94':
            Sup_ForestP[i] += Scoring(park, 0, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '95':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 6, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 1, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 2, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, imsangWeight, i)
        elif park['KOFTR_GROU'][i] == '99':
            Sup_ForestP[i] += Scoring(park, 0, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 0, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 0, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 0, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 0, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 0, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 0, imsangWeight, i)

        # Diameter Class (경급)
        if park['DMCLS_CD'][i] == '0':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 3, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['DMCLS_CD'][i] == '1':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['DMCLS_CD'][i] == '2':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i)
        elif park['DMCLS_CD'][i] == '3':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 10, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 10, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)

        #Age Class (영급)

        if park['AGCLS_CD'][i] == '1':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 1, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 1, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['AGCLS_CD'][i] == '2':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 3, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['AGCLS_CD'][i] == '3':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 3, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i) 
        elif park['AGCLS_CD'][i] == '4':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i) 
        elif park['AGCLS_CD'][i] == '5':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i) 
        elif park['AGCLS_CD'][i] == '6':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i) 
        elif park['AGCLS_CD'][i] == '7':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i) 
        elif park['AGCLS_CD'][i] == '8':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 10, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 10, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i) 
        elif park['AGCLS_CD'][i] == '9':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 10, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 10, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i) 

        # Crown Density (수관밀도)
        if park['DNST_CD'][i] == 'A':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 3, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i) 
        elif park['DNST_CD'][i] == 'B':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i) 
        elif park['DNST_CD'][i] == 'C':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 10, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i) 

        # Height (수고)
        if park['HEIGHT'][i] == '0':
            Sup_ForestP[i] += Scoring(park, 0, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 0, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 1, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 0, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 0, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, imsangWeight, i) 
        elif park['HEIGHT'][i] == '2':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 9, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 1, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 1, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, imsangWeight, i)
        elif park['HEIGHT'][i] == '4':
            Sup_ForestP[i] += Scoring(park, 1, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 9, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 1, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 1, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['HEIGHT'][i] == '6':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 3, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 3, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 3, imsangWeight, i)
        elif park['HEIGHT'][i] == '8':
            Sup_ForestP[i] += Scoring(park, 3, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 3, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 3, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['HEIGHT'][i] == '10':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['HEIGHT'][i] == '12':
            Sup_ForestP[i] += Scoring(park, 5, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 5, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 5, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 5, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 5, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 5, imsangWeight, i)
        elif park['HEIGHT'][i] == '14':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['HEIGHT'][i] == '16':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['HEIGHT'][i] == '18':
            Sup_ForestP[i] += Scoring(park, 7, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 7, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 3, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 5, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 7, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 7, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i)
        elif park['HEIGHT'][i] == '20':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 10, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 1, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 10, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, imsangWeight, i)
        elif park['HEIGHT'][i] == '22':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 10, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 1, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 10, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)
        elif park['HEIGHT'][i] == '24':
            Sup_ForestP[i] += Scoring(park, 10, imsangWeight, i)
            Sup_MedHurb[i] += Scoring(park, 10, imsangWeight, i)  
            Sup_Water[i] += Scoring(park, 1, imsangWeight, i)
            Reg_Erosion[i] += Scoring(park, 7, imsangWeight, i)
            Reg_Bio[i] += Scoring(park, 3, imsangWeight, i)
            Cul_Landscape[i] += Scoring(park, 10, imsangWeight, i)
            Cul_Recre[i] += Scoring(park, 10, imsangWeight, i)  
            Cul_heritage[i] += Scoring(park, 7, imsangWeight, i)  
            Support_Habitat[i] += Scoring(park, 10, imsangWeight, i)
            Support_BioDiv[i] += Scoring(park, 7, imsangWeight, i)



        # 국토환경성평가지도 - 숫자형인지 object형인지 확인해야 함. - int
        if park['gridcode'][i] == '1':
            Sup_ForestP[i] += Scoring(park, 3, GuktoWeight, i)
            Sup_MedHurb[i] += Scoring(park, 2, GuktoWeight, i)  
            Sup_Water[i] += Scoring(park, 2, GuktoWeight, i)
            Reg_Erosion[i] += Scoring(park, 10, GuktoWeight, i)
            Reg_Bio[i] += Scoring(park, 10, GuktoWeight, i)
            Cul_Landscape[i] += Scoring(park, 9, GuktoWeight, i)
            Cul_Recre[i] += Scoring(park, 8, GuktoWeight, i)  
            Cul_heritage[i] += Scoring(park, 10, GuktoWeight, i)  
            Support_Habitat[i] += Scoring(park, 8, GuktoWeight, i)
            Support_BioDiv[i] += Scoring(park, 10, GuktoWeight, i)
        elif park['gridcode'][i] == '2':
            Sup_ForestP[i] += Scoring(park, 6, GuktoWeight, i)
            Sup_MedHurb[i] += Scoring(park, 6, GuktoWeight, i)  
            Sup_Water[i] += Scoring(park, 4, GuktoWeight, i)
            Reg_Erosion[i] += Scoring(park, 8, GuktoWeight, i)
            Reg_Bio[i] += Scoring(park, 8, GuktoWeight, i)
            Cul_Landscape[i] += Scoring(park, 7, GuktoWeight, i)
            Cul_Recre[i] += Scoring(park, 6, GuktoWeight, i)  
            Cul_heritage[i] += Scoring(park, 8, GuktoWeight, i)  
            Support_Habitat[i] += Scoring(park, 6, GuktoWeight, i)
            Support_BioDiv[i] += Scoring(park, 8, GuktoWeight, i)
        elif park['gridcode'][i] == '3':
            Sup_ForestP[i] += Scoring(park, 9, GuktoWeight, i)
            Sup_MedHurb[i] += Scoring(park, 8, GuktoWeight, i)  
            Sup_Water[i] += Scoring(park, 6, GuktoWeight, i)
            Reg_Erosion[i] += Scoring(park, 6, GuktoWeight, i)
            Reg_Bio[i] += Scoring(park, 4, GuktoWeight, i)
            Cul_Landscape[i] += Scoring(park, 4, GuktoWeight, i)
            Cul_Recre[i] += Scoring(park, 5, GuktoWeight, i)  
            Cul_heritage[i] += Scoring(park, 6, GuktoWeight, i)  
            Support_Habitat[i] += Scoring(park, 4, GuktoWeight, i)
            Support_BioDiv[i] += Scoring(park, 6, GuktoWeight, i)
        elif park['gridcode'][i] == '4':
            Sup_ForestP[i] += Scoring(park, 6, GuktoWeight, i)
            Sup_MedHurb[i] += Scoring(park, 6, GuktoWeight, i)  
            Sup_Water[i] += Scoring(park, 8, GuktoWeight, i)
            Reg_Erosion[i] += Scoring(park, 4, GuktoWeight, i)
            Reg_Bio[i] += Scoring(park, 1, GuktoWeight, i)
            Cul_Landscape[i] += Scoring(park, 3, GuktoWeight, i)
            Cul_Recre[i] += Scoring(park, 4, GuktoWeight, i)  
            Cul_heritage[i] += Scoring(park, 4, GuktoWeight, i)  
            Support_Habitat[i] += Scoring(park, 2, GuktoWeight, i)
            Support_BioDiv[i] += Scoring(park, 4, GuktoWeight, i)
        elif park['gridcode'][i] == '5':
            Sup_ForestP[i] += Scoring(park, 1, GuktoWeight, i)
            Sup_MedHurb[i] += Scoring(park, 1, GuktoWeight, i)  
            Sup_Water[i] += Scoring(park, 1, GuktoWeight, i)
            Reg_Erosion[i] += Scoring(park, 1, GuktoWeight, i)
            Reg_Bio[i] += Scoring(park, 1, GuktoWeight, i)
            Cul_Landscape[i] += Scoring(park, 1, GuktoWeight, i)
            Cul_Recre[i] += Scoring(park, 2, GuktoWeight, i)  
            Cul_heritage[i] += Scoring(park, 1, GuktoWeight, i)  
            Support_Habitat[i] += Scoring(park, 1, GuktoWeight, i)
            Support_BioDiv[i] += Scoring(park, 1, GuktoWeight, i)
                                  
    # New Fields
    park['Sup_ForestP'] = Sup_ForestP
    park['Sup_MedHurb'] = Sup_MedHurb
    park['Sup_Water'] = Sup_Water
    park['Reg_Erosion'] = Reg_Erosion
    park['Reg_Bio'] = Reg_Bio
    park['Cul_Landscape'] = Cul_Landscape
    park['Cul_Recre'] = Cul_Recre
    park['Cul_heritage'] = Cul_heritage
    park['Support_Habitat'] = Support_Habitat
    park['Support_BioDiv'] = Support_BioDiv
    
   # print(park)

    
    return park


# ## Arrange columns

# In[33]:


import pandas as pd

def rearrange_columns(df):
    """
    This function takes a DataFrame (Result of Scoring function) and checks for the existence of specific columns. If the columns
    are present, it rearranges the DataFrame to ensure the specified columns are included and places the 'geometry'
    column at the end.

    Parameters:
    df (DataFrame): A pandas DataFrame containing various columns including the specified ES score columns.

    Returns:
    DataFrame: A DataFrame with the specified columns included and the 'geometry' column moved to the end.
    
    Examples
    --------
    >>> arrangedSample = rearrange_columns(sampleScored)

    """
    # Define the columns of interest
    columns_of_interest = [
        'Cell_Area', 'Cell_ID', 'Own_Area', 'geometry', 
        'Sup_ForestP', 'Sup_MedHurb', 'Sup_Water', 
        'Reg_Erosion', 'Reg_Bio', 
        'Cul_Landscape', 'Cul_Recre', 'Cul_heritage', 
        'Support_Habitat', 'Support_BioDiv'
    ]
    
    # Check if the columns exist in the DataFrame and extract them
    existing_columns = [col for col in columns_of_interest if col in df.columns]
    
    # Ensure 'geometry' is the last column
    if 'geometry' in existing_columns:
        existing_columns.remove('geometry')
        existing_columns.append('geometry')
    
    # Rearrange the DataFrame columns
    arranged_df = df[existing_columns]
    
    return arranged_df


# ## Execution

# In[34]:


# sampleScored = ESScoring(sample_data.copy(), togiWe = 0.5, imsangWe = 0.5, GuktoWe = 1)


# In[35]:


# arrangedSample = rearrange_columns(sampleScored)


# In[36]:


# arrangedSample


# In[ ]:




