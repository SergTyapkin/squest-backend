------- Users data -------
CREATE TABLE IF NOT EXISTS users (
    id               SERIAL PRIMARY KEY,
    name             TEXT NOT NULL UNIQUE,
    password         TEXT NOT NULL,
    email            TEXT DEFAULT NULL UNIQUE,
    isAdmin          BOOLEAN DEFAULT FALSE,
    joinedDate       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    isConfirmed      BOOLEAN DEFAULT FALSE,
    avatarUrl        TEXT DEFAULT NULL
    -- chosenQuestId    SERIAL -- will adds by ALTER in end
    -- chosenBranchId   SERIAL -- will adds by ALTER in end
);

CREATE TABLE IF NOT EXISTS sessions (
    userId   SERIAL NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token    TEXT NOT NULL UNIQUE,
    expires  TIMESTAMP WITH TIME ZONE
);

------ Quests data -------
CREATE TABLE IF NOT EXISTS quests (
    id             SERIAL PRIMARY KEY,
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    createdDate    TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    author         SERIAL NOT NULL REFERENCES users(id),
    isPublished    BOOL NOT NULL DEFAULT false,
    isModerated    BOOL NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS questsPrivacy (
    id           SERIAL PRIMARY KEY,
    userId       SERIAL NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    questId      SERIAL NOT NULL REFERENCES quests(id) ON DELETE CASCADE,
    isInBlackList  BOOL NOT NULL DEFAULT false,
    UNIQUE (userId, questId)
);

CREATE TABLE IF NOT EXISTS questsHelpers (
    id           SERIAL PRIMARY KEY,
    userId       SERIAL NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    questId      SERIAL NOT NULL REFERENCES quests(id) ON DELETE CASCADE,
    UNIQUE (userId, questId)
);

CREATE TABLE IF NOT EXISTS branches (
    id             SERIAL PRIMARY KEY,
    orderId        SERIAL NOT NULL,
    questId        SERIAL NOT NULL REFERENCES quests(id) ON DELETE CASCADE,
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    isPublished    BOOL NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS progresses (
    userId       SERIAL NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    branchId     SERIAL NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    progress     INT NOT NULL DEFAULT 0,
    maxProgress  INT NOT NULL DEFAULT 0,
    isFoundBonus BOOL NOT NULL DEFAULT FALSE,
    UNIQUE (userId, branchId)
);

CREATE TABLE IF NOT EXISTS tasks (
    id             SERIAL PRIMARY KEY,
    orderId        SERIAL,
    branchId       SERIAL NOT NULL REFERENCES branches(id) ON DELETE CASCADE,
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    question       TEXT DEFAULT NULL,
    answers        TEXT ARRAY NOT NULL
);


CREATE TABLE IF NOT EXISTS images (
    id             SERIAL PRIMARY KEY,
    author         SERIAL REFERENCES users(id),
    type           TEXT NOT NULL,
    base64         TEXT NOT NULL
);

----------
DO $$
BEGIN
    IF NOT EXISTS(
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'users'
          AND column_name = 'chosenquestid'
    ) THEN
        ALTER TABLE users ADD COLUMN
            ChosenQuestId SERIAL REFERENCES quests(id) ON DELETE SET NULL;
        ALTER TABLE users ALTER COLUMN ChosenQuestId
            DROP NOT NULL;

        ALTER TABLE users ADD COLUMN
            ChosenBranchId SERIAL REFERENCES branches(id) ON DELETE SET NULL;
        ALTER TABLE users ALTER COLUMN ChosenBranchId
            DROP NOT NULL;
    END IF;
END;
$$;



--------
CREATE OR REPLACE FUNCTION set_actual_max_progress() RETURNS TRIGGER AS
$$
BEGIN
    IF NEW.progress > OLD.maxProgress THEN
        NEW.maxprogress = NEW.progress;
    END IF;

    RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS before_update ON progresses;
CREATE TRIGGER before_update
    BEFORE UPDATE ON progresses
    FOR EACH ROW
        EXECUTE PROCEDURE set_actual_max_progress();
