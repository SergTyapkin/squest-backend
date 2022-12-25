# -----------------------
# -- Default user part --
# -----------------------
_userColumns = "users.id, name, username, email, isadmin, joineddate, isconfirmed, avatarimageid, chosenquestid, chosenbranchid, chosenmode"
# ----- INSERTS -----
insertUser = \
    "INSERT INTO users (username, password, avatarImageId, email, name, ChosenQuestId, ChosenBranchId) " \
    "VALUES (%s, %s, NULL, %s, %s, NULL, NULL) " \
    f"RETURNING {_userColumns}"

insertSession = \
    "INSERT INTO sessions (userId, token, expires) " \
    "VALUES (%s, %s, NOW() + interval '1 hour' * %s) " \
    "RETURNING *"

insertSecretCode = \
    "INSERT INTO secretCodes (userId, code, type, expires) " \
    "VALUES (%s, %s, %s, NOW() + interval '1 hour' * %s)" \
    "RETURNING *"

# ----- SELECTS -----
selectUserByUsernamePassword = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE username = %s AND password = %s"

selectUserByEmailPassword = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE email = %s AND password = %s"

selectUserById = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE id = %s"

selectAnotherUserById = \
    f"SELECT users.id, name, username, joineddate, avatarImageId, chosenbranchid, chosenquestid, quests.title as chosenQuest, branches.title as chosenBranch FROM users " \
    "LEFT JOIN quests ON users.chosenquestid = quests.id " \
    "LEFT JOIN branches ON users.chosenbranchid = branches.id " \
    "WHERE users.id = %s"

selectCreatedQuestsByUserid = \
    f"SELECT quests.id, quests.title FROM users " \
    "JOIN quests ON users.id = quests.author " \
    "WHERE users.id = %s"

selectCompletedBranchesByUserid = \
    f"SELECT branches.id as branchid, branches.title as branchtitle, quests.id as questid, quests.title as questtitle FROM users " \
    "LEFT JOIN progresses ON progresses.userid = users.id " \
    "LEFT JOIN branches ON progresses.branchid = branches.id " \
    "LEFT JOIN quests ON branches.questid = quests.id " \
    "WHERE users.id = %s AND progresses.isfinished = True"

selectUserByUsername = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE username = %s"

selectUserByEmail = \
    f"SELECT {_userColumns} FROM users " \
    "WHERE email = %s"

selectUserIdBySessionToken = \
    "SELECT userId FROM sessions " \
    "WHERE token = %s"

selectSessionByUserId = \
    "SELECT token, expires FROM sessions " \
    "WHERE userId = %s"

selectUserDataBySessionToken = \
    f"SELECT {_userColumns}, quests.title as chosenQuest, branches.title as chosenBranch FROM sessions " \
    "JOIN users ON sessions.userId = users.id " \
    "LEFT JOIN quests ON users.chosenquestid = quests.id " \
    "LEFT JOIN branches ON users.chosenbranchid = branches.id " \
    "WHERE token = %s"

selectSecretCodeByUserIdType = \
    "SELECT * FROM secretCodes " \
    "WHERE userId = %s AND " \
    "type = %s AND " \
    "expires > NOW()"

selectUserByEmailCodeType = \
    "SELECT users.id, name, username, joineddate, avatarImageId, chosenbranchid, chosenquestid, chosenmode FROM users " \
    "JOIN secretCodes ON secretCodes.userId = users.id " \
    "WHERE email = %s AND " \
    "code = %s AND " \
    "type = %s AND " \
    "expires > NOW()"

# ----- UPDATES -----
updateUserById = \
    "UPDATE users SET " \
    "username = %s, " \
    "name = %s, " \
    "email = %s, " \
    "avatarImageId = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateUserPasswordByIdPassword = \
    "UPDATE users SET " \
    "password = %s " \
    "WHERE id = %s AND password = %s " \
    "RETURNING id"

updateUserPasswordBySecretcodeType = \
    "UPDATE users " \
    "SET password = %s " \
    "FROM secretCodes " \
    "WHERE secretCodes.userId = users.id AND " \
    "secretCodes.code = %s AND " \
    "secretCodes.type = %s " \
    "RETURNING users.*"


updateUserConfirmationBySecretcodeType = \
    "UPDATE users " \
    "SET isConfirmed = True " \
    "FROM secretCodes " \
    "WHERE secretCodes.userId = users.id AND " \
    "secretCodes.code = %s AND " \
    "secretCodes.type = %s " \
    "RETURNING users.*"

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

deleteExpiredSecretCodes = \
    "DELETE FROM secretCodes "\
    "WHERE expires <= NOW()"

deleteSecretCodeByUseridCode = \
    "DELETE FROM secretCodes " \
    "WHERE userId = %s AND " \
    "code = %s"

# -----------------
# -- Quests part --
# -----------------

# ----- INSERTS -----
insertQuest = \
    "INSERT INTO quests (uid, title, description, author, isPublished) " \
    "VALUES (%s, %s, %s, %s, %s) " \
    "RETURNING *"

insertProgress = \
    "INSERT INTO progresses (userId, branchId) " \
    "VALUES (%s, %s) " \
    "RETURNING * "

insertHelper = \
    "INSERT INTO questsHelpers (userId, questId) " \
    "VALUES (%s, %s) " \
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
selectPublishedQuestsByAuthorUserid = \
    "SELECT id, author, title, description, isPublished, previewUrl FROM quests " \
    "WHERE author = %s AND ( " \
    "   isPublished = true OR " \
    "   (id IN " \
    "      (SELECT questid FROM questshelpers" \
    "          JOIN users on questshelpers.userid = users.id " \
    "          WHERE userid = %s " \
    "      ) " \
    "   )" \
    ")"

selectQuestById = \
    "SELECT quests.id, uid, author, title, description, isPublished, isLinkActive, previewUrl, users.username as authorName " \
    "FROM quests LEFT JOIN users ON quests.author = users.id " \
    "WHERE quests.id = %s"

selectPublishedQuestById = \
    "SELECT quests.id, author, title, description, isPublished, previewUrl, users.username as authorName " \
    "FROM quests JOIN users ON quests.author = users.id " \
    "WHERE quests.id = %s " \
    "AND ispublished = true"

selectQuestByUid = \
    "SELECT quests.id, author, title, description, isPublished, previewUrl, users.username as authorName " \
    "FROM quests LEFT JOIN users ON quests.author = users.id " \
    "WHERE uid = %s " \
    "AND islinkactive = true"

selectQuestUidById = \
    "SELECT uid FROM quests " \
    "WHERE id = %s"

selectQuestByIdHelperid = \
    "SELECT quests.id, author, title, description, isPublished, isLinkActive, previewUrl, users.username as authorName " \
    "FROM quests LEFT JOIN users ON quests.author = users.id " \
    "LEFT JOIN questshelpers on quests.id = questshelpers.questid " \
    "WHERE quests.id = %s AND questshelpers.userid = %s"

selectHelpersUserNamesByQuestId = \
    "SELECT users.username as name, questsHelpers.id as id FROM questsHelpers " \
    "JOIN users ON userId = users.id " \
    "WHERE questId = %s"

selectHelperById = \
    "SELECT * FROM questsHelpers " \
    "WHERE id = %s"

# выбрать все квесты
# 1. где ты автор
# 2. где ты в соавторах
selectEditableQuestsByUseridx2 = \
    "SELECT quests.id, author, title, description, ispublished, islinkactive, previewUrl, users.username as authorName, True as canEdit " \
    "FROM quests JOIN users ON quests.author = users.id " \
    "WHERE " \
    "(author = %s) OR " \
    "(quests.id IN " \
    "   (SELECT questid FROM questshelpers" \
    "       JOIN users on questshelpers.userid = users.id " \
    "       WHERE userid = %s " \
    "   ) " \
    ")"

selectPublishedQuests = \
    "SELECT quests.id, author, title, description, isPublished, isLinkActive, previewUrl, users.username as authorName " \
    "FROM quests JOIN users ON quests.author = users.id " \
    "WHERE ispublished = True"

selectPublishedQuestsByUserid = \
    "SELECT id, author, title, description, ispublished FROM quests " \
    "WHERE isPublished = true OR quests.author = %s"

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

selectQuestByBranchidHelperId = \
    "SELECT branches.*, quests.author, quests.ispublished as qispublished, quests.title as qtitle FROM quests " \
    "JOIN branches ON branches.questId = quests.id " \
    "LEFT JOIN questshelpers on quests.id = questshelpers.questid " \
    "WHERE branches.id = %s AND questshelpers.userid = %s"

selectQuestByTaskId = \
    "SELECT tasks.*, branches.ispublished as bispublished, branches.title as btitle, quests.author, quests.ispublished as qispublished FROM tasks " \
    "JOIN branches ON tasks.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE tasks.id = %s"

