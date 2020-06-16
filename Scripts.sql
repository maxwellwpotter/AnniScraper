/* Calculates the average time of all matches */
select SEC_TO_TIME(AVG(TIME_TO_SEC(TIMEDIFF(snapshots.shotTime, snapshots.matchID)))) as AverageTime 
	from snapshots 
    inner join (select matchID, max(shotTIme) as latest from snapshots group by matchID) m 
    on snapshots.shotTime = m.latest and snapshots.matchID = m.matchID;