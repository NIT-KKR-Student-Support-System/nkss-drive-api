from dataclasses import dataclass
import psycopg2


@dataclass
class File:
    name: str
    link: str
    tags: list[str]


def list_files(tags: list[str]) -> list[File]:
    """
    List files in database that have the tags.
    """
    cur = _conn.cursor()
    if tags:
        query = f"""
            select f.name, f.link, array_agg(t.name) as tags
            from (
                select ft.fid
                from file_tags ft
                where ft.tid in (select tid from tags where name = ANY(%s))
                group by ft.fid
                having count(ft.tid) = (%s)
            ) as f1
            join files f on f.fid = f1.fid
            join file_tags ft on f.fid = ft.fid
            join tags t on ft.tid = t.tid
            group by f.fid, f.name, f.link;
        """
        cur.execute(query, [tags, len(tags)])
    else:
        query = f"""
            select f.name, f.link, array_agg(t.name) as tags
            from files f
            join file_tags ft on f.fid = ft.fid
            join tags t on ft.tid = t.tid
            group by f.fid;
        """
        cur.execute(query)

    results = cur.fetchall()
    return [File(name, link, tags) for name, link, tags in results]


def add_files(files: list[File]):
    """
    Add files to database.
    """
    cur = _conn.cursor()
    
    for file in files:
        query1 = "INSERT INTO files(name, link) VALUES (%s, %s) RETURNING fid"
        cur.execute(query1, [file.name, file.link])
        fid = cur.fetchone()[0]

        for tag in file.tags:
            tid = get_tagid_or_insert(cur, tag)
            query2 = "INSERT INTO file_tags(tid,fid) VALUES (%s, %s)"
            cur.execute(query2, [tid, fid])

    _conn.commit()

def get_tagid_or_insert(cur, tag: str) -> int:
    """
    Caller needs to commit to the database.
    """
    query = "SELECT tid FROM tags WHERE name = %s"
    cur.execute(query, [tag])
    tid = cur.fetchone()
    if tid is None:
        query = "INSERT INTO tags(name) VALUES (%s) RETURNING tid"
        cur.execute(query, [tag])
        tid = cur.fetchone()[0]
    else:
        tid = tid[0]

    return tid  



# export PGHOST, PGPORT, PGUSER, PGDATABASE in the shell
_conn = psycopg2.connect()
