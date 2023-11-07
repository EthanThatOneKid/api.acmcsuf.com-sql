""" Import either ones to main for usage and use inside of cur.execute() """

team = """ 
    CREATE TABLE IF NOT EXISTS team (
        team_id INTEGER PRIMARY KEY REFERENCES resources(resource_id) ON DELETE CASCADE,         
        name TEXT NOT NULL,
        member INTEGER,
        display_name TEXT NOT NULL,
        FOREIGN KEY (member) REFERENCES person(person_id),
        UNIQUE(team_id)
    );
"""

team_insert = """
    INSERT INTO team (team_id, name, member, display_name)
    VALUES (?, ?, ?, ?);
"""

team_get = """ SELECT * FROM team WHERE team_id = ? """

team_delete = """ DELETE FROM team WHERE team_id  = ? """

person = """ 
    CREATE TABLE IF NOT EXISTS person (
        person_id INTEGER PRIMARY KEY REFERENCES resources(resource_id) ON DELETE CASCADE,
        username TEXT NOT NULL,
        full_name TEXT NOT NULL,
        url TEXT NOT NULL,
        picture_url TEXT,
        team TEXT NOT NULL REFERENCES team(name),
        UNIQUE(person_id)
    );
"""

person_insert = """
    INSERT INTO person (team_id, name, member, display_name)
    VALUES (?, ?, ?, ?);
"""

person_get = """ SELECT * FROM person WHERE person_id = ? """

person_delete = """ DELETE FROM person WHERE person_id = ? """

blog_post = """ 
    CREATE TABLE IF NOT EXISTS blog_post (
        blog_post_id INTEGER PRIMARY KEY REFERENCES resources(resource_id) ON DELETE CASCADE,     
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author TEXT NOT NULL REFERENCES person(name),
        author_id INTEGER REFERENCES person(person_id),
        author_display_name TEXT NOT NULL REFERENCES person(display_name),
        date_posted DATE NOT NULL,
        last_updated DATE,
        tags TEXT,
        html TEXT NOT NULL,
        UNIQUE(blog_post_id, author_id)
    );
"""

blog_post_insert = """
    INSERT (blog_post_id, title, content, author, author_id, 
    author_display_name, date_posted, last_updated, tags, html)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?); 
"""

blog_post_get = """ SELECT * FROM blog_post WHERE blog_post_id = ? """

blog_post_delete = """ DELETE FROM blog_post_id WHERE blog_post_id = ? """
