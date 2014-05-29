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
	 
Now if you look back on the **settings** page of the repository, it will let you know that your changes have been published:

![site-is-published-github-settings](site-is-published-github-settings.png)

If you want you can update your git user configuration to reflect your username. And you can also use SSH keys instead regular password over https to do commits to the github repository. More information on how to configure the SSH keys are seen in [Generating SSH Keys](https://help.github.com/articles/generating-ssh-keys). 

After sometime if you visit your user github page you will see the contents of the index.html file that you uploaded:

![test-page-seen-from-github](test-page-seen-from-github.png)

### Running Jekyll Locally
I was using a mac for my testing, so I decided to run **jekyll** locally. MacOSX comes with a ruby version but I didn't want to mess with the system version. I already had **macports** setup on the mac ([here](/2013/07/mount-various-file-system-with-autofs-on-mac-os-x-mountain-lion/) is a post for the macports setup). Once you have macports, you can run the following to install the **ruby** version from macports:

	sudo port install ruby19

Then create a symbolic link to ease the ruby usage:

	sudo ln -s /opt/local/bin/ruby1.9 /opt/local/bin/ruby

Next install the **ruby-gems**

	sudo port install rb-rubygems

Then fix the path for that as well:

	sudo ln -s /opt/local/bin/gem1.9 /opt/local/bin/gem

When you install *macports*, it includes **/opt/local/bin/** in the path prior to other locations. Make sure the **gem** and **ruby** versions by default are the macports one:

	elatov@kmac:~$type -a gem
	gem is /opt/local/bin/gem
	gem is /usr/bin/gem
	elatov@kmac:~$type -a ruby
	ruby is /opt/local/bin/ruby
	ruby is /usr/bin/ruby

Now let's update the system gems:

	elatov@kmac:~$sudo gem update --system
	Updating rubygems-update
	Fetching: rubygems-update-2.2.2.gem (100%)
	Successfully installed rubygems-update-2.2.2
	Installing RubyGems 2.2.2
	RubyGems 2.2.2 installed
	Installing ri documentation for rubygems-2.2.2
	
	= 2.2.1 / 2014-01-06

Then install the **rdoc** gem before the jekyll install:

	sudo gem install rdoc

Lastly go ahead and install **jekyll**

	sudo gem install jekyll

#### Jekyll Structure
From [Directory structure](http://jekyllrb.com/docs/structure/):

> A basic Jekyll site usually looks something like this:
> 
> 	.
> 	├── _config.yml
> 	├── _drafts
> 	|   ├── begin-with-the-crazy-ideas.textile
> 	|   └── on-simplicity-in-technology.markdown
> 	├── _includes
> 	|   ├── footer.html
> 	|   └── header.html
> 	├── _layouts
> 	|   ├── default.html
> 	|   └── post.html
> 	├── _posts
> 	|   ├── 2007-10-29-why-every-programmer-should-play-nethack.textile
> 	|   └── 2009-04-26-barcamp-boston-4-roundup.textile
> 	├── _data
> 	|   └── members.yml
> 	├── _site
> 	└── index.html
>
> An overview of what each of these does:
>
> | FILE / DIRECTORY|	DESCRIPTION|
> |:----------------|:-----------|
> | _config.yml     | Stores **configuration** data. Many of these options can be specified from the command line executable but it’s easier to specify them here so you don’t have to remember them.|
> | _drafts         | Drafts are unpublished posts. The format of these files is without a date: **title.MARKUP**. Learn how to work with drafts.
> | _includes       | These are the partials that can be mixed and matched by your layouts and posts to facilitate reuse. The liquid tag  `{% include file.ext %}` can be used to include the partial in  **_includes/file.ext**.
> | _layouts        | These are the templates that wrap posts. Layouts are chosen on a post- by-post basis in the YAML front matter, which is described in the next section. The liquid tag  `{{ content }}` is used to inject content into the web page.
> | _posts          | Your dynamic content, so to speak. The naming convention of these files is important, and must follow the format: **YEAR-MONTH-DAY-title.MARKUP**. The permalinks can be customized for each post, but the date and markup language are determined solely by the file name.|
> | _data           | Well-formatted site data should be placed here. The jekyll engine will autoload all yaml files (ends with **.yml** or **.yaml**) in this directory. If there's a file members.yml under the directory, then you can access contents of the file through **site.data.members**.|
> | _site           | This is where the generated site will be placed (by default) once Jekyll is done transforming it. It’s probably a good idea to add this to your **.gitignore** file.
> | index.html and other HTML, Markdown, Textile files | Provided that the file has a YAML Front Matter section, it will be transformed by Jekyll. The same will happen for any **.html**, **.markdown**,  **.md**, or **.textile** file in your site’s root directory or directories not listed above.|
> | Other Files/Folders   | Every other directory and file except for those listed above—such as **css** and **images** folders,  **favicon.ico** files, and so forth—will be copied verbatim to the generated site. There are plenty of sites already using Jekyll if you’re curious to see how they’re laid out.|

#### Jekyll Bootstrap
Most people just take a copy of an existing blog and go from there, since you don't really want to create the above layout by hand. A lot of jekyll powered sites are listed in [Jekyll Sites](https://github.com/jekyll/jekyll/wiki/Sites). If you like one just clone it. To get started with a Jekyll site, there is a a project called [JekyllBootstrap](http://jekyllbootstrap.com/). It basically eases the process of managing a Jekyll site. To create the first jekyll site, check out the instructions laid out in [Jekyll QuickStart](http://jekyllbootstrap.com/usage/jekyll-quick-start.html). So let's try it out, first let's clone their github repo:

