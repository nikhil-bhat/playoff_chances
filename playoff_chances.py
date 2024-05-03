"""
written by noktor
"""
import requests
import re
import json
from pprint import pprint
from collections import defaultdict

points_table = defaultdict(int)
match_history = []
remaining_matches = []

outcomes = []

class Outcome:
  
  def __init__(self,team_points, history):
    self.team_points = team_points
    self.history = history

def playoff_predictor(team_name):
   team_chances = 0
   for outcome in outcomes:
      sorted_team_points = sorted(outcome.team_points.items(), key=lambda item: item[1],reverse=True)[0:4]
      for team,points in sorted_team_points:
         if team == team_name:
            #print(f"{sorted_team_points}, {outcome.history}")
            team_chances+=1
   playoff_chance_team = (team_chances/len(outcomes)) *100          
   print(f"{team_name} playoff chances are {playoff_chance_team}") 
   
def get_outcome(team_points,rem_matches,history):
    
    team1,team2 = rem_matches[0]
    team1win_his = history[:]
    team1win_teamp = team_points.copy()
    team1win_teamp[team1] += 2
    team1win_his.append(f"possibily {team1} wins vs {team2}")
    team2win_his = history[:]
    team2win_teamp = team_points.copy()
    team2win_teamp[team2] += 2
    team2win_his.append(f"possibily {team2} wins vs {team1}")
    
    if len(rem_matches) == 1:
       outcomes.append(Outcome(team1win_teamp, team1win_his))
       outcomes.append(Outcome(team2win_teamp, team2win_his))  
    else:
      get_outcome(team1win_teamp, rem_matches[1:], team1win_his)
      get_outcome(team2win_teamp, rem_matches[1:], team2win_his)

      
    

r = requests.get("https://ipl-stats-sports-mechanic.s3.ap-south-1.amazonaws.com/ipl/feeds/148-matchschedule.js")
data = r.text

match = re.search("\w\((.*)\);",data)
if match:
   json_data = json.loads(match.group(1))
   for m  in json_data["Matchsummary"]:
        if m["MatchStatus"] == "Post":
          fbtc = m["FirstBattingTeamCode"]
          sbtc = m["SecondBattingTeamCode"]
          if int(m["WinningTeamID"]) == int(m["FirstBattingTeamID"]):
             points_table[m["FirstBattingTeamCode"]] +=2
             match_history.append(f"{fbtc} wins vs {sbtc}")
          elif int(m["WinningTeamID"]) == int(m["SecondBattingTeamID"]):
             points_table[m["SecondBattingTeamCode"]] +=2
             match_history.append(f"{sbtc} wins vs {fbtc}")
        elif m["MatchStatus"] == "UpComing" and m["FirstBattingTeamCode"] !="TBD":
          remaining_matches.append((m["FirstBattingTeamCode"],m["SecondBattingTeamCode"]))
  
   pprint(points_table)
   pprint(match_history)
   pprint(len(remaining_matches))

   get_outcome(points_table, remaining_matches, match_history)
   
   playoff_predictor("MI")
   playoff_predictor("PBKS")
   playoff_predictor("RCB")
   playoff_predictor("CSK")
          
                                         
