"""
CTF Web Challenge - deliberately vulnerable login app (SQL injection).

Vulnerability: classic SQLi in the login query (' OR '1'='1 -- bypass).
Detection: every suspicious input is logged with the marker SQLI_ATTEMPT,
which the custom Wazuh rule (id 100200, local_rules.xml) matches.

Run:        python app.py            (listens on 0.0.0.0:80)
Container:  docker build -t ctf-web-challenge . && docker run -d -p 8080:80 ctf-web-challenge
"""
import logging
import re
import sqlite3

from flask import Flask, request, render_template_string

app = Flask(__name__)

FLAG = "flag{sql1_byp4ss_m4st3r}"

# Plain stdout logging -> picked up by Docker logs / syslog -> Wazuh agent
logging.basicConfig(level=logging.INFO, format="CTF_WEB %(levelname)s %(message)s")
log = logging.getLogger("ctf-web")

# Patterns that look like injection attempts
SUSPECT = re.compile(r"('|--|;|/\*|\bunion\b|\bselect\b|\bor\b\s+\d|\bor\b\s+')", re.I)

PAGE = """<!doctype html>
<html><head><title>SecureVault Login</title>
<style>body{font-family:sans-serif;background:#0d1117;color:#c9d1d9;display:flex;justify-content:center;margin-top:10vh}
.box{background:#161b22;padding:2rem;border-radius:10px;border:1px solid #30363d;width:320px}
input{width:100%;padding:.5rem;margin:.4rem 0;background:#0d1117;color:#c9d1d9;border:1px solid #30363d;border-radius:6px}
button{width:100%;padding:.6rem;background:#1f6feb;color:#fff;border:0;border-radius:6px;cursor:pointer}
.flag{color:#3fb950;font-weight:bold}</style></head>
<body><div class="box"><h2>SecureVault</h2><p>{{ msg }}</p>
<form method="post" action="/login">
<input name="username" placeholder="Username" autocomplete="off">
<input name="password" type="password" placeholder="Password">
<button type="submit">Login</button></form></div></body></html>"""


def init_db():
    db = sqlite3.connect(":memory:", check_same_thread=False)
    db.execute("CREATE TABLE users (username TEXT, password TEXT)")
    db.execute("INSERT INTO users VALUES ('admin', 'S3cur3V4ult!2024')")
    db.execute("INSERT INTO users VALUES ('guest', 'guest123')")
    return db


DB = init_db()


@app.route("/")
def index():
    log.info("PAGE_VIEW src=%s path=/", request.remote_addr)
    return render_template_string(PAGE, msg="Authorized personnel only.")


@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username", "")
    p = request.form.get("password", "")

    if SUSPECT.search(u) or SUSPECT.search(p):
        # This exact marker is what the Wazuh custom rule matches on.
        log.warning("SQLI_ATTEMPT src=%s username=%r password=%r",
                    request.remote_addr, u, p)

    # VULNERABLE: string interpolation directly into the query. Do NOT copy
    # this pattern into real code - use parameterized queries instead.
    query = f"SELECT * FROM users WHERE username = '{u}' AND password = '{p}'"
    try:
        rows = DB.execute(query).fetchall()
    except sqlite3.Error as e:
        log.warning("SQL_ERROR src=%s error=%s", request.remote_addr, e)
        return render_template_string(PAGE, msg="Something went wrong.")

    if rows:
        log.warning("SQLI_SUCCESS src=%s username=%r", request.remote_addr, u)
        return render_template_string(
            PAGE, msg=f'<span class="flag">Access granted. {FLAG}</span>')
    log.info("LOGIN_FAIL src=%s username=%r", request.remote_addr, u)
    return render_template_string(PAGE, msg="Invalid credentials.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
