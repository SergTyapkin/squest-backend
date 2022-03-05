# -----------------------
# -- Default user part --
# -----------------------
_userColumns = "id, name, email, isadmin, joineddate, isconfirmed, avatarurl, chosenquestid, chosenbranchid"
# ----- INSERTS -----
insertUser = \
    "INSERT INTO users (name, password, avatarUrl, email, ChosenQuestId, ChosenBranchId) " \
    "VALUES (%s, %s, %s, %s, NULL, NULL) " \
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

selectUserByName = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE name = %s"

selectUserIdBySessionToken = \
    "SELECT userId FROM sessions " \
    "WHERE token = %s"

selectSessionByUserId = \
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
deleteExpiredSessions = \
    "DELETE FROM sessions "\
    "WHERE expires <= NOW()"

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
    "INSERT INTO quests (title, description, author, isPublished) " \
    "VALUES (%s, %s, %s, %s) " \
    "RETURNING *"

insertProgress = \
    "INSERT INTO progresses (userId, branchId) " \
    "VALUES (%s, %s) " \
    "RETURNING * "

insertPrivacy = \
    "INSERT INTO questsPrivacy (userId, questId, isInBlackList) " \
    "VALUES (%s, %s, %s) " \
    "RETURNING *"

insertBranch = \
    "INSERT INTO branches (questId, title, description, orderid) " \
    "VALUES (%s, %s, %s, %s) " \
    "RETURNING *"

insertTask = \
    "INSERT INTO tasks (branchId, title, description, question, answers, orderid) " \
    "VALUES (%s, %s, %s, %s, %s, %s) " \
    "RETURNING *"

# ----- SELECTS -----
selectPublishedQuestsByAuthor = \
    "SELECT id, author, title, description, isPublished FROM quests " \
    "WHERE author = %s AND isPublished = true"

selectQuestById = \
    "SELECT id, author, title, description, isPublished FROM quests " \
    "WHERE id = %s"

selectQuestsByAuthor = \
    "SELECT id, author, title, description, isPublished FROM quests " \
    "WHERE author = %s"

selectPrivacyUsersIdByQuestId = \
    "SELECT id, userId, isInBlackList FROM questsPrivacy " \
    "WHERE questId = %s"

selectPrivacyUserNamesByQuestId = \
    "SELECT users.name as name, questsprivacy.id as id, isInBlackList FROM questsPrivacy " \
    "JOIN users ON userId = users.id " \
    "WHERE questId = %s"

selectPrivacyById = \
    "SELECT * FROM questsPrivacy " \
    "WHERE id = %s"

selectPublishedQuests = \
    "SELECT id, author, title, description FROM quests " \
    "WHERE isPublished = true"

# selectPublishedBranchesByQuestid = \
#     "SELECT branches.*, count(tasks.id) as length FROM tasks " \
#     "RIGHT JOIN branches ON tasks.branchid = branches.id " \

#     "GROUP BY branches.id"

selectPublishedBranchesByQuestid = \
    "SELECT * FROM branches " \
    "WHERE ispublished = true AND questid = %s " \
    "ORDER BY orderid"

selectBranchesByQuestid = \
    "SELECT * FROM branches " \
    "WHERE questId = %s " \
    "ORDER BY orderid"

selectBranchById = \
    "SELECT * FROM branches " \
    "WHERE id = %s"

selectBranchLengthById = \
    "SELECT branches.*, count(tasks.id) as length FROM tasks " \
    "RIGHT JOIN branches ON tasks.branchid = branches.id " \
    "WHERE branches.id = %s " \
    "GROUP BY branches.id"

selectBranchMaxOrderidByQuestid = \
    "SELECT max(orderid) as maxorderid FROM branches " \
    "WHERE questid = %s"

selectTaskMaxOrderidByBranchid = \
    "SELECT max(orderid) as maxorderid FROM tasks " \
    "WHERE branchid = %s"

