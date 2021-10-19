#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import base64
import lxml
import os


# function to retrieve current EPL table
def get_league_table():
    html_content = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text.replace('<!--', '').replace('-->', '')
    df = pd.read_html(html_content)
    return df[0]


# function to retrieve this weeks fixtures
def get_fixtures():
    html_content = requests.get('https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures').text.replace('<!--', '').replace('-->', '')
    df = pd.read_html(html_content)
    return df[0]


#  HERE WE ESTABLISH THE VARIABLES FOUND ON FBREF TO BE CALLED AND ORGANIZED LATER
league = ['rank', 'Squad', 'Matches Played', 'Wins', 'Draws', 'Loses', 'Goals For', 'Goals Against', 'Goal Difference', 'points', 'xG', 'xGA', 'xGD', 'xGD/90']
stats = ["player","nationality","position","squad","age","birth_year","games","games_starts","minutes","goals","assists","pens_made","pens_att","cards_yellow","cards_red","goals_per90","assists_per90","goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","xg","npxg","xa","xg_per90","xa_per90","xg_xa_per90","npxg_per90","npxg_xa_per90"]
stats3 = ["players_used","possession","games","games_starts","minutes","goals","assists","pens_made","pens_att","cards_yellow","cards_red","goals_per90","assists_per90","goals_assists_per90","goals_pens_per90","goals_assists_pens_per90","xg","npxg","xa","xg_per90","xa_per90","xg_xa_per90","npxg_per90","npxg_xa_per90"] 

# goalkeeping(keepers)
keepers = ["player","nationality","position","squad","age","birth_year","games_gk","games_starts_gk","minutes_gk","goals_against_gk","goals_against_per90_gk","shots_on_target_against","saves","save_pct","wins_gk","draws_gk","losses_gk","clean_sheets","clean_sheets_pct","pens_att_gk","pens_allowed","pens_saved","pens_missed_gk"]
keepers3 = ["players_used","games_gk","games_starts_gk","minutes_gk","goals_against_gk","goals_against_per90_gk","shots_on_target_against","saves","save_pct","wins_gk","draws_gk","losses_gk","clean_sheets","clean_sheets_pct","pens_att_gk","pens_allowed","pens_saved","pens_missed_gk"]

# advance goalkeeping(keepers adv)
keepersadv = ["player","nationality","position","squad","age","birth_year","minutes_90s","goals_against_gk","pens_allowed","free_kick_goals_against_gk","corner_kick_goals_against_gk","own_goals_against_gk","psxg_gk","psnpxg_per_shot_on_target_against","psxg_net_gk","psxg_net_per90_gk","passes_completed_launched_gk","passes_launched_gk","passes_pct_launched_gk","passes_gk","passes_throws_gk","pct_passes_launched_gk","passes_length_avg_gk","goal_kicks","pct_goal_kicks_launched","goal_kick_length_avg","crosses_gk","crosses_stopped_gk","crosses_stopped_pct_gk","def_actions_outside_pen_area_gk","def_actions_outside_pen_area_per90_gk","avg_distance_def_actions_gk"]
keepersadv2 = ["minutes_90s","goals_against_gk","pens_allowed","free_kick_goals_against_gk","corner_kick_goals_against_gk","own_goals_against_gk","psxg_gk","psnpxg_per_shot_on_target_against","psxg_net_gk","psxg_net_per90_gk","passes_completed_launched_gk","passes_launched_gk","passes_pct_launched_gk","passes_gk","passes_throws_gk","pct_passes_launched_gk","passes_length_avg_gk","goal_kicks","pct_goal_kicks_launched","goal_kick_length_avg","crosses_gk","crosses_stopped_gk","crosses_stopped_pct_gk","def_actions_outside_pen_area_gk","def_actions_outside_pen_area_per90_gk","avg_distance_def_actions_gk"]

# shooting(shooting)
shooting = ["player","nationality","position","squad","age","birth_year","minutes_90s","goals","pens_made","pens_att","shots_total","shots_on_target","shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]
shooting2 = ["minutes_90s","goals","pens_made","pens_att","shots_total","shots_on_target","shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]
shooting3 = ["goals","pens_made","pens_att","shots_total","shots_on_target","shots_free_kicks","shots_on_target_pct","shots_total_per90","shots_on_target_per90","goals_per_shot","goals_per_shot_on_target","xg","npxg","npxg_per_shot","xg_net","npxg_net"]
passing = ["player","nationality","position","squad","age","birth_year","minutes_90s","passes_completed","passes","passes_pct","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short","passes_pct_short","passes_completed_medium","passes_medium","passes_pct_medium","passes_completed_long","passes_long","passes_pct_long","assists","xa","xa_net","assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","progressive_passes"]
passing2 = ["passes_completed","passes","passes_pct","passes_total_distance","passes_progressive_distance","passes_completed_short","passes_short","passes_pct_short","passes_completed_medium","passes_medium","passes_pct_medium","passes_completed_long","passes_long","passes_pct_long","assists","xa","xa_net","assisted_shots","passes_into_final_third","passes_into_penalty_area","crosses_into_penalty_area","progressive_passes"]

# pass types(passing_types)
passing_types = ["player","nationality","position","squad","age","birth_year","minutes_90s","passes","passes_live","passes_dead","passes_free_kicks","through_balls","passes_pressure","passes_switches","crosses","corner_kicks","corner_kicks_in","corner_kicks_out","corner_kicks_straight","passes_ground","passes_low","passes_high","passes_left_foot","passes_right_foot","passes_head","throw_ins","passes_other_body","passes_completed","passes_offsides","passes_oob","passes_intercepted","passes_blocked"]
passing_types2 = ["passes","passes_live","passes_dead","passes_free_kicks","through_balls","passes_pressure","passes_switches","crosses","corner_kicks","corner_kicks_in","corner_kicks_out","corner_kicks_straight","passes_ground","passes_low","passes_high","passes_left_foot","passes_right_foot","passes_head","throw_ins","passes_other_body","passes_completed","passes_offsides","passes_oob","passes_intercepted","passes_blocked"]

# goal and shot creation(gca)
gca = ["player","nationality","position","squad","age","birth_year","minutes_90s","sca","sca_per90","sca_passes_live","sca_passes_dead","sca_dribbles","sca_shots","sca_fouled", "sca_def","gca","gca_per90","gca_passes_live","gca_passes_dead","gca_dribbles","gca_shots","gca_fouled","gca_def"]
gca2 = ["sca","sca_per90","sca_passes_live","sca_passes_dead","sca_dribbles","sca_shots","sca_fouled","sca_def","gca","gca_per90","gca_passes_live","gca_passes_dead","gca_dribbles","gca_shots","gca_fouled","gca_def"]

# defensive actions(defense)
defense = ["player","nationality","position","squad","age","birth_year","minutes_90s","tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd","dribble_tackles","dribbles_vs","dribble_tackles_pct","dribbled_past","pressures","pressure_regains","pressure_regain_pct","pressures_def_3rd","pressures_mid_3rd","pressures_att_3rd","blocks","blocked_shots","blocked_shots_saves","blocked_passes","interceptions","clearances","errors"]
defense2 = ["tackles","tackles_won","tackles_def_3rd","tackles_mid_3rd","tackles_att_3rd","dribble_tackles","dribbles_vs","dribble_tackles_pct","dribbled_past","pressures","pressure_regains","pressure_regain_pct","pressures_def_3rd","pressures_mid_3rd","pressures_att_3rd","blocks","blocked_shots","blocked_shots_saves","blocked_passes","interceptions","clearances","errors"]

# possession(possession)
possession = ["player","nationality","position","squad","age","birth_year","minutes_90s","touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd","touches_att_pen_area","touches_live_ball","dribbles_completed","dribbles","dribbles_completed_pct","players_dribbled_past","nutmegs","carries","carry_distance","carry_progressive_distance","progressive_carries","carries_into_final_third","carries_into_penalty_area","pass_targets","passes_received","passes_received_pct","miscontrols","dispossessed"]
possession2 = ["touches","touches_def_pen_area","touches_def_3rd","touches_mid_3rd","touches_att_3rd","touches_att_pen_area","touches_live_ball","dribbles_completed","dribbles","dribbles_completed_pct","players_dribbled_past","nutmegs","carries","carry_distance","carry_progressive_distance","progressive_carries","carries_into_final_third","carries_into_penalty_area","pass_targets","passes_received","passes_received_pct","miscontrols","dispossessed"]

# playing time(playing time)
playingtime = ["player","nationality","position","squad","age","birth_year","minutes_90s","games","minutes","minutes_per_game","minutes_pct","games_starts","minutes_per_start","games_subs","minutes_per_sub","unused_subs","points_per_match","on_goals_for","on_goals_against","plus_minus","plus_minus_per90","plus_minus_wowy","on_xg_for","on_xg_against","xg_plus_minus","xg_plus_minus_per90","xg_plus_minus_wowy"]
playingtime2 = ["games","minutes","minutes_per_game","minutes_pct","games_starts","minutes_per_start","games_subs","minutes_per_sub","unused_subs","points_per_match","on_goals_for","on_goals_against","plus_minus","plus_minus_per90","plus_minus_wowy","on_xg_for","on_xg_against","xg_plus_minus","xg_plus_minus_per90","xg_plus_minus_wowy"]

# miscallaneous(misc)
misc = ["player","nationality","position","squad","age","birth_year","minutes_90s","cards_yellow","cards_red","cards_yellow_red","fouls","fouled","offsides","crosses","interceptions","tackles_won","pens_won","pens_conceded","own_goals","ball_recoveries","aerials_won","aerials_lost","aerials_won_pct"]
misc2 = ["cards_yellow","cards_red","cards_yellow_red","fouls","fouled","offsides","crosses","interceptions","tackles_won","pens_won","pens_conceded","own_goals","ball_recoveries","aerials_won","aerials_lost","aerials_won_pct"]


# Functions to get the data in a dataframe using BeautifulSoup

def get_tables(url):
    res = requests.get(url)
    # The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    team_table = all_tables[0]
    player_table = all_tables[2]
    return player_table, team_table


def get_frame(features, player_table):
    pre_df_player = dict()
    features_wanted_player = features
    rows_player = player_table.find_all('tr')
    for row in rows_player:
        if(row.find('th',{"scope":"row"}) != None):
    
            for f in features_wanted_player:
                cell = row.find("td", {"data-stat": f})
                if cell == None:
                    cell = '0'
                else:
                    a = cell.text.strip().encode()
                text = a.decode("utf-8")
                if(text == ''):
                    text = '0'
                if((f!='player')&(f!='nationality')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')):
                    text = float(text.replace(',',''))
                if f in pre_df_player:
                    pre_df_player[f].append(text)
                else:
                    pre_df_player[f] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)
    return df_player


def get_frame_team(features, team_table):
    pre_df_squad = dict()
    # Note: features does not contain squad name, it requires special treatment
    features_wanted_squad = features
    rows_squad = team_table.find_all('tr')
    for row in rows_squad:
        if(row.find('th',{"scope":"row"}) != None):
            name = row.find('th',{"data-stat":"squad"}).text.strip().encode().decode("utf-8")
            if 'squad' in pre_df_squad:
                pre_df_squad['squad'].append(name)
            else:
                pre_df_squad['squad'] = [name]
            for f in features_wanted_squad:
                cell = row.find("td",{"data-stat": f})
                if cell == None:
                    cell = '0'
                else:
                    a = cell.text.strip().encode()
                text=a.decode("utf-8")
                if(text == ''):
                    text = '0'
                if((f!='player')&(f!='nationality')&(f!='position')&(f!='squad')&(f!='age')&(f!='birth_year')):
                    text = float(text.replace(',',''))
                if f in pre_df_squad:
                    pre_df_squad[f].append(text)
                else:
                    pre_df_squad[f] = [text]
    df_squad = pd.DataFrame.from_dict(pre_df_squad)
    return df_squad


def frame_for_category(category,top,end,features):
    url = (top + category + end)
    player_table, team_table = get_tables(url)
    df_player = get_frame(features, player_table)
    return df_player


def frame_for_category_team(category,top,end,features):
    url = (top + category + end)
    player_table, team_table = get_tables(url)
    df_team = get_frame_team(features, team_table)
    return df_team


# Function to get the player data for outfield player, includes all categories - standard stats, shooting
# passing, passing types, goal and shot creation, defensive actions, possession, etc...
def get_outfield_data(top, end):
    df1 = frame_for_category('stats',top,end,stats)
    df2 = frame_for_category('shooting',top,end,shooting2)
    df3 = frame_for_category('passing',top,end,passing2)
    df4 = frame_for_category('passing_types',top,end,passing_types2)
    df5 = frame_for_category('gca',top,end,gca2)
    df6 = frame_for_category('defense',top,end,defense2)
    df7 = frame_for_category('possession',top,end,possession2)
    df8 = frame_for_category('misc',top,end,misc2)
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df


# Function to get keeper and advanced goalkeeping data
def get_keeper_data(top,end):
    df1 = frame_for_category('keepers',top,end,keepers)
    df2 = frame_for_category('keepersadv',top,end,keepersadv2)
    df = pd.concat([df1, df2], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df


# Function to get team specific data across all categories mentioned above
def get_team_data(top,end):
    df1 = frame_for_category_team('stats',top,end,stats3)
    df2 = frame_for_category_team('keepers',top,end,keepers3)
    df3 = frame_for_category_team('keepersadv',top,end,keepersadv2)
    df4 = frame_for_category_team('shooting',top,end,shooting3)
    df5 = frame_for_category_team('passing',top,end,passing2)
    df6 = frame_for_category_team('passing_types',top,end,passing_types2)
    df7 = frame_for_category_team('gca',top,end,gca2)
    df8 = frame_for_category_team('defense',top,end,defense2)
    df9 = frame_for_category_team('possession',top,end,possession2)
    df10 = frame_for_category_team('misc',top,end,misc2)
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], axis=1)
    df = df.loc[:,~df.columns.duplicated()]
    return df


# function to retrieve last 3 chars in string
def last_3(x):
    return x[-3:]


# function to retrieve front 2 chars in string
def front_2(x):
    return x[:2]


def player_imgs(eplsquad):

    if eplsquad == 'Wolves':
        eplsquad = 'Wolverhampton Wanderers'

    page = requests.get('https://www.premierleague.com/clubs')
    soup = BeautifulSoup(page.text, 'html.parser')
    lsoup = BeautifulSoup(page.text, 'lxml')
    links = soup.find_all(href=re.compile("clubs/\d{1,2}"))
    teams_soup = soup.find_all("h4", class_="clubName")

    x = 0
    team_dict = {}
    for team in teams_soup:
        team_dict.update({team.text: F"https://www.premierleague.com{links[x]['href'].replace('overview', 'squad')}"})
        x += 1

    team_dict['Manchester Utd'] = team_dict.pop('Manchester United')
    team_dict['Brighton'] = team_dict.pop('Brighton and Hove Albion')
    team_dict['Newcastle Utd'] = team_dict.pop('Newcastle United')
    team_dict['Tottenham'] = team_dict.pop('Tottenham Hotspur')
    team_dict['West Ham'] = team_dict.pop('West Ham United')

    squadhtml = requests.get(team_dict[eplsquad])
    a_soup = BeautifulSoup(squadhtml.text, 'html.parser')
    b = a_soup.find_all(class_="playerOverviewCard active")
    player = a_soup.find_all(class_='squadPlayerHeader')
    names = [i.find_all(class_="name") for i in player]
    img = [i.find_all('img') for i in player]
    player_dict = {}
    for num in range(len(player)):
        player_dict.update({names[num][0].text: img[num][0]['data-player']})

    missing_dict = {'Emile Smith Rowe': 'Emile Smith-Rowe','Gabriel Martinelli': 'Martinelli',
                    'Benjamin White': 'Ben White', 'Gabriel Magalhães': 'Gabriel Dos Santos',
                    'Sead Kolasinac': 'Sead Kolašinac','Emiliano Buendía': 'Emi Buendía',
                    'Jaden Philogene-Bidace': 'Jaden Philogene Bidace', 'Matthew Cash': 'Matty Cash',
                    'Jóhann Gudmundsson': 'Jóhann Berg Guðmundsson', 'Matej Vydra': 'Matěj Vydra',
                    'Édouard Mendy': 'Edouard Mendy', 'Mateo Kovacic': 'Mateo Kovačić',
                    'Jairo Riedewald': 'Jaïro Riedewald', 'Jesurun Rak-Sakyi': 'Jesuran Rak Sakyi',
                    'Luka Milivojevic': 'Luka Milivojević', 'Asmir Begovic': 'Asmir Begović',
                    'Raphinha': 'Raphael Dias Belloli', 'Kiernan Dewsbury-Hall': 'Kiernan Dewsbury Hall',
                    'Çaglar Söyüncü': 'Çağlar Söyüncü', 'Caoimhin Kelleher': 'Caoimhín Kelleher',
                    'Joseph Gomez': 'Joe Gomez', 'Joel Matip': 'Joël Matip', 'Konstantinos Tsimikas': 'Kostas Tsimikas',
                    'Thiago': 'Thiago Alcántara', 'Ferran Torres': 'Ferrán Torres', 'Ilkay Gündogan': 'İlkay Gündoğan',
                    'Nemanja Matic': 'Nemanja Matić', 'Joseph Willock': 'Joe Willock', 'Joshua Sargent': 'Josh Sargent',
                    'Bryan Gil': 'Bryan', 'Emerson Royal': 'Emerson', 'Pierre-Emile Højbjerg': 'Pierre Højbjerg',
                    'Son Heung-Min': 'Son Heung-min', 'Cucho Hernández': 'Cucho','Peter Etebo': 'Oghenekaro Etebo',
                    'Nikola Vlasic': 'Nikola Vlašić', 'Tomas Soucek': 'Tomáš Souček', 'Vladimir Coufal': 'Vladimír Coufal',
                    'Lukasz Fabianski': 'Łukasz Fabiański', 'Marçal': 'Fernando Marçal', 'Trincão': 'Francisco Trincão',
                    'Hwang Hee-Chan': 'Hwang Hee-chan', 'Maximilian Kilman': 'Max Kilman',
                    'Rayan Aït-Nouri': 'Rayan Aït Nouri'}
    for name in missing_dict.keys():
        if name in player_dict.keys():
            player_dict[missing_dict[name]] = player_dict.pop(name)

    return player_dict