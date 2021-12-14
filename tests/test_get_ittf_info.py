from get_ittf_info import get_ittf_info

def test_grab_ranking_data():
    test_rank_df = get_ittf_info.grab_ranking_data('Male')
    expected_first_hundr_ranking_list = list(range(1,101))
    assert expected_first_hundr_ranking_list == test_rank_df['rank'].to_list()[:100]

