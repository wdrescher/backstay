ALTER TABLE profile 
    ADD COLUMN role ENUM("COACH", "ROWER", "EBOARD") DEFAULT "ROWER"
;

CREATE TABLE coach (
    coach_id int PRIMARY KEY AUTO_INCREMENT,
    profile_id int UNIQUE NOT NULL,
    CONSTRAINT FOREIGN KEY (profile_id) REFERENCES profile(profile_id) ON DELETE CASCADE
);

CREATE TABLE reset_token(
    reset_token_id varchar(64) PRIMARY KEY, 
    expiration_date DATETIME NOT NULL,
    profile_id int, 
    CONSTRAINT FOREIGN KEY (profile_id) REFERENCES profile(profile_id) ON DELETE CASCADE
);

CREATE TABLE team(
    team_id int PRIMARY KEY AUTO_INCREMENT
);

CREATE TABLE week(
    start_date DATE, 
    team_id int,
    constraint primary key (start_date, team_id),
    CONSTRAINT FOREIGN KEY (team_id) REFERENCES team(team_id)
);

CREATE TABLE attendance(
    attendance_id int PRIMARY KEY AUTO_INCREMENT,
    start_date DATE,
    team_id int,
    CONSTRAINT FOREIGN KEY (start_date, team_id) REFERENCES week(start_date, team_id)
);

CREATE TABLE workout_plan(
    workout_plan_id int PRIMARY KEY AUTO_INCREMENT,
    start_date DATE NOT NULL, 
    team_id int NOT NULL,
    meters int,
    description varchar(200),
    CONSTRAINT FOREIGN KEY (start_date, team_id) REFERENCES week(start_date, team_id)
);

CREATE TABLE workout(
    workout_id int PRIMARY KEY AUTO_INCREMENT,
    profile_id int NOT NULL, 
    meters int not NULL, 
    seconds int not NULL,
    workout_plan_id int, 
    constraint foreign key (workout_plan_id) references workout_plan(workout_plan_id),
    CONSTRAINT FOREIGN KEY (profile_id) REFERENCES profile(profile_id)
);