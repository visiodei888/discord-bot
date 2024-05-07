# Discord Bot Implementation

This Discord bot implementation utilizes the Discord.py library to perform various tasks on a Discord server. The project is structured to ensure efficiency, maintainability, and adherence to best practices.

## Tasks Overview

### Task 1 - Welcome Card Implementation

The welcome card implementation sends a welcome message in a specific channel and initiates a direct message to new members joining the server.

**Key Steps:**
1. Set up the Discord.py bot and connect it to the Discord server.
2. Implement an event handler for the `on_member_join` event.
3. Send a welcome message in a designated channel using the `send` method when a new member joins.
4. Initiate a direct message to the new member using the `send` method.

### Task 2 - Word Counting

This task involves counting each word sent to a guild and displaying the most used words using commands. Additionally, it implements a command to show the most used words by a specific user.

**Key Steps:**
1. Set up a MySQL database.
2. Create a table named 'user_words' with columns 'discord_id' and 'word'.
3. Implement an event handler for `on_message` to extract and store words along with the sender's user ID.
4. Implement commands:
   - `/word-status`: Displays the 10 most used words.
   - `/user-status <user>`: Displays the 10 most used words by the specified user.

### Task 3 - User Role Selection Implementation

This task allows users to select their roles via a select menu using the Discord.py library.

**Key Steps:**
1. Create a table named "user_role" with columns 'discord_id' and 'role'.
2. Implement a slash command `/select-role` to send a message with a select menu containing available roles.
3. Upon selection, update the user's role in the database and grant the selected role to the user on Discord.

## Error Handling and Best Practices

The implementation ensures error handling for potential exceptions that may occur during the process, such as database connection issues or Discord API rate limits. Meaningful error messages are provided to users when something goes wrong.

## Repository Link

The project repository can be found [here](#).
