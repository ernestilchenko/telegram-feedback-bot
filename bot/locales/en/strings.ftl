cmd-start=Hello { $name }! Send me a message and I'll forward it to the administrator.
sent-confirmation = Message sent!

user-info =
    Name: { $name }
    ID: { NUMBER($id, useGrouping: 0) }
    Username: { $username }

user-banned = ID { NUMBER($id, useGrouping: 0) } added to the banned list. When attempting to send a message, the user will receive a notification that they are blocked.
user-banned = ID { NUMBER($id, useGrouping: 0) } added to the banned list. When attempting to send a message, the user will receive a notification that they are blocked.
user-unbanned = ID { NUMBER($id, useGrouping: 0) } unblocked.
