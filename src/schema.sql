create table if not exists files(
  fid         serial primary key,
  name        text not null,
  link        text not null
);

create table if not exists tags(
  tid         serial primary key,
  name        text not null
);

create table if not exists file_tags(
  tid         int,
  fid         int,
  primary key (tid, fid)
);