selectQuestByBranchId = \
    "SELECT branches.*, quests.author, quests.ispublished as qispublished, quests.title as qtitle FROM quests " \
    "JOIN branches ON branches.questId = quests.id " \
    "WHERE branches.id = %s"


selectQuestByTaskId = \
    "SELECT tasks.*, branches.ispublished as bispublished, branches.title as btitle, quests.author, quests.ispublished as qispublished FROM tasks " \
    "JOIN branches ON tasks.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE tasks.id = %s"

selectTasksByBranchid = \
    "SELECT * FROM tasks " \
    "WHERE branchid = %s " \
    "ORDER BY orderid"

selectTasksByPublishedBranchid = \
    "SELECT tasks.id, tasks.title, tasks.description, tasks.question FROM tasks " \
    "JOIN branches ON tasks.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE branchid = %s AND quests.isPublished = true AND branches.isPublished = true"

selectTaskByBranchidNumber = \
    "SELECT id, orderid, title, description, question FROM tasks " \
    "WHERE branchid = %s " \
    "ORDER BY orderid " \
    "OFFSET %s LIMIT 1"

selectTaskAnswersByBranchidNumber = \
    "SELECT answers FROM tasks " \
    "WHERE branchid = %s " \
    "ORDER BY orderid " \
    "OFFSET %s LIMIT 1"

selectProgressByUseridBranchid = \
    "SELECT * FROM progresses " \
    "WHERE userid = %s AND branchid = %s"

selectRatings = \
    "SELECT sum(progresses.maxprogress) as rating, users.id, users.name " \
    "FROM users LEFT JOIN progresses ON progresses.userid = users.id " \
    "GROUP BY users.id " \
    "ORDER BY rating"


# ----- UPDATES -----
updateUserChooseBranchByUserId = \
    "UPDATE users SET " \
    "chosenQuestId = %s, " \
    "chosenBranchId = %s " \
    "WHERE id = %s"

updateQuestById = \
    "UPDATE quests SET " \
    "title = %s, " \
    "description = %s, " \
    "isPublished = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateBranchById = \
    "UPDATE branches SET " \
    "orderid = %s, " \
    "title = %s, " \
    "description = %s, " \
    "isPublished = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateBranchOrderidById = \
    "UPDATE branches SET " \
    "orderid = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateBranchTitleById = \
    "UPDATE branches SET " \
    "title = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updatePrivacyByIdQuestid = \
    "UPDATE questsPrivacy SET " \
    "userId = %s, " \
    "isInBlackList = %s " \
    "WHERE id = %s AND questId = %s " \
    "RETURNING *"

increaseProgressByUseridBranchid = \
    "UPDATE progresses SET " \
    "progress = progress + 1 " \
    "WHERE userId = %s AND branchId = %s " \
    "RETURNING *"

updateProgressByUseridBranchid = \
    "UPDATE progresses SET " \
    "progress = %s " \
    "WHERE userId = %s AND branchId = %s " \
    "RETURNING *"

updateTaskById = \
    "UPDATE tasks SET " \
    "orderid = %s, " \
    "title = %s, " \
    "description = %s, " \
    "question = %s, " \
    "answers = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateTaskOrderidById = \
    "UPDATE tasks SET " \
    "orderid = %s, " \
    "WHERE id = %s " \
    "RETURNING *"

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

deletePrivacyById = \
    "DELETE FROM questsPrivacy " \
    "WHERE id = %s"

deletePrivacyByQuestidUserid = \
    "DELETE FROM questsPrivacy " \
    "WHERE questId = %s AND userid = %s"

deleteProgressByUserid = \
    "DELETE FROM progresses " \
    "WHERE userId = %s"


# --- IMAGES ---
insertImage = \
    "INSERT INTO images (author, type, base64) " \
    "VALUES (%s, %s, %s) " \
    "RETURNING *"

selectImageById = \
    "SELECT * FROM images " \
    "WHERE id = %s"

deleteImageByIdAuthor = \
    "DELETE FROM images " \
    "WHERE id = %s AND author = %s"
