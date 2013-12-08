insolater
=========

A simple version control system for small personal projects.
insolater has an easy to use interface to save, open, and transfer versions
of your work.

TODO
--------
  - Allow updates to the original version
  - Merging

Examples
-------
In a python script:
```python
  import insolater
  insolater.init()
  insolater.save_version('v1')
  insolater.change_version('v1')
  # Modify some files
  insolater.push_version('user@host:path_to_dir_for_version')
  insolater.pull_version('user@host:path_to_dir_for_version', 'pulled_ver')
  insolater.current_version()
  insolater.change_version('original')
  # Changes are not present.
  insolater.change_version('pulled_ver')
  # Changes are back.
  insolater.delete_version('v1')
  insolater.all_versions()
  insolater.exit(True)
  # .insolater_repo is deleted and files are in their original condition.
````

Running from command line:
```
~/test $ ls *
fa  fb

d:
fa  fc
~/test $ inso init
Initialized repository with versions: original
~/test $ inso list
* original
~/test $ echo data > f
~/test $ rm fb
~/test $ echo data >> fa
~/test $ echo data >> d/fa
~/test $ inso save changes
is_version() takes exactly 2 arguments (1 given)
~/test $ ls *
f  fa

d:
fa  fc
~/test $ inso open original
Switched to original
~/test $ ls *
fa  fb

d:
fa  fc
~/test $ cat fa
old data a
~/test $ cat d/fa
old data da
~/test $ inso open changes
Version not found: changes
~/test $ ls *
fa  fb

d:
fa  fc
~/test $ cat fa
old data a
~/test $ cat d/fa
old data da
~/test $ cat f
cat: f: No such file or directory
~/test $ ls ~/test_changes
~/test $ inso save changes2
is_version() takes exactly 2 arguments (1 given)
~/test $ inso list
* original
~/test $ inso open changes
Version not found: changes
~/test $ inso rm changes2
Version not found: changes2
~/test $ inso list
* original
~/test $ inso push $USER@localhost:~/test_changes/
user@localhost's password:
fa    transfered
d     transfered
fb    transfered

~/test $ inso exit
Do you want to discard all changes (y/[n]): y
Session Ended
~/test $ ls ../test_changes/ ../test_changes/d
../test_changes/:
d  fa  fb

../test_changes/d:
fa  fc
~/test $ ls *
fa  fb

d:
fa  fc
~/test $ cat d/fa
old data da
~/test $ inso init $USER@localhost:~/test_changes/
user@localhost's password: 
Initialized repository with versions: original
~/test $ ls *
fa  fb

d:
fa  fc
~/test $ cat d/fa
old data da
~/test $ inso exit
Do you want to discard all changes (y/[n]): y
Session Ended
~/test $ cat d/fa
old data da

````
