insolater
=========

Easily switch between original and modified versions of a directory.


Warnings
--------
This project is still in its early stages and some features are not ideal.
General rule: If something goes wrong DO NOT run 'insolate.exit()' or 'inso exit'

Problems you may encounter include:
  - Changes made in ORIG version are discarded when changing versions.
    - If this happens and you lose important changes DO NOT run 'insolate.exit()'
      or 'inso exit'.  The changes are not perminantly lost until you do.
    - To recover the changes run 'insolater.cd("master")' or 'inso cd master', then save
      the changes to a location outside of the directory before using the exit command.
  - Changes cannot be merged into the original version yet, so if you don't have a remote
    host to store them on, you'll need to either: move them outside of the directory by hand
    OR run 'inso push $USER@localhost:~/path_from_home_dir_to_backup_location'
    - make sure not to backup changes into the insolated directory or they will be removed
      on exit.
  - Deleting a file, sending changes elsewhere, then restoring changes will not re-delete
    the file.

Examples
-------
In a python script:
```python
  import insolate
  
  insolater.init()
  #returns (True, 'Initialized versions ORIG, CHANGES')
  
  insolater.cd('CHANGES')
  #returns (True, 'Switched to CHANGES')

  ... changes to files ...

  insolater.cd('ORIG')
  #returns (True, 'Switched to ORIG')
  #directory now has its original state except for the .insolater_repo

  insolater.cd('CHANGES')
  #returns (True, 'Switched to CHANGES')
  #back to the modified copy

  insolater.push('user@host:path_to_dir_for_changes')
  #returns (True, '<transfered files>')

  insolater.exit(discard_changes=True)
  #returns (True, 'Session Ended')

  insolater.init('user@host:path_to_dir_for_changes')
  #returns (True, 'Initialized versions ORIG, CHANGES')
  #directory is in modified state

  insolater.cd('ORIG')
  #returns (True, 'Switched to ORIG')
  #directory now has its original state except for the .insolater_repo

  insolater.exit('user@host:path_to_dir_for_changes')
  #returns (True, '<transfered files>\nSession Ended')
````

Running from command line:
```
  ~/test $ ls *
  a  b

  d:
  a  c
  ~/test $ inso init
  Initialized versions ORIG, CHANGES
  ~/test $ inso pwd
  Currently in CHANGES version.
  ~/test $ echo 'data' >> f
  ~/test $ rm b
  ~/test $ echo 'data' >> a
  ~/test $ echo 'other' >> d/a
  ~/test $ ls *
  a  f

  d:
  a  c
  ~/test $ inso cd ORIG
  Switched to ORIG
  ~/test $ ls *
  a  b

  d:
  a  c
  ~/test $ cat a
  old data a
  ~/test $ cat d/a
  old data d/a
  ~/test $ inso cd CHANGES
  Switched to CHANGES
  ~/test $ ls *
  a  f

  d:
  a  c
  ~/test $ cat a
  old data a
  data
  ~/test $ cat d/a
  old data d/a
  other
  ~/test $ cat f
  data
  ~/test $ ls ../test_changes/
  ~/test $ inso exit $USER@localhost:~/test_changes/
  name@localhost's password:
  a               transfered
  b               transfered
  d/a             transfered
  f               transfered
  Session Ended
  ~/test $ ls ../test_changes/*
  ../test_changes/a  ../test_changes/f

  ../test_changes/d:
  a
  ~/test $ ls *
  a  b

  d:
  a  c
  ~/test $ cat d/a
  old data d/a
  ~/test $ inso init $USER@localhost:~/test_changes/
  name@localhost's password:
  Initialized versions ORIG, CHANGES
  ~/test $ ls *
  a  b  f

  d:
  a  c
  ~/test $ cat d/a
  old data d/a
  other
  ~/test $ inso exit
  Do you want to discard changes (y/[n]): y
  Session Ended
  ~/test $ cat d/a
  old data d/a
````
