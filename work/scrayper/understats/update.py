import scraping.match_scraper as ms
import scraping.season_scraper as ss

# Updates the shots datasets and the players datasets
ms.update_shots_dataset(2022)
ss.generate_players_csv(2022,2022)
