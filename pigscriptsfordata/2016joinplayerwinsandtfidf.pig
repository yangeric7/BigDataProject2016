playerdata = LOAD '2016playerandteam.csv' using PigStorage(',');
labeledplayerdata = FOREACH playerdata GENERATE $0 as Season, $1 as Team, $2 as Wins, $3 as Player, $4 as Position, $5
as Age, $6 as G, $7 as GS, $8 as MP, $9 as FG, $10 as FGA, $11 as FGPercentage, $12 as ThreeP, $13 as ThreePA, $14 as
ThreePPercentage, $15 as TwoP, $16 as TwoPA, $17 as TwoPPercentage, $18 as eFGPercentage, $19 as FT, $20 as FTA, $21 as
FTPercentage, $22 as ORB, $23 as DRB, $24 as TRB, $25 as AST, $26 as STL, $27 as BLK, $28 as TOV, $29 as PF, $30 as PTS,
$31 as MVP;

tfidf = LOAD 'playerWikiData.csv' using PigStorage(',');
labeledtfidf = FOREACH tfidf GENERATE $0 as Player, $1 as MVPtfidf, $2 as Championshiptfidf, $3 as Awardtfidf, $4 as
Timetfidf;

combinedtfidfplayerdata = JOIN labeledtfidf BY (Player), labeledplayerdata BY (Player);
labeledcombinedtfidfplayerdata = FOREACH combinedtfidfplayerdata GENERATE $0 as Player, $1 as MVPtfidf, $2 as
Championshiptfidf, $3 as Awardtfidf, $4 as Timetfidf, $5 as Season, $6 as Team, $7 as Wins, $9 as Position, $10 as Age,
$11 as G, $12 as GS, $13 as MP, $14 as FG, $15 as FGA, $16 as FGPercentage, $17 as ThreeP, $18 as ThreePA, $19 as
ThreePPercentage, $20 as TwoP, $21 as TwoPA, $22 as TwoPPercentage, $23 as eFGPercentage, $24 as FT, $25 as FTA, $26 as
FTPercentage, $27 as ORB, $28 as DRB, $29 as TRB, $30 as AST, $31 as STL, $32 as BLK, $33 as TOV, $34 as PF, $35 as PTS,
$36 as MVP;
STORE labeledcombinedtfidfplayerdata INTO '2016combinedtfidfplayerdata' USING PigStorage(',');

