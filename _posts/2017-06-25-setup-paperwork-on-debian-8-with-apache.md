---
published: false
layout: post
title: "Setup Paperwork on Debian 8 with Apache"
author: Karim Elatov
categories: [os]
tags: [paperworkrocks,nodejs,apache]
---
### Paperwork
I wanted to find an application that helps with note taking and it wasn't cloud based. I just wanted my own app that I could manage myself. So I ran into [Paperwork](http://paperwork.rocks/) and I decided to give it a try.

### Install Paperwork on Debian
Most of the setup is covered here:
[Installing Paperwork on Debian 7](https://github.com/twostairs/paperwork/wiki/Installing-Paperwork-on-Debian-7). First install the prereqs:

	$ sudo apt-get install php5-mysql curl wget git php5-cli php5-gd php5-mcrypt nodejs nodejs-legacy

Next install **composer**: 

	<> curl -sS https://getcomposer.org/installer | php
	All settings correct for using Composer
	Downloading 1.2.4...
	
	Composer successfully installed to: /home/elatov/composer.phar
	Use it: php composer.phar

Then move **composer** to **/usr/local/bin**

	<> sudo mv composer.phar /usr/local/bin/composer

Then get the source for **paperwork**

	<> git clone https://github.com/twostairs/paperwork.git
	Cloning into 'paperwork'...
	remote: Counting objects: 10065, done.
	remote: Compressing objects: 100% (18/18), done.
	remote: Total 10065 (delta 6), reused 0 (delta 0), pack-reused 10046
	Receiving objects: 100% (10065/10065), 27.28 MiB | 9.02 MiB/s, done.
	Resolving deltas: 100% (6780/6780), done.
	Checking connectivity... done.

And put it under the doc root of **apache** (this way it will a subfolder within **apache**):

	$ sudo mv paperwork /var/www/.

Then install all the necessary packages:

	<> cd /var/www/paperwork/frontend
	<> composer install
	Loading composer repositories with package information
	Updating dependencies (including require-dev)
	  - Installing erusev/parsedown (dev-master 20ff8bb)
	    Downloading: 100%
	
	  - Installing strebl/adldap (v4.0.5)
	    Downloading: 100%
	
	  ...
	  ...
	  - Installing jeremeamia/superclosure (1.0.2)
	    Downloading: 100%
	
	  - Installing monolog/monolog (1.22.0)
	    Downloading: 100%
	
	...
	...
	
	monolog/monolog suggests installing aws/aws-sdk-php (Allow sending log messages to AWS services like DynamoDB)
	
	symfony/security-core suggests installing symfony/validator (For using the user password constraint)
	phpdocumentor/reflection-docblock suggests installing dflydev/markdown (~1.0)
	Package strebl/adldap is abandoned, you should avoid using it. Use adldap2/adldap2 instead.
	Writing lock file
	Generating autoload files
	> php artisan clear-compiled
	> php artisan ide-helper:generate
	PDOException: SQLSTATE[HY000] [2002] Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
	Please configure your database connection correctly, or use the sqlite memory driver (-M). Skipping \Illuminate\Support\Facades\Password.
	PDOException: SQLSTATE[HY000] [2002] Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
	Please configure your database connection correctly, or use the sqlite memory driver (-M). Skipping \Illuminate\Support\Facades\Schema.
	A new helper file was written to _ide_helper.php
	> php artisan optimize
	Generating optimized class loader

#### MariaDB setup for Paperwork
Next let's prepare the **mariadb** setup, on the **apache** machine where **paperwork** is installed, configure the dabatase connection parameters:

	<> cd /var/www/paperwork/frontend
	<> cp app/storage/config/default_database.json app/storage/config/database.json
	<> cat app/storage/config/database.json
	{
	    "driver": "mysql",
	    "database": "paperwork",
	    "host": "10.0.0.3",
	    "username": "paperwork",
	    "password": "password",
	    "port": 3306
	}

Then on the DB server:

	<> mysql -u root -p
	Enter password:
	Welcome to the MariaDB monitor.  Commands end with ; or \g.
	Your MariaDB connection id is 48561
	Server version: 10.0.27-MariaDB FreeBSD Ports
	
	Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.
	
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	
	MariaDB [(none)]> DROP DATABASE IF EXISTS paperwork;
	Query OK, 0 rows affected, 1 warning (0.00 sec)
	
	MariaDB [(none)]> CREATE DATABASE IF NOT EXISTS paperwork DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
	Query OK, 1 row affected (0.01 sec)
	
	MariaDB [(none)]> GRANT ALL PRIVILEGES ON paperwork.* TO 'paperwork'@'10.0.0.2' IDENTIFIED BY 'password' WITH GRANT OPTION;
	Query OK, 0 rows affected (0.01 sec)
	
	MariaDB [(none)]> FLUSH PRIVILEGES;
	Query OK, 0 rows affected (0.02 sec)
	
	MariaDB [(none)]> quit
	Bye

Then from **apache** server make sure you can login to the new db:

	<> /usr/bin/mysql -h 10.0.0.3 -u paperwork -ppassword
	Welcome to the MariaDB monitor.  Commands end with ; or \g.
	Your MariaDB connection id is 48564
	Server version: 10.0.27-MariaDB FreeBSD Ports
	
	Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.
	
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	
	MariaDB [(none)]>

Next let's fill the database the all the data:

	> php artisan migrate
	**************************************
	*     Application In Production!     *
	**************************************
	
	Do you really wish to run this command? y
	Migration table created successfully.
	Migrated: 2014_07_22_194050_initialize
	Migrated: 2014_07_24_103915_create_password_reminders_table
	Migrated: 2014_10_08_203732_add_visibility_to_tags_table
	Migrated: 2015_01_21_034728_add_admin_to_users
	Migrated: 2015_05_05_094021_modify_tag_user_relation
	Migrated: 2015_05_22_220540_add_version_user_relation
	Migrated: 2015_06_15_224221_add_tag_parent
	Migrated: 2015_06_30_125536_add_sessions_table
	Migrated: 2015_07_29_130508_alter_versions

#### Install NPM packages
First install **npm**, I grabbed the one provided my Debian:

	<> sudo apt-get install npm
	
Next install **bower** and **gulp** globally:

	<> sudo npm install -g gulp bower
	/usr/local/bin/gulp -> /usr/local/lib/node_modules/gulp/bin/gulp.js
	/usr/local/bin/bower -> /usr/local/lib/node_modules/bower/bin/bower
	gulp@3.9.1 /usr/local/lib/node_modules/gulp
	...
	├── gulp-util@3.0.7 (array-differ@1.0.0, lodash._reevaluate@3.0.0, lodash._reinterpolate@3.0.0, lodash._reescape@3.0.0, beeper@1.1.1, array-uniq@1.0.3, object-assign@3.0.0, replace-ext@0.0.1, has-gulplog@0.1.0, fancy-log@1.2.0, gulplog@1.0.0, lodash.template@3.6.2, vinyl@0.5.3, through2@2.0.3, multipipe@0.1.2, dateformat@1.0.12)
	└── vinyl-fs@0.3.14 (strip-bom@1.0.0
	
	bower@1.8.0 /usr/local/lib/node_modules/bower

Now let's get all the **nodejs** packages:

	<> cd /var/www/paperwork/frontend
	<> npm install
	
	gulp-rename@1.2.2 node_modules/gulp-rename
	...
	...
	└── less@2.7.1 (graceful-fs@4.1.11, mime@1.3.4, image-size@0.5.0, mkdirp@0.5.1, errno@0.1.4, source-map@0.5.6, promise@7.1.1)
	
	bower@1.8.0 node_modules/bower

Same thing with **bower**:

	<> cd /var/www/paperwork/frontend
	<> bower install
	bower not-cached    https://github.com/nervgh/angular-file-upload.git#1.1.5
	bower resolve       https://github.com/nervgh/angular-file-upload.git#1.1.5
	...
	...
	font-awesome#4.7.0 app/js/bower_components/font-awesome

Finally build the project:

	<> cd /var/www/paperwork/frontend
	<> gulp
	[17:10:54] Using gulpfile /var/www/paperwork/frontend/gulpfile.js
	[17:10:54] Starting 'compileLessBootstrapTheme'...
	[17:10:54] Finished 'compileLessBootstrapTheme' after 8.01 ms
	..
	..
	[17:10:54] Starting 'default'...
	[17:10:54] Finished 'default' after 8.8 μs

### Initial Setup for Paperwork

I kept getting into a redirect loop and the issue is described [here](https://github.com/twostairs/paperwork/issues/649). So following the instructions laid out in: [Installing and configuring Paperwork without using the Setup Wizard](https://github.com/twostairs/paperwork/wiki/Installing-and-configuring-Paperwork-without-using-the-Setup-Wizard) I manually configured the Application. First set the config file to be **8**:

	[/var/www/paperwork/frontend] - [2016-12-17 09:38:59]
	└─[0] <git:(master 50527ed✱✈) > cat app/storage/config/setup
	8

Then copy the default **paperwork** config and leave the **registration** option enabled:

	[/var/www/paperwork/frontend] - [2016-12-17 09:39:03]
	└─[0] <git:(master 50527ed✱✈) > cp app/storage/config/default_paperwork.json app/storage/config/paperwork.json
	┌─[elatov@kerch] - [/var/www/paperwork/frontend] - [2016-12-17 09:39:42]
	└─[0] <git:(master 50527ed✱✈) > cat app/storage/config/paperwork.json
	{
	    "registration": true,
	    "forgot_password": true,
	    "showIssueReportingLink": false
	}


Lastly go ahead and change ownership to apache:

	<> sudo chown www-data:www-data -R /var/www/paperwork

Then when you go to the application (**http://\<APACHE\>/paperwork/frontend/public**) it should redirect you to the login page:

![pw-login-page](https://seacloud.cc/d/480b5e8fcd/files/?p=/paperwork-on-debian/pw-login-page.png&raw=1)

Then register the first user (by clicking **Sign Up**) which will be the admin and if you want you can disable the registration by modifying the **app/storage/config/paperwork.json** file.

I was looking over [Using Apache in place of Nginx](https://github.com/twostairs/paperwork/wiki/Using-Apache-in-place-of-Nginx) and I couldn't get the rewrite to work (some of the **js** files kept trying to be loaded from the document root of **apache**). So I just redirect to the app with the following config:

	<> cat /etc/apache2/conf-enabled/paperwork.conf
	Alias /pw /var/www/paperwork
	<Directory /var/www/paperwork/>
		RewriteEngine on
		RewriteRule ^(/paperwork/)?$ /paperwork/frontend/public [R=301,L]
	</Directory>
	
	#Alias /paperwork /var/www/paperwork/frontend/public
	
	<Directory /var/www/paperwork/frontend/public/>
	    Options Indexes FollowSymLinks
	    AllowOverride All
	    <IfVersion >= 2.3>
	        Require all granted
	    </IfVersion>
	</Directory>
	
Then going to **https://\<APACHE\>/pw** I was redirected to the application, I could login, and use it without issues.

### Updating Paperwork
To do an update I followed the following steps, first **chown** the project to your self:

	<> sudo chown elatov:elatov -R /var/www/paperwork

Then do the update:

	<> cd /var/www/paperwork/frontend
	[/var/www/paperwork/frontend] - [2016-12-17 09:34:45]
	└─[0] <git:(master 50527ed✱✈) > php artisan paperwork:update
	Running git pull
	Already up-to-date.
	Already up-to-date.
	Running composer update
	Loading composer repositories with package information
	Updating dependencies (including require-dev)
	Nothing to install or update
	Package strebl/adldap is abandoned, you should avoid using it. Use adldap2/adldap2 instead.
	Generating autoload files
	> php artisan clear-compiled
	> php artisan ide-helper:generate
	A new helper file was written to _ide_helper.php
	> php artisan optimize
	Generating optimized class loader
	Generating optimized class loader
	Running npm update
	object-assign@3.0.0 node_modules/gulp-livereload/node_modules/gulp-util/node_modules/object-assign
	..
	..
	└── jshint@2.9.4 (strip-json-comments@1.0.4, exit@0.1.2, console-browserify@1.1.0, shelljs@0.3.0, minimatch@3.0.3, cli@1.0.1, htmlparser2@3.8.3, lodash@3.7.0)
	Running npm run bower-update
	
	> @ bower-update /var/www/paperwork/frontend
	> gulp bower-update
	
	[21:35:46] Using gulpfile /var/www/paperwork/frontend/gulpfile.js
	[21:35:46] Starting 'bower-update'...
	[21:35:46] Using cwd:  /var/www/paperwork/frontend
	[21:35:46] Using bower dir:  app/js/bower_components
	..
	..
	[21:35:52] bower extra-resolution Unnecessary resolution: angular-route#~1.2
	[21:35:53] Finished 'bower-update' after 6.91 s
	[21:35:53] Finished 'bower-update' after 6.91 s
	Running npm run build
	
	> @ build /var/www/paperwork/frontend
	> gulp
	
	[21:35:55] Using gulpfile /var/www/paperwork/frontend/gulpfile.js
	[21:35:55] Starting 'compileLessBootstrapTheme'...
	[21:35:55] Finished 'compileLessBootstrapTheme' after 7.44 ms
	..
	..
	[21:35:55] Finished 'default' after 9.11 μs
	[21:35:55] Finished 'default' after 9.11 μs
	Done.

Then **chown** it back to **apache**:

	<> sudo chown www-data:www-data -R /var/www/paperwork