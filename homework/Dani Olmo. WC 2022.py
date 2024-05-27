#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 11:19:09 2024

@author: g.m.bykov
"""

from statsbombpy import sb
import pandas as pd

# Get WC 2022
competitions = sb.competitions()
wc = competitions.loc[competitions["competition_id"] == 43]

#%%

# Get all matches of Spain
# WC 2022
matches = sb.matches(competition_id = 43, season_id = 106)
# Filter only Spain matches
spain_matches_mask = (matches["home_team"] == "Spain") | (matches["away_team"] == "Spain")
spain_matches = matches.loc[spain_matches_mask]

#%%

# Create function to simplify getting data of different types.
def filter_events_by_player_and_type(df, columns, player: str, event_type: str):
    dani_olmo_event_mask = (df["player"] == player) & (df["type"] == event_type)
    return df.loc[dani_olmo_event_mask, columns]

# Get ALL events from Spain matches
all_spain_events = pd.DataFrame()

for match_id in spain_matches['match_id']:
    match_events = sb.events(match_id = match_id)
    all_spain_events = pd.concat([all_spain_events, match_events], ignore_index=True)

#%%
all_spain_shots_mask = (all_spain_events["type"] == "Shot") & (all_spain_events["team"] == "Spain")
all_spain_shots = all_spain_events.loc[all_spain_shots_mask, ['team', 'player', 'minute', 'second', 'type', 'location']]

dani_olmo_shots = filter_events_by_player_and_type(
     df=all_spain_events,
     columns=['team', 'player', 'minute', 'second', 'type', 'location', 'shot_end_location', 'shot_outcome', 'shot_type', 'shot_statsbomb_xg'],
     player="Daniel Olmo Carvajal",
     event_type="Shot"
)