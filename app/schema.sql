DROP TABLE IF EXISTS tasks;
DROP TYPE IF EXISTS priorities;

CREATE TYPE priorities AS ENUM (
  'low',
  'normal',
  'high',
  'critical'
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(50),
  priority priorities,
  done BOOL
);
