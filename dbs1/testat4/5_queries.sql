-- Mirio Eggmann, Nick Wallner

-- Testat 3:
-- --------------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------------

-- Aufgabe 1: Einfache Queries
-- --------------------------------------------------------------------------------------------------------------------
-- 1.1: Alle Mailadressen von Kunden, die über ihr Kundenkonto effektiv schon einen Auftrag aufgegeben haben.
SELECT DISTINCT(mail)
FROM person AS p
JOIN auftrag AS a ON p.id=a.person_id;

-- 1.2: Gibt aus welche Ausbildungen ein Mitarbeiter für welches Gerät (Modellnummer) wann absolviert hat
SELECT p.name, p.vorname, a.erwerbungsdatum, g.modellnummer
FROM mitarbeiter AS m
JOIN person AS p ON p.id=m.person_id
JOIN ausbildung AS a ON m.person_id=a.person_id
JOIN geraet AS g ON g.id=a.geraet_id;

-- 1.3. Gibt aus welches Gerät am häufigsten als Auftrag aufgegeben wird.
--      Ist unkorreliert, da die Subquery auch alleinstehend die am häufigsten gebrauchten Geräte Ids liefert.
SELECT id, modellnummer, prozessor, speicher, ram
FROM geraet
WHERE id = (
    SELECT geraet_id
    FROM auftrag
    GROUP BY geraet_id
    ORDER BY count(geraet_id) DESC
    LIMIT 1);

-- 1.4. Liefert nur Geräte, falls diese kein Prozessor besitzen der in der Liste mit den aktuellsten Prozessoren ist.
SELECT id, modellnummer, prozessor, speicher, ram
FROM geraet
WHERE prozessor NOT IN ('AMD Ryzen 9 3950X', 'Intel Core i7-9700K');

-- Aufgabe 2: Common Table Expressions und Window-Funktionen
-- --------------------------------------------------------------------------------------------------------------------
-- 2.1 Subselect Query: Diese Query holt den Mitarbeiter, der in der Subquery die meiste Anzahl an Ausbildungen besitzt.
SELECT p.name, p.vorname, p.mail
FROM mitarbeiter AS m
JOIN person AS p ON m.person_id = p.id
WHERE person_id = (
    SELECT a.person_id
    FROM ausbildung AS a
    GROUP BY a.person_id
    ORDER BY count(a.person_id) DESC
    LIMIT 1);

-- 2.1 Common Table Expression (CTE) mit WITH clause: Umgeschriebenes Subselect query
WITH tmptable AS (
    SELECT a.person_id
    FROM ausbildung AS a
    GROUP BY a.person_id
    ORDER BY count(a.person_id) DESC
    LIMIT 1)
SELECT p.name, p.vorname, p.mail
FROM tmptable AS t
JOIN mitarbeiter AS m ON t.person_id = m.person_id
JOIN person AS p ON m.person_id = p.id
WHERE m.person_id = t.person_id;

-- 2.2 GROUP-BY: Reparaturen an Geräten mit AMD Prozessoren mit Gruppierung von Anzahl Durchführungen pro Modell
SELECT g.prozessor, COUNT(g.prozessor)
FROM reparaturdurchfuehrung AS r
JOIN auftrag AS a ON a.id = r.auftrag_id
JOIN geraet AS g ON g.id = a.geraet_id
WHERE g.prozessor LIKE '%AMD%'
GROUP BY g.prozessor;

-- Window-Funktion: Anzahl Reparaturen an Geräten wo der jeweilige Prozessor drin war
SELECT DISTINCT(g.prozessor),
       COUNT(g.prozessor) OVER (PARTITION BY g.prozessor ORDER BY g.prozessor) AS "count_repairs"
FROM reparaturdurchfuehrung AS r
JOIN auftrag AS a ON a.id = r.auftrag_id
JOIN geraet AS g ON g.id = a.geraet_id;

-- Aufgabe 3: Views
-- --------------------------------------------------------------------------------------------------------------------
-- 3.1 Views: View die alle Mitarbeiter und ihre Qualifikationen beinhaltet
CREATE VIEW mitarbeiter_qualifikationen (mitarbeiternummer, name, vorname, erwerbungsdatum, modellnummer) AS
    SELECT m.mitarbeiternummer, p.name, p.vorname, a.erwerbungsdatum, g.modellnummer
    FROM mitarbeiter AS m
    JOIN person AS p ON p.id=m.person_id
    JOIN ausbildung AS a ON m.person_id=a.person_id
    JOIN geraet AS g ON g.id=a.geraet_id;

-- 3.1 Views: Mitarbeiternummer und Vorname ausgeben für Mitarbeitende die die Ausbildung für Modellnummer 100006 verfügen
SELECT mitarbeiternummer, vorname
FROM mitarbeiter_qualifikationen
WHERE modellnummer=100006;

-- 3.2 Updatable View: Alle Email Adressen zu den jewiligen Personen Ids
CREATE VIEW person_email (id, mail) AS
    SELECT p.id, p.mail
    FROM person AS p;

-- 3.2 UPDATE über Updatable View machen: Email von Hans Affolter über person_email View updaten
UPDATE person_email
SET mail = 'affolter.hans@bluewin.ch'
WHERE mail = 'affolter.hans@example.com';

-- Testat 4:
-- --------------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------------

-- Aufgabe 1: Lateral Join-Query - neuste ausbildung pro Mitarbeiter ausgeben
-- --------------------------------------------------------------------------------------------------------------------
SELECT name, vorname, geraet_id, erwerbungsdatum
FROM person AS p
JOIN LATERAL (
    SELECT person_id, geraet_id, erwerbungsdatum
    FROM ausbildung as a
    WHERE a.person_id=p.id
    ORDER BY a.erwerbungsdatum desc
    LIMIT 1
) AS neuste_ausbildung ON true
ORDER BY erwerbungsdatum DESC;

-- Aufgabe 5: Tests
-- --------------------------------------------------------------------------------------------------------------------
-- 5.1 : Falscher BOOLEAN einfügen bzw falscher ENUM (soll nicht gehen)
-- INSERT INTO person (name, vorname, mail, active, deactivated_at)
-- VALUES ('Mirio', 'Eggmann', 'mirio.eggmann@example.com', 1, null);

-- INSERT INTO ausbildung (person_id, geraet_id, erwerbungsdatum, ausbildungs_typ)
-- VALUES (2, 7, to_date('2020-12-08', 'YYYY-MM-DD'), 'blabla');

-- 5.2: Unique constraint verletzen (soll nicht gehen)
-- INSERT INTO person (name, vorname, mail, active, deactivated_at)
-- VALUES ('Erichsen', 'Tom2', 'erichsen.tom@example.com', true, null);
