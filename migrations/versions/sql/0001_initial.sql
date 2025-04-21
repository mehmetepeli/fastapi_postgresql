BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> aa2699453ea4

CREATE TABLE users (
    id SERIAL NOT NULL, 
    name VARCHAR(50) NOT NULL, 
    username VARCHAR(50) NOT NULL, 
    email VARCHAR(100) NOT NULL, 
    password VARCHAR(100) NOT NULL, 
    role VARCHAR(10), 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    CONSTRAINT uq_username UNIQUE (username)
);

INSERT INTO alembic_version (version_num) VALUES ('aa2699453ea4') RETURNING alembic_version.version_num;

COMMIT;

