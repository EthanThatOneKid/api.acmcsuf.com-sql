import sqlite3
con = sqlite3.connect("tutorial.db")
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS resource_references;")
cur.execute("""
CREATE TABLE IF NOT EXISTS resource_lists (
  resource_list_id INTEGER PRIMARY KEY,
  note TEXT,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  UNIQUE(resource_list_id)
);
""")

cur.execute("DROP TABLE IF EXISTS resources;")
cur.execute("""
CREATE TABLE IF NOT EXISTS resources (
  resource_id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  md_content TEXT NOT NULL,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  resource_list_id INTEGER REFERENCES resource_lists(resource_list_id) ON DELETE CASCADE
);
""")

cur.execute("DROP TABLE IF EXISTS resource_references;")
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

# Creates a new resource.
CREATE_RESOURCE_QUERY = """
INSERT INTO resources (title, md_content, created_at, updated_at, resource_list_id)
VALUES (?, ?, ?, ?, ?);
"""

cur.execute(CREATE_RESOURCE_QUERY, ("Hello World", "# Hello World!", 0, 0, 1))

# Get a resource.
GET_RESOURCE_QUERY = """
SELECT * FROM resources WHERE resource_id = ?;
"""

data = cur.execute(GET_RESOURCE_QUERY, (1,))
print(data.fetchone())

# Delete a resource.
DELETE_RESOURCE_QUERY = """
DELETE FROM resources WHERE resource_id = ?;
"""

cur.execute(DELETE_RESOURCE_QUERY, (1,))

# Create a resource list and assign a resource to it as its parent.
CREATE_RESOURCE_LIST_QUERY = """
INSERT INTO resource_lists (name, created_at, updated_at)
VALUES (?, ?, ?);
"""

cur.execute(CREATE_RESOURCE_LIST_QUERY, ("My Resource List", 0, 0))

# Get a resource list.
GET_RESOURCE_LIST_QUERY = """
SELECT * FROM resource_lists WHERE resource_list_id = ?;
"""

# Get all resource lists.
GET_ALL_RESOURCE_LISTS_QUERY = """
SELECT * FROM resource_lists;
"""

# Delete a resource list.
DELETE_RESOURCE_LIST_QUERY = """
DELETE FROM resource_lists WHERE resource_list_id = ?;
"""

# Add a resource to a resource list by creating a reference.
APPEND_TO_RESOURCE_LIST_QUERY = """
INSERT INTO resource_references (resource_list_id, resource_id, index_in_resource_list, created_at, updated_at)
VALUES (?, ?, ?, ?, ?);
"""

# Remove a resource from a resource list.
REMOVE_FROM_RESOURCE_LIST_QUERY = """
DELETE FROM resource_references WHERE resource_list_id = ? AND resource_id = ?;
"""

# Get all resources in a resource list returned in the order described by the resource_references table.
GET_ALL_RESOURCES_IN_RESOURCE_LIST_QUERY = """
SELECT resources.* FROM resources
INNER JOIN resource_references ON resources.resource_id = resource_references.resource_id
WHERE resource_references.resource_list_id = ?
ORDER BY resource_references.index_in_resource_list;
"""

# Reorder the resources in a resource list.
REORDER_RESOURCE_LIST_QUERY = """
UPDATE resource_references SET resource_id = ? WHERE resource_list_id = ? AND resource_id = ?;
"""

