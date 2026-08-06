import sqlite3

DB_NAME = "reviews.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ----------------------------------------------------
# Initialize Database
# ----------------------------------------------------

def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        language TEXT,
        score INTEGER,
        review TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ----------------------------------------------------
# Save Review
# ----------------------------------------------------

def save_review(filename, language, score, review):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reviews
        (filename, language, score, review)
        VALUES (?,?,?,?)
    """, (filename, language, score, review))

    conn.commit()
    conn.close()


# ----------------------------------------------------
# Dashboard Stats
# ----------------------------------------------------

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reviews")
    total_reviews = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM reviews")
    avg = cursor.fetchone()[0]

    if avg is None:
        avg = 0

    cursor.execute("SELECT COUNT(DISTINCT language) FROM reviews")
    languages = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reviews WHERE score>=80")
    production_ready = cursor.fetchone()[0]

    conn.close()

    return {
        "total_reviews": total_reviews,
        "avg_score": round(avg,1),
        "languages": languages,
        "production_ready": production_ready
    }


# ----------------------------------------------------
# Recent Reviews
# ----------------------------------------------------

def get_recent_reviews(limit=10):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT filename,
               language,
               score,
               created_at
        FROM reviews
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    data = cursor.fetchall()

    conn.close()

    return data


# ----------------------------------------------------
# All Reviews
# ----------------------------------------------------

def get_all_reviews():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               filename,
               language,
               score,
               review,
               created_at
        FROM reviews
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ----------------------------------------------------
# Delete Review
# ----------------------------------------------------

def delete_review(review_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reviews WHERE id=?",
        (review_id,)
    )

    conn.commit()
    conn.close()


# ----------------------------------------------------
# Reviews by Language
# ----------------------------------------------------

def get_language_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT language,
               COUNT(*)
        FROM reviews
        GROUP BY language
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ----------------------------------------------------
# Score Distribution
# ----------------------------------------------------

def get_score_distribution():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        CASE

        WHEN score>=90 THEN '90-100'

        WHEN score>=80 THEN '80-89'

        WHEN score>=70 THEN '70-79'

        WHEN score>=60 THEN '60-69'

        ELSE 'Below 60'

        END AS bucket,

        COUNT(*)

        FROM reviews

        GROUP BY bucket
    """)

    data = cursor.fetchall()

    conn.close()

    return data


# ----------------------------------------------------
# Daily Reviews
# ----------------------------------------------------

def get_daily_reviews():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        DATE(created_at),
        COUNT(*)

        FROM reviews

        GROUP BY DATE(created_at)

        ORDER BY DATE(created_at)
    """)

    data = cursor.fetchall()

    conn.close()

    return data