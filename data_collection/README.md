# Data collection (Lichess API)

Example code used to download analysed games from Lichess with [berserk](https://github.com/lichess-org/berserk). The final PMind dataset was produced with a very similar pipeline, repeated for many players and split by time control.

- `lichess_scraping.py`: downloads a player's games (with engine evaluations and clocks), filters them by time control and minimum length, and saves them as JSONL.
- `step_1_collect_games.ipynb`: tests the API token and runs the collection for a player.
- `step_2_clean_data.ipynb`: cleans the collected games and turns them into tables.

## Lichess API token

1. Create a token at <https://lichess.org/account/oauth/token>.
2. Expose it as an environment variable. Never commit it.

macOS / Linux:

```bash
export LICHESS_API_TOKEN="lip_..."                               # current session
echo 'export LICHESS_API_TOKEN="lip_..."' >> ~/.bashrc           # permanent
```

Windows (PowerShell):

```powershell
setx LICHESS_API_TOKEN "lip_..."
```
