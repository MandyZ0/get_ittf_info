import pandas as pd
import lxml
from lxml import html
import requests
from lxml import etree
import xml.etree.ElementTree as ET
import re
import numpy as np
import matplotlib.pyplot as plt

## Use xpath to extract first 1000 ranking table from Tabletennis Guide website
def grab_ranking_data(gender):
    #!USE THIS ONE summary of following code:
    gender_dummy = 0
    if gender == 'Male':
        gender_dummy = 1
    elif gender == 'Female':
        gender_dummy = 2
    ply_info_list = []
    for page_i in range(1,10):
            
        test_url = 'https://tabletennis.guide/rating_ittf.php?gender=%s&page=%s'%(gender_dummy,page_i)
        test_html = requests.get(test_url)
        test_doc = html.fromstring(test_html.content)
        # soup = bs4.BeautifulSoup(test_html.text, 'lxml')
        print('currenlty processing page %s'%page_i)
        #extract table list:
        xml_path = r'//*[@id="rightarea"]/div[4]/node()'
        # print(etree.tostring(test_doc.xpath(xml_path)[0], encoding='unicode', pretty_print=True))

        node_list = test_doc.xpath(xml_path)

        node_list = list(dict.fromkeys(node_list))
        node_list.remove('\n\t\t')
        node_list.remove('\n\t')


        # use regular expression to extract 
        reg_exp_info = r'Rank: (.*)Δ: (.*)YOB: (.*)Full name: (.*)Country:  (.*)Rating: (.*)Increment: (.*)'
        reg_exp_id = r'-(\d+)"'
        for node_i in node_list:
            #extract player info
            one_ply_info_lst = re.split(reg_exp_info, node_i.text_content())[1:-1]

            # use regular expression to extract player id
            node_html = etree.tostring(node_i, encoding='unicode')
            one_ply_id = re.split(reg_exp_id, node_html)
            if (len(one_ply_id) == 3):
                one_ply_info_lst.append(one_ply_id[1])
            else:
                one_ply_info_lst.append('')
            
            ply_info_list.append(one_ply_info_lst)

    # generate dataframe
    ply_ranking_df = pd.DataFrame(ply_info_list, columns =['rank', 'rank_increment','YOB','full_name','country','rating','point_increment','id'])

    ## change ply_ranking_df column type: 

    # change ply_ranking_df column type:

    ply_ranking_df['rank'] = (
        ply_ranking_df.replace(r'^\s*$', np.nan, regex=True)['rank'].fillna(0)
        .astype(int)
        .replace(0, np.nan)
    )
    ply_ranking_df['YOB'] = (
        ply_ranking_df.replace(r'^\s*$', np.nan, regex=True)['YOB'].fillna(0)
        .astype(int)
        .replace(0, np.nan)
    )
    ply_ranking_df['rating'] = (
        ply_ranking_df.replace(r'^\s*$', np.nan, regex=True)['rating'].fillna(0)
        .astype(int)
        .replace('0', np.nan)
    )

    ply_ranking_df['id'] = (
        ply_ranking_df.replace(r'^\s*$', np.nan, regex=True)['id'].fillna(0)
        .astype(int)
        .replace('0', np.nan)
    )

    return ply_ranking_df

## get the player's information data from ITTF website

