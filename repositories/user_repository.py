from psycopg import Connection


def create_user(
    connection: Connection,
    email: str,
    password_hash: str,
    role: str
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (email, password_hash, role)
            VALUES (%s, %s, %s)
            RETURNING id, email, role;
            """,
            (email, password_hash, role)
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
        SELECT id, email, password_hash, role
        FROM users
        WHERE email = %s;
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()

    return user