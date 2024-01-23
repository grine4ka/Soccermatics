#Load in Statsbomb competition and match data
#This is a library for loading json files.
import json

#Load the competition file
#Got this by searching 'how do I open json in Python'
with open('Statsbomb/data/competitions.json') as f:
    competitions = json.load(f)
    
# World Cup 2022 has competition_id=43 and season_id=106
competition_id=43

#Load the list of matches for this competition
with open('Statsbomb/data/matches/'+str(competition_id)+'/106.json') as f:
    matches = json.load(f)

#Look inside matches
matches[0]
matches[0]['home_team']
matches[0]['home_team']['home_team_name']
matches[0]['away_team']['away_team_name']

# Print all match results
# Exercise #1, print out the result list for the Mens World cup
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    home_score=match['home_score']
    away_score=match['away_score']
    describe_text = 'The match between ' + home_team_name + ' and ' + away_team_name
    result_text = ' finished ' + str(home_score) +  ' : ' + str(away_score)
    print(describe_text + result_text)

# Now lets find a match we are interested in
# Exercise #2, find the ID for Argentina vs. France
home_team_required = "Argentina"
away_team_required = "France"

# Find ID for the match
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==home_team_required) and (away_team_name==away_team_required):
        match_id_required = match['match_id']
        break
print(home_team_required + ' vs ' + away_team_required + ' has id:' + str(match_id_required))

#Exercise #3, Write new code to write out a list of just Argentina's results in the tournament.
team_name_required = "Argentina"
print("All matches for " + team_name_required + " are:")
sorted_matches = sorted(matches, key=lambda x:x['match_id'])

for match in sorted_matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name == team_name_required) or (away_team_name == team_name_required):
        home_score=match['home_score']
        away_score=match['away_score']
        describe_text = 'The match between ' + home_team_name + ' and ' + away_team_name
        stage_text = ' was on stage ' + match['competition_stage']['name'] + ' and'
        result_text = ' finished ' + str(home_score) +  ' : ' + str(away_score)
        print(describe_text + stage_text + result_text)

