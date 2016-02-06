---
published: false
layout: post
title: "Updating to Snorby 2.6.3"
author: Karim Elatov
categories: [security,os]
tags: [snorby,linux,debian]
---
So I decided to update Snorby. Snce my [last update](/2015/06/upgrade-debian-wheezy7-to-jessie8/) I ensured that ruby 1.9 was used and I wanted to get rid of that hack.

### Update Snorby
The instuctions are laid out in the [Updating Snorby](https://github.com/Snorby/snorby/wiki/Updating-Snorby) git page. Here is what I ended up running, first let's update the git repo:

	$ cd /usr/local/snorby
	$ git pull origin master

Next let's update our ruby link to point to the latest version:

	$ cd /usr/bin
	$ sudo unlink ruby
	$ sudo ln -s ruby2.1 ruby

Now let's install **bundler** for this version of *ruby*:

	$ sudo gem install bundle

I also ended up creating a symlink to this version:

	$ sudo ln -s /var/lib/gems/2.1.0/gems/bundler-1.10.4/bin/bundle /usr/local/bin/bundle

After that I clear our my old gems and reinstalled them with **bundle**:

	$ rm -rf /usr/local/snorby/vendor/cache/*

And then I reinstalled all the dependencies:

	$ cd /usr/local/snorby
	$ bundle install
	
Then I finally performed the update:

	$ bundle exec 'rake snorby:update'

As a quick test I ran the following to make sure it's working okay:

	$ cd /usr/local/snorby/
	$ bundle exec 'rails c production'
	syck has been removed, psych is used instead
	Loading production environment (Rails 3.2.22)
	irb(main):001:0> Snorby::Jobs.sensor_cache?
	=> true

Lastly I ran the following cause I kept getting warnings about *PDF* variables, as per the instructions in the [main](https://github.com/Snorby/snorby) snorby page:

	sed -i 's/\(^.*\)\(Mime::Type.register.*application\/pdf.*$\)/\1if Mime::Type.lookup_by_extension(:pdf) != "application\/pdf"\n\1  \2\n\1end/' vendor/cache/ruby/*.*.*/bundler/gems/ezprint-*/lib/ezprint/railtie.rb
	sed -i 's/\(^.*\)\(Mime::Type.register.*application\/pdf.*$\)/\1if Mime::Type.lookup_by_extension(:pdf) != "application\/pdf"\n\1  \2\n\1end/' vendor/cache/ruby/*.*.*/gems/actionpack-*/lib/action_dispatch/http/mime_types.rb
	sed -i 's/\(^.*\)\(Mime::Type.register.*application\/pdf.*$\)/\1if Mime::Type.lookup_by_extension(:pdf) != "application\/pdf"\n\1  \2\n\1end/' vendor/cache/ruby/*.*.*/gems/railties-*/guides/source/action_controller_overview.textile

### Update Passenger Apache Module
The system passenger is actually okay, here is what I had installed on the system:

	┌─[elatov@kerch] - [/home/elatov] - [2016-02-06 09:55:09]
	└─[0] <> dpkg -l libapache2-mod-passenger | tail -1
	ii  libapache2-mod-passenger 4.0.53-1     amd64        Rails and Rack support for Apache2

I then fixed my snorby passenger config to use the default ruby:

	--- /snorby.conf.orig	2016-02-06 09:56:24.700399842 -0700
	+++ /snorby.conf	2016-02-05 21:17:46.017633340 -0700
	@@ -2,7 +2,8 @@
	 <Location /snorby>
	     PassengerBaseURI /snorby
	     PassengerAppRoot /usr/local/snorby
	-    PassengerRuby /usr/bin/ruby1.9.1
	+#    PassengerRuby /usr/bin/ruby1.9.1
	+    PassengerRuby /usr/bin/ruby
	 </Location>

That actually worked out but during start up I was receiving the following message:

	App 31674 stderr: env:
	App 31674 stderr: /usr/bin/passenger-config
	App 31674 stderr: : No such file or directory
	App 31674 stderr:

I noticed the OS passenger package didn't provide that. It actually wasn't a big deal (everything was still working without issues), but I decided to update the module just for the heck of it. So let's install the **gem**:

	$ sudo gem install passenger

Then let's get some source packages that we need to build the module:

	$ sudo apt-get install apache2-threaded-dev libapr1-dev libaprutil1-dev

Next let's build the module:

	$ sudo /var/lib/gems/2.1.0/gems/passenger-5.0.24/bin/passenger-install-apache2-module -a
	
Then I had to modify the apache module configs to use the new versions:

	<> cat /etc/apache2/mods-available/passenger.load
	#LoadModule passenger_module /usr/lib/apache2/modules/mod_passenger.so
	LoadModule passenger_module /var/lib/gems/2.1.0/gems/passenger-5.0.24/buildout/apache2/mod_passenger.so
	
And here is the module conf file:

	<> cat /etc/apache2/mods-available/passenger.conf
	#<IfModule mod_passenger.c>
	#  PassengerRoot /usr/lib/ruby/vendor_ruby/phusion_passenger/locations.ini
	#  PassengerDefaultRuby /usr/bin/ruby
	#</IfModule>
	<IfModule mod_passenger.c>
	    PassengerRoot /var/lib/gems/2.1.0/gems/passenger-5.0.24
	    PassengerDefaultRuby /usr/bin/ruby
	</IfModule>


After an **apache** restart:

	sudo systemctl restart apache2
	
The above error went away.

### Post Upgrade Issues
After the update I ran into a couple of issues.

#### Fix the Redirect issue
After the update I would visit the snorby page and after logging in it would just show me a json object of a successful login but would never redirect to the actual app. I found a known issue for that [here](https://github.com/Snorby/snorby/issues/411) and the fix was in the java script (**/usr/local/snorby/public/assets/snorby.js**):

	-  $('#login form#user_new').submit(function(event) {
	+  $('#login form#new_user').submit(function(event) {

After that the login started working without issues.

#### Fix Daily Email Report
You can run the email report manually as decribed in [Manually Run Reports](https://github.com/Snorby/snorby/wiki/Manually-Run-Reports). When I ran it manually I saw the following error:

	┌─[elatov@kerch] - [/usr/local/snorby] - [2016-02-06 07:59:57]
	└─[0] <git:(master 94c7f18✱✈) > bundle exec 'rails c production'
	syck has been removed, psych is used instead
	Loading production environment (Rails 3.2.22)
	irb(main):001:0> ReportMailer.daily_report.deliver
	ArgumentError: wrong number of arguments (0 for 1..2)
	    from /usr/local/snorby/app/mailers/report_mailer.rb:3:in `daily_report'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/actionpack-3.2.22/lib/abstract_controller/base.rb:167:in `process_action'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/actionpack-3.2.22/lib/abstract_controller/base.rb:121:in `process'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/actionpack-3.2.22/lib/abstract_controller/rendering.rb:45:in `process'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/actionmailer-3.2.22/lib/action_mailer/base.rb:459:in `process'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/actionmailer-3.2.22/lib/action_mailer/base.rb:453:in `initialize'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/actionmailer-3.2.22/lib/action_mailer/base.rb:439:in `new'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/actionmailer-3.2.22/lib/action_mailer/base.rb:439:in `method_missing'
	    from (irb):1
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/railties-3.2.22/lib/rails/commands/console.rb:47:in `start'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/railties-3.2.22/lib/rails/commands/console.rb:8:in `start'
	    from /usr/local/snorby/vendor/cache/ruby/2.1.0/gems/railties-3.2.22/lib/rails/commands.rb:41:in `<top (required)>'
	    from script/rails:6:in `require'
	    from script/rails:6:in `<main>'
	irb(main):002:0>

Also running the daily cache job I saw the following:

	irb(main):001:0> Snorby::Jobs::DailyCacheJob.new(true).perform
	
	[~] Building Sensor Metrics
	[~] Building Signature Metrics
	[~] Building Classification Metrics
	[~] Building Severity Metrics
	
	wrong number of arguments (0 for 1..2)
	/usr/local/snorby/app/mailers/report_mailer.rb:3:in `daily_report'
	Sensor 1: Error: Unable to send report - please make sure your mail configurations are correct.
	Dropping old events
	=> #<Delayed::Backend::DataMapper::Job @id=22648 @priority=1 @attempts=0 @handler="--- !ruby/struct:Snorby::Jobs::DailyCacheJob\nverbose: false\n" @run_at=Sun, 07 Feb 2016 00:00:00 -0700 @locked_at=nil @locked_by=nil @failed_at=nil @last_error=nil>
	
I ran into this [google groups thread](https://groups.google.com/forum/#!topic/snorby/5VF7BLY_5i0) that had a similar issue and they fixed it by manually setting their **email**, so I modified the ruby script as such (**/usr/local/snorby/app/mailers/report_mailer.rb**):

	--- report_mailer.rb.orig	2016-02-06 08:54:00.049765323 -0700
	+++ report_mailer.rb		2016-02-06 10:38:56.634103519 -0700
	@@ -1,6 +1,6 @@
	 class ReportMailer < ActionMailer::Base
	
	-  def daily_report(email,timezone="UTC")
	+  def daily_report(email="elatov@test.com",timezone="UTC")
	     report = Snorby::Report.build_report('yesterday', timezone)
	     attachments["snorby-daily-report.pdf"] = report[:pdf]

And then my emails started to work. Don't forget to get the right version of **wkhtmltopdf** as per [this](https://github.com/Snorby/snorby/issues/73) snorby issue. Consolidated instructions:

> * At the step of installing wkhtmltopdf, do this:
>  
> 		wget http://wkhtmltopdf.googlecode.com/files/wkhtmltopdf-0.10.0_rc2-static-amd64.tar.bz2
		tar xjf wkhtmltopdf-0.10.0_rc2-static-amd64.tar.bz2 
		cp wkhtmltopdf-amd64 /usr/local/bin/wkhtmltopdf 
> 
> * Be sure you have created an administrator with a valid email address. 
> * Be sure the timezone in your new admin and the sensor is correct
> * Delete de default Administrator acccount (snorby default): Note that you recreate it with the exact same infos be take care of the TimeZone
> * then in **/var/www/snorby** run 
> 
> 		RAILS_ENV=production rails r "Snorby::Jobs::SensorCacheJob.new(true).perform"

else you will run into this issue:

	irb(main):001:0> Snorby::Jobs::DailyCacheJob.new(true).perform
	
	[~] Building Sensor Metrics
	[~] Building Signature Metrics
	[~] Building Classification Metrics
	[~] Building Severity Metrics
	
	The switch --print-media-type, is not support using unpatched qt, and will be ignored.QXcbConnection: Could not connect to display
	Broken pipe
	/usr/local/snorby/vendor/cache/ruby/2.1.0/gems/pdfkit-0.4.6/lib/pdfkit/pdfkit.rb:62:in `write'
	Sensor 1: Error: Unable to send report - please make sure your mail configurations are correct.
	Dropping old events
	=> #<Delayed::Backend::DataMapper::Job @id=22650 @priority=1 @attempts=0 @handler="--- !ruby/struct:Snorby::Jobs::DailyCacheJob\nverbose: false\n" @run_at=Sun, 07 Feb 2016 00:00:00 -0700 @locked_at=nil @locked_by=nil @failed_at=nil @last_error=nil>
	irb(main):002:0>
	
Also another note is that since I was using **exim4** instead of **sendmail**, my email config looked like this (**/usr/local/snorby/config/initializers/mail_config.rb**):

	 ActionMailer::Base.delivery_method = :sendmail
	 ActionMailer::Base.sendmail_settings = {
	   :location => '/usr/sbin/sendmail',
	   :arguments => '-i'
	#   :arguments => '-i -t'
	 }
	
	ActionMailer::Base.perform_deliveries = true
	ActionMailer::Base.raise_delivery_errors = true
	
Another person fixed the above issue by reinstalling everything as decribed in [this](https://github.com/Snorby/snorby/issues/312) snorby issue page (but I didn't want to do that yet).
