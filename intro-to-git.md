# Intro to Git

## The basics

`git add [file_name]` This command is used to add a particular file to the staging directory, from the working directory. The working directory is the folder you create the git file in, and the staging directory is the intermediate area before you commit any changes to the local repository.

`git commit` This command is used to commit any changes made to the branch you are on currently, to the local repository.

`git checkout [branch_name]` This command is used to move to the `[branch_name]`. It can be used with the `-b` modifier to create a new branch and move to it in one command, like so: `git checkout -b [branch_name]`. You are now on your new branch.

`git log` This command is used to check commit history in the branch you are in.

`git status` This command is used to check the current status of files in the staging directory, if any files are checked or unchecked etc.

## Beyond the basics

`git pull [online_repository_name]` This command lets you pull all the files from an online repository to a local repository that you can edit yourself.

`git push [branch_name] [online_name]` This command lets you push a branch from a local repository to an online repository.

`gitignore` This is a file that git will ignore when pushing files to an online repository, and is good to use anything you don't want the general public seeing, such as keys, hashes or credentials.

`git merge [branch_to_merge_from] [branch_to_merge_to]` This command is used to merge two branches together, and the order matters - the first branch will be merged into the second branch.
