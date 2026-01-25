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
    games_data=[]
    games=client.games.export_by_player(USERNAME,max=MAX_GAMES,moves=True,players="all")
    for game in games:
        #if speed is not recognized
        if game.get("speed") not in ALLOWED_SPEEDS:
            continue
        moves=game.get("moves","")
        moves_list=moves.split()
        # moves must >=MIN_PLIES: get only interessing game data
        if len(moves_list)<MIN_PLIES:
            continue
        players=game.get("players",{})
        white=players.get("white",{}).get("user",{}).get("name")
        black=players.get("black",{}).get("user",{}).get("name")
        #give up if we don't have information of all player
        if not white or not black:
            continue
        games_data.append({"id":game["id"], #game id
                       "speed":game["speed"], #speed
                       "white":white, #white player
                       "black":black, #black player
                       "winner":game.get("winner"), #winner
                       "moves":moves_list}) #game movements
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
    
def print_games_data(games_data,nblines=-1):
    """
    print games informations
    
    :param games_data: games data list
    :param nblines: number of line to print (default: -1 -> print all)
    """
    #TypeError
    if not isinstance(games_data,list):
        raise TypeError("your games data is not correct format")
    #basical case
    if nblines==0:
        return
    #compter initialization
    cpt=0
    #print information
    for game in games_data:
        if nblines==cpt:
            return
        print("===================================================")
        print(f"game id: {game.get('id')}\ngame information:\n")
        print(f"game movements: {game.get('moves')}")
        print(f"white: {game.get('white')}")
        print(f"black: {game.get('black')}")
        print(f"game winner: {game.get('winner')}")
        print("===================================================")
        if nblines>-1:
            cpt+=1