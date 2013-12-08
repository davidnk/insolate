insolater
=========

A simple version control system.


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
  insolater.new_version('v1')
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
  ~/test $ rm b
  rm: cannot remove ‘b’: No such file or directory
  ~/test $ echo data >> fa
  ~/test $ echo data >> d/fa
  ~/test $ inso new changes
  Version changes created and opened
  ~/test $ ls *
  f  fa  fb

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
  Switched to changes
  ~/test $ ls *
  f  fa  fb

  d:
  fa  fc
  ~/test $ cat fa
  old data a
  data
  ~/test $ cat d/fa
  old data da
  data
  ~/test $ cat f
  data
  ~/test $ ls ~/test_changes
  ~/test $ inso new changes2
  Version changes2 created and opened
  ~/test $ inso list
    original
  * changes2
    changes
  ~/test $ inso open changes
  Switched to changes
  ~/test $ inso rm changes2
  Version changes2 deleted
  ~/test $ inso list
    original
  * changes
  ~/test $ inso push $USER@localhost:~/test_changes/
  user@localhost's password:
  f     transfered
  fa    transfered
  d     transfered
  fb    transfered

  ~/test $ inso exit
  Do you want to discard all changes (y/[n]): y
  Session Ended
  ~/test $ ls ../test_changes/ ../test_changes/d
  ../test_changes/:
  d  f  fa  fb

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
  f  fa  fb

  d:
  fa  fc
  ~/test $ cat d/fa
  old data da
  data
  ~/test $ inso exit
  Do you want to discard all changes (y/[n]): y
  Session Ended
  ~/test $ cat d/fa
  old data da
````
