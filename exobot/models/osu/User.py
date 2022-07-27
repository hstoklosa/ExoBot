from exobot.models.osu import BaseModel

"""

data = {
    'avatar_url': 'https://osu.ppy.sh/images/layout/avatar-guest.png',
    'country_code': 'GB',
    'default_group': 'default',
    'id': 23568946,
    'is_active': True,
    'is_bot': False,
    'is_deleted': False,
    'is_online': False,
    'is_supporter': False,
    'last_visit': '2022-07-16T23:56:02+00:00',
    'pm_friends_only': False,
    'profile_colour': None,
    'username': 'levsiak',
    'cover_url': 'https://osu.ppy.sh/images/headers/profile-covers/c3.jpg',
    'discord': None,
    'has_supported': False,
    'interests': None,
    'join_date': '2021-05-21T18:25:54+00:00',
    'kudosu': {'total': 0, 'available': 0},
    'location': None,
    'max_blocks': 50,
    'max_friends': 250,
    'occupation': None,
    'playmode': 'osu',
    'playstyle': None,
    'post_count': 0,
    'profile_order': [
        'me',
        'recent_activity',
        'top_ranks',
        'medals',
        'historical',
        'beatmaps',
        'kudosu',
        ],
    'title': None,
    'title_url': None,
    'twitter': None,
    'website': None,
    'country': {'code': 'GB', 'name': 'United Kingdom'},
    'cover': {'custom_url': None,
              'url': 'https://osu.ppy.sh/images/headers/profile-covers/c3.jpg',
              'id': '3'},
    'account_history': [],
    'active_tournament_banner': None,
    'badges': [],
    'beatmap_playcounts_count': 167,
    'comments_count': 0,
    'favourite_beatmapset_count': 0,
    'follower_count': 2,
    'graveyard_beatmapset_count': 0,
    'groups': [],
    'guest_beatmapset_count': 0,
    'loved_beatmapset_count': 0,
    'mapping_follower_count': 0,
    'monthly_playcounts': [
        {'start_date': '2021-05-01', 'count': 67},
        {'start_date': '2021-10-01', 'count': 542},
        {'start_date': '2021-11-01', 'count': 300},
        {'start_date': '2021-12-01', 'count': 61},
        {'start_date': '2022-02-01', 'count': 57},
        {'start_date': '2022-05-01', 'count': 6},
        {'start_date': '2022-06-01', 'count': 21},
        ],
    'page': {'html': '', 'raw': ''},
    'pending_beatmapset_count': 0,
    'previous_usernames': [],
    'ranked_beatmapset_count': 0,
    'replays_watched_counts': [],
    'scores_best_count': 40,
    'scores_first_count': 0,
    'scores_pinned_count': 0,
    'scores_recent_count': 0,
    'statistics': {
        'level': {'current': 33, 'progress': 37},
        'global_rank': 2019736,
        'pp': 124.332,
        'ranked_score': 19517017,
        'hit_accuracy': 79.9839,
        'play_count': 1044,
        'play_time': 74737,
        'total_score': 242428220,
        'total_hits': 195767,
        'maximum_combo': 444,
        'replays_watched_by_others': 0,
        'is_ranked': True,
        'grade_counts': {
            'ss': 0,
            'ssh': 0,
            's': 0,
            'sh': 0,
            'a': 7,
            },
        'country_rank': 55255,
        'rank': {'country': 55255},
        },
    'support_level': 0,
    'user_achievements': [
        {'achieved_at': '2021-11-05T11:20:24+00:00',
         'achievement_id': 58},
        {'achieved_at': '2021-10-23T10:21:10+00:00',
         'achievement_id': 57},
        {'achieved_at': '2021-10-17T16:09:02+00:00',
         'achievement_id': 127},
        {'achieved_at': '2021-10-12T11:18:43+00:00',
         'achievement_id': 56},
        {'achieved_at': '2021-05-26T17:38:12+00:00',
         'achievement_id': 79},
        {'achieved_at': '2021-05-21T18:35:52+00:00',
         'achievement_id': 55},
        ],
    'rankHistory': {'mode': 'osu', 'data': [1892290,1894031,1895804,1897542,1899502,1901634,1903621,1905254,1906966,1908592,1910182,1911953,1913872,1915668,1917251,1917902,1919524,
        1921096,1922723,1924559,1926362,1926321,1927792,1929275,1930719,1932300,1934160,1935795,1937211,1938614,1940104,1941620,1943241,1944988,1946744,1948219,1949778,1951202,1952853,1954622,1956380,1958073,1959647,1961180,1962705,1964129,1965641,1967370,1969017,1970501,1972009,1973447,1974916,1976509,1978297,1979885,1981473,1983088,1984629,1986270,1987925,1989610,1991337,1992977,1988603,1983320,1984884,1986407,1988107,1989669,1991212,1992733,1994302,1995840,1997317,1998773,2000245,2001697,2003145,2004550, 2006108,2007703,2009229,2010790,2012330,2013927,2015418,2016862,2018284,2019736,
        ]},
    'rank_history': {'mode': 'osu', 'data': [1892290,1894031,1895804,1897542,1899502,1901634,1903621,1905254,1906966,1908592,1910182,1911953,1913872,1915668,1917251,1917902,1919524,1921096,1922723,1924559,1926362,1926321,1927792,1929275,1930719,1932300,1934160,1935795,1937211,1938614,1940104,1941620,1943241,1944988,1946744,1948219,1949778,1951202,1952853,1954622,1956380,1958073,1959647,1961180,1962705,1964129,1965641,1967370,1969017,1970501,1972009,1973447,1974916,1976509,1978297,1979885,1981473,1983088,1984629,1986270,1987925,1989610,1991337,1992977,1988603,1983320,1984884,1986407,1988107,1989669,1991212,1992733,1994302,1995840,1997317,1998773,2000245,2001697,2003145,2004550,2006108,2007703,2009229,2010790,2012330,2013927,2015418,2016862,2018284,2019736,
        ]},
    'ranked_and_approved_beatmapset_count': 0,
    'unranked_beatmapset_count': 0,
    }
"""


class User():

    def __init__(self, data):

        # super().__init__(api)

        self.avatar_url      =         data.get('avatar_url'     , "")
        self.username        =         data.get('username'       , "")
        self._id             =         data.get('id'        , 0)
        self.current_level   =   float(data.get('statistics').get('level').get('current', 0.0))
        self.progress        =   float(data.get('statistics').get('level').get('progress', 0.0))
        self.accuracy        =   float(data.get('statistics').get('hit_accuracy', 0.0))
        self.pp_raw          =   float(data.get('statistics').get('pp'         , 0.0))  # For inactive players this will be 0 to purge them from leaderboards
        self.playcount       =     int(data.get('statistics').get('play_count', 0))    # Only counts ranked, approved, and loved beatmaps
        self.global_rank     =     int(data.get('statistics').get('global_rank', 0))
        self.country_rank    =     int(data.get('statistics').get('country_rank', 0))
        self.country         =         data.get('country_code', "")   
