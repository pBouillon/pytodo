# Pytodo
Small Todo list in terminal.

## First run
On the first run, pytodo will create your profile, you will be able to delete it later.
```
It seems that no users are registered 
Do you want to sign in ?
(y/n) > y

Please enter your informations: 
Name> test
Password> 
Repeat password> 

--- SUCCESSFULLY CONNECTED ---

pytodo> _
```

## Options
* [add new task](#add)
* [help](#help)
* [list all tasks](#list)
* [quit](#quit)
* [remove a task](#remove)
* [rename a task](#rename)
* [reset pytodo](#reset)
* [toggle task status](#toggle)

### Add
To add a task, there is two ways:
- using the command: 

```
pytodo> /a this is a new task
Task added.

pytodo> _
```
will add a new task with `this is a new task` as topic.
- Using the command prompt:

```
pytodo> /a
Please specify a description: 
> This is a new task
Task added.

pytodo> _
```

### Help
Display help with `/h`. The display will be:
```
pytodo> /h

Available commands:
	- add a new task .......... /a [desc]
	- pass the task to done ... /d [undo] id
	- list all tasks .......... /l 
	- remove task ............. /rm all | id
	- rename a task ........... /m id new_name
	- reset pytodo ............ /rs
	- displays help ........... /h
	- quit pytodo cli ......... /q

pytodo> _
```
### List
Lists all existing tasks and their state. Use `/l` to display that list.
```
pytodo> /l
Registered task(s):
	[x] (1) task 1
	[ ] (2) task 2
	[ ] (3) task 3

pytodo> _
```
### Quit
Exit pytodo with `/q`.
### Remove
To remove one task, use `/rm id` where `id` is the id of the task you want to remove.

Considering the tasks in the [example for list](#List):
```
pytodo> /rm 1
Task removed.

pytodo> /l
Registered task(s):
	[ ] (2) task 2
	[ ] (3) task 3

pytodo> _
```

To remove all tasks, specify `all` instead of an id:
```
pytodo> /rm all 
Do you really want to delete all tasks?
(y/n) > y
Tasks removed.

pytodo> /l
No task planified yet, add one with /a

pytodo> _
```
### Rename
To remove one task, use `/m id topic` where `id` is the id of the task you want to rename and `topic` its new content.

Considering the tasks in the [example for list](#List):
```
pytodo> /m 3 task 3 renamed
Task renamed.

pytodo> /l
Registered task(s):
	[x] (1) task 1
	[ ] (2) task 2
	[ ] (3) task 3 renames

pytodo> _
```
### Reset
You can delete all your informations using `/rs`. It will delete all your tasks and your profile
```
pytodo> /reset
Unhandled command type /h for help
pytodo> /rs
Are you sure ?
(y/n) > y
Please verify your identity: 
Name> test
Password> 

Deleting data...
Success.
```
### Toggle
To mark a task as done, use `/d id ` where `id` is the id of the task you want to mark as done.
Considering the tasks in the [example for list](#List):
```
pytodo> /d 2
Task status changed.

pytodo> /l
Registered task(s):
	[x] (1) task 1
	[x] (2) task 2
	[ ] (3) task 3

pytodo> _
```

To mark a task as not done, just revert it with `/d undo id` where `id` is the id of the task you want to mark as not done.
Considering the tasks in the [example for list](#List):
```
pytodo> /d undo 1
Task status changed.

pytodo> /l
Registered task(s):
	[ ] (1) task 1
	[ ] (2) task 2
	[ ] (3) task 3

pytodo> _
```




