from get_ittf_info import get_ittf_info

def test_grab_ranking_data_Male():
    test_rank_df = get_ittf_info.grab_ranking_data('Male',2)
    expected_first_hundr_ranking_list = list(range(1,101))
    assert expected_first_hundr_ranking_list == test_rank_df['rank'].to_list()[:100]

def test_grab_player_data():
    test_df = get_ittf_info.grab_player_data(1)
    expected_first_id = 200266
    assert expected_first_id == test_df.iloc[0,0]

def test_grab_tournament_data():
    test_df = get_ittf_info.grab_tournament_data(1)
    expected_latest_tourn_city = 'Budapest'
    assert expected_latest_tourn_city == test_df.iloc[0,2]