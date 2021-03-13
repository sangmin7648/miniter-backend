from sqlalchemy import text


class UserDao:
    def __init__(self, database):
        self.db = database

    def insert_user(self, new_user):
        return self.db.execute(text(
            """
            INSERT INTO users (name, email, profile, hashed_password)
            VALUES (:name, :email, :profile, :password)
            """), new_user).lastrowid

    def get_user(self, user_id):
        return self.db.execute(text(
            """
            SELECT id, name, email, profile
            FROM users
            WHERE id=:user_id
            """
        ), {'user_id': user_id}).fetchone()

    def get_user_id_and_password(self, email):
        return self.db.execute(text(
            """
            SELECT id, hashed_password
            FROM users
            WHERE email=:email
            """
        ), {'email': email}).fetchone()

    def insert_follow(self, user_id, follow_id):
        return self.db.execute(text(
            """
            INSERT INTO users_follow_list (user_id, follow_id)
            VALUES (:user_id, :follow_id)
            """
        ), {'user_id': user_id,
            'follow_id': follow_id}).rowcount

    def insert_unfollow(self, user_id, unfollow_id):
        return self.db.execute(text(
            """
            DELETE FROM users_follow_list
            WHERE user_id=:user_id AND unfollow_id=:unfollow_id
            """
        ), {'user_id': user_id,
            'unfollow_id': unfollow_id}).rowcount
