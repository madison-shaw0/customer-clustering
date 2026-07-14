CREATE TABLE business (
    business_id SERIAL PRIMARY KEY,
    canonical_name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    website_url TEXT,
    primary_domain VARCHAR(255),
    industry VARCHAR(100)
);

CREATE TABLE business_alias (
    alias_id SERIAL PRIMARY KEY,
    business_id INT NOT NULL,
    alias_text VARCHAR(255) NOT NULL,
    alias_type VARCHAR(50),
    FOREIGN KEY (business_id)
        REFERENCES business(business_id)
        ON DELETE CASCADE
);

CREATE TABLE business_source (
    source_id SERIAL PRIMARY KEY,
    business_id INT NOT NULL,
    source_type VARCHAR(50),
    source_name VARCHAR(100),
    source_identifier VARCHAR(255),
    source_url TEXT,
    search_query TEXT,
    connector_type VARCHAR(50),
    FOREIGN KEY (business_id)
        REFERENCES business(business_id)
        ON DELETE CASCADE
);

CREATE TABLE business_search_seed (
    seed_id SERIAL PRIMARY KEY,
    business_id INT NOT NULL,
    source_type VARCHAR(50),
    seed_text TEXT,
    seed_type VARCHAR(50),
    FOREIGN KEY (business_id)
        REFERENCES business(business_id)
        ON DELETE CASCADE
);

CREATE TABLE discovered_course (
    discovered_source_id SERIAL PRIMARY KEY,
    business_id INT NOT NULL,
    url TEXT,
    domain VARCHAR(255),
    source_type VARCHAR(50),
    confidence_score NUMERIC(4,3),
    discovered_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (business_id)
        REFERENCES business(business_id)
        ON DELETE CASCADE
);