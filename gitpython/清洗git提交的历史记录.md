## 删除指定文件的历史提交记录

用于清洗提交记录。
```
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch {dir/file}' --prune-empty --tag-name-filter cat -- --all
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now
git gc --aggressive --prune=now
git push --force --verbose --dry-run origin refs/heads/{branch}:refs/heads/{branch} 
git push --force origin refs/heads/{branch}:refs/heads/{branch} 
```