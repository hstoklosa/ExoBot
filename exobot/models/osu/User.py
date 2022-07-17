from exobot.models.osu import BaseModel

class User():

    def __init__(self, data):

        # super().__init__(api)

        self.country         =       data.get('country'        , "")   # Uses the ISO3166-1 alpha-2 country code naming.
        self.username        =       data.get('username'       , "")
        self.pp_rank         =   int(data.get('pp_rank'        , 0))
        self.user_id         =   int(data.get('user_id'        , 0))
        self.count50         =   int(data.get('count50'        , 0))    # Total amount for all ranked, approved, and loved beatmaps played
        self.count100        =   int(data.get('count100'       , 0))    # Total amount for all ranked, approved, and loved beatmaps played
        self.count300        =   int(data.get('count300'       , 0))    # Total amount for all ranked, approved, and loved beatmaps played
        self.playcount       =   int(data.get('playcount'      , 0))    # Only counts ranked, approved, and loved beatmaps
        self.count_rank_a    =   int(data.get('count_rank_a'   , 0))    
        self.count_rank_s    =   int(data.get('count_rank_s'   , 0))    # Counts for SS/SSH/S/SH/A ranks on maps
        self.count_rank_ss   =   int(data.get('count_rank_ss'  , 0))
        self.count_rank_sh   =   int(data.get('count_rank_sh'  , 0))
        self.count_rank_ssh  =   int(data.get('count_rank_ssh' , 0))
        self.pp_country_rank =   int(data.get('pp_country_rank', 0))   # The user's rank in the country.
        self.level           = float(data.get('level'          , 0.0))
        self.pp_raw          = float(data.get('pp_raw'         , 0.0))  # For inactive players this will be 0 to purge them from leaderboards
        self.accuracy        = float(data.get('accuracy'       , 0.0))
        self.total_score     = float(data.get('total_score'    , 0.0))  # Counts every score on ranked, approved, and loved beatmaps
        self.ranked_score    = float(data.get('ranked_score'   , 0.0))  # Counts the best individual score on each ranked, approved, and loved beatmaps
