from seaborn import color_palette
CM = color_palette("RdYlGn", as_cmap=True)
HOT = color_palette("YlOrRd", as_cmap=True)
MONEY = color_palette("YlGn", as_cmap=True)
NEW_COLUMNS = {
    "2": "Ro32",
    "3": "Sweet16",
    "4": "Elite8",
    "5": "Final4",
    "6": "Championship",
    "7": "Winner",
    "total_proj_wins": "Sim # Wins",
    "true_volatility": "Volatility",
    "team": "Team",
    "region": "Region",
    "seed": "Seed",
    "wins_abv_seed":"Wins>Seed Exp",
    "roi":"ESPN ROI",
    "value_rating":"Value Rating"
}

TLM_NAME = "Lehigh Method(w/ Flancer sRAPM)"
FTE_NAME = "538"