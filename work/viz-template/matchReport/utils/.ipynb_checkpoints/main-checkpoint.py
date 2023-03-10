import datetime
import json
import re
import time
from collections import OrderedDict

import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tqdm import trange


def getLeagueLinks(main_url):

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options,
    )
    driver.minimize_window()

    main = driver.get(main_url)
    leagues = []
    for i in range(20):
        league = driver.find_element_by_xpath(
#            ex. premiar league -> //*[@id="popular-tournaments-list"]/li[1]/a
            '//*[@id="popular-tournaments-list"]/li[' + str(i + 1) + ']/a').get_attribute('href')
        leagues.append(league)
    driver.close()
    return leagues


def getMatchLinks(comp_url, main_url):
#   1617->13955 1718->15375 1819->16546 1920->17702
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options,
    )
    teams = []
    comp = driver.get(comp_url)
    season = driver.find_element_by_xpath(
        '//*[@id="seasons"]/option[1]').click()
    time.sleep(5)
    for i in range(20): # 20or18
        team = driver.find_element_by_xpath(
            '//*[@id="standings-18851-content"]/tr[' + str(i + 1) + ']/td[1]/a').text
#             premier -> standings-18685-content
#             liga -> standings-18851-content
#             bundes -> standings-18762-content
#             serie -> standings-18873-content
        teams.append(team)

    time.sleep(5)
    fixtures_page = driver.find_element_by_xpath(
        '//*[@id="link-fixtures"]').click()
    time.sleep(5)
    date_config_btn = driver.find_element_by_xpath(
        '//*[@id="date-config-toggle-button"]').click()
    time.sleep(5)
    year1 = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[1]/div/table/tbody/tr[1]/td').click()
    selectable_months = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[2]/div/table').find_elements_by_class_name("selectable")

    n_months = len(selectable_months)

    year2 = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[1]/div/table/tbody/tr[2]/td').click()
    selectable_months = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[2]/div/table').find_elements_by_class_name("selectable")

    n_months += len(selectable_months)
    date_config_btn = driver.find_element_by_xpath(
        '//*[@id="date-config-toggle-button"]').click()

    #for month_element in selectable_months:
    match_links = []

    for i in range(n_months):
        time.sleep(2)
        fixtures_table = driver.find_element_by_xpath('//*[@id="tournament-fixture"]')
        fixtures_table = fixtures_table.get_attribute('innerHTML')
        fixtures_table = soup(fixtures_table, features="lxml")
        table_rows1 = fixtures_table.find_all("div", {"class":"divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12"})    
        table_rows2 = fixtures_table.find_all("div", {"class":"divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 alt"})
        
        table_rows = table_rows1+table_rows2

        links = []
#         links = [main_url+row.find("a", {"class":"result-1 rc"}).get("href") for row in table_rows]
        for row in table_rows:
            try:
                sub_link = row.find('a', {"class":"result-1 rc"}).get('href')
            except AttributeError:
                pass
            link = main_url + sub_link
            links.append(link)
#         links = [main_url+row.find("a", {"class":"result-4 rc"}).get("href") for row in table_rows]  
            
        for link in links:
            match_links.append(link)
            
        previous_month = driver.find_element_by_xpath('//*[@id="date-controller"]/a[1]').click()
        
    if len(match_links) != 38:
        fixtures_table = driver.find_element_by_xpath('//*[@id="tournament-fixture"]')
        fixtures_table = fixtures_table.get_attribute('innerHTML')
        fixtures_table = soup(fixtures_table)
        table_rows1 = fixtures_table.find_all("div", {"class":"divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12"})    
        table_rows2 = fixtures_table.find_all("div", {"class":"divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 alt"})
        table_rows = table_rows1+table_rows2
        links = []
        links = [main_url+row.find("a", {"class":"result-1 rc"}).get("href") for row in table_rows]
        for link in links:
            match_links.append(link)
            
    match_links = list(dict.fromkeys(match_links))
    driver.close()
    return teams, match_links


def getTeamLinks(team, match_links):
    team = team.split()
    team_links = []
    for link in match_links:
        if len(team) == 1:
            if team[0] in link:
                team_links.append(link)
        else:
            if team[0] + '-' + team[1] in link:
                team_links.append(link)

    return team_links




def getTeamData(team_links):
    matches = []

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options,
    )
    driver.minimize_window()
    


    for i in trange(len(team_links), desc='Single loop'):
        driver.get(team_links[i])
        time.sleep(2)
        element = driver.find_element_by_xpath(
                '//*[@id="layout-wrapper"]/script[1]')
        script_content = driver.find_element_by_xpath('//*[@id="layout-wrapper"]/script[1]').get_attribute('innerHTML')
        # clean script content
        script_content = re.sub(r"[\n\t]*", "", script_content)
        script_content = script_content[script_content.index("matchId"):script_content.rindex("}")]

        # this will give script content in list form 
        script_content_list = list(filter(None, script_content.strip().split(',            ')))
        metadata = script_content_list.pop(1) 

        # string format to json format
        match_data = json.loads(metadata[metadata.index('{'):])
        keys = [item[:item.index(':')].strip() for item in script_content_list]
        values = [item[item.index(':')+1:].strip() for item in script_content_list]
        for key,val in zip(keys, values):
            match_data[key] = json.loads(val)

        region = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/span[1]').text
        league = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')[0]
        season = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')[1]
        if len(driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')) == 2:
            competition_type = 'League'
            competition_stage = ''
        elif len(driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')) == 3:
            competition_type = 'Knock Out'
            competition_stage = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')[-1]
        else:
            print('Getting more than 3 types of information about the competition.')
        match_data['region'] = region
        match_data['league'] = league
        match_data['season'] = season
        match_data['competitionType'] = competition_type
        match_data['competitionStage'] = competition_stage

        # sort match_data dictionary alphabetically
        match_data = OrderedDict(sorted(match_data.items()))
        match_data = dict(match_data)

#         driver.get(team_links[i])
#         time.sleep(2)
#         try:
#             element = driver.find_element_by_xpath(
#                 '//*[@id="layout-wrapper"]/script[1]')
#         except:
#             print(team_links[i])
#         script_content = element.get_attribute('innerHTML')
#         script_ls = script_content.split(sep="  ")
#         script_ls = list(filter(None, script_ls))
#         script_ls = [name for name in script_ls if name.strip()]
#         script_ls_mod = []
#         keys = []
#         for item in script_ls:
#             if "}" in item:
#                 item = item.replace(";", "")
#                 script_ls_mod.append(item[item.index("{"):])
#                 keys.append(item.split()[1])

#             else:
#                 item = item.replace(";", "")
#                 script_ls_mod.append(int(''.join(filter(str.isdigit, item))))
#                 keys.append(item.split()[1])

#         match_data = json.loads(script_ls_mod[0])
#         for key, item in zip(keys[1:], script_ls_mod[1:]):
#             if type(item) == str:
#                 match_data[key] = json.loads(item)                
#             else:
#                 match_data[key] = item

        matches.append(match_data)
                 

    driver.close()

    return matches


def getMatchData(url, close_window=True):
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options,
    )
    driver.minimize_window()
    driver.get(url)

    script_content = driver.find_element_by_xpath('//*[@id="layout-wrapper"]/script[1]').get_attribute('innerHTML')
    # clean script content
    script_content = re.sub(r"[\n\t]*", "", script_content)
    script_content = script_content[script_content.index("matchId"):script_content.rindex("}")]
    
    # this will give script content in list form 
    script_content_list = list(filter(None, script_content.strip().split(',            ')))
    metadata = script_content_list.pop(1) 
    
    # string format to json format
    match_data = json.loads(metadata[metadata.index('{'):])
    keys = [item[:item.index(':')].strip() for item in script_content_list]
    values = [item[item.index(':')+1:].strip() for item in script_content_list]
    for key,val in zip(keys, values):
        match_data[key] = json.loads(val)
        
    region = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/span[1]').text
    league = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')[0]
    season = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')[1]
    if len(driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')) == 2:
        competition_type = 'League'
        competition_stage = ''
    elif len(driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')) == 3:
        competition_type = 'Knock Out'
        competition_stage = driver.find_element_by_xpath('//*[@id="breadcrumb-nav"]/a').text.split(' - ')[-1]
    else:
        print('Getting more than 3 types of information about the competition.')
    match_data['region'] = region
    match_data['league'] = league
    match_data['season'] = season
    match_data['competitionType'] = competition_type
    match_data['competitionStage'] = competition_stage
    
    # sort match_data dictionary alphabetically
    match_data = OrderedDict(sorted(match_data.items()))
    match_data = dict(match_data)
    print('Region: {}, League: {}, Season: {}, Match Id: {}'.format(region, league, season, match_data['matchId']))


    if close_window:
        driver.close()

    return match_data



def createEventsDF(matches):
    if type(matches) == dict:
        events = matches['events']
        for event in events:
            event.update({'matchId': matches['matchId'],
                          'startDate': matches['startDate'],
                          'startTime': matches['startTime'],
                          'score': matches['score'],
                          'ftScore': matches['ftScore'],
                          'htScore': matches['htScore'],
                          'etScore': matches['etScore'],
                          'venueName': matches['venueName'],
                          'maxMinute': matches['maxMinute']})
        events_df = pd.DataFrame(events)
        return events_df
    else:
        for i in trange(len(matches), desc='Single loop'):
            events = matches[i]['events']
            for event in events:
                event.update({'matchId': matches[i]['matchId'],
                              'startDate': matches[i]['startDate'],
                              'startTime': matches[i]['startTime'],
                              'score': matches[i]['score'],
                              'ftScore': matches[i]['ftScore'],
                              'htScore': matches[i]['htScore'],
                              'etScore': matches[i]['etScore'],
                              'venueName': matches[i]['venueName'],
                              'maxMinute': matches[i]['maxMinute']})
        events_ls = []
        for match in matches:
            match_events = match['events']
            match_events_df = pd.DataFrame(match_events)
            events_ls.append(match_events_df)

        events_df = pd.concat(events_ls)
        return events_df


def createMatchesDF(data):
    columns_req_ls = [
        'matchId',
        'attendance',
        'venueName',
        'startTime',
        'startDate',
        'score',
        'home',
        'away',
        'referee']
    matches_df = pd.DataFrame(columns=columns_req_ls)
    if type(data) == dict:
        matches_dict = dict(
            [(key, val) for key, val in data.items() if key in columns_req_ls])
        matches_df = matches_df.append(matches_dict, ignore_index=True)
    else:
        for match in data:
            matches_dict = dict(
                [(key, val) for key, val in match.items() if key in columns_req_ls])
            matches_df = matches_df.append(matches_dict, ignore_index=True)

    matches_df = matches_df.set_index('matchId')
    return matches_df


def getUnderstatShotData(match_url, driver):
    
    driver.get(match_url)

    # getting shot data from script
    shot_data_tag = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[1]/div/script')
    script_data = shot_data_tag.get_attribute('innerHTML')
    json_data = script_data[script_data.index("('")+2:script_data.index("')")]
    json_data = json_data.encode('utf8').decode('unicode_escape')
    shot_data = json.loads(json_data)
    
    # closing browser window
    driver.close()

    # converting shot data from json to dataframe format
    h_df = pd.DataFrame(shot_data['h'])
    a_df = pd.DataFrame(shot_data['a'])
    shot_data_df = pd.concat([h_df,a_df]).reset_index(drop=True)
    shot_data_df = shot_data_df.astype({'X':'float', 'Y':'float', 'xG':'float'}) 

    # sorting by minute sequence
    shot_data_df = shot_data_df.astype({'minute':int}) 
    shot_data_df = shot_data_df.sort_values('minute')
    
    return shot_data_df



def getxGFromUnderstat(match_data, events_df, driver):
    
    # Opening home page
    url = 'https://understat.com'
    driver.get(url)
    
    
    # Getting leagues available in understat
    und_leagues = driver.find_element_by_xpath('//*[@id="header"]/div/nav[1]/ul').text.split('\n')
    found = False
    for lg in und_leagues:
        if match_data['league'].upper() == ''.join(lg.split()).upper():
            driver.find_element_by_link_text(lg).click()
            found = True
            break
    
    
    # If league not found -> exit
    if found == False:
        print('Expected Goals data for league not available')
        driver.close()
        
    else:
        # Getting seasons available in understat
        season_btn = driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div').click()
        und_seasons = driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/ul').text.split('\n')
        found = False
        for szn in und_seasons:
            if match_data['season'] == szn:
                i = str(und_seasons.index(szn)+1)
                driver.find_element_by_xpath("//*[@id='header']/div/div[2]/ul/li["+i+"]").click()
                found = True
                break
        
        
        # If season not found -> exit
        if found == False:
            print('Expected Goals data for season not available')
            driver.close()

        else:
            # Getting match date display
            timezn_off_btn = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[1]/div/label[3]').click()
            date = '-'.join(match_data['startDate'].split('T')[0].split('-')[::-1])
            d = datetime.datetime.strptime(date, '%d-%m-%Y')
            date = datetime.date.strftime(d, "%A, %B %d, %Y")
            prev_btn = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/button[1]')
            next_btn = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/button[2]')
            btn_ls = []
            found = True
            while found:
                display_dates = [datetime.datetime.strptime(d.text, '%A, %B %d, %Y') for d in driver.find_elements_by_class_name('calendar-date')]
                if d in display_dates:
                    found = False
                elif datetime.datetime(d.year, d.month, d.day) < datetime.datetime(display_dates[0].year, display_dates[0].month, display_dates[0].day):
                    prev_btn.click()
                    btn_ls.append('p')
                else:   
                    next_btn.click()
                    btn_ls.append('n')
                if btn_ls.count('p') != len(btn_ls) and btn_ls.count('n') != len(btn_ls):
                    found = False
                    print('Date not found')


            # Getting match url
            title = match_data['home']['name']+match_data['score']+match_data['away']['name']
            games_on_date = [soup(contain.get_attribute('innerHTML'), features="lxml").find_all('div', {'class':'calendar-game'}) 
                             for contain in driver.find_elements_by_class_name("calendar-date-container") 
                             if contain.text.split('\n')[0]==date][0]
            match_url = [url+'/'+game.find('a', {'class':'match-info'}).get('href') for game in games_on_date 
                         if game.find('div', {'class':'block-home team-home'}).text in match_data['home']['name']
                         and game.find('div', {'class':'block-away team-away'}).text in match_data['away']['name']][0]


            # Addding xG from shot data to events dataframe
            und_shotdata = getUnderstatShotData(match_url, driver)
            events_df['xG'] = np.nan
            und_shotdata.index = events_df.loc[events_df.isShot==True].index
            for i in events_df.loc[events_df.isShot==True].index:
                events_df.loc[[i],'xG'] = und_shotdata.loc[[i],'xG']
    
    
    return events_df


def load_EPV_grid(fname='EPV_grid.csv'):
    """ load_EPV_grid(fname='EPV_grid.csv')
    
    # load pregenerated EPV surface from file. 
    
    Parameters
    -----------
        fname: filename & path of EPV grid (default is 'EPV_grid.csv' in the curernt directory)
        
    Returns
    -----------
        EPV: The EPV surface (default is a (32,50) grid)
    
    """
    epv = np.loadtxt(fname, delimiter=',')
    return epv






def get_EPV_at_location(position,EPV,attack_direction,field_dimen=(106.,68.)):
    """ get_EPV_at_location
    
    Returns the EPV value at a given (x,y) location
    
    Parameters
    -----------
        position: Tuple containing the (x,y) pitch position
        EPV: tuple Expected Possession value grid (loaded using load_EPV_grid() )
        attack_direction: Sets the attack direction (1: left->right, -1: right->left)
        field_dimen: tuple containing the length and width of the pitch in meters. Default is (106,68)
            
    Returrns
    -----------
        EPV value at input position
        
    """
    
    x,y = position
    if abs(x)>field_dimen[0]/2. or abs(y)>field_dimen[1]/2.:
        return 0.0 # Position is off the field, EPV is zero
    else:
        if attack_direction==-1:
            EPV = np.fliplr(EPV)
        ny,nx = EPV.shape
        dx = field_dimen[0]/float(nx)
        dy = field_dimen[1]/float(ny)
        ix = (x+field_dimen[0]/2.-0.0001)/dx
        iy = (y+field_dimen[1]/2.-0.0001)/dy
        return EPV[int(iy),int(ix)]



                

def to_metric_coordinates_from_whoscored(data,field_dimen=(106.,68.) ):
    '''
    Convert positions from Whoscored units to meters (with origin at centre circle)
    '''
    x_columns = [c for c in data.columns if c[-1].lower()=='x'][:2]
    y_columns = [c for c in data.columns if c[-1].lower()=='y'][:2]
    x_columns_mod = [c+'_metrica' for c in x_columns]
    y_columns_mod = [c+'_metrica' for c in y_columns]
    data[x_columns_mod] = (data[x_columns]/100*106)-53
    data[y_columns_mod] = (data[y_columns]/100*68)-34
    return data




def addEpvToDataFrame(data):

    # loading EPV data
    EPV = load_EPV_grid('/work/scrayper/whoscored/EPV_grid.csv')

    # converting opta coordinates to metric coordinates
    data = to_metric_coordinates_from_whoscored(data)

    # calculating EPV for events
    EPV_difference = []
    for i in data.index:
        if data.loc[i, 'type'] == 'Pass' and data.loc[i, 'outcomeType'] == 'Successful':
            start_pos = (data.loc[i, 'x_metrica'], data.loc[i, 'y_metrica'])
            start_epv = get_EPV_at_location(start_pos, EPV, attack_direction=1)
            
            end_pos = (data.loc[i, 'endX_metrica'], data.loc[i, 'endY_metrica'])
            end_epv = get_EPV_at_location(end_pos, EPV, attack_direction=1)
            
            diff = end_epv - start_epv
            EPV_difference.append(diff)
            
        else:
            EPV_difference.append(np.nan)
    
    data = data.assign(EPV_difference = EPV_difference)
    
    
    # dump useless columns
    drop_cols = ['x_metrica', 'endX_metrica', 'y_metrica',
                 'endY_metrica']
    data.drop(drop_cols, axis=1, inplace=True)
    data.rename(columns={'EPV_difference': 'EPV'}, inplace=True)
    
    return data
