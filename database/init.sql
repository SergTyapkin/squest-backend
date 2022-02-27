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
);

CREATE TABLE IF NOT EXISTS sessions (
    userId   SERIAL NOT NULL REFERENCES users(id),
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
    isPublished    BOOL NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS progresses (
    userId       SERIAL NOT NULL REFERENCES users(id),
    questId      SERIAL NOT NULL REFERENCES quests(id),
    progress     INT NOT NULL DEFAULT 0,
    isFoundBonus BOOL NOT NULL DEFAULT FALSE,
    UNIQUE (userId, questId)
);

CREATE TABLE IF NOT EXISTS questsPrivacy (
    userId       SERIAL NOT NULL REFERENCES users(id),
    questId      SERIAL NOT NULL REFERENCES quests(id),
    isInBlackList  BOOL NOT NULL DEFAULT false,
    UNIQUE (userId, questId)
);

CREATE TABLE IF NOT EXISTS branches (
    id             SERIAL PRIMARY KEY,
    questId        SERIAL NOT NULL REFERENCES quests(id),
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    isPublished    BOOL NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS tasks (
    id             SERIAL PRIMARY KEY,
    branchId       SERIAL NOT NULL REFERENCES branches(id),
    title          TEXT DEFAULT NULL,
    description    TEXT DEFAULT NULL,
    question       TEXT DEFAULT NULL,
    answers        TEXT ARRAY NOT NULL
);

----------
-- DO $$
-- BEGIN
--     IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_chosenquestid_fkey') THEN
--         ALTER TABLE users
--             ADD CONSTRAINT users_chosenquestid_fkey
--                 FOREIGN KEY (chosenQuestId) REFERENCES quests(id);
--     END IF;
-- END;
-- $$;

DO $$
BEGIN
    IF NOT EXISTS(
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'users'
          AND column_name = 'chosenquestid'
    ) THEN
        ALTER TABLE users ADD COLUMN
            ChosenQuestId SERIAL REFERENCES quests(id);
        ALTER TABLE users ALTER COLUMN ChosenQuestId
            DROP NOT NULL;
    END IF;
END;
$$;
