CREATE SCHEMA IF NOT EXISTS bearwatch;

CREATE  TABLE bearwatch.assets ( 
	id                   uuid DEFAULT uuid_generate_v4() NOT NULL  ,
	name                 varchar  NOT NULL  ,
	code                 varchar  NOT NULL  ,
	CONSTRAINT pk_assets PRIMARY KEY ( id )
 );

CREATE  TABLE bearwatch.users ( 
	id                   uuid DEFAULT uuid_generate_v4() NOT NULL  ,
	email                varchar  NOT NULL  ,
	phone                varchar  NOT NULL  ,
	CONSTRAINT pk_users PRIMARY KEY ( id )
 );

CREATE  TABLE bearwatch.alerts ( 
	id                   uuid DEFAULT uuid_generate_v4() NOT NULL  ,
	user_id              uuid  NOT NULL  ,
	asset_id             uuid  NOT NULL  ,
	price                bigint  NOT NULL  ,
	alert_type           boolean  NOT NULL  ,
	last_modified        timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL  ,
	soft_delete          boolean DEFAULT false NOT NULL  ,
	CONSTRAINT pk_alerts PRIMARY KEY ( id )
 );

ALTER TABLE bearwatch.alerts ADD CONSTRAINT fk_alerts_users FOREIGN KEY ( user_id ) REFERENCES bearwatch.users( id );

ALTER TABLE bearwatch.alerts ADD CONSTRAINT fk_alerts_assets FOREIGN KEY ( asset_id ) REFERENCES bearwatch.assets( id );

