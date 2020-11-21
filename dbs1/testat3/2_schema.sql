-- Mirio Eggmann, Nick Wallner

CREATE TABLE person
(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(80) NOT NULL,
    vorname VARCHAR(80) NOT NULL,
    mail    VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE mitarbeiter
(
    person_id         INTEGER NOT NULL PRIMARY KEY,
    mitarbeiternummer INTEGER NOT NULL UNIQUE,
    CONSTRAINT fk_mitarbeiter_person FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE
);

CREATE TABLE geraet
(
    id           SERIAL PRIMARY KEY,
    modellnummer INTEGER     NOT NULL,
    prozessor    VARCHAR(80) NOT NULL,
    speicher     INTEGER     NOT NULL,
    ram          INTEGER     NOT NULL
);

CREATE TABLE ausbildung
(
    person_id       INTEGER,
    geraet_id       INTEGER,
    erwerbungsdatum DATE NOT NULL,
    CONSTRAINT pk_ausbildung PRIMARY KEY (person_id, geraet_id),
    CONSTRAINT fk_ausbildung_geraet FOREIGN KEY (geraet_id) REFERENCES geraet (id),
    CONSTRAINT fk_ausbildung_mitarbeiter FOREIGN KEY (person_id) REFERENCES mitarbeiter (person_id)
);

CREATE TABLE auftrag
(
    id                SERIAL PRIMARY KEY,
    beschreibung      VARCHAR(255) NOT NULL,
    eroeffnungsdatum  DATE         NOT NULL,
    schliessungsdatum DATE,
    person_id         INTEGER      NOT NULL,
    geraet_id         INTEGER      NOT NULL,
    CONSTRAINT fk_auftrag_person FOREIGN KEY (person_id) REFERENCES person (id),
    CONSTRAINT fk_auftrag_geraet FOREIGN KEY (geraet_id) REFERENCES geraet (id)
);

CREATE TABLE reparaturdurchfuehrung
(
    id         SERIAL PRIMARY KEY,
    startdatum DATE,
    enddatum   DATE,
    auftrag_id INTEGER NOT NULL,
    person_id  INTEGER NOT NULL,
    CONSTRAINT fk_reparaturdurchfuehrung_auftrag FOREIGN KEY (auftrag_id) REFERENCES auftrag (id),
    CONSTRAINT fk_reparaturdurchfuehrung_mitarbeiter FOREIGN KEY (person_id) REFERENCES mitarbeiter (person_id)
);

