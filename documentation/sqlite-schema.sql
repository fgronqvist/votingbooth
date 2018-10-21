CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	firstname VARCHAR(256) NOT NULL, 
	lastname VARCHAR(256) NOT NULL, 
	email VARCHAR(256) NOT NULL, 
	password VARCHAR(256) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
CREATE TABLE account_role (
	id INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	name VARCHAR(256) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE poll (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(256) NOT NULL, 
	owner_id INTEGER NOT NULL, 
	date_open DATETIME, 
	date_close DATETIME, 
	anynomous BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES account (id), 
	CHECK (anynomous IN (0, 1))
);
CREATE TABLE vote_option (
	id INTEGER NOT NULL, 
	poll_id INTEGER NOT NULL, 
	ordernum INTEGER NOT NULL, 
	name VARCHAR(256) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(poll_id) REFERENCES poll (id)
);
CREATE TABLE user_voted (
	id INTEGER NOT NULL, 
	poll_id INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	date_created DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(poll_id) REFERENCES poll (id), 
	FOREIGN KEY(account_id) REFERENCES account (id)
);
CREATE TABLE vote (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	poll_id INTEGER NOT NULL, 
	vote_option_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(poll_id) REFERENCES poll (id), 
	FOREIGN KEY(vote_option_id) REFERENCES vote_option (id)
);
