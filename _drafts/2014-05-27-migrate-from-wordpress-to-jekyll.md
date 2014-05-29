---
layout: post
title: "Migrate From Wordpress to Jekyll With Github Pages"
description: ""
category: 
tags: []
---
{% include JB/setup %}
We decided to move away from Wordpress to Jekyll. There are many guides on the process and also a lot of reasons as well. Check out some posts on the process already:

- [Migrating from WordPress.com to Jekyll](http://hadihariri.com/2013/12/24/migrating-from-wordpress-to-jekyll/)
- [How-to: Migrating Blog from WordPress to Jekyll, and Host on Github](http://girliemac.com/blog/2013/12/27/wordpress-to-jekyll/)
- [Migrating My Blog from WordPress to Jekyll](http://juliemao.com/blog/2013/07/migrating-from-wordpress-to-jekyll/)
- [How to Migrate from WordPress to Jekyll Running on Github](http://johnnycode.com/2012/07/10/how-to-migrate-from-wordpress-to-jekyll-running-on-github/)

Here are the steps to the process.

### 1. Prepare Github
Most of the steps are covered in [GitHub Pages](https://pages.github.com/). First go and create your self an account on github.com:

![github-account-creation](github-account-creation.png)

For the plan you can choose free:

![github-plan-free](github-plan-free.png)

After you done with the creation it will take you to your github account:

![github-account-created-login-page](github-account-created-login-page.png)

After the account we have to create a repository with a special name. From [Using Jekyll with Pages](https://help.github.com/articles/using-jekyll-with-pages):

> Using Jekyll
> 
> Every GitHub Page is run through Jekyll when you push content to a specially named branch within your repository. For User Pages, use the master branch in your **username.github.io** repository. For Project Pages, use the **gh-pages** branch in your project's repository. Because a normal HTML site is also a valid Jekyll site, you don't have to do anything special to keep your standard HTML files unchanged. Jekyll has thorough documentation that covers its features and usage. Simply start committing Jekyll formatted files and you'll be using Jekyll in no time.

So let's go ahead and create a repository with name of **username**.github.io. First select "Create New Repository" from the top:

![create-new-repo-github](create-new-repo-github.png)

Then name it appropriately:

![github-new-repo-name](github-new-repo-name.png)

After it's created, you will see quick instructions on how to initialize the git repository:

![github-initialization-instruct](github-initialization-instruct.png)

After it's done, go to settings of the repository and check the box that says "Restrict editing to collabolators only":

![github-restrict-editting](github-restrict-editting.png)

So let's clone the repository and add a test home page:

	elatov@ccl:~$git clone https://moxz1@github.com/moxz1/moxz1.github.io.git
	Initialized empty Git repository in /home/elatov/moxz1.github.io/.git/
	Password:
	warning: You appear to have cloned an empty repository.
	elatov@ccl:~$cd moxz1.github.io/
	elatov@ccl:~/moxz1.github.io$echo "Test Page" > index.html
	elatov@ccl:~/moxz1.github.io$git add --all
	elatov@ccl:~/moxz1.github.io$git commit -m "Initial Commit"
	[master (root-commit) 197ba87] Initial Commit
	 Committer: elatov <elatov@ccl.local.com>
	Your name and email address were configured automatically based
	on your username and hostname. Please check that they are accurate.
	You can suppress this message by setting them explicitly:
	
	    git config --global user.name "Your Name"
	    git config --global user.email you@example.com
	
	If the identity used for this commit is wrong, you can fix it with:
	
	    git commit --amend --author='Your Name <you@example.com>'
	
	 1 files changed, 1 insertions(+), 0 deletions(-)
	 create mode 100644 index.html
	elatov@ccl:~/moxz1.github.io$git push origin master
	Password:
	Counting objects: 3, done.
	Writing objects: 100% (3/3), 219 bytes, done.
	Total 3 (delta 0), reused 0 (delta 0)
	To https://moxz1@github.com/moxz1/moxz1.github.io.git
	 * [new branch]      master -> master
	 
Now if you look back on the setting page of the repository, it will let you know that your changes have been published:

