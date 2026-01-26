import json
import berserk


def scrapping_data(client,ALLOWED_SPEEDS,USERNAME,MAX_GAMES,MIN_PLIES,ORIGINAL_DATA_PARENT=None):
    """
    scrapping data from Lichess
    
    :param client: client session established
    :param ALLOWED_SPEEDS: all valable speeds
    :param USERNAME: player username
    :param MAX_GAMES: max game number 
    :param MIN_PLIES: min movement number
    :param ORIGINAL_DATA_PARENT: data destination repertory
    """
    def get_player_data(players,color):
        """
        get player information
        
        :param players: player information
        :param color: color selector
        """
        #choose player by color
        player=players.get(color,{})
        #return information in dict type
        return {"name":player.get("user",{}).get("name"),"rating":player.get("rating"),"analysis":player.get("analysis",{})}
    games_data=[]
    games=client.games.export_by_player(USERNAME,max=MAX_GAMES,moves=True,players="all",evals=True)
    for game in games:
        #Filtering: if speed is not recognized
        if game.get("speed") not in ALLOWED_SPEEDS:
            continue
        moves=game.get("moves","")
        moves_list=moves.split()
        #Filtering: moves must >=MIN_PLIES: get only interessing game data
        if len(moves_list)<MIN_PLIES:
            continue
        players=game.get("players",{})
        #Filtering: give up if we don't have information of all player
        if "white" not in players or "black" not in players:
            continue
        white_data,black_data=get_player_data(players,"white"),get_player_data(players,"black")
        #print game to check structure 
        print(game)
        print(f"white_rating:{white_data['rating']}\nblack_rating:{black_data['rating']}")

        #movement analysis part
        analysis=game.get("analysis",[])
        #print analysis information to verify the format
        print(analysis)
        moves_analysis=[]

        #get analytical information for each movement
        for i,move in enumerate(moves_list):
            
            move_info={"ply":i+1,#id of movement
                       "move":move,#movement
                       "eval":None,#evaluation
                       "meta":None,#revise
                       "best":None,#best movement
                       "judgment":None,#judgment: inaccuracy,mistake,blunder
                       "comment":None}#comment
            #evaluation
            a=analysis[i]
            if "eval" in a.keys():
                move_info["eval"]=a.get('eval')
            elif "mate" in a.keys():
                move_info["eval"]=f"mate {a['mate']}"
            #best movement
            if "best" in a.keys():
                move_info["best"] = a.get('best')
            #judgment+comment
            if "judgment" in a.keys():
                judgment=a.get('judgment')
                move_info["judgment"] = judgment.get("name")
                move_info["comment"] = judgment.get("comment")

            moves_analysis.append(move_info)
        #make the summary
        game_summary = {
            "speed": game.get("speed"), #tempo(cadence) of the game
            "variant": game.get("variant"),#variant:standard,chess960
            "winner": game.get("winner"),#winner

            "white": {
                "name": white_data["name"],
                "rating": white_data["rating"],#rating of player in game
                "acpl": white_data["analysis"].get("acpl"),#average centipawn loss(global quality)
                "blunder": white_data["analysis"].get("blunder"),#blunder number
                "mistake": white_data["analysis"].get("mistake"),#mistake number
                "inaccuracy": white_data["analysis"].get("inaccuracy"),#inaccuracy number
            },

            "black": {#same then white
                "name": black_data["name"],
                "rating": black_data["rating"],
                "acpl": black_data["analysis"].get("acpl"),
                "blunder": black_data["analysis"].get("blunder"),
                "mistake": black_data["analysis"].get("mistake"),
                "inaccuracy": black_data["analysis"].get("inaccuracy"),
            }
        }
        games_data.append({
            "id": game["id"],#game id
            "summary": game_summary,#summary
            "moves_analysis": moves_analysis #analysis
        })
        print(f"loading: {len(games_data)}")
    print(f"[USERNAME]: {USERNAME}\nGames kept after clearning: {len(games_data)}")
    if ORIGINAL_DATA_PARENT is not None:
        #save as .jsonl file -> one line = one game
        save_games_data(games_data,f"{ORIGINAL_DATA_PARENT}/{USERNAME}_original.jsonl")
    return games_data

def save_games_data(games_data,file_path):
    """
    save games data scrapped in local

    :param games_data: player games informations
    :param file_path: destination -> Always "{ORIGINAL_DATA_PARENT}/{USERNAME}_original.jsonl"
    """
    with open(file_path,"w",encoding="utf-8") as f:
        for game in games_data:
            f.write(json.dumps(game)+"\n")

def load_games_data(file_path):
    """
    get local scrapped data
    :param file_path: file path
    """
    games=[]
    with open(file_path,"r",encoding="utf-8") as f:
        for line in f:
            games.append(json.loads(line))
    return games
    
def print_games_data(games_data, nblines=-1):
    """
    Print games informations (new structured format)

    :param games_data: list of parsed games
    :param nblines: number of games to print (-1 = all)
    """

    if not isinstance(games_data, list):
        raise TypeError("your games data is not correct format")

    if nblines == 0:
        return

    cpt = 0

    for game in games_data:
        if nblines != -1 and cpt >= nblines:
            return

        summary = game.get("summary", {})
        white = summary.get("white", {})
        black = summary.get("black", {})

        print("=" * 60)
        print(f"Game ID : {game.get('id')}")
        print(f"Speed   : {summary.get('speed')}")
        print(f"Variant : {summary.get('variant')}")
        print(f"Winner  : {summary.get('winner')}")
        print("-" * 60)

        print(
            f"White : {white.get('name')} | "
            f"Rating: {white.get('rating')} | "
            f"ACPL: {white.get('acpl')} | "
            f"Blunders: {white.get('blunder')}"
        )

        print(
            f"Black : {black.get('name')} | "
            f"Rating: {black.get('rating')} | "
            f"ACPL: {black.get('acpl')} | "
            f"Blunders: {black.get('blunder')}"
        )

        print("-" * 60)
        print(f"Number of moves : {len(game.get('moves_analysis', []))}")
        print("=" * 60)
        print()

        cpt += 1
