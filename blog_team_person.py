""" Import either ones to main for usage. """

team = """ 
    CREATE TABLE IF NOT EXISTS team (
        resource_id INTEGER PRIMARY KEY REFERENCES resources(resource_id) ON DELETE CASCADE,         
        name TEXT NOT NULL,
        member INTEGER NOT NULL,
        displayname TEXT NOT NULL,
        FOREIGN KEY (member) REFERENCES person(person_id),
        UNIQUE(resource_id)
    );
"""

person = """ 
    CREATE TABLE IF NOT EXISTS person (
        resource_id INTEGER PRIMARY KEY REFERENCES resources(resource_id) ON DELETE CASCADE,
        person_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        fullname TEXT NOT NULL,
        url TEXT NOT NULL,
        picture_url TEXT,
        team TEXT NOT NULL REFERENCES team(name),
        UNIQUE(resource_id, person_id)
    );
"""

blog_post = """ 
    CREATE TABLE IF NOT EXISTS blog_post (
        resource_id INTEGER PRIMARY KEY REFERENCES resources(resource_id) ON DELETE CASCADE,     
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author TEXT NOT NULL REFERENCES person(name),
        author_id INTEGER REFERENCES person(person_id),
        author_displayname TEXT NOT NULL REFERENCES person(displayname),
        date_posted DATE NOT NULL,
        last_updated DATE NOT NULL,
        tags TEXT,
        html TEXT NOT NULL,
        UNIQUE(resource_id, author_id)
    );
"""