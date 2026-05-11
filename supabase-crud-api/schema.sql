create table students (
  id bigint generated always as identity primary key,
  name text not null,
  email text unique not null,
  course text not null,
  created_at timestamp with time zone default now()
);