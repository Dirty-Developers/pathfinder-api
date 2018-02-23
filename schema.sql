create table user(
    id integer not null primary key autoincrement,
    name text not null
);

create table agenda(
    agenda_id integer not null primary key autoincrement,
    title text not null,
    user_id integer,
    foreign key (user_id) references user(agenda_id) on delete cascade
);

create table event(
    event_id string not null primary key,
    title text not null,
	longitude real,
	latitude real,
	event_type string not null default 'activity'
);

create table agenda_event(
	agenda_id integer not null,
	event_id string not null,
	checkin string,
	checkout string,
	foreign key(agenda_id) references agenda(agenda_id),
	foreign key(event_id) references event(event_id),
	primary key(agenda_id, event_id)
);


insert into user(name) values ('user');
select * from user;
