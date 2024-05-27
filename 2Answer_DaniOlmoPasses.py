#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:54:10 2024

@author: g.m.bykov
"""

# Make a pass map using Statsbomb data
# Set match id in match_id_required.

## Imports
import json
import matplotlib.pyplot as plt
import pandas as pd
from FCPython import createPitch
import numpy as np

## GET DATA FROM STATSBOMB

# ID for Spain vs Costa Rica World Cup 2022 (7-0)
match_id_required = 3857291
home_team_required ="Spain"
away_team_required ="Costa Rica"

# Load in the data
# I took this from https://znstrider.github.io/2018-11-11-Getting-Started-with-StatsBomb-Data/
file_name=str(match_id_required)+'.json'

# Load in all match events 
with open('Statsbomb/data/events/'+file_name) as data_file:
    data = json.load(data_file)

## CLEAR DATA
# Get the nested structure into a dataframe 
# Store the dataframe in a dictionary with the match id as key (remove '.json' from string)

df = pd.json_normalize(data, sep = "_").assign(match_id = file_name[:-5])

# A dataframe of passes
mask_home_team_passes = (df['type_name'] == 'Pass') & (df['team_name'] == home_team_required)

df_passes_home = df.loc[mask_home_team_passes, ['team_name', 'player_name', 'minute', 'second', 'type_name', 'pass_outcome_name', 'location', 'pass_end_location']]

# Split location column to x, y columns, and drop location column
df_passes_home[['x','y']] = df_passes_home['location'].to_list()
df_passes_home.drop('location', axis=1, inplace=True)

# Split pass_end_location column to endX and endY columns, and drop pass_end_location column
df_passes_home[['endX','endY']] = df_passes_home['pass_end_location'].to_list()
df_passes_home.drop('pass_end_location', axis=1, inplace=True)

# Fill NaN at pass_outcome column with Successful string
df_passes_home['pass_outcome_name'] = df_passes_home['pass_outcome_name'].fillna('Successful')

# Rename pass_outcome column to just outcome
df_passes_home.rename(columns={'pass_outcome_name': 'outcome'}, inplace=True)

# Filter only Dani Olmo's passes
mask_dani_olmo = df_passes_home['player_name'] == "Daniel Olmo Carvajal"
df_passes_dani_olmo = df_passes_home.loc[mask_dani_olmo].reset_index()


## DRAW THE PITCH

# Size of the pitch in yards (!!!)
pitchLengthX=120
pitchWidthY=80

(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')


## PLOT THE PASSES FOR DANI OLMO
for i, df_pass in df_passes_dani_olmo.iterrows():
    complete = df_pass['outcome'] == 'Successful'
    
    if complete:
        x_line = df_pass['x'], df_pass['endX']
        y_line = pitchWidthY-df_pass['y'], pitchWidthY-df_pass['endY']
        plt.plot(x_line, y_line, color='green')
        plt.scatter(df_pass['x'], pitchWidthY-df_pass['y'], color = 'green', s = 15)
    else:
        x_line = df_pass['x'], df_pass['endX']
        y_line = pitchWidthY-df_pass['y'], pitchWidthY-df_pass['endY']
        plt.plot(x_line, y_line, color='red')
        plt.scatter(df_pass['x'], pitchWidthY-df_pass['y'], color = 'red', s = 15)
    
    
plt.title("Dani Olmo Pass Map vs Costa Rica. WC 2022")
     
#fig.set_size_inches(10, 7)
#fig.savefig('Output/Dani Olmo's Passes.pdf', dpi=500) 
#plt.show()

#Exercise: 
#1, Create a dataframe of passes which contains all the passes in the match
#2, Plot the start point of every Spain pass.
#3, Plot only passes made by Dani Olmo (he is Daniel Olmo Carvajal in the database)
#4, Plot arrows to show where the passes we

