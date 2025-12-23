import pandas as pd
import mysql.connector
import hashlib

# ====== Config ======
CSV_PATH = "/Users/yvony/Downloads/google-play-scraper-demo-main/data/chatgpt_google_play_reviews_clean.csv"
DB_NAME = "review_analytics"

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "MYSQL_PASSWORD",   # Change to your code
    "database": DB_NAME
}

PACKAGE_NAME = "com.openai.chatgpt"
APP_NAME = "ChatGPT"


# ====== Helpers ======
def make_review_id(row) -> str:
    base = f"{row.get('userName','')}_{row.get('at','')}_{row.get('content','')}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


# ====== Load CSV ======
df = pd.read_csv(CSV_PATH)
df["review_id"] = df.apply(make_review_id, axis=1)

df = df.rename(columns={
    "content": "content",
    "score": "score",
    "at": "reviewed_at",
    "appVersion": "app_version",
    "userName": "user_name",
    "thumbsUpCount": "thumbs_up_count"
})

df["reviewed_at"] = pd.to_datetime(df["reviewed_at"], errors="coerce")
df = df[df["reviewed_at"].notna()]
df["content"] = df["content"].astype(str).str.strip()
df = df[df["content"] != ""]

df = df.where(pd.notnull(df), None)

# ====== Connect MySQL ======
conn = mysql.connector.connect(**MYSQL_CONFIG)
cur = conn.cursor()

# Insert app if not exists
cur.execute(
    "INSERT IGNORE INTO apps (package_name, app_name) VALUES (%s, %s)",
    (PACKAGE_NAME, APP_NAME)
)
conn.commit()

cur.execute(
    "SELECT app_id FROM apps WHERE package_name = %s",
    (PACKAGE_NAME,)
)
app_id = cur.fetchone()[0]


# ====== Insert reviews ======
insert_sql = """
INSERT IGNORE INTO reviews
(review_id, app_id, source, content, score, reviewed_at, app_version, user_name, thumbs_up_count)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

rows = []
for _, r in df.iterrows():
    rows.append((
        r["review_id"],
        app_id,
        "google_play",
        r["content"],
        int(r["score"]),
        r["reviewed_at"].to_pydatetime(),
        r.get("app_version", None),
        r.get("user_name", None),
        int(r.get("thumbs_up_count", 0)),
    ))

cur.executemany(insert_sql, rows)
conn.commit()

cur.close()
conn.close()

print("df shape:", df.shape)
print("Total rows in CSV:", len(df))
print("Rows attempted to insert:", len(rows))
print("Rows actually inserted:", cur.rowcount)
