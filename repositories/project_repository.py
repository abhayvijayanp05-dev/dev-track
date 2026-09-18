from psycopg import Connection


def get_all_projects(connection: Connection):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM projects;
        """
    )

    rows = cursor.fetchall()

    cursor.close()

    return rows


def create_project(
    connection: Connection,
    name: str,
    status: str,
    owner_id: int
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO projects (name, status, owner_id)
            VALUES (%s, %s, %s)
            RETURNING id, name, status, owner_id;
            """,
            (
                name,
                status,
                owner_id
            )
        )

        row = cursor.fetchone()

        connection.commit()

        return row

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        
def get_project_by_id(connection: Connection, project_id: int):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, status, owner_id
        FROM projects
        WHERE id = %s;
        """,
        (project_id,)
    )

    row = cursor.fetchone()

    cursor.close()

    return row

def update_project(
    connection: Connection,
    project_id: int,
    name: str,
    status: str
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE projects
            SET name = %s,
                status = %s
            WHERE id = %s;
            """,
            (name, status, project_id)
        )

        row_count = cursor.rowcount

        connection.commit()

        return row_count

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()



def delete_project(
    connection: Connection,
    project_id: int
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            DELETE FROM projects
            WHERE id = %s;
            """,
            (project_id,)
        )

        row_count = cursor.rowcount

        connection.commit()

        return row_count

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()