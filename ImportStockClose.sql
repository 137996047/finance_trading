load data local infile 'TWDaily.txt' into table stockclose fields terminated by ','
enclosed by '"'
lines terminated by '\n'
(tDate, Symbol, Open, High, Low , Close, Volume)