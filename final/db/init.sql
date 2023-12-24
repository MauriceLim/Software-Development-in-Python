CREATE DATABASE IF NOT EXISTS zen_nilpferd;
USE zen_nilpferd;

DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS mortality;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS parameters;
DROP TABLE IF EXISTS results;

CREATE TABLE scenarios (
    id int unsigned NOT NULL,
    risk_free_rate float NOT NULL,
    dividend_yield float NOT NULL,
    volatility float NOT NULL,
    record_description varchar(250),
    PRIMARY KEY (id)
);

CREATE TABLE mortality (
    age int unsigned NOT NULL,
    qx float NOT NULL
);

CREATE TABLE policies (
    id int unsigned NOT NULL,
    issue_age int unsigned NOT NULL,
    initial_premium float NOT NULL,
    fee_pct_av float NOT NULL,
    benefit_type ENUM("PRINCIPAL_BACK", "FOR_LIFE") NOT NULL,
    ratchet_type ENUM("NO_RATCHET", "CONSTANT") NOT NULL,
    guarantee_wd_rate float NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE assumptions (
    id int unsigned NOT NULL,
    mortality_multiplier float NOT NULL,
    wd_age float NOT NULL,
    min_wd_delay float NOT NULL,
    record_description varchar(250),
    PRIMARY KEY (id)
);

CREATE TABLE parameters (
    id int unsigned NOT NULL,
    proj_periods int unsigned NOT NULL,
    num_paths int unsigned NOT NULL,
    seed int unsigned NOT NULL,
    record_description varchar(250),
    PRIMARY KEY (id)
);

CREATE TABLE results (
    id char(36) NOT NULL,
    scenario_id int unsigned NOT NULL,
    assumption_id int unsigned NOT NULL,
    parameter_id int unsigned NOT NULL,
    policy_id int unsigned NOT NULL,
    cost float NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id),
    FOREIGN KEY (assumption_id) REFERENCES assumptions(id),
    FOREIGN KEY (parameter_id) REFERENCES parameters(id),
    FOREIGN KEY (policy_id) REFERENCES policies(id)
);