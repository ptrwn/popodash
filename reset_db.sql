DROP DATABASE IF EXISTS popodash;
DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'popodash') THEN

      RAISE NOTICE 'Role "popodash" already exists. Skipping.';
   ELSE
      create user popodash with encrypted password '123qwe';
   END IF;
END
$do$;

CREATE DATABASE popodash OWNER popodash;
grant all privileges on database popodash to popodash;

-- drop type if exists drink_kinds_enum cascade;
-- create type drink_kinds_enum as enum('beer', 'wine', 'spirit', 'cocktail');
