1.这个文件夹已经和远程仓库对应的 gevent_img_downloader 相关联
2.这个文件夹创建的时候使用 git init 创建一个全新的分支，不会受到父文件夹 git 的影响
3.这个文件夹的主分支是master，父文件夹git的主分支也是master，两个是相互独立的
4.如果这个文件夹后续有文件更新，那么就直接执行步骤：
（1）git add 新文件
（2）git commit -m 本次提交命名
（3）git push origin master  # 可以直接推送到GitHub仓库的主分支中
