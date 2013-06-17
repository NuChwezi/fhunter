-- DB : fhunter
DROP TABLE IF EXISTS fhunter_hits;
CREATE TABLE fhunter_hits (
    id serial primary key,
    created timestamp default NOW(),
    ip text not null,
    score int,
    method varchar(20),
    extra text
);
