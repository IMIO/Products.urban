--
-- clean_labruyere_dbtest database creation script: can be run with command 'psql -f clean_labruyere_dbtest.sql'
--

UPDATE PE SET pe = 'Nom Prénom' WHERE pe ilike '%';
UPDATE PE SET adr1 = '0000 Village' WHERE adr1 ilike '%';
UPDATE PE SET adr2 = 'Rue Numéro' WHERE adr2 ilike '%';
UPDATE da SET divname = 'Village1' WHERE divname ilike 'Bovesse%';
UPDATE da SET divname = 'Village2' WHERE divname ilike 'Emines%';
UPDATE da SET divname = 'Village3' WHERE divname ilike 'Meux%';
UPDATE da SET divname = 'Village4' WHERE divname ilike 'Rhisnes%';
UPDATE da SET divname = 'Village5' WHERE divname ilike 'Saint-denis%';
UPDATE da SET divname = 'Village6' WHERE divname ilike 'Villers%';
UPDATE da SET divname = 'Village6' WHERE divname ilike 'Warisoulx%';


