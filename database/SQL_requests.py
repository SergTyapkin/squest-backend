# -----------------------
# -- Default user part --
# -----------------------
_userColumns = "id, name, email, isadmin, joineddate, isconfirmed, avatarurl"
# ----- INSERTS -----
insertUser = \
    "INSERT INTO users (name, password, avatarUrl, email, ChosenQuestId) " \
    "VALUES (%s, %s, %s, %s, NULL) " \
    f"RETURNING {_userColumns}"

insertSession = \
    "INSERT INTO sessions (userId, token, expires) " \
    "VALUES (%s, %s, %s)"

# ----- SELECTS -----
selectUserByNamePassword = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE name = %s AND password = %s"

selectUserById = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE id = %s"

selectUserIdBySessionToken = \
    "SELECT userId FROM sessions " \
    "WHERE token = %s"

selectSessionById = \
    "SELECT token, expires FROM sessions " \
    "WHERE userId = %s"

selectUserDataBySessionToken = \
    f"SELECT {_userColumns} FROM sessions " \
    "JOIN users ON sessions.userId = users.id " \
    "WHERE token = %s"

# ----- UPDATES -----
updateUserConfirmationByName = \
    "UPDATE users SET " \
    "isConfirmed = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserNameByName = \
    "UPDATE users SET " \
    "name = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserAvatarByName = \
    "UPDATE users SET " \
    "avatarUrl = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserEmailByName = \
    "UPDATE users SET " \
    "email = %s " \
    "WHERE name = %s " \
    "RETURNING id"

updateUserById = \
    "UPDATE users SET " \
    "name = %s, " \
    "email = %s, " \
    "avatarUrl = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateUserPasswordByIdPassword = \
    "UPDATE users SET " \
    "password = %s " \
    "WHERE id = %s AND password = %s " \
    "RETURNING id"


# ----- DELETES -----
deleteUserById = \
    "DELETE FROM users "\
    "WHERE id = %s"

deleteSessionByToken = \
    "DELETE FROM sessions " \
    "WHERE token = %s"


# -----------------
# -- Quests part --
# -----------------

# ----- INSERTS -----
insertQuest = \
    "INSERT INTO quests (title, description, author) " \
    "VALUES (%s, %s, %s) " \
    f"RETURNING *"

insertProgress = \
    "INSERT INTO progresses (userId, questId) " \
    "VALUES (%s, %s) " \
    "RETURNING * "

insertQuestPrivacy = \
    "INSERT INTO questsPrivacy (userId, questId, isInBlackList) " \
    "VALUES (%s, %s, %s) " \
    "RETURNING *"

insertBranch = \
    "INSERT INTO branches (questId, title, description) " \
    "VALUES (%s, %s, %s) " \
    "RETURNING *"

insertTask = \
    "INSERT INTO tasks (branchId, title, description, question, answers) " \
    "VALUES (%s, %s, %s, %s, %s) " \
    "RETURNING *"

# ----- SELECTS -----
selectPublishedQuestsByAuthor = \
    "SELECT * FROM quests " \
    "WHERE author = %s AND isPublished = true"

selectQuestById = \
    "SELECT * FROM quests " \
    "WHERE id = %s"

selectQuestsByAuthor = \
    "SELECT * FROM quests " \
    "WHERE author = %s"

selectPrivacyUsersIdByQuestId = \
    "SELECT userId, isInBlackList FROM questsPrivacy " \
    "WHERE questId = %s"

selectPublishedQuests = \
    "SELECT * FROM quests " \
    "WHERE isPublished = true"


selectPublishedBranchesByQuestid = \
    "SELECT branches.* FROM branches " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE questId = %s AND quests.isPublished = true AND branches.isPublished = true"

selectBranchesByQuestid = \
    "SELECT * FROM branches " \
    "WHERE questId = %s"

selectQuestByBranchId = \
    "SELECT branches.*, quests.author, quests.ispublished as qispubliched FROM quests " \
    "JOIN branches ON branches.questId = quests.id " \
    "WHERE branches.id = %s"


selectQuestByTaskId = \
    "SELECT tasks.*, branches.ispublished, quests.author, quests.ispublished as qispubliched FROM tasks " \
    "JOIN branches ON tasks.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE tasks.id = %s"

selectTasksByBranchid = \
    "SELECT * FROM tasks " \
    "WHERE branchid = %s"

selectTasksByPublishedBranchid = \
    "SELECT tasks.* FROM tasks " \
    "JOIN branches ON tasks.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE branchid = %s AND quests.isPublished = true AND branches.isPublished = true"

# ----- UPDATES -----
updateUserChosenquestidByUserId = \
    "UPDATE users SET " \
    "chosenQuestId = %s " \
    "WHERE id = %s"

updateQuestById = \
    "UPDATE quests SET " \
    "title = %s, " \
    "description = %s, " \
    "isPublished = %s " \
    "WHERE id = %s"

updateBranchById = \
    "UPDATE quests SET " \
    "title = %s, " \
    "description = %s, " \
    "isPublished = %s " \
    "WHERE id = %s "

updatePrivacyIsInBlackListByQuestidUserid = \
    "UPDATE questsPrivacy SET " \
    "isInBlackList = %s " \
    "WHERE questId = %s AND userId = %s"

increaseProgressByUseridQuestid = \
    "UPDATE progresses SET " \
    "progress = progress + 1 " \
    "WHERE userId = %s AND questId = %s"

updateProgressByUseridQuestid = \
    "UPDATE progresses SET " \
    "progress = %s " \
    "WHERE userId = %s AND questId = %s"

updateTaskById = \
    "UPDATE tasks SET " \
    "title = %s, " \
    "description = %s, " \
    "question = %s, " \
    "answers = %s " \
    "WHERE id = %s"

# ----- DELETES -----
deleteQuestById = \
    "DELETE FROM quests " \
    "WHERE id = %s"

deleteBranchById = \
    "DELETE FROM branches " \
    "WHERE id = %s"

deleteTaskById = \
    "DELETE FROM tasks " \
    "WHERE id = %s"

deletePrivacyByQuestid = \
    "DELETE FROM questsPrivacy " \
    "WHERE questId = %s"

deletePrivacyByQuestidUserid = \
    "DELETE FROM questsPrivacy " \
    "WHERE questId = %s AND userid = %s"

deleteProgressByUserid = \
    "DELETE FROM progresses " \
    "WHERE userId = %s"