selectQuestByTaskidHelperId = \
    "SELECT tasks.*, branches.ispublished as bispublished, branches.title as btitle, quests.author, quests.ispublished as qispublished FROM tasks " \
    "JOIN branches ON tasks.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "LEFT JOIN questshelpers on quests.id = questshelpers.questid " \
    "WHERE tasks.id = %s AND questshelpers.userid = %s"


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
    "SELECT id, orderid, title, description, question, isqranswer FROM tasks " \
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

selectProgressStatsByUseridBranchid = \
    "SELECT ratingvote as rating, finished - started as time FROM progresses " \
    "WHERE userid = %s AND branchid = %s"

# строка с WHERE нужна для удаления рейтингов авторов и хелперов в своих же квестах
selectRatings = \
    "SELECT sum(progresses.maxprogress) as rating, users.id, users.username " \
    "FROM users " \
    "LEFT JOIN progresses ON progresses.userid = users.id " \
    "LEFT JOIN branches ON branchid = branches.id " \
    "LEFT JOIN quests ON branches.questid = quests.id " \
    "LEFT JOIN questshelpers on quests.id = questshelpers.questid " \
    "WHERE ((quests.author IS NULL OR quests.author != users.id) AND (questshelpers.userid IS NULL OR questshelpers.userid != users.id)) AND " \
    "users.isConfirmed = True " \
    "GROUP BY users.id " \
    "ORDER BY rating DESC"


selectPLayersProgressesByQuestid = \
    "SELECT users.id, users.username, progresses.maxprogress as progress, branches.title as branchTitle, NOW() - progresses.started as time " \
    "FROM progresses " \
    "JOIN users ON progresses.userid = users.id " \
    "JOIN branches ON progresses.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE quests.id = %s " \
    "AND progresses.isfinished = False " \
    "AND progress != 0 " \
    "ORDER BY branchTitle, progress DESC"

selectFinishedQuestPLayersByQuestid = \
    "SELECT users.id, users.username, STRING_AGG(branches.title, ', ') as branches, SUM(progresses.finished - progresses.started) as time " \
    "FROM progresses " \
    "JOIN users ON progresses.userid = users.id " \
    "JOIN branches ON progresses.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE quests.id = %s " \
    "AND progresses.isfinished = True " \
    "GROUP BY users.id " \
    "ORDER BY time"

selectQuestStatisticsByQuestid = \
    "SELECT quests.id, avg(ratingvote) as rating, avg(finished - started) as time, count(*) as played " \
    "FROM progresses " \
    "JOIN branches ON progresses.branchid = branches.id " \
    "JOIN quests ON branches.questid = quests.id " \
    "WHERE quests.id = %s " \
    "AND progresses.isfinished = true " \
    "GROUP BY quests.id"

# ----- S -----
updateUserChooseBranchByUserId = \
    "UPDATE users SET " \
    "chosenQuestId = %s, " \
    "chosenBranchId = %s, " \
    "chosenMode = %s " \
    "WHERE id = %s"

updateQuestById = \
    "UPDATE quests SET " \
    "title = %s, " \
    "description = %s, " \
    "isPublished = %s, " \
    "isLinkActive = %s, " \
    "previewUrl = %s " \
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

updateHelperByIdQuestid = \
    "UPDATE questsHelpers SET " \
    "userId = %s " \
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
    "answers = %s, " \
    "isQrAnswer = %s " \
    "WHERE id = %s " \
    "RETURNING *"

updateTaskOrderidById = \
    "UPDATE tasks SET " \
    "orderid = %s, " \
    "WHERE id = %s " \
    "RETURNING *"

updateProgressRatingByBranchidUserid = \
    "UPDATE progresses SET " \
    "ratingvote = %s " \
    "WHERE isfinished = True AND " \
    "branchid = %s AND " \
    "userid = %s " \
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

deleteHelperById = \
    "DELETE FROM questsHelpers " \
    "WHERE id = %s"

deleteHelperByQuestidUserid = \
    "DELETE FROM questsHelpers " \
    "WHERE questId = %s AND userid = %s"

deleteProgressByUserid = \
    "DELETE FROM progresses " \
    "WHERE userId = %s"


# --- IMAGES ---
insertImage = \
    "INSERT INTO images (author, type, bytes) " \
    "VALUES (%s, %s, %s) " \
    "RETURNING id, author, type"

selectImageById = \
    "SELECT * FROM images " \
    "WHERE id = %s"

deleteImageByIdAuthor = \
    "DELETE FROM images " \
    "WHERE id = %s AND author = %s"
