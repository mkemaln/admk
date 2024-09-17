<!DOCTYPE html>
<html>
<head>
    <title>Add New User</title>
</head>
<body>
    <button><a href="index2.php">login</a></button>
    <form action="add_users.php" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>
        <input type="submit" value="Add User">
    </form>
</body>
</html>
