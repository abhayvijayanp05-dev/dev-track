from psycopg import Connection

def create_user(
    connection: Connection,
    email: str,
    password_hash: str,
    role: str,
    status: str
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, role, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, role, status;
            """,
            (email, password_hash, role, status)
        )

        user = cursor.fetchone()

        connection.commit()

        return user

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()


        #geting user 

def get_user_by_email(
    connection: Connection,
    email: str
):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, email, password_hash, role, status
        FROM users
        WHERE email = %s;
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()

    return user



def approve_teacher(
    connection: Connection,
    user_id: int
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE users
            SET status = 'active'
            WHERE id = %s
            AND role = 'teacher'
            AND status = 'pending'
            RETURNING id, email, role, status;
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        connection.commit()

        return user

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()