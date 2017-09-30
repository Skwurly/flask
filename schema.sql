drop table if exists entries;
create table entries(
  id integer primary key autoincrement,
  date_created date default current_date,
  title text not null,
  'text' text not null
  img 
);
