wget https://cdn.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip
unzip chinook.zip
echo .dump | sqlite3 chinook.db > chinook.sql