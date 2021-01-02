# -*- coding: utf-8 -*-
"""
Created on Wed December 30 13:17 2020

@author: Bucciarati
@twitter: Bucciaratimes
"""

# import packages
import csv
import time
import pandas as pd
import json
from bs4 import BeautifulSoup as soup
from tqdm import trange
from selenium import webdriver


import selenium
from selenium import common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import openpyxl
import xlsxwriter

def getLeagueLinks(base_url):

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        # please replace ylenium container with your selenium container
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options
    )

    driver.minimize_window()

    base_page = driver.get(base_url)

    league_links = []
    for i in range(22):
        league = driver.find_element_by_xpath(
            '//*[@id="popular-tournaments-list"]/li[' + str(i + 1) + ']/a').get_attribute('href')
        league_links.append(league)

    driver.close()
    return league_links

def getMatchLinks(comp_url, base_url):

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options
    )

    teams = []
    comp_page = driver.get(comp_url)
    season = driver.find_element_by_xpath(
        '//*[@id="seasons"]/option[2]').click()
    
    for i in range(20):
        team = driver.find_element_by_xpath(
            '//*[@id="standings-17702-content"]/tr[' + str(i + 1) + ']/td[1]/a').text
        teams.append(team)

    time.sleep(5)

    fixtures_page = driver.find_element_by_xpath(
        '//*[@id="link-fixtures"]').click()

    time.sleep(5)

    date_config_btn = driver.find_element_by_xpath(
        '//*[@id="date-config-toggle-button"]').click()

    time.sleep(5)

    a_year = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[1]/div/table/tbody/tr[1]/td').click()

    selectable_months = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[2]/div/table').find_elements_by_class_name("selectable")

    n_months = len(selectable_months)

    b_year = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[1]/div/table/tbody/tr[2]/td').click()

    selectable_months = driver.find_element_by_xpath(
        '//*[@id="date-config"]/div[1]/div/table/tbody/tr/td[2]/div/table').find_elements_by_class_name("selectable")

    n_months += len(selectable_months)

    date_config_btn = driver.find_element_by_xpath(
        '//*[@id="date-config-toggle-button"]').click()

    match_links = []
    for i in range(n_months):

        time.sleep(2)

        fixtures_table = driver.find_element_by_xpath(
            '//*[@id="tournament-fixture"]')
        fixtures_table = fixtures_table.get_attribute('innerHTML')
        fixtures_table = soup(fixtures_table, features="lxml")

        table_a = fixtures_table.find_all(
            "div", {"class": "divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12"})

        table_b = fixtures_table.find_all(
            "div", {
                "class": "divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 alt"})

        table_rows = table_a + table_b

        links = []
        links = [
            base_url + row.find('a', {'class': "result-1 rc"}).get("href") for row in table_rows]

        for link in links:
            match_links.(link)

        previous_month = driver.find_element_by_xpath(
            '//*[@id="date-controller"]/a[1]').click()
        
    if len(match_links) != 38:

        fixtures_table = driver.find_element_by_xpath(
            '//*[@id="tournament-fixture"]')
        fixtures_table = fixtures_table.get_attribute('innerHTML')
        fixtures_table = soup(fixtures_table)

        table_a = fixtures_table.find_all(
            "div", {"class": "divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12"})

        table_b = fixtures_table.find_all(
            "div", {
                "class": "divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 alt"})
                
        table_rows = table_a + table_b

        links = []
        links = [
            main_url + row.find("a", {"class": "result-1 rc"}).get("href") for row in table_rows]
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

def getMatchesData(team_links):

    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options
    )
    driver.minimize_window()
    
    matches = []
    for i in trange(len(team_links), desc='Single loop'):

        driver.get(team_links[i])
        
        time.sleep(2)
        
        element = driver.find_element_by_xpath('//*[@id="layout-wrapper"]/script[1]')

        script_content = element.get_attribute('innerHTML')

        script_ls = script_content.split(sep="  ")

        script_ls = list(filter(None, script_ls))

        script_ls = [name for name in script_ls if name.strip()]

        script_ls_mod = []

        keys = []

        for item in script_ls:

            if "}" in item:
                item = item.replace(";", "")
                script_ls_mod.append(item[item.index("{"):])
                keys.append(item.split()[1])
            else:
                item = item.replace(";", "")
                script_ls_mod.append(int(''.join(filter(str.isdigit, item))))
                keys.append(item.split()[1])

        match_data = json.loads(script_ls_mod[0])

        for key, item in zip(keys[1:], script_ls_mod[1:]):
            if type(item) == str:
                match_data[key] == json.loads(item)
            else:
                matches[key] == item

        matches.append(match_data)

    driver.close()
    
    return matches

def getMatchData(match_url):
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options
    )
    driver.get(match_url)

    element = driver.find_element_by_xpath(
        '//*[@id="layout-wrapper"]/script[1]')

    script_content = element.get_attribute('innerHTML')

    script_ls = script_content.split(sep="  ")

    script_ls = list(filter(None, script_ls))

    script_ls = [name for name in script_ls if name.strip()]

    script_ls_mod = []

    keys = []
    for item in script_ls:
        if "}" in item:
            item = item.replace(";", "")
            script_ls_mod.append(item[item.index("{"):])
            keys.append(item.split()[1])
        else:
            item = item.replace(";", "")
            script_ls_mod.append(int(''.join(filter(str.isdigit, item))))
            keys.append(item.split()[1])

    match_data = json.loads(script_ls_mod[0])
    for key, item in zip(keys[1:], script_ls_mod[1:]):
        if type(item) == str:
            match_data[key] = json.loads(item)
        else:
            match_data[key] = item
    driver.close()

    return match_data

def getPlayerStats(stats_url):

    venues = ['home', 'away']
    types = {'summary': '1', 'offensive': '2', 'defensive': '3', 'passing': '4'}
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='ylenium_driver_1:4444/wd/hub',
        options=options
    )
    wait = WebDriverWait(driver, 30)

    for venue in venues:
        for key in types.keys():
            
            driver.get(stats_url)

            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="player-table-statistics-body"]/tr/td')))

            button = driver.find_element_by_xpath(
                '//*[@id="live-player-%s-options"]/li[%s]/a' % (venue, types[key]))
	        button.click()

            time.sleep(5)
            
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="player-table-statistics-body"]/tr/td')))

             
            sides = driver.find_elements_by_xpath('//h2/a')
            if venue == 'home':
                side = sides[0].text
                # team = driver.find_elements_by_xpath('//*[@id="layout-wrapper"]/div[3]/h2/a').text
                opponent = driver.find_elements_by_xpath('//*[@id="live-player-stats"]/h2/a').text

            elif venue == 'away':
                side = sides[1].text
                # team = driver.find_elements_by_xpath('//*[@id="live-player-stats"]/h2/a').text
                opponent = driver.find_elements_by_xpath('//*[@id="layout-wrapper"]/div[3]/h2/a').text


            header_data = driver.find_elements_by_xpath(
                '//*[@id="statistics-table-%s-%s"]//tr/th' % (venue, key))
	        master_data = driver.find_elements_by_xpath(
                '//*[@id="statistics-table-%s-%s"]//tr/td' % (venue, key))

            header_list = data_to_list(header_data, 'header')
            length = len(header_list)

            master_list = data_to_list(master_data, 'master')
            master_list = [master_list[x:x + length] for x in range(0, len(master_list) - (length - 1), length)]

            globals()['%s_%s_%s_dataframe' % (side, venue, key)] = pd.DataFrame(master_list, columns=header_list)
            # excel_writer = pd.ExcelWriter(r'C:\Users\leslie hau\Documents\python\whoscored.xlsx')
            # globals()['%s_%s_%s_dataframe' % (side, venue, t)].to_excel(excel_writer, sheet_name=['%s_%s_%s_dataframe' % (side, venue, t)], engine='xlsxwriter')
            # excel_writer.save()

            with open('/work/assets/whoscored/player_stats.csv', 'w') as csv_file:
                writer = csv.writer(csv_file)
            globals()['%s_%s_%s_dataframe' % (side, venue, key)].to_csv(f'/work/assets/whoscored/{side}_vs_{opponent}_{venue}_{key}.csv')





        driver.quit()


def data_to_list(data, name):
	globals()['%s_list' % (name)] = []
	for element in data:
		globals()['%s_list' % (name)].append(element.text)
	return globals()['%s_list' % (name)]


def main():
	print('running')
	url = 'https://www.whoscored.com/Matches/1492070/LiveStatistics/Spain-LaLiga-2020-2021-Barcelona-Eibar'
	getPlayerStats(url)


if __name__ == '__main__':
   main()




                








    






