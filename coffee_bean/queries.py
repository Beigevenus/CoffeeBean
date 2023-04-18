SELECT_MEMBER_ID = "SELECT member_id FROM intro WHERE member_id = ?;"
SELECT_INTRO_LINK = "SELECT intro_link FROM intro WHERE member_id = ?;"
UPDATE_INTRO_LINK = "UPDATE intro SET intro_link = ? WHERE member_ID = ?"
INSERT_INTRO = "INSERT INTO intro (member_id, intro_link) VALUES (?, ?)"
