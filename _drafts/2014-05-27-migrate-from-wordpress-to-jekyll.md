---
layout: post
title: "Migrate From Wordpress to Jekyll With Github Pages"
description: ""
category: 
tags: []
---
We decided to move away from Wordpress to Jekyll. There are many guides on the process and also a lot of reasons as well. Check out some posts on the process already:

- [Migrating from WordPress.com to Jekyll](http://hadihariri.com/2013/12/24/migrating-from-wordpress-to-jekyll/)
- [How-to: Migrating Blog from WordPress to Jekyll, and Host on Github](http://girliemac.com/blog/2013/12/27/wordpress-to-jekyll/)
- [Migrating My Blog from WordPress to Jekyll](http://juliemao.com/blog/2013/07/migrating-from-wordpress-to-jekyll/)
- [How to Migrate from WordPress to Jekyll Running on Github](http://johnnycode.com/2012/07/10/how-to-migrate-from-wordpress-to-jekyll-running-on-github/)

Here are the steps to the process.

### Prepare Github
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
> | _includes       | These are the partials that can be mixed and matched by your layouts and posts to facilitate reuse. The liquid tag  `{\% include file.ext %}` can be used to include the partial in  **_includes/file.ext**.
> | _layouts        | These are the templates that wrap posts. Layouts are chosen on a post- by-post basis in the YAML front matter, which is described in the next section. The liquid tag  `{{ content }}` is used to inject content into the web page.
> | _posts          | Your dynamic content, so to speak. The naming convention of these files is important, and must follow the format: **YEAR-MONTH-DAY-title.MARKUP**. The permalinks can be customized for each post, but the date and markup language are determined solely by the file name.|
> | _data           | Well-formatted site data should be placed here. The jekyll engine will autoload all yaml files (ends with **.yml** or **.yaml**) in this directory. If there's a file members.yml under the directory, then you can access contents of the file through **site.data.members**.|
> | _site           | This is where the generated site will be placed (by default) once Jekyll is done transforming it. It’s probably a good idea to add this to your **.gitignore** file.
> | index.html and other HTML, Markdown, Textile files | Provided that the file has a YAML Front Matter section, it will be transformed by Jekyll. The same will happen for any **.html**, **.markdown**,  **.md**, or **.textile** file in your site’s root directory or directories not listed above.|
> | Other Files/Folders   | Every other directory and file except for those listed above—such as **css** and **images** folders,  **favicon.ico** files, and so forth—will be copied verbatim to the generated site. There are plenty of sites already using Jekyll if you’re curious to see how they’re laid out.|

#### Jekyll Bootstrap
Most people just take a copy of an existing blog and go from there, since you don't really want to create the above layout by hand. A lot of jekyll powered sites are listed in [Jekyll Sites](https://github.com/jekyll/jekyll/wiki/Sites). If you like one just clone it. To get started with a Jekyll site, there is a a project called [JekyllBootstrap](http://jekyllbootstrap.com/). It basically eases the process of managing a Jekyll site. To create the first jekyll site, check out the instructions laid out in [Jekyll QuickStart](http://jekyllbootstrap.com/usage/jekyll-quick-start.html). So let's try it out, first let's clone their github repo:

	elatov@kmac:~$git clone https://github.com/plusjade/jekyll-bootstrap.git
	Cloning into 'jekyll-bootstrap'...
	remote: Reusing existing pack: 2062, done.
	remote: Total 2062 (delta 0), reused 0 (delta 0)
	Receiving objects: 100% (2062/2062), 811.25 KiB | 0 bytes/s, done.
	Resolving deltas: 100% (790/790), done.
	Checking connectivity... done.

Now let's build and serve that jekyll-bootstrap template locally:

	elatov@kmac:~$cd jekyll-bootstrap/
	elatov@kmac:~/jekyll-bootstrap$jekyll serve -w
	Configuration file: /Users/elatov/jekyll-bootstrap/_config.yml
	       Deprecation: The 'pygments' configuration option has been renamed to 'highlighter'. Please update your config file accordingly. The allowed values are 'rouge', 'pygments' or null.
	            Source: /Users/elatov/jekyll-bootstrap
	       Destination: /Users/elatov/jekyll-bootstrap/_site
	      Generating...
	                    done.
	 Auto-regeneration: enabled
	    Server address: http://0.0.0.0:4000/
	  Server running... press ctrl-c to stop.
  
  
Now if you point your browser to http://localhost:4000 you should see the template:

![jekyll-running-example-bootstrap](jekyll-running-example-bootstrap.png)

#### Jekyll Themes
There are a bunch of themes out there. Here are a couple of pages that have themes:

- [JekyllBootstrap Theme Explorer](http://themes.jekyllbootstrap.com/)
- [Jekyll Themes](http://jekyllthemes.org/)

Like I mentioned before, you can either clone the whole project or you can actually use JekyllBootstrap to install a theme. For example here is an easy way to install the twitter-bootstrap based theme with JekyllBootstrap:

	elatov@kmac:~/jekyll-bootstrap$rake theme:install git="https://github.com/jekybootstrap/theme-twitter.git"
	Cloning into './_theme_packages/_tmp'...
	remote: Reusing existing pack: 26, done.
	remote: Total 26 (delta 0), reused 0 (delta 0)
	Unpacking objects: 100% (26/26), done.
	Checking connectivity... done.
	mv ./_theme_packages/_tmp ./_theme_packages/twitter
	./_includes/themes/twitter/default.html already exists. Do you want to overwrite? [y/n] y
	mkdir -p ./_includes/themes/twitter
	cp -r ./_theme_packages/twitter/_includes/themes/twitter/default.html ./_includes/themes/twitter/default.html
	./_includes/themes/twitter/page.html already exists. Do you want to overwrite? [y/n] y
	mkdir -p ./_includes/themes/twitter
	cp -r ./_theme_packages/twitter/_includes/themes/twitter/page.html ./_includes/themes/twitter/page.html
	./_includes/themes/twitter/post.html already exists. Do you want to overwrite? [y/n] y
	mkdir -p ./_includes/themes/twitter
	cp -r ./_theme_packages/twitter/_includes/themes/twitter/post.html ./_includes/themes/twitter/post.html
	./_includes/themes/twitter/settings.yml already exists. Do you want to overwrite? [y/n] y
	mkdir -p ./_includes/themes/twitter
	cp -r ./_theme_packages/twitter/_includes/themes/twitter/settings.yml ./_includes/themes/twitter/settings.yml
	mkdir -p ./assets/themes/twitter/css/1.4.0
	cp -r ./_theme_packages/twitter/assets/themes/twitter/css/1.4.0/bootstrap.css ./assets/themes/twitter/css/1.4.0/bootstrap.css
	./assets/themes/twitter/css/style.css already exists. Do you want to overwrite? [y/n] y
	mkdir -p ./assets/themes/twitter/css
	cp -r ./_theme_packages/twitter/assets/themes/twitter/css/style.css ./assets/themes/twitter/css/style.css
	=> twitter theme has been installed!
	=> ---
	=> Want to switch themes now? [y/n] y
	Generating 'twitter' layout: default.html
	Generating 'twitter' layout: page.html
	Generating 'twitter' layout: post.html
	=> Theme successfully switched!
	=> Reload your web-page to check it out =)
	
Now if you re-run jekyll you should see the following after you visit **http://localhost:4000** :

![jekyll-with-twitter-theme-running](jekyll-with-twitter-theme-running.png)

#### Customize Jekyll Configurations
Let's add the information regarding the site. I ended up modifying the following lines in the **_config.yml** file:

	elatov@kmac:~/jekyll-bootstrap$git diff
	diff --git a/_config.yml b/_config.yml
	index 17bd3e2..7f185e3 100644
	--- a/_config.yml
	+++ b/_config.yml
	@@ -1,21 +1,19 @@
	 # This is the default format.
	 # For more see: http://jekyllrb.com/docs/permalinks/
	-permalink: /:categories/:year/:month/:day/:title
	+permalink: /:year/:month/:title
	
	 exclude: [".rvmrc", ".rbenv-version", "README.md", "Rakefile", "changelog.md"]
	-pygments: true
	+highligher: pygments
	
	 # Themes are encouraged to use these universal variables
	 # so be sure to set them if your theme uses them.
	 #
	-title : Jekyll Bootstrap
	-tagline: Site Tagline
	+title : My Blog
	+tagline: Just a Blog
	 author :
	-  name : Name Lastname
	-  email : blah@email.test
	-  github : username
	-  twitter : username
	-  feedburner : feedname
	+  name : Me Moxz
	+  email : moxz@me.com
	+  github : moxz1
	
	 # The production_url is only used when full-domain names are needed
	 # such as sitemap.txt
	@@ -25,7 +23,7 @@ author :
	 # Else if you are pushing to username.github.io, replace with your username.
	 # Finally if you are pushing to a GitHub project page, include the project name at the end.
	 #
	-production_url : http://username.github.io
	+production_url : http://moxz1.github.io
	
On the main page, I decided to just list posts and nothing else. Here is what I ended up with in the **index.md** file:

	elatov@kmac:~/jekyll-bootstrap$cat index.md
	---
	layout: page
	title: Posts
	---
	{% include JB/setup %}
	
	<ul class="posts">
	{% for post in site.posts  limit:10 %}
	    <a href="{{ BASE_PATH }}{{ post.url }}"><h3> {{ post.title }}<br /></h3></a>
		<i>{{ post.date | date_to_string }}<br /></i>
	        {{ post.content | strip_html | truncatewords:75}}
	            <a href="{{ post.url }}">Read more...</a>
	    {% endfor %}
	</ul>

After a reload of **jekyll**, saw the following on the local site:

![jekyll-personal-info-added](jekyll-personal-info-added.png)

If you like how it looks you can push it to the github pages:

	elatov@kmac:~/jekyll-bootstrap$git remote set-url origin https://moxz1@github.com/moxz1/moxz1.github.io.git
	elatov@kmac:~/jekyll-bootstrap$git add --all
	elatov@kmac:~/jekyll-bootstrap$git commit -m "updates"
	[master f692c6f] updates
	10 files changed, 482 insertions(+), 197 deletions(-)
	create mode 100644 assets/themes/twitter/css/1.4.0/bootstrap.css
	rewrite assets/themes/twitter/css/style.css (91%)
	rewrite index.md (94%)
	elatov@kmac:~/jekyll-bootstrap$git push origin master --force
	Counting objects: 38, done.
	Delta compression using up to 8 threads.
	Compressing objects: 100% (19/19), done.
	Writing objects: 100% (21/21), 11.15 KiB | 0 bytes/s, done.
	Total 21 (delta 5), reused 8 (delta 0)
	To https://moxz1@github.com/moxz1/moxz1.github.io.git
	 1f3596c..f692c6f  master -> master
	 
Then after some time, if you visit the github user pages, you will see the same site:

![github-updates-pushed-and-live](github-updates-pushed-and-live.png)

### Migrate Wordpress Posts to Jekyll
There are a couple of methods to the approach. Here are a few:

- [jekyll-importer](http://import.jekyllrb.com/docs/wordpressdotcom/)
- [exit-wp](https://github.com/thomasf/exitwp)
- [wordpress-to-jekyll-exporter](https://github.com/benbalter/wordpress-to-jekyll-exporter)

I ended up using the bottom one. After you install the plugin in your wordpress install, you can either go to the Wordpress Managament Page and you will see the  **Export to Jekyll** button there:

![export-to-jekyl-plugin-wp](export-to-jekyl-plugin-wp.png)

Upon clicking that, it will start the export and you should get a zip of the export. Mine kept timing out, so I did it manually on the host it self:

	$ cd /var/www/wp-content/plugins/wordpress-to-jekyll-exporter
	$ php jekyll-export-cli.php > ~/jekyll-export.zip

I copied the zip from the host and here were the contents of the zip extracted:

	elatov@web1:~/jek$ tree -L 1 jekyll-export
	jekyll-export
	├── about
	├── _config.yml
	├── contact
	├── _posts
	└── wp-content
	
	4 directories, 1 file


#### Clean up Converted Markdown
None of the above converters are perfect, and after the migration you will definitely end up with some left over HTML. Here are a couple of sites that help with clean up:

- [Migrating From Wordpress To Jekyll](http://www.carlboettiger.info/2012/09/19/migrating-from-wordpress-to-jekyll.html)
- [How To Migrate Your Blog From Wordpress To Jekyll](https://devblog.supportbee.com/2012/08/27/how-to-migrate-your-blog-from-wordpress-to-jekyll/)

The first one has an R Script which clean up a bunch of HTML tags and the second one has a ruby script to clean up UTF-8 encoded characters.