import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import warnings
import streamlit as st
import FBref_scrape as fbr

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
pd.options.mode.chained_assignment = None  # default='warn'

# SET UP ----------------------------------------------------------
st.set_page_config(
    page_title="EPL 2021-22 Dashboard",
    layout="wide",
    page_icon="EPL Crests/zEPL.png",
    initial_sidebar_state='expanded'
)

# COLOR DICTIONARY FOR TEAMS - PRIMARY AND SECONDARY COLORS
team_colors = {'Arsenal': ['#DB0007', '#FFFFFF'], 'Aston Villa': ['#95BEE5', '#670E36'],
               'Brentford': ['#E4010B', '#FFFFFF'], 'Brighton': ['#005CAC', '#FFCD00'],
               'Burnley': ['#6C1D45', '#99D6EA'], 'Chelsea': ['#034694', '#EE242C'],
               'Crystal Palace': ['#1B458F', '#A7A5A6'], 'Everton': ['#274488', '#FFFFFF'],
               'Leeds United': ['#FFE000', '#1D428A'], 'Leicester City': ['#0053A0', '#FDBE11'],
               'Liverpool': ['#D00027', '#00A398'], 'Manchester City': ['#97C1E7', '#D6A62B'],
               'Manchester Utd': ['#E01A22', '#FBE122'], 'Newcastle Utd': ['#BABDBF', '#241F20'],
               'Norwich City': ['#00A650', '#FFF200'], 'Southampton': ['#D71920', '#FFFFFF'],
               'Tottenham': ['#132257', '#FFFFFF'], 'Watford': ['#FBEE23', '#ED2127'],
               'West Ham': ['#60223B', '#5299C6'], 'Wolves': ['#FDB914', '#231F20']}


# GET FBREF DATA FUNCTIONS ---------------------------------------

# TEAMS TABLE
@st.cache
def team_data():
    df = fbr.get_team_data('https://fbref.com/en/comps/9/', '/Premier-League-Stats').convert_dtypes()
    df = df.set_index('player')
    return df


# PLAYERS TABLE
@st.cache
def players_data():
    df = fbr.get_outfield_data('https://fbref.com/en/comps/9/', '/Premier-League-Stats').convert_dtypes()
    df = df.set_index('player')
    df['age'] = df['age'].apply(fbr.front_2)
    df.drop(columns=['birth_year', 'games_starts', 'pens_att'], inplace=True)
    return df


# KEEPERS TABLE
@st.cache
def keeper_data():
    df = fbr.get_keeper_data('https://fbref.com/en/comps/9/', '/Premier-League-Stats')
    return df


# LEAGUE TABLE
@st.cache()
def league_table():
    league_ = fbr.get_league_table().convert_dtypes().set_index('Rk')
    league_.drop(columns=['Attendance', 'Top Team Scorer', 'Goalkeeper', 'Notes'], inplace=True)
    league_ = pd.DataFrame(league_)
    return league_


# FIXTURES TABLE
@st.cache
def fixes():
    fix = fbr.get_fixtures()
    fix = fix[fix['Score'].notna()]
    fix.drop(columns=['Day', 'Time', 'Attendance', 'Match Report', 'Notes', 'Venue'], inplace=True)
    # latest = fix[fix['Wk'] == fix.Wk.max()]
    fix.Wk = fix.Wk.astype(int)
    return fix


# CALL TABLES FOR INITIAL LOAD
players = players_data()
gk = keeper_data()
league_df = league_table()

# CREATE LIST OF TEAMS FROM LEAGUE TABLE FOR SIDEBAR
teams = league_df['Squad'].tolist()
teams.append('ALL')


# EPL LEAGUE PAGE --------------------------------------
def epl_ui():

    # INITIAL LANDING PAGE - ALL EPL STATS

    st.markdown("<h1 style='text-align: center; color: white;'>English Premier League Table & Fixtures</h1>",
                unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white; font-size: 25px;'>Current Premier League Table</h1>",
                unsafe_allow_html=True)

    # DISPLAY CURRENT LEAGUE TABLE
    st.table(league_df.style
             .format({'xG': '{:.1f}', 'xGA': '{:.1f}', 'xGD': '{:.1f}', 'xGD/90': '{:.1f}'}))
    # DROP DOWN TO SELECT WEEKLY FIXTURE
    week = st.selectbox('Select Matchweek:', fixes().Wk.unique())
    st.subheader(f"Week {week} Fixtures")
    fix_df = fixes()[fixes()['Wk'] == week]
    fix_df.rename(columns={'xG': 'Home xG', 'xG.1': 'Away xG'}, inplace=True)

    # DISPLAY FIXTURES OF ALL MATCHWEEK GAMES
    st.table(fix_df.style.format({'Home xG': '{:.1f}', 'Away xG': '{:.1f}'}))


# SELECTED TEAM PAGE ------------------------------------------
def team_ui(squad):

    # TEAM PAGE SELECTED BY SIDEBAR VALUE

    # ALIGN CLUB CREST TO CENTER
    col1, col2, col3 = st.columns([1, .8, 1])
    col2.image(f"EPL Crests/{squad}.png", use_column_width=True)

    st.markdown(f"<h1 style='text-align: center; color: white;'>{squad} 2021-22 Premier League Stats</h1>",
                unsafe_allow_html=True)

    squad_df = players[players['squad'] == squad]
    squad_df.drop(columns=['squad'], inplace=True)

    # CALL FIXTURES TABLE
    fix = fixes()

    # USE INDEXERS TO RETURN ONLY SELECT TEAM FIXTURES - HOME & AWAY
    team_a = fix[fix.Home == squad]
    team_h = fix[fix.Away == squad]
    fix_df = pd.concat([team_a, team_h]).sort_values(by='Wk').set_index('Wk')
    fix_df.rename(columns={'xG': 'Home xG', 'xG.1': 'Away xG'}, inplace=True)

    # HIGHLIGHT CELLS OF SELECTED TEAM WITH TEAM PRIMARY COLOR
    def highlight_cells(val):
        color = team_colors[squad][0] if squad in val else ''
        return f'background-color: {color}'

    # DISPLAY FIXTURES AND CURRENT EPL TABLE ROW FOR SELECTED TEAM --------------------
    st.table(fix_df
             .style
             .applymap(highlight_cells, subset=['Home', 'Away'])  # highlight team cells w/ team colors
             .format({'Home xG': '{:.1f}', 'Away xG': '{:.1f}'}))
    st.write(f"<h1 style='text-align: center; color: white; font-size: 25px;'>{squad} Current Standings</h1>",
             unsafe_allow_html=True)
    st.table(league_df.loc[league_df['Squad'] == squad]
             .style
             .format({'xG': '{:.1f}', 'xGA': '{:.1f}', 'xGD': '{:.1f}', 'xGD/90': '{:.1f}'}))

    # POPULATE TEAM STAT SELECTION DROPDOWN MENU
    stat_dict = {'Goals': 'goals', 'Assists': 'assists', 'Passing %': 'passes_pct', 'Key Passes': 'assisted_shots',
                 'Passes into final 3rd': 'passes_into_final_third', 'Goal-creating Actions': 'gca',
                 'Shot-creating Actions': 'sca', 'Tackles Won': 'tackles_won', 'Pressures': 'pressures',
                 'Blocked Shots': 'blocked_shots', 'Interceptions': 'interceptions',
                 'Dribbles Completed': 'dribbles_completed', 'Progressive Carries': 'progressive_carries',
                 'Carries into final 3rd': 'carries_into_final_third', 'Ariel Duel Win %': 'aerials_won_pct'}
    squad_stat = st.selectbox("Select Stat:", stat_dict.keys())

    # CREATE DATAFRAME FOR SELECTED STAT
    ss_df = squad_df[squad_df[stat_dict[squad_stat]] >= 1]

    # BAR CHART OF SELECTED STAT FOR TEAM ---------------------------------------

    bar_fig = px.bar(ss_df, x=ss_df.index, y=ss_df[stat_dict[squad_stat]], text=ss_df[stat_dict[squad_stat]],
                     color=ss_df[stat_dict[squad_stat]], color_continuous_scale=[[0, f'{team_colors[squad][1]}'],
                                                                                 [1, f'{team_colors[squad][0]}']])
    bar_fig.update_layout(plot_bgcolor='#0F1117',
                          title={'text': squad_stat, 'x': 0.5, 'xanchor': 'center'},
                          coloraxis_colorbar=dict(title=squad_stat))
    bar_fig.update_layout(yaxis={'title': ''},
                          xaxis={'title': ''})
    bar_fig.update_traces(hovertemplate="<br>".join(["%{x}", "%{y}"]))
    bar_fig.update_xaxes(showgrid=False)
    bar_fig.update_yaxes(showgrid=False)
    st.plotly_chart(bar_fig, use_container_width=True)

    # CREATE INDEXERS AND NEW DATA FOR XG LINE CHART
    indexer = fix_df[fix_df['Home'] == squad].index
    a_indexer = fix_df[fix_df['Away'] == squad].index
    op_indexer = fix_df[fix_df['Home'] != squad].index
    op_a_indexer = fix_df[fix_df['Away'] != squad].index

    # TEAM XG DATAFRAME
    xg = pd.DataFrame(pd.concat([fix_df.loc[indexer, 'Home xG'],
                                 fix_df.loc[a_indexer, 'Away xG']])).sort_values(by='Wk').reset_index()

    # OPPONENT XG DATAFRAME
    opxg = pd.DataFrame(pd.concat([fix_df.loc[op_indexer, 'Home xG'],
                                   fix_df.loc[op_a_indexer, 'Away xG']])).sort_values(by='Wk').reset_index()
    opname = pd.DataFrame(pd.concat([fix_df.loc[op_indexer, 'Home'],
                                     fix_df.loc[op_a_indexer, 'Away']])).sort_values(by='Wk').reset_index()
    opxg = opxg.merge(opname, on='Wk').rename(columns={'0_x': 'OPxG', '0_y': 'team'})

    # FINAL MERGED DATAFRAME FOR XG LINE CHART
    fxg = opxg.merge(xg, on='Wk').rename(columns={0: 'squad_xG'})

    # LINE CHART TRACKING XG AND VS XG PER GAME ---------------------------------------

    xg_fig = go.Figure()
    xg_fig.add_trace(go.Scatter(x=fxg['Wk'], y=fxg['OPxG'],
                                fill='tozeroy', name="Opponent xG",
                                line=dict(dash='dash')))
    xg_fig.add_trace(go.Scatter(x=fxg['Wk'], y=fxg['squad_xG'],
                                fill='tozeroy', name=f'{squad} xG'))
    xg_fig.update_traces(mode='markers+lines')
    xg_fig.update_layout(plot_bgcolor='#0F1117',
                         hovermode="x",
                         title="Tracking xG by Matchweek",
                         title_x=0.5)
    xg_fig.update_layout(xaxis=dict(tickvals=fxg['Wk'], ticktext=fxg['team']))
    st.plotly_chart(xg_fig, use_container_width=True)

    # PLAYER DROPDOWN FOR INDIVIDUAL STATS
    footballer = st.selectbox('Select Player:', sorted(squad_df.index))

    # CALL PLAYER DICT WITH HEADSHOT URLS
    player_dict = fbr.player_imgs(squad)

    # ASSIGN DATAFRAME TO SELECTED PLAYER
    footballer_df = squad_df[squad_df.index == footballer]

    # UPPER COLUMNS TO SPACE DATA
    uppercol1, uppercol2, uppercol3 = st.columns([1, .5, 1])

    with uppercol1:
        # HANDLE MISSING HEADSHOT EXCEPTIONS
        try:
            img_url = f'https://resources.premierleague.com/premierleague/photos/players/250x250/{player_dict[footballer]}.png'
            st.image(img_url)
        except KeyError:
            st.write(f'No Headshot available for {footballer}')

    # DISPLAY PLAYER INFO
    with uppercol3:
        st.subheader(' ')
        st.text(' ')
        st.text(' ')
        st.subheader(f"{footballer}")
        st.markdown(f"Position: **{footballer_df['position'].item()}**")
        st.markdown(f"Age: **{footballer_df['age'].item()}**")
        st.markdown(f"Goals: **{footballer_df['goals'].item()}**")
        st.markdown(f"Assists: **{footballer_df['assists'].item()}**")
        st.markdown(f"Minutes: **{footballer_df['minutes'].item()}**")
        st.markdown(f"Nationality: **{footballer_df['nationality'].item()[-3:]}**")

    # LOWER COLUMNS TO CENTER RADAR CHART
    lowcol1, lowcol2, lowercol3 = st.columns([1, 3, 1])

    with lowcol2:
        # RADAR CHART FUNCTION - SELECTED PLAYER AGAINST EPL AVG IN SAME POSITION
        def radar():

            # CREATE VARIABLES FOR POSITIONS, COLUMN DATA
            def_list = ['DF', 'DF,MF', 'DF,FW', 'MF,DF']
            att_list = ['FW', 'MF', 'FW,MF', 'MF,FW', 'FW,DF']
            def_cols = ['clearances', 'blocked_passes', 'blocked_shots', 'interceptions',
                        'tackles_won', 'tackles_def_3rd', 'tackles_mid_3rd', 'tackles_att_3rd']
            att_cols = ['goals_per90', 'assists_per90', 'goals_assists_per90',
                        'xg_per90', 'xa_per90', 'xg_xa_per90', 'gca_per90']
            gk_cols = ['saves', 'clean_sheets', 'def_actions_outside_pen_area_gk', 'psxg_gk', 'crosses_stopped_gk']
            def_dict = {
                    'clearances': 'Clearances',
                    'blocked_passes': 'Blocked Passes',
                    'blocked_shots': 'Blocked Shots',
                    'interceptions': 'Interceptions', 'tackles_won': 'Tackles Won',
                    'tackles_def_3rd': 'Tackles in Defensive 3rd',
                    'tackles_mid_3rd': 'Tackles in Middle 3rd',
                    'tackles_att_3rd': 'Tackles in Attacking 3rd'}
            att_dict = {
                    'goals_per90': 'Goals per 90',
                    'assists_per90': 'Assists per 90',
                    'goals_assists_per90': 'Goals & Assists per 90',
                    'xg_per90': 'xG per 90',
                    'xa_per90': 'xA per 90',
                    'xg_xa_per90': 'xG & xA per 90',
                    'gca_per90': 'Goal-creating actions per 90'}
            gk_dict = {
                    'saves': 'Saves',
                    'clean_sheets': 'Clean Sheets',
                    'def_actions_outside_pen_area_gk': 'Defensive Actions Outside Box',
                    'psxg_gk': 'Post-Shot xG',
                    'crosses_stopped_gk': 'Crosses Stopped'}

            # CONTROL FLOW FOR EACH POSITION - DEFENSE, MIDFIELD, FORWARD, GOALKEEPER
            if footballer_df.position.item() in def_list:
                footballer_df_radar = footballer_df[def_cols]
                footballer_df_radar.rename(columns=def_dict, inplace=True)

            elif footballer_df.position.item() in att_list:
                footballer_df_radar = footballer_df[att_cols]
                footballer_df_radar.rename(columns=att_dict, inplace=True)

            elif footballer_df.position.item() == 'GK':
                gk_df = gk[gk['player'] == footballer]
                footballer_df_radar = gk_df[gk_cols]
                footballer_df_radar.rename(columns=gk_dict, inplace=True)

            # SPLIT PLAYER POSITION - ADD ALL TO LIST - LIMIT DATAFRAME TO POSITION
            lst = footballer_df['position'].values[0].split(',')
            lst.append(footballer_df.position.values[0])
            avg_df = players[players['position'].isin(lst)]

            # SAME CONTROL FLOW BY POSITION - AVG EPL PLAYER
            if avg_df.position.iloc[0] in def_list:
                avg_df = avg_df[def_cols]
                avg_df.rename(columns=def_dict, inplace=True)

            elif avg_df.position.iloc[0] in att_list:
                avg_df = avg_df[att_cols]
                avg_df.rename(columns=att_dict, inplace=True)

            elif avg_df.position.iloc[0] == 'GK':
                avg_df = gk[gk_cols]
                avg_df.rename(columns=gk_dict, inplace=True)

            # TRANSPOSE AND RENAME COLUMNS IN DATAFRAMES
            footballer_df_radar = footballer_df_radar.T.reset_index()
            footballer_df_radar.rename(columns={footballer_df_radar.columns[0]: 'stats',
                                                footballer_df_radar.columns[-1]: 'values'}, inplace=True)

            avg_df = avg_df.T
            avg_df = pd.DataFrame(avg_df.mean(axis=1)).reset_index()
            avg_df.rename(columns={avg_df.columns[0]: 'stats',
                                   avg_df.columns[-1]: 'values'}, inplace=True)

            # RADAR CHART WITH DATAFRAMES - FUNC CALL PLOTS RADAR ----------------------------
            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(
                r=avg_df['values'],
                theta=avg_df['stats'],
                fill='toself',
                name=F'Average EPL {footballer_df.position.item()}',
                hovertemplate="%{theta}<br> %{r:.2f}"))
            radar_fig.add_trace(go.Scatterpolar(
                r=footballer_df_radar['values'],
                theta=footballer_df_radar['stats'],
                fill='toself',
                name=f'{footballer}',
                hovertemplate="%{theta}<br> %{r:.2f}"))
            radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, angle=90)), showlegend=True)
            radar_fig.update_polars(dict(radialaxis_autorange=True, bgcolor='#0F1117'))
            radar_fig.update_layout(legend=dict(yanchor="top", y=1.3, xanchor="left", x=0.04))
            return radar_fig

        st.plotly_chart(radar())


# SET SIDEBAR DETAILS - DISPLAY ALL EPL TEAMS IN ALPHABETICAL ORDER -------------------------
with st.sidebar:
    st.image(f"EPL Crests/zzEPL.png", use_column_width=True)
    st.title("Select EPL Team:")
    mode = st.radio(
        "Team",
        sorted(teams))
    st.subheader("A web app created by [Joshua Suchon](https://github.com/j-suchon)")

# LINK SIDEBAR SELECTION TO TEAM UI PAGE
for team in sorted(teams)[1:]:
    if mode == team:
        team_ui(team)

# SET DEFAULT LANDING PAGE TO EPL LEAGUE TABLE PAGE
if mode == 'ALL':
    epl_ui()
