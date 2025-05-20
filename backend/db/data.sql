create table users (
  id bigint primary key generated always as identity,
  username text unique not null,
  email text unique not null,
  password_hash text not null,
  created_at timestamp with time zone default now(),
  last_login timestamp with time zone
);

create table roles (
  id bigint primary key generated always as identity,
  name text unique not null
);

create table user_roles (
  id bigint primary key generated always as identity,
  user_id bigint references users (id) on delete cascade,
  role_id bigint references roles (id) on delete cascade
);

create table image_tasks (
  id bigint primary key generated always as identity,
  user_id bigint references users (id) on delete cascade,
  image_path text not null,
  status text not null,
  created_at timestamp with time zone default now(),
  completed_at timestamp with time zone,
  transformation jsonb
);

create table task_logs (
  id bigint primary key generated always as identity,
  task_id bigint references image_tasks (id) on delete cascade,
  log_message text not null,
  created_at timestamp with time zone default now()
);