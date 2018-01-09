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
To add a task, there is two ways by using `a` or `add`:
- using the command: 

```
pytodo> a this is a new task
Task added.

pytodo> _
```
will add a new task with `this is a new task` as topic.
- Using the command prompt:

```
pytodo> a
Please specify a description: 
> This is a new task
Task added.

pytodo> _
```

### Help
Display help with `h` or `help`. The display will be:
```
pytodo> h

Available commands:
	- add a new task .......... add [desc]
	- pass the task to done ... done [undo] id
	- list all tasks .......... list 
	- remove task ............. remove (all | id)
	- rename a task ........... modif id new_name
	- reset pytodo ............ reset 
	- displays help ........... help 
	- quit pytodo cli ......... quit 

Shortcuts:
	- add    -> a 
	- done   -> d 
	- list   -> l 
	- remove -> rm 
	- modif  -> m 
	- reset  -> rs 
	- help   -> h 
	- quit   -> q 

pytodo> _
```
### List
Lists all existing tasks and their state. Use `l` or `list` to display that list.
```
pytodo> l
Registered task(s):
	[x] (1) task 1
	[ ] (2) task 2
	[ ] (3) task 3

pytodo> _
```
### Quit
Exit pytodo with `q` or `quit`.
### Remove
To remove one task, use `rm id` (or `remove id` )where `id` is the id of the task you want to remove.

Considering the tasks in the [example for list](#List):
```
pytodo> rm 1
Task removed.

pytodo> l
Registered task(s):
	[ ] (2) task 2
	[ ] (3) task 3

pytodo> _
```

To remove all tasks, specify `all` instead of an id:
```
pytodo> rm all 
Do you really want to delete all tasks?
(y/n) > y
Tasks removed.

pytodo> l
No task planified yet, add one with /a

pytodo> _
```
### Rename
To rename one task, use `m id topic` (or `modif id topic`) where `id` is the id of the task you want to rename and `topic` its new content.

Considering the tasks in the [example for list](#List):
```
pytodo> m 3 task 3 renamed
Task renamed.

pytodo> l
Registered task(s):
	[x] (1) task 1
	[ ] (2) task 2
	[ ] (3) task 3 renames

pytodo> _
```
### Reset
You can delete all your informations using `rs` or `reset`. It will delete all your tasks and your profile
```
pytodo> rs
Are you sure ?
(y/n) > y
Please verify your identity: 
Name> test
Password> 

Deleting data...
Success.
```
### Toggle
To mark a task as done, use `d id` or `done id` where `id` is the id of the task you want to mark as done.
Considering the tasks in the [example for list](#List):
```
pytodo> d 2
Task status changed.

pytodo> l
Registered task(s):
	[x] (1) task 1
	[x] (2) task 2
	[ ] (3) task 3

pytodo> _
```

To mark a task as not done, just revert it with `d undo id` (same with `done`) where `id` is the id of the task you want to mark as not done.
Considering the tasks in the [example for list](#List):
```
pytodo> d undo 1
Task status changed.

pytodo> l
Registered task(s):
	[ ] (1) task 1
	[ ] (2) task 2
	[ ] (3) task 3

pytodo> _
```
