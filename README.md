# moteur-d-checs-adaptatif-personnalis-par-apprentissage-automatique
L’objectif du projet est de développer un moteur d’échecs capable de s’adapter dynamiquement au niveau et au style de jeu d’un joueur spécifique, en combinant analyse de parties historiques et adaptation en temps réel, puis d’évaluer rigoureusement sa capacité à maintenir des parties équilibrées et engageantes.

### envirnment setting
#### generate your lichess API Token 
- open https://lichess.org/account/oauth/token and click on generate a new token
- copy your token carefully
##### macOS/Linux system
- open your terminal and set export LICHESS_API_TOKEN="lip_yourAPI" (no permanent solution) or tap nano ~/.bashrc export LICHESS_API_TOKEN="lip_yourAPI" then do source ~/.bashrc echo $LICHESS_API_TOKEN to make sure(permanent solution)
##### windows system
- open your PowerShell terminal and tap setx LICHESS_API_TOKEN "lip_yourAPI" then verify your setting with echo $Env:LICHESS_API_TOKEN