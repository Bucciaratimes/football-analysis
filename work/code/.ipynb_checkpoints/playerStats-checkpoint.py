import csv
import getopt
import re
import sys
import urllib

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment


class FootBallScrayper:
    def __init__(self, url=None, team=None, player=None):
        self.url = url
        if self.url is None:
            self.url = 'https://fbref.com/en/players/89f951b5/Ivan-Rakitic'
        self.team = team
        self.player = player

    def get_standard_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T0 = table[0]
        T0_data = {}

        minute = T0.find_all(attrs={'data-stat': 'minutes_90s'})
        minute_list = []
        for minute in minute:
            minute_list.append(minute.text)
        T0_data['minute90'] = minute_list

        goals = T0.find_all(attrs={'data-stat': 'goals'})
        T0_data['goal'] = [goal.text for goal in goals]

        goals = T0.find_all(attrs={'data-stat': 'goals_per90'})
        T0_data['goal90'] = [goal.text for goal in goals]

        assts = T0.find_all(attrs={'data-stat': 'assists'})
        T0_data['assist'] = [asst.text for asst in assts]

        asst90s = T0.find_all(attrs={'data-stat': 'assists_per90'})
        T0_data['assist90'] = [asst90.text for asst90 in asst90s]

        goals_assists = T0.find_all(attrs={'data-stat': 'goals_assists_per90'})
        T0_data['G+A90'] = [g_a.text for g_a in goals_assists]

        xg = T0.find_all(attrs={'data-stat': 'xg'})
        xg_list = []
        for xg in xg:
            xg_list.append(xg.text)
        T0_data['xG'] = xg_list

        xg = T0.find_all(attrs={'data-stat': 'xg_per90'})
        xg_list = []
        for xg in xg:
            xg_list.append(xg.text)
        T0_data['xG90'] = xg_list

        xa = T0.find_all(attrs={'data-stat': 'xa'})
        xa_list = []
        for xa in xa:
            xa_list.append(xa.text)
        T0_data['xA'] = xa_list

        xa = T0.find_all(attrs={'data-stat': 'xa_per90'})
        xa_list = []
        for xa in xa:
            xa_list.append(xa.text)
        T0_data['xA90'] = xa_list

        npxgs = T0.find_all(attrs={'data-stat': 'npxg'})
        npxg_list = []
        for npxg in npxgs:
            npxg_list.append(npxg.text)
        T0_data['nPxG'] = npxg_list

        npxg90s = T0.find_all(attrs={'data-stat': 'npxg_per90'})
        npxg90_list = []
        for npxg90 in npxg90s:
            npxg90_list.append(npxg90.text)
        T0_data['nPxG90'] = npxg90_list

        npxg_xas = T0.find_all(attrs={'data-stat': 'npxg_xa_per90'})
        npxg_xa_per90_list = []
        for npxg_xa in npxg_xas:
            npxg_xa_per90_list.append(npxg_xa.text)
        T0_data['nPxGxA90'] = npxg_xa_per90_list


        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/standard.csv', 'w') as csv_file:
            fieldnames = T0_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T0_data.keys()
            value = T0_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i],
                    key[4]: value[4][i],
                    key[5]: value[5][i],
                    key[6]: value[6][i],
                    key[7]: value[7][i],
                    key[8]: value[8][i],
                    key[9]: value[9][i],
                    key[10]: value[10][i],
                    key[11]: value[11][i],
                    key[12]: value[12][i]})

    def get_shoot_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T1 = table[1]
        T1_data = {}

        shoots_total = T1.find_all(attrs={'data-stat': 'shots_total'})
        shoot_total_list = []
        for shoot in shoots_total:
            shoot_total_list.append(shoot.text)
        T1_data['Total Shoot'] = shoot_total_list

        shoot90s = T1.find_all(attrs={'data-stat': 'shots_total_per90'})
        shoot90_list = []
        for shoot90 in shoot90s:
            shoot90_list.append(shoot90.text)
        T1_data['Total Shoot90'] = shoot90_list


        sots = T1.find_all(attrs={'data-stat': 'shots_on_target'})
        sot_list = []
        for sot in sots:
            sot_list.append(sot.text)
        T1_data['On Target'] = sot_list


        sot90s = T1.find_all(attrs={'data-stat': 'shots_on_target_per90'})
        sot90_list = []
        for sot in sot90s:
            sot90_list.append(sot.text)
        T1_data['On Target90'] = sot90_list

        sot_pcts = T1.find_all(attrs={'data-stat': 'shots_on_target_pct'})
        T1_data['On Target %'] = [sot_pct.text for sot_pct in sot_pcts]

        aver_dists = T1.find_all(attrs={'data-stat': 'average_shot_distance'})
        T1_data['average Distance'] = [aver_dist.text for aver_dist in aver_dists]


        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/shoot.csv', 'w') as csv_file:
            fieldnames = T1_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T1_data.keys()
            value = T1_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i],
                    key[4]: value[4][i],
                    key[5]: value[5][i]})


    def get_pass_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T2 = table[2]
        T2_data = {}

        pass_attempts = T2.find_all(attrs={'data-stat': 'passes'})
        attempt_list = []
        for pass_attempt in pass_attempts:
            attempt_list.append(pass_attempt.text)
        T2_data['Pass Attempt'] = attempt_list

        pass_comps = T2.find_all(attrs={'data-stat': 'passes_completed'})
        comp_list = []
        for pass_comp in pass_comps:
            comp_list.append(pass_comp.text)
        T2_data['Pass Complete'] = comp_list


        pass_pct = T2.find_all(attrs={'data-stat': 'passes_pct'})
        pct_list = []
        for pct in pass_pct:
            pct_list.append(pct.text)
        T2_data['Pass Comp %'] = pct_list


        pass_distances = T2.find_all(attrs={'data-stat': 'passes_total_distance'})
        distance_list = []
        for pass_distance in pass_distances:
            distance_list.append(pass_distance.text)
        T2_data['PassTotalDistance'] = distance_list


        pass_progress = T2.find_all(attrs={'data-stat': 'passes_progressive_distance'})
        progres_list = []
        for pass_progres in pass_progress:
            progres_list.append(pass_progres.text)
        T2_data['PassProgressDistance'] = progres_list

        keypasses = T2.find_all(attrs={'data-stat': 'assisted_shots'})
        keypass_list = []
        for keypass in keypasses:
            keypass_list.append(keypass.text)
        T2_data['KeyPass'] = keypass_list

        pass_final_thirds = T2.find_all(attrs={'data-stat': 'passes_into_final_third'})
        final_third_list = []
        for pass_final_third in pass_final_thirds:
            final_third_list.append(pass_final_third.text)
        T2_data['FinalThirdPass'] = final_third_list

        pass_into_penaltys = T2.find_all(
            attrs={'data-stat': 'passes_into_penalty_area'})
        into_penalty_list = []
        for pass_into_penalty in pass_into_penaltys:
            into_penalty_list.append(pass_into_penalty.text)
        T2_data['PassIntoPenalty'] = into_penalty_list


        cross_into_penaltys = T2.find_all(
            attrs={'data-stat': 'crosses_into_penalty_area'})
        cross_list = []
        for cross_into_penalty in cross_into_penaltys:
            cross_list.append(cross_into_penalty.text)
        T2_data['CrossIntoPenalty '] = cross_list


        progressive_passes = T2.find_all(attrs={'data-stat': 'progressive_passes'})
        progressive_pass_list = []
        for progressive_pass in progressive_passes:
            progressive_pass_list.append(progressive_pass.text)
        T2_data['Progree Pass'] = progressive_pass_list


        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/pass.csv', 'w') as csv_file:
            fieldnames = T2_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T2_data.keys()
            value = T2_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i],
                    key[4]: value[4][i],
                    key[5]: value[5][i],
                    key[6]: value[6][i],
                    key[7]: value[7][i],
                    key[8]: value[8][i],
                    key[9]: value[9][i]})

    
    def get_passtype_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T3 = table[3]
        T3_data = {}

        pass_throws = T3.find_all(attrs={'data-stat': 'through_balls'})
        throw_list = []
        for throw in pass_throws:
            throw_list.append(throw.text)
        T3_data['ThroughPass'] = throw_list

        pass_presses = T3.find_all(attrs={'data-stat': 'passes_pressure'})
        press_list = []
        for pass_press in pass_presses:
            press_list.append(pass_press.text)
        T3_data['PassUnderPress'] = press_list


        pass_switches = T3.find_all(attrs={'data-stat': 'passes_switches'})
        switch_list = []
        for pass_switch in pass_switches:
            switch_list.append(pass_switch.text)
        T3_data['SwitchPass'] = switch_list


        pass_intercepts = T3.find_all(attrs={'data-stat': 'passes_intercepted'})
        intercept_list = []
        for pass_intercept in pass_intercepts:
            intercept_list.append(pass_intercept.text)
        T3_data['PassIntercepted'] = intercept_list


        pass_blockes = T3.find_all(attrs={'data-stat': 'passes_blocked'})
        block_list = []
        for pass_block in pass_blockes:
            block_list.append(pass_block.text)
        T3_data['PassBlocked'] = block_list


        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/passtype.csv', 'w') as csv_file:
            fieldnames = T3_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T3_data.keys()
            value = T3_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i],
                    key[4]: value[4][i]})

    def get_creation_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T4 = table[4]
        T4_data = {}


        scas = T4.find_all(attrs={'data-stat': 'sca'})
        sca_list = []
        for sca in scas:
            sca_list.append(sca.text)
        T4_data['Shoot Create Action'] = sca_list

        sca_per90s = T4.find_all(attrs={'data-stat': 'sca_per90'})
        sca_per90_list = []
        for sca_per90 in sca_per90s:
            sca_per90_list.append(sca_per90.text)
        T4_data['Shoot Create Action90'] = sca_per90_list


        sca_passes_lives = T4.find_all(attrs={'data-stat': 'sca_passes_live'})
        sca_passes_live_list = []
        for sca_passes_live in sca_passes_lives:
            sca_passes_live_list.append(sca_passes_live.text)
        T4_data['SCA(Pass)'] = sca_passes_live_list

        sca_dribbles = T4.find_all(attrs={'data-stat': 'sca_dribbles'})
        sca_dribble_list = []
        for sca_dribble in sca_dribbles:
            sca_dribble_list.append(sca_dribble.text)
        T4_data['SCA(Dribble)'] = sca_dribble_list


        sca_shots = T4.find_all(attrs={'data-stat': 'sca_shots'})
        sca_shot_list = []
        for sca_shot in sca_shots:
            sca_shot_list.append(sca_shot.text)
        T4_data['SCA(Shoot)'] = sca_shot_list


        sca_fouleds = T4.find_all(attrs={'data-stat': 'sca_fouled'})
        sca_fouled_list = []
        for sca_fouled in sca_fouleds:
            sca_fouled_list.append(sca_fouled.text)
        T4_data['SCA(Fouled)'] = sca_fouled_list


        sca_defenses = T4.find_all(attrs={'data-stat': 'sca_defense'})
        sca_defense_list = []
        for sca_defense in sca_defenses:
            sca_defense_list.append(sca_defense.text)
        T4_data['SCA(Defense)'] = sca_defense_list


        gcas = T4.find_all(attrs={'data-stat': 'gca'})
        gca_list = []
        for gca in gcas:
            gca_list.append(gca.text)
        T4_data['Goal Create Action'] = gca_list


        gca_per90s = T4.find_all(attrs={'data-stat': 'gca_per90'})
        gca_per90_list = []
        for gca_per90 in gca_per90s:
            gca_per90_list.append(gca_per90.text)
        T4_data['Goal Create Action90'] = gca_per90_list


        gca_passes_lives = T4.find_all(attrs={'data-stat': 'gca_passes_live'})
        gca_passes_live_list = []
        for gca_passes_live in gca_passes_lives:
            gca_passes_live_list.append(gca_passes_live.text)
        T4_data['GCA(Pass)'] = gca_passes_live_list


        gca_dribbles = T4.find_all(attrs={'data-stat': 'gca_dribbles'})
        gca_dribble_list = []
        for gca_dribble in gca_dribbles:
            gca_dribble_list.append(gca_dribble.text)
        T4_data['GCA(Dribble)'] = gca_dribble_list


        gca_shots = T4.find_all(attrs={'data-stat': 'gca_shots'})
        gca_shot_list = []
        for gca_shot in gca_shots:
            gca_shot_list.append(gca_shot.text)
        T4_data['GCA(Shoot)'] = gca_shot_list


        gca_fouleds = T4.find_all(attrs={'data-stat': 'gca_fouled'})
        gca_fouled_list = []
        for gca_fouled in gca_fouleds:
            gca_fouled_list.append(gca_fouled.text)
        T4_data['GCA(Fouled)'] = gca_fouled_list


        gca_defenses = T4.find_all(attrs={'data-stat': 'gca_defense'})
        gca_defense_list = []
        for gca_defense in gca_defenses:
            gca_defense_list.append(gca_defense.text)
        T4_data['GCA(Defense)'] = gca_defense_list


        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/goal&shot.csv', 'w') as csv_file:
            fieldnames = T4_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T4_data.keys()
            value = T4_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i],
                    key[4]: value[4][i],
                    key[5]: value[5][i],
                    key[6]: value[6][i],
                    key[7]: value[7][i],
                    key[8]: value[8][i],
                    key[9]: value[9][i],
                    key[10]: value[10][i],
                    key[11]: value[11][i],
                    key[12]: value[12][i],
                    key[13]: value[13][i]})


    def get_defense_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T5 = table[5]
        T5_data = {}

        tackles = T5.find_all(attrs={'data-stat': 'tackles'})
        tackle_list = []
        for tackle in tackles:
            tackle_list.append(tackle.text)
        T5_data['Tackles'] = tackle_list

        tackle_wons = T5.find_all(attrs={'data-stat': 'tackles_won'})
        tackle_won_list = []
        for tackle_won in tackle_wons:
            tackle_won_list.append(tackle_won.text)
        T5_data['Tackles Won'] = tackle_won_list


        tackle_passes_lives = T5.find_all(attrs={'data-stat': 'tackles_def_3rd'})
        tackle_passes_live_list = []
        for tackle_passes_live in tackle_passes_lives:
            tackle_passes_live_list.append(tackle_passes_live.text)
        T5_data['Tackle-In-Def3rd'] = tackle_passes_live_list


        tackle_passes_deads = T5.find_all(attrs={'data-stat': 'tackles_mid_3rd'})
        tackle_passes_dead_list = []
        for tackle_passes_dead in tackle_passes_deads:
            tackle_passes_dead_list.append(tackle_passes_dead.text)
        T5_data['Tackle-In-Mid3rd'] = tackle_passes_dead_list


        tackle_dribbles = T5.find_all(attrs={'data-stat': 'tackles_att_3rd'})
        tackle_dribble_list = []
        for tackle_dribble in tackle_dribbles:
            tackle_dribble_list.append(tackle_dribble.text)
        T5_data['Tackle-In-Att3rd'] = tackle_dribble_list


        dribble_tackles = T5.find_all(attrs={'data-stat': 'dribble_tackles'})
        dribble_tackle_list = []
        for dribble_tackle in dribble_tackles:
            dribble_tackle_list.append(sca_shot.text)
        T5_data['Tackle(Dribble)'] = dribble_tackle_list


        vsdribblepcts = T5.find_all(attrs={'data-stat': 'dribble_tackles_pct'})
        vsdribblepct_list = []
        for vsdribblepct in vsdribblepcts:
            vsdribblepct_list.append(vsdribblepct.text)
        T5_data['Tackle(Dribble)%'] = vsdribblepct_list


        dribble_pasts = T5.find_all(attrs={'data-stat': 'dribbled_past'})
        dribble_past_list = []
        for dribble_past in dribble_pasts:
            dribble_past_list.append(dribble_past.text)
        T5_data['Dribble Past'] = dribble_past_list


        pressures = T5.find_all(attrs={'data-stat': 'pressures'})
        pressure_list = []
        for pressure in pressures:
            pressure_list.append(pressure.text)
        T5_data['Press'] = pressure_list


        press_regains = T5.find_all(attrs={'data-stat': 'pressure_regains'})
        press_regain_list = []
        for press_regain in press_regains:
            press_regain_list.append(press_regain.text)
        T5_data['Press Success'] = press_regain_list


        press_regain_pcts = T5.find_all(attrs={'data-stat': 'pressure_regain_pct'})
        press_regain_pct_list = []
        for press_regain_pct in press_regain_pcts:
            press_regain_pct_list.append(press_regain_pct.text)
        T5_data['Press Success %'] = press_regain_pct_list


        press_def3rds = T5.find_all(attrs={'data-stat': 'pressures_def_3rd'})
        press_def3rd_list = []
        for press_def3rd in press_def3rds:
            press_def3rd_list.append(press_def3rd.text)
        T5_data['Press-In-Def3rd'] = press_def3rd_list


        press_mid_3rds = T5.find_all(attrs={'data-stat': 'pressures_mid_3rd'})
        press_mid_3rd_list = []
        for press_mid_3rd in press_mid_3rds:
            press_mid_3rd_list.append(press_mid_3rd.text)
        T5_data['Press-In-Mid3rd'] = press_mid_3rd_list


        press_att_3rds = T5.find_all(attrs={'data-stat': 'pressures_att_3rd'})
        press_att_3rd_list = []
        for press_att_3rd in press_att_3rds:
            press_att_3rd_list.append(press_att_3rd.text)
        T5_data['Press-In-Att3rd'] = press_att_3rd_list

        scas = T5.find_all(attrs={'data-stat': 'blocks'})
        sca_list = []
        for sca in scas:
            sca_list.append(sca.text)
        T5_data['Block'] = sca_list

        sca_passes_deads = T5.find_all(attrs={'data-stat': 'interceptions'})
        sca_passes_dead_list = []
        for sca_passes_dead in sca_passes_deads:
            sca_passes_dead_list.append(sca_passes_dead.text)
        T5_data['Intercept'] = sca_passes_dead_list

        sca_dribbles = T5.find_all(attrs={'data-stat': 'tackles_interceptions'})
        sca_dribble_list = []
        for sca_dribble in sca_dribbles:
            sca_dribble_list.append(sca_dribble.text)
        T5_data['Tackle + Intercept'] = sca_dribble_list

        sca_shots = T5.find_all(attrs={'data-stat': 'clearances'})
        sca_shot_list = []
        for sca_shot in sca_shots:
            sca_shot_list.append(sca_shot.text)
        T5_data['Clear'] = sca_shot_list


        sca_fouleds = T5.find_all(attrs={'data-stat': 'errors'})
        sca_fouled_list = []
        for sca_fouled in sca_fouleds:
            sca_fouled_list.append(sca_fouled.text)
        T5_data['Error'] = sca_fouled_list

        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/defense.csv', 'w') as csv_file:
            fieldnames = T5_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T5_data.keys()
            value = T5_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i],
                    key[4]: value[4][i],
                    key[5]: value[5][i],
                    key[6]: value[6][i],
                    key[7]: value[7][i],
                    key[8]: value[8][i],
                    key[9]: value[9][i],
                    key[10]: value[10][i],
                    key[11]: value[11][i],
                    key[12]: value[12][i],
                    key[13]: value[13][i],
                    key[14]: value[14][i],
                    key[15]: value[15][i],
                    key[16]: value[16][i],
                    key[17]: value[17][i],
                    key[18]: value[18][i]})

    def get_possession_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T6 = table[6]
        T6_data = {}

        touches = T6.find_all(attrs={'data-stat': 'touches'})
        touch_list = []
        for touch in touches:
            touch_list.append(touch.text)
        T6_data['touches'] = touch_list


        touches_def_pen_area = T6.find_all(attrs={'data-stat': 'touches_def_pen_area'})
        tdpa_list = []
        for touch in touches_def_pen_area:
            tdpa_list.append(touch.text)
        T6_data['touch-In-Def-Penalty'] = tdpa_list


        touches_def_3rd = T6.find_all(attrs={'data-stat': 'touches_def_3rd'})
        td3_list = []
        for touch in touches_def_3rd:
            td3_list.append(touch.text)
        T6_data['touch-In-Def3rd'] = td3_list


        touches_mid_3rd = T6.find_all(attrs={'data-stat': 'touches_mid_3rd'})
        tm3_list = []
        for touch in touches_mid_3rd:
            tm3_list.append(touch.text)
        T6_data['touch-In-Mid3rd'] = tm3_list


        touches_att_3rd = T6.find_all(attrs={'data-stat': 'touches_att_3rd'})
        ta3_list = []
        for touch in touches_att_3rd:
            ta3_list.append(touch.text)
        T6_data['touch-In-Att3rd'] = ta3_list


        touches_att_pen_area = T6.find_all(attrs={'data-stat': 'touches_att_pen_area'})
        tapa_list = []
        for touch in touches_att_pen_area:
            tapa_list.append(touch.text)
        T6_data['touch-In-Att-Penalty'] = tapa_list


        pass_targets = T6.find_all(attrs={'data-stat': 'pass_targets'})
        pt_list = []
        for touch in pass_targets:
            pt_list.append(touch.text)
        T6_data['Pass Target Num'] = pt_list


        passes_received = T6.find_all(attrs={'data-stat': 'passes_received'})
        pr_list = []
        for touch in passes_received:
            pr_list.append(touch.text)
        T6_data['Pass Received Num'] = pr_list

        passes_received = T6.find_all(attrs={'data-stat': 'passes_received_pct'})
        pr_list = []
        for touch in passes_received:
            pr_list.append(touch.text)
        T6_data['Pass Received %'] = pr_list


        touches = T6.find_all(attrs={'data-stat': 'dribbles_completed'})
        touch_list = []
        for touch in touches:
            touch_list.append(touch.text)
        T6_data['Dribble Comp'] = touch_list


        touches_def_pen_area = T6.find_all(attrs={'data-stat': 'dribbles'})
        tdpa_list = []
        for touch in touches_def_pen_area:
            tdpa_list.append(touch.text)
        T6_data['Dribble Attempt'] = tdpa_list


        touches_def_3rd = T6.find_all(attrs={'data-stat': 'dribbles_completed_pct'})
        td3_list = []
        for touch in touches_def_3rd:
            td3_list.append(touch.text)
        T6_data['Dribble Comp %'] = td3_list


        touches_mid_3rd = T6.find_all(attrs={'data-stat': 'nutmegs'})
        tm3_list = []
        for touch in touches_mid_3rd:
            tm3_list.append(touch.text)
        T6_data['Nutmeg'] = tm3_list


        touches_att_3rd = T6.find_all(
            attrs={'data-stat': 'carry_progressive_distance'})
        ta3_list = []
        for touch in touches_att_3rd:
            ta3_list.append(touch.text)
        T6_data['Dribble Progress Dist'] = ta3_list


        touches_att_pen_area = T6.find_all(attrs={'data-stat': 'progressive_carries'})
        tapa_list = []
        for touch in touches_att_pen_area:
            tapa_list.append(touch.text)
        T6_data['Progress Dribble  Num'] = tapa_list


        pass_targets = T6.find_all(attrs={'data-stat': 'carries_into_final_third'})
        pt_list = []
        for touch in pass_targets:
            pt_list.append(touch.text)
        T6_data['Dribble-Into-Final3rd'] = pt_list


        passes_received = T6.find_all(attrs={'data-stat': 'carries_into_penalty_area'})
        pr_list = []
        for touch in passes_received:
            pr_list.append(touch.text)
        T6_data['Dribble-Into-Penalty'] = pr_list

        touches_att_3rd = T6.find_all(attrs={'data-stat': 'miscontrols'})
        ta3_list = []
        for touch in touches_att_3rd:
            ta3_list.append(touch.text)
        T6_data['Control Miss'] = ta3_list

        touches_att_3rd = T6.find_all(attrs={'data-stat': 'dispossessed'})
        ta3_list = []
        for touch in touches_att_3rd:
            ta3_list.append(touch.text)
        T6_data['Lost'] = ta3_list


        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/possession.csv', 'w') as csv_file:
            fieldnames = T6_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T6_data.keys()
            value = T6_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i],
                    key[4]: value[4][i],
                    key[5]: value[5][i],
                    key[6]: value[6][i],
                    key[7]: value[7][i],
                    key[8]: value[8][i],
                    key[9]: value[9][i],
                    key[10]: value[10][i],
                    key[11]: value[11][i],
                    key[12]: value[12][i],
                    key[13]: value[13][i],
                    key[14]: value[14][i],
                    key[15]: value[15][i],
                    key[16]: value[16][i],
                    key[17]: value[17][i],
                    key[18]: value[18][i]})

    def get_miscellaneous_data(self):
        res = requests.get(self.url)
        comm = re.compile('<!--|-->')
        soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
        table = soup.findAll('tbody')

        T7 = table[8]
        T7_data = {}

        ball_recoveres = T7.find_all(attrs={'data-stat': 'ball_recoveries'})
        T7_data['Ball Recovery'] = [recover.text for recover in ball_recoveres]

        aerial_won_pct = T7.find_all(attrs={'data-stat': 'aerials_won_pct'})
        T7_data['Aerials Won %'] = [won.text for won in aerial_won_pct]

        aerial_won = T7.find_all(attrs={'data-stat': 'aerials_won'})
        T7_data['Aerials Won'] = [won.text for won in aerial_won]

        aerial_lost = T7.find_all(attrs={'data-stat': 'aerials_lost'})
        T7_data['Aerials Lost'] = [lost.text for lost in aerial_lost]


        with open(f'/work/assets/fbref/team/{self.team}/player/total_stats/{self.player}/miscellaneous.csv', 'w') as csv_file:
            fieldnames = T7_data.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            key = T7_data.keys()
            value = T7_data.values()
            key = list(key)
            value = list(value)
            for i in range(len(value[0])):
                writer.writerow({
                    key[0]: value[0][i],
                    key[1]: value[1][i],
                    key[2]: value[2][i],
                    key[3]: value[3][i]
                })
