import sqlite3

# Create and connect to the SQLite database
con = sqlite3.connect("tutorial.db")
cur = con.cursor()

# Create tables with corrected foreign keys and primary keys
cur.execute("""
CREATE TABLE IF NOT EXISTS resource_lists (
  resource_list_id INTEGER PRIMARY KEY,
  name TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  UNIQUE(resource_list_id)
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS resources (
  resource_id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  md_content TEXT NOT NULL,
  image_url TEXT,
  resource_type TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  resource_list_id INTEGER REFERENCES resource_lists(resource_list_id) ON DELETE CASCADE
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS persons (
  person_id INTEGER PRIMARY KEY,
  resource_id INTEGER REFERENCES resources(resource_id) ON DELETE CASCADE,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  UNIQUE(person_id)
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS events (
  event_id INTEGER PRIMARY KEY,
  resource_id INTEGER REFERENCES resources(resource_id) ON DELETE CASCADE,
  location TEXT NOT NULL,
  start_datetime_utc INTEGER NOT NULL,
  duration_ms INTEGER NOT NULL,
  all_day BOOLEAN NOT NULL,
  visibility TEXT NOT NULL,
  team TEXT NOT NULL,
  author INTEGER REFERENCES persons(person_id) ON DELETE CASCADE,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  UNIQUE(event_id)
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS announcements (
  announcement_id INTEGER PRIMARY KEY,
  start_datetime_utc INTEGER NOT NULL,
  duration_ms INTEGER NOT NULL,
  visibility TEXT NOT NULL,
  scheduled_datetime_utc INTEGER NOT NULL,
  author INTEGER REFERENCES persons(person_id) ON DELETE CASCADE,
  resource_list_id INTEGER REFERENCES resource_lists(resource_list_id) ON DELETE CASCADE,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  UNIQUE(announcement_id)
);
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS resource_references (
  resource_reference_id INTEGER PRIMARY KEY,
  resource_list_id INTEGER REFERENCES resource_lists(resource_list_id) ON DELETE CASCADE,
  resource_id INTEGER REFERENCES resources(resource_id) ON DELETE CASCADE,
  index_in_resource_list INTEGER NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  UNIQUE(resource_list_id, resource_id)
);
""")

# Sample data for demonstration
cur.execute("""
INSERT INTO resource_lists (name, created_at, updated_at)
VALUES (?, ?, ?);
""", ("My Resources List", 0, 0))

cur.execute("""
INSERT INTO resources (title, md_content, image_url, resource_type, created_at, updated_at, resource_list_id)
VALUES (?, ?, ?, ?, ?, ?, ?);
""", ("My Event", "This is my event.", "image_url", "resource_type", 0, 0, 1))

cur.execute("""
INSERT INTO events (resource_id, location, start_datetime_utc, duration_ms, all_day, visibility, team, author, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
""", (1, "My Location", 0, 0, 0, "My Visibility", "My Team", 1, 0, 0))

cur.execute("""
INSERT INTO announcements (start_datetime_utc, duration_ms, visibility, scheduled_datetime_utc, author, resource_list_id, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", (0, 0, "My Visibility", 0, 0, 1, 0, 0))

# Commit the changes to the database
con.commit()

# Example queries

# Get a resource
resource_id = 1
cur.execute("SELECT * FROM resources WHERE resource_id = ?", (resource_id,))
result = cur.fetchone()
print("Resource:")
print(result)

# Get an announcement
announcement_id = 1
cur.execute("SELECT * FROM announcements WHERE announcement_id = ?", (announcement_id,))
result = cur.fetchone()
print("Announcement:")
print(result)

# List all resources in the announcement list
announcement_list_id = 1
cur.execute("""
SELECT resources.* FROM resources
INNER JOIN resource_references ON resources.resource_id = resource_references.resource_id
WHERE resource_references.resource_list_id = ?;
""", (announcement_list_id,))
results = cur.fetchall()
print("Resources in Announcement List:")
for row in results:
    print(row)

# Get list of events by announcement ID
cur.execute("SELECT * FROM events WHERE resource_id = ?", (announcement_id,))
results = cur.fetchall()
print("Events in Announcement:")
for row in results:
    print(row)

# Close the database connection
con.close()
