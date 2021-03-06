-- Mirio Eggmann, Nick Wallner

-- TABLE person (angepasst für Testat 4)
INSERT INTO person (name, vorname, mail, active, deactivated_at)
VALUES ('Erichsen', 'Tom', 'erichsen.tom@example.com', true, null),
       ('Marxer', 'Markus', 'marxer1000@example.com', true, null),
       ('Widmer', 'Hedi', 'widmer.hedi@example.com', true, null),
       ('Steiner', 'Anna', 'steiner.anna@example.com', true, null),
       ('Affolter', 'Hans', 'affolter.hans@example.com', true, null),
       ('Widmer', 'Vreni', 'widmer.vreni@example.com', true, null),
       ('Meier', 'Karl', 'meier.karl@example.com', true, null),
       ('Keineahnung', 'Alex', 'alex.keineahnung@example.com', true, null),
       ('Fox', 'Peter', 'peter.fox@example.com', true, null),
       ('Mustermann', 'Max', 'max.mustermann@example.com', true, null),
       ('Müller', 'Heidi', 'heidi.mueller@example.com', true, null),
       ('Kunde','Ohne Auftrag', 'kunde@ohneauftrag.ch', false, to_timestamp('2020-03-31 09:30:20', 'YYYY-MM-DD HH:MI:SS'));

-- TABLE mitarbeiter
INSERT INTO mitarbeiter (person_id, mitarbeiternummer)
VALUES (1, 10000),
       (2, 10001),
       (3, 10002),
       (4, 10003),
       (5, 10004),
       (6, 10005),
       (7, 10006);

-- TABLE geraet
INSERT INTO geraet (modellnummer, prozessor, speicher, ram)
VALUES (100000, 'AMD Ryzen 9 3950X', 1000, 16),
       (100001, 'AMD Ryzen 7 2700X', 512, 16),
       (100002, 'AMD Ryzen 5 3600X', 512, 8),
       (100003, 'Intel Core i7-9700K', 2000, 32),
       (100004, 'Intel Core i5 4700K', 1000, 16),
       (100005, 'Intel Core i5 4800K', 512, 16),
       (100006, 'Intel Core i5 9600K', 256, 8);

-- TABLE ausbildung (angepasst für Testat 4)
INSERT INTO ausbildung (person_id, geraet_id, erwerbungsdatum, ausbildungs_typ)
VALUES (2, 1, to_date('2019-03-20', 'YYYY-MM-DD'), 'zwingend'),
       (3, 7, to_date('2019-04-20', 'YYYY-MM-DD'), 'optional'),
       (3, 2, to_date('2019-05-10', 'YYYY-MM-DD'), 'zwingend'),
       (3, 5, to_date('2019-05-11', 'YYYY-MM-DD'), 'zwingend'),
       (4, 6, to_date('2019-06-16', 'YYYY-MM-DD'), 'optional'),
       (5, 7, to_date('2019-02-16', 'YYYY-MM-DD'), 'zwingend'),
       (5, 4, to_date('2020-02-16', 'YYYY-MM-DD'), 'zwingend');

-- TABLE auftrag
INSERT INTO auftrag(beschreibung, eroeffnungsdatum, schliessungsdatum, person_id, geraet_id)
VALUES ('Bildschirm funktioniert nicht mehr', to_date('2020-01-10', 'YYYY-MM-DD'), to_date('2020-01-15', 'YYYY-MM-DD'),
        8, 1),
       ('Gerät extrem langsam', to_date('2020-02-12', 'YYYY-MM-DD'), to_date('2020-02-14', 'YYYY-MM-DD'), 9, 2),
       ('Laptop will nicht mehr starten', to_date('2020-03-08', 'YYYY-MM-DD'), to_date('2020-03-12', 'YYYY-MM-DD'), 9,
        7),
       ('Daten korrupt', to_date('2020-04-20', 'YYYY-MM-DD'), to_date('2020-04-25', 'YYYY-MM-DD'), 10, 5),
       ('Wackelkontakt beim Laden', to_date('2020-05-20', 'YYYY-MM-DD'), to_date('2020-05-22', 'YYYY-MM-DD'), 11, 4),
       ('Maus funktioniert nicht', to_date('2020-06-10', 'YYYY-MM-DD'), to_date('2020-06-14', 'YYYY-MM-DD'), 8, 3),
       ('Bildschirm zersplittert', to_date('2020-07-10', 'YYYY-MM-DD'), to_date('2020-07-12', 'YYYY-MM-DD'), 1, 1),
       ('Problem mit dem Lüfter', to_date('2020-08-10', 'YYYY-MM-DD'), NULL, 11, 1);

-- TABLE reparaturdurchfuehrung
INSERT INTO reparaturdurchfuehrung(startdatum, enddatum, auftrag_id, person_id)
VALUES (to_date('2020-01-11', 'YYYY-MM-DD'), to_date('2020-01-15', 'YYYY-MM-DD'), 1, 5),
       (to_date('2020-02-12', 'YYYY-MM-DD'), to_date('2020-02-14', 'YYYY-MM-DD'), 2, 1),
       (to_date('2020-03-09', 'YYYY-MM-DD'), to_date('2020-03-12', 'YYYY-MM-DD'), 3, 5),
       (to_date('2020-04-20', 'YYYY-MM-DD'), to_date('2020-04-25', 'YYYY-MM-DD'), 4, 5),
       (to_date('2020-05-20', 'YYYY-MM-DD'), to_date('2020-05-22', 'YYYY-MM-DD'), 5, 5),
       (to_date('2020-06-10', 'YYYY-MM-DD'), to_date('2020-06-14', 'YYYY-MM-DD'), 6, 5),
       (to_date('2020-07-10', 'YYYY-MM-DD'), to_date('2020-07-12', 'YYYY-MM-DD'), 7, 5),
       (to_date('2020-08-10', 'YYYY-MM-DD'), NULL, 7, 5);
