create table if not exists `TASK` (
    `id`     integer     primary key autoincrement,
    `topic`  varchar(50) not null,
    `done`   integer     default 0
) ;

-- 

create table if not exists `USER` (
    `login`  varchar(150)  not null,
    `psswd`  varchar(150)  not null
) ;