def grab_player_data():
    # write up to a for loop
    pages_list = list(range(0,38601,50))

    all_ranked_ply_info_list = []

    for i in pages_list[:2]:
        print('in page %s, percent %s'%(i,round(float(i/38600),2)))
        test_url = 'https://results.ittf.link/index.php?option=com_fabrik&view=list&listid=35&limitstart35=%s'%i
        test_html = requests.get(test_url)
        test_doc = html.fromstring(test_html.content)
        # soup = bs4.BeautifulSoup(test_html.text, 'lxml')
        
        #extract table list:
        xml_path = r'//*[@id="list_35_com_fabrik_35"]/tbody/node()'
        # print(etree.tostring(test_doc.xpath(xml_path)[0], encoding='unicode', pretty_print=True))
        node_list = test_doc.xpath(xml_path)
        node_list = list(dict.fromkeys(node_list))
        node_list = [ x for x in node_list if "\n" not in x ]
        node_list = node_list[1:]
        


        for node_i in node_list:
            one_ply_reg_split_list = node_i.text_content().replace('\t','').split('\n')[2:-3:2]
            all_ranked_ply_info_list.append(one_ply_reg_split_list)

    #Generate dataframe        
    all_player_info_df = pd.DataFrame(all_ranked_ply_info_list, columns =['id', 'full_name','assoc','gender','YOB','activity','playing_hand','playing_style','grip'])

    # change all_player_info_df column type:
    #id
    all_player_info_df['id'] = (
        all_player_info_df['id'].astype(int)
    )
    #Year of Birth
    all_player_info_df['YOB'] = (
        all_player_info_df.replace(r'^\s*$', np.nan, regex=True)['YOB'].fillna(0)
        .astype(int)
        .replace(0, np.nan)
    )
    # Clean '-'
    all_player_info_df = (
        all_player_info_df.replace(r'^-$', '', regex=True)
    )

    return all_player_info_df

## Get World Table Tennis Championships participants info from WTTF website
def grab_tournament_data():
    # write up to a for loop
    pages_list = list(range(0,25601,100))

    tournament_ply_info_list = []

    for i in pages_list[:2]:
        print('in page %s, percent %s'%(i,round(float(i/25600),2)))
        test_url = 'https://results.ittf.link/index.php?option=com_fabrik&view=list&listid=111&Itemid=286&limitstart111=%s'%i
        test_html = requests.get(test_url)
        test_doc = html.fromstring(test_html.content)
        # soup = bs4.BeautifulSoup(test_html.text, 'lxml')
        
        #extract table list:
        xml_path = r'//*[@id="list_111_com_fabrik_111"]/tbody/node()'
        # print(etree.tostring(test_doc.xpath(xml_path)[0], encoding='unicode', pretty_print=True))
        node_list = test_doc.xpath(xml_path)
        node_list = list(dict.fromkeys(node_list))
        node_list = [ x for x in node_list if "\n" not in x ]
        node_list = node_list[1:]
        
        reg_exp = r'(\n+|\t+)'


        for node_i in node_list:
            tourn_one_participant_split_list = node_i.text_content().replace('\t','').split('\n')
            tourn_one_participant_split_list = [tourn_one_participant_split_list[i] for i in [2,4,7,10,12,14,16,18]]  
            
            # extract tournament info
            reg_exp_tourn = r'(\d+) - (.*), (.*) \((\w+)\)'

            # re.sub(reg_exp, '/', node_list[0].text_content())
            tournament_split_list = re.split(reg_exp_tourn, tourn_one_participant_split_list[0])[1:-1]
            
            one_ply_reg_split_list = tournament_split_list + tourn_one_participant_split_list[1:]
            
            tournament_ply_info_list.append(one_ply_reg_split_list)

    #generate dataframe
    tournament_ply_info_df = pd.DataFrame(tournament_ply_info_list, columns =['year', 'tournament_name','venue_city','venue_country','player_country','full_name','gender','result_singles','result_doubles','result_teams','result_mixed'])
    
    return tournament_ply_info_df

def vis_frequency_bar_chart(df,y_col,x_label,y_label,title,num_of_bars):
    # number of times for each player taking part in the tournament:
    count = df[y_col].value_counts()
    count = count.to_frame()
    count.reset_index(inplace=True)
    count_sub = count[:num_of_bars]

    plt.figure(figsize=(16, 9), dpi=80)
    plt.style.use('ggplot')
    bars = plt.bar(count_sub['index'], count_sub[y_col], color='green')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=90)

    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center', va='bottom')
    
    plt.show()

def percentage_pie_chart(df,y_col):
    df.loc[df[y_col] != ''][['id',y_col]].drop_duplicates()[y_col].value_counts().plot.pie(autopct = "%.2f%%", colors = ['grey', 'yellow'], figsize=(5, 5))