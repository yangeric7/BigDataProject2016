playerstats = LOAD 'playerstatsno2016.csv' using PigStorage(',');
labeledstats = FOREACH playerstats GENERATE $1 as player, $2 as pos, $3 as age, $4 as team, $5 as G, $6 as GS, $7 as MP,
$8 as FG, $9 as FGA, $10 as FGPercentage, $11 as ThreeP, $12 as ThreePA, $13 as ThreePPercentage, $14 as TwoP, $15 as
TwoPA, $16 as
TwoPPercentage, $17 as eFGPercentage, $18
as FT, $19 as FTA, $20 as FTPercentage, $21 as ORB, $22 as DRB, $23 as TRB, $24 as AST, $25 as STL, $26 as BLK, $27 as TOV, $28
as PF, $29 as Pts, $30 as Season, $31 as MVP;
actualplayers = FILTER labeledstats BY player != 'Player';
playersabovegamethreshold = FILTER actualplayers BY G > 40;
playersaboveminutethreshold = FILTER playersabovegamethreshold BY MP > 1000;

teamwins = LOAD 'adjustedteamwins.csv' using PigStorage(',');
labeledteamwins = FOREACH teamwins GENERATE $0 as Season, $1 as team, $2 as wins;

combinedplayerandteam = JOIN labeledteamwins BY (Season, team), playersaboveminutethreshold BY (Season, team);
labelcombinedplayerandteam = FOREACH combinedplayerandteam GENERATE $0 as Season, $1 as Team, $2 as Wins, $3 as Player,
$4 as Position, $5 as Age, $7 as G, $8 as GS, $9 as MP, $10 as FG, $11 as FGA, $12 as FGPercentage, $13 as ThreeP, $14
as ThreePA, $15 as ThreePPercentage, $16 as TwoP, $17 as TwoPA, $18 as TwoPPercentage, $19 as eFGPercentage, $20 as FT,
$21 as FTA, $22 as FTPercentage, $23 as ORB, $24 as DRB, $25 as TRB, $26 as AST, $27 as STL, $28 as BLK, $29 as TOV, $30
as PF, $31 as PTS, $33 as MVP;

STORE labelcombinedplayerandteam INTO 'playerjointeam' using PigStorage(',');

