# ptsqld

You suffered torment setting up SQL Database... You fear the day you will have to setup storage connect it to an engine ... maintain it...
Fear no more... It is now as easy as setting up a git repository... No daemon server required everything is now decentralized ... distributes...

All that available through Python DB API 2.0 interface ... wow ...

# Usage

First create a git repository (you could use dulwich (heart))
```sh
git init {path to my database}
```

```python
from ptsqld import connect

connection = connect(path_to_my_database)

cursor = connection.cursor()

cursor.execute("create table jokes (Name, Description)")
cursor.execute("insert into jokes (Name, Description) values ('Good', 'One'), ('Bad', 'One')")

connection.commit()
```

Then look the logs of your git repository :).