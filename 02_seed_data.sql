PRAGMA foreign_keys = ON;

-- CONDITIONS (keep yours)
INSERT INTO card_condition (condition_id, condition_code, description) VALUES
(1,'NM','Near Mint'),
(2,'LP','Lightly Played'),
(3,'MP','Moderately Played'),
(4,'HP','Heavily Played'),
(5,'DMG','Damaged');

-- SETS (keep your full set list here)
INSERT INTO card_set (set_id, set_code, set_name, release_date, era) VALUES
(1, 'SWSH1', 'Sword & Shield Base', '2020-02-07', 'Sword & Shield'),
(2, 'SWSH2', 'Rebel Clash', '2020-05-01', 'Sword & Shield'),
(3, 'SWSH3', 'Darkness Ablaze', '2020-08-14', 'Sword & Shield'),
(4, 'CPA',   'Champions Path', '2020-09-25', 'Sword & Shield'),
(5, 'SWSH4', 'Vivid Voltage', '2020-11-13', 'Sword & Shield'),
(6, 'SHF',   'Shining Fates', '2021-02-19', 'Sword & Shield'),
(7, 'SWSH5', 'Battle Styles', '2021-03-19', 'Sword & Shield'),
(8, 'SWSH6', 'Chilling Reign', '2021-06-18', 'Sword & Shield'),
(9, 'SWSH7', 'Evolving Skies', '2021-08-27', 'Sword & Shield'),
(10,'CEL',   'Celebrations', '2021-10-08', 'Sword & Shield'),
(11,'SWSH8', 'Fusion Strike', '2021-11-12', 'Sword & Shield'),
(12,'SWSH9', 'Brilliant Stars', '2022-02-25', 'Sword & Shield'),
(13,'SWSH10','Astral Radiance', '2022-05-27', 'Sword & Shield'),
(14,'PGO',   'Pokemon GO', '2022-07-01', 'Sword & Shield'),
(15,'SWSH11','Lost Origin', '2022-09-09', 'Sword & Shield'),
(16,'SWSH12','Silver Tempest', '2022-11-11', 'Sword & Shield'),
(17,'CRZ',   'Crown Zenith', '2023-01-20', 'Sword & Shield'),
(18,'SV1',   'Scarlet & Violet Base', '2023-03-31', 'Scarlet & Violet'),
(19,'SV2',   'Paldea Evolved', '2023-06-09', 'Scarlet & Violet'),
(20,'SV3',   'Obsidian Flames', '2023-08-11', 'Scarlet & Violet'),
(21,'SV3.5', '151', '2023-09-22', 'Scarlet & Violet'),
(22,'SV4',   'Paradox Rift', '2023-11-03', 'Scarlet & Violet'),
(23,'SV4.5', 'Paldean Fates', '2024-01-26', 'Scarlet & Violet'),
(24,'SV5',   'Temporal Forces', '2024-03-22', 'Scarlet & Violet'),
(25,'SV6',   'Twilight Masquerade', '2024-05-24', 'Scarlet & Violet'),
(26,'SV6.5', 'Shrouded Fable', '2024-08-02', 'Scarlet & Violet'),
(27,'SV7',   'Stellar Crown', '2024-09-13', 'Scarlet & Violet'),
(28,'SV8',   'Surging Sparks', '2024-11-08', 'Scarlet & Violet'),
(29,'SV8.5', 'Prismatic Evolutions', '2025-01-17', 'Scarlet & Violet'),
(30,'SV9',   'Journey Together', '2025-03-28', 'Scarlet & Violet'),
(31,'SV10',  'Destined Rivals', '2025-05-30', 'Scarlet & Violet'),
(32,'SV11',  'Black Bolt', '2025-06-18', 'Scarlet & Violet'),
(33,'SV12',  'White Flare', '2025-06-18', 'Scarlet & Violet'),
(34,'ME1',   'Mega Evolution Base', '2025-09-26', 'Mega Evolution'),
(35,'ME2',   'Phantasmal Flames', '2025-11-24', 'Mega Evolution'),
(36,'ME3',   'Ascended Heros', '2026-01-30', 'Mega Evolution'),
(37,'ME4',   'Perfect Order', '2026-03-27', 'Mega Evolution');
