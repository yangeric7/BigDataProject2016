playerstats = LOAD '2016stats.csv' using PigStorage(',');
labeledplayerstats = FOREACH playerstats GENERATE $1 as Player, $2 as Position, $3 as Age, $4 as Team, $5 as G, $6 as
GS, $7 as MP, $8 as FG, $9 as FGA, $10 as FGPercentage, $11 as ThreeP, $12 as ThreePA, $13 as ThreePPercentage, $14 as
TwoP, $15 as TwoPA, $16 as TwoPPercentage, $17 as eFGPercentage, $18 as FT, $19 as FTA, $20 as FTPercentage, $21 as ORB,
$22 as DRB, $23 as TRB, $24 as AST, $25 as STL, $26 as BLK, $27 as TOV, $28 as PF, $29 as PTS, $30 as Season, $31 as MVP;
validplayers = FILTER labeledplayerstats BY Player != 'Player';
gamethreshold = FILTER validplayers BY G > 40;
minutethreshold = FILTER gamethreshold BY MP > 1000;

teamstats = LOAD '2016teamwindata.csv' using PigStorage(',');
labeledteamstats = FOREACH teamstats GENERATE $0 as Season, $1 as Team, $2 as Wins;

joinplayerteamtwentysixteen = JOIN labeledteamstats BY (Season, Team), minutethreshold BY (Season, Team);
labeljoin2016 = FOREACH joinplayerteamtwentysixteen GENERATE $0 as Season, $1 as Team, $2 as Wins, $3 as Player, $4 as
Position, $5 as Age, $7 as G, $8 as GS, $9 as MP, $10 as FG, $11 as FGA, $12 as FGPercentage, $13 as ThreeP, $14 as
ThreePA, $15 as ThreePPercentage, $16 as TwoP, $17 as TwoPA, $18 as TwoPPercentage, $19 as eFGPercentage, $20 as FT, $21
as FTA, $22 as FTPercentage, $23 as ORB, $24 as DRB, $25 as TRB, $26 as AST, $27 as STL, $28 as BLK, $29 as TOV, $30 as
PF, $31 as Pts, $33 as MVP;

STORE labeljoin2016 INTO '2016playerandteam' USING PigStorage(','); 
