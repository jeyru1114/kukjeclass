create database flaskdb;
use flaskdb;
create table flask_tbl(
	fno int primary key auto_increment,
    math int,
    eng int,
    korea int,
    total int,
    avg float,
    grade varchar(20));
insert into flask_tbl values(null, 30, 40, 50, 100, 34.0, '가');
select * from flask_tbl;
drop table flask_tbl;