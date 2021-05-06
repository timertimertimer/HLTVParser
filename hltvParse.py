import requests
from bs4 import BeautifulSoup
import json


def make_match(m):
    match_obj = dict()
    bo = m.find('div', {'class': 'matchMeta'}).text
    match_page_url = 'https://www.hltv.org' + m.find('a').get('href')
    headers['referer'] = url
    res = requests.get(match_page_url, headers=headers)
    match_page = BeautifulSoup(res.text, 'lxml')
    team_ranks = match_page.find_all('div', {'class': 'teamRanking'})
    if len(team_ranks) == 2:
        team1_rank = team_ranks[0].text.split()[-1][1:]
        team2_rank = team_ranks[1].text.split()[-1][1:]
        if int(team1_rank) <= 100 and int(team2_rank) <= 100 and int(bo[-1]) >= 3:
            team_names = m.find_all('div', {'class': 'matchTeamName text-ellipsis'})
            match_obj['team1'] = {team_names[0].text: 'Rank: ' + team1_rank}
            match_obj['team2'] = {team_names[1].text: 'Rank: ' + team2_rank}
            match_obj['bo'] = bo
            match_obj['url'] = match_page_url
            match_obj['event'] = m.find("div", {"class": "matchEvent"}).text.strip()
            return match_obj
    return None


url = 'https://www.hltv.org/matches'
# С headers статус-код становится 200 (видимо обход CloudFlare)
headers = {
    'referer': 'https://www.hltv.org/',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(url, headers=headers)
Matches = BeautifulSoup(response.text, 'lxml')

# Live matches
liveMatchesList = []
liveMatches = Matches.find_all('div', {'class': 'liveMatch-container'})
for match in liveMatches:
    matchObj = make_match(match)
    if matchObj:
        matchObj['maps'] = match.get('data-maps')
        liveMatchesList.append(matchObj)
lived = {'live': liveMatchesList}
with open('live.json', 'w') as live:
    json.dump(lived, live, indent=4)

upcomingMatches = Matches.find_all('div', {"class": 'upcomingMatchesSection'})

# Today and tomorrow matches
today_and_tomorrow = upcomingMatches[:2]
matchesList = []
dates = []
i = 0
for day in today_and_tomorrow:
    matches = day.find_all("div", {"class": "upcomingMatch"})
    date = day.find({'span': {'class': 'matchDayHeadline'}}).text
    dates.append(date)
    day_matches = []
    for match in matches:
        matchObj = make_match(match)
        if matchObj:
            time = match.find('div', {'class': 'matchTime'}).text.split(':')
            matchObj['time'] = str((int(time[0]) + 1) % 24) + ':' + time[1]
            day_matches.append(matchObj)
    matchesList.append(day_matches)
    i += 1
tt = {'today (' + dates[0] + ')': matchesList[0], 'tomorrow (' + dates[1] + ')': matchesList[1]}
with open('today_and_tomorrow.json', 'w') as todayAndTomorrow:
    json.dump(tt, todayAndTomorrow, indent=4)
