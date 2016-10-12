# Let-s-Go
Let's Go


## Code

1. use pyvenv-3.5 to develop: `pyvenv-3.5 None && cd None && source bin/activate`, on the head of shell line there is `(None)`
2. do as follow **Fetch and Push**
3. pre check your code before push: `cd Let-s-Go && tox`(tox should run in **pyvenv**)
4. if you get `congratulations :)` finally, you can push it to your repo and create a pull request; or please modify your code with reference to the error message

## Fetch and Push

1. fork from NoneGroupTeam: `https://github.com/NoneGroupTeam/Let-s-Go`
2. clone from your forked repo: `git clone git@github.com:[username]/Let-s-Go.git`
or `git clone https://github.com/[username]/Let-s-Go.git`
3. create branch for what you will do: `git checkout -b [branch_name]`
4. add remote repo: `git remote add [remote_name] git@github.com:NoneGroupTeam/Let-s-Go.git`, then you can `git remote -v` to check repos updater
5. fetch and merge from remote: `git pull [remote_name] [branch_name]` or you can do setp by step: `git [remote_name] [branch_name]; git diff;  git merge`
6. add changes: `git add [your_files]`
7. commit and write commit line: `git commit`
8. push `git push --set-upstream origin [branch_name]; git push`
9. create pull request on github page and check if it pass the ai test
