DROP TABLE IF EXISTS requests;

CREATE TABLE requests (
    id INTEGER PRIMARY KEY, 
    FileName FILESTREAM,
    Mail TEXT,
    Algorithm TEXT
    
);

