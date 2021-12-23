# EPL-Dashboard
Premier League Dashboard for 2021-22 Season. Breakdown  stats by league, team, and player.

This app is a dashboard that runs an analysis on any desired EPL player or squad. Visualizations of various statistics are displayed for the selected player or squad. They are briefly described below:

EPL Page
Current League Table - A snapshot of the current league table. The champions league, europa league, and relegation spots are highlighted in green, blue, and red, respectively.

Top 5 Stat League Leaders - A display of the top 5 players for each stat in the dropdown and their headshot sourced from http://www.premierleague.com.

Stats include:
Goals, Assists, Key Passes, Passes into final 3rd, Goal-creating Actions, Shot-creating Actions, Tackles Won, Pressures, Blocked Shots, Interceptions, Dribbles Completed, Progressive Carries, Carries into final 3rd, Aerial Duel Win %

Week by Week - A table corresponding to the selected matchweek in the dropdown.

Team Page
Previous Fixture Table - A table combining all previous fixtures for selected team. The team is highlighted with the primary team color. Table also displays xG and score for selected team and opponent.

Team Current Standings - A slice of the league table of the selected team.

Next Fixture - Compares the upcoming opponent to the selected team. Categories: Goals per 90, xG per 90, Goals against per 90, Clean Sheets, Shots on Target per 90, Shot-Creating Actions per 90, Goal-Creating Actions per 90, Pressures in Defensive 3rd, Pressures in Middle 3rd, Pressures in Attacking 3rd. The dominant team stat is highlighted in green and the lesser in red.

Team Stats - Displays a bar chart of the stat selected from the dropdown. Stats: Goals, Assists, Key Passes, Passes into final 3rd, Goal-creating Actions, Shot-creating Actions, Tackles Won, Pressures, Blocked Shots, Interceptions, Dribbles Completed, Progressive Carries, Carries into final 3rd, Aerial Duel Win %

Tracking xG by Week - This line chart tracks the Expected Goals statistic of the selected team and their opponent through each week of the current season.

Player Stats - A radar/spider chart for the selected player from the dropdown box. The stats in the radar chart depend on the players position. The selected players stats are compared to the league average for that position. Information and basic statistics are also displayed to the right of the headshot.

Tip - To get a better look at any individual chart, click the expander box

Disclaimer:

The initial page load will take around 40 seconds. Since I am not storing this data, nor are there any public API's, this initial load is a webscrape and cleansing of all related data. Streamlit provides a great caching decorator that is used on all functions so beyond the first page load, all wait times should be minimal

# Landing Page - League Table

<img width="1440" alt="Screen Shot 2021-11-21 at 8 50 23 AM" src="https://user-images.githubusercontent.com/78511692/142771372-17d6f4c2-8e68-490e-bb1c-76e986800787.png">

# Landing Page - Top 5 Stat Leaders

<img width="990" alt="Screen Shot 2021-11-21 at 8 51 05 AM" src="https://user-images.githubusercontent.com/78511692/142771400-91d20c62-c9f5-4e51-ba38-bed7bc25626d.png">



# Team Page - Results

<img width="877" alt="Screen Shot 2021-10-19 at 11 47 34 AM" src="https://user-images.githubusercontent.com/78511692/137973167-55a705f1-b0a5-42df-91ca-987a0b160281.png">

# Team Page - Next Opponent

<img width="1051" alt="Screen Shot 2021-11-21 at 8 51 59 AM" src="https://user-images.githubusercontent.com/78511692/142771441-68a43dcd-f18d-45ce-9c2b-a10dc2becc2b.png">


# Team Page - Team Stats Bar Chart

<img width="916" alt="Screen Shot 2021-10-19 at 11 48 27 AM" src="https://user-images.githubusercontent.com/78511692/137973236-a889591f-ccda-43af-ba06-d0334fc496e7.png">

# Team Page - Tracking xG per Opponent

<img width="991" alt="Screen Shot 2021-10-19 at 11 49 17 AM" src="https://user-images.githubusercontent.com/78511692/137973284-3b3287f3-9329-4bf9-b8aa-4f04737705fb.png">

# Team Page - Individual Player Stats vs. Avgerage EPL of Same Position

<img width="1005" alt="Screen Shot 2021-10-19 at 11 49 00 AM" src="https://user-images.githubusercontent.com/78511692/137973391-7af67aad-1361-483a-b861-1103099f7ad6.png">
