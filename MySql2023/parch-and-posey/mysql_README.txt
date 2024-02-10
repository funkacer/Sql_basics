Původní databáze byla pro PostGRE
změnit:
bpchar na varchar(255)
(numeric v accounts na decimal - není nutné)
long (v accounts) na `long`

Dělá chybu! Změnit čas na 3
INSERT INTO web_events VALUES (4831,1401,'2014-03-30 02:14:03','facebook');