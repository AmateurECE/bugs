# The Stupid Bug Tracker #

This tools is based off of [t](https://github.com/sjl/t). It searches the
current git repository (and all subdirectories) for `TODO` comments in code. It
then puts these comments into a file in the top level directory of the
repository with the name `bugs`. It matches C/C++, LaTeX, and Bash style `TODO`
comments of the form:

```
(%|#|/(\*|/))\s*TODO:\s*(.*)
```

When run without any arguments, it prints the bugs in the `bugs` file in the
top level directory of the current git repository. If the current working
directory is not in a git repository, `bugs.py` exits with an error. When run
with `update` as the first argument, `bugs.py` will update the `bugs` file in
the top level directory of the git repository containing the current working
directory to contain the most up-to-date index of bugs.

```
bugs.py [update]
```

The script will not index `TODO` comments in the `.git/` directory by default,
nor any files listed in the `.gitignore` (if it exists). If this is not enough
control, the user may also have a file with the name `.bignore` in the top
level directory of the git repository containing the current working directory
that contains a list of more files and directories to ignore.

I have it aliased to just `b` in my shell. It's a pretty neat tool, and it
plays nicely with [Sysgit](https://github.com/AmateurECE/Sysgit).