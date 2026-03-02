-- 01_create_tables.sql
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS inventory_item;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS card_set;
DROP TABLE IF EXISTS card_condition;

CREATE TABLE card_set (
  set_id        INTEGER PRIMARY KEY,
  set_code      TEXT NOT NULL UNIQUE,              -- e.g., "BS", "JU", "SV1"
  set_name      TEXT NOT NULL,
  release_date  TEXT NOT NULL,                     -- ISO date string "YYYY-MM-DD"
  era           TEXT NOT NULL                       -- e.g., "WOTC", "EX", "Modern"
);

CREATE TABLE card (
  card_id     INTEGER PRIMARY KEY,
  set_id      INTEGER NOT NULL,
  card_number TEXT NOT NULL,                       -- e.g., "4/102"
  card_name   TEXT NOT NULL,
  rarity      TEXT NOT NULL,
  card_type   TEXT NOT NULL,                       -- e.g., "Pokémon", "Trainer", "Energy"
  -- relationships
  FOREIGN KEY (set_id) REFERENCES card_set(set_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  -- constraints
  CONSTRAINT uq_card_per_set UNIQUE (set_id, card_number),
  CONSTRAINT ck_rarity CHECK (rarity IN ('Common','Uncommon','Rare','Double Rare','Ultra Rare','IR','SIR','Hyper Rare','Promo')),
  CONSTRAINT ck_card_type CHECK (card_type IN ('Pokémon','Trainer','Energy'))
);

CREATE TABLE card_condition (
  condition_id   INTEGER PRIMARY KEY,
  condition_code TEXT NOT NULL UNIQUE,             -- "NM", "LP", etc.
  description    TEXT NOT NULL,
  CONSTRAINT ck_condition_code CHECK (condition_code IN ('NM','LP','MP','HP','DMG'))
);

CREATE TABLE inventory_item (
  item_id        INTEGER PRIMARY KEY,
  card_id        INTEGER NOT NULL,
  condition_id   INTEGER NOT NULL,
  is_foil        INTEGER NOT NULL DEFAULT 0,        -- 0/1
  is_graded      INTEGER NOT NULL DEFAULT 0,        -- 0/1
  graded_company TEXT,                             -- PSA/BGS/CGC (nullable)
  grade          REAL,                             -- 1.0 - 10.0 (nullable)
  quantity       INTEGER NOT NULL DEFAULT 1,
  purchase_price REAL NOT NULL DEFAULT 0.0,
  purchase_date  TEXT,                             -- "YYYY-MM-DD" (nullable)
  notes          TEXT,

  FOREIGN KEY (card_id) REFERENCES card(card_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (condition_id) REFERENCES card_condition(condition_id) ON DELETE RESTRICT ON UPDATE CASCADE,

  CONSTRAINT ck_is_foil CHECK (is_foil IN (0,1)),
  CONSTRAINT ck_is_graded CHECK (is_graded IN (0,1)),
  CONSTRAINT ck_quantity CHECK (quantity >= 0),
  CONSTRAINT ck_purchase_price CHECK (purchase_price >= 0),

  -- If graded, must have a company and grade. If not graded, both must be NULL.
  CONSTRAINT ck_graded_fields CHECK (
    (is_graded = 1 AND graded_company IS NOT NULL AND grade IS NOT NULL AND grade BETWEEN 1.0 AND 10.0)
    OR
    (is_graded = 0 AND graded_company IS NULL AND grade IS NULL)
  ),

  CONSTRAINT ck_graded_company CHECK (
    graded_company IS NULL OR graded_company IN ('PSA','BGS','CGC')
  )
);

-- Helpful indexes for lookups
CREATE INDEX idx_card_set_id ON card(set_id);
CREATE INDEX idx_inventory_card_id ON inventory_item(card_id);

