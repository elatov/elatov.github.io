---
published: true
layout: post
title: "Kibana Reports with Phantomjs"
author: Karim Elatov
categories: [os]
tags: [kibana,phantomjs]
---
### Reporting with Kibana

There have been numerous requests for reporting in **Kibana**:

* [Generate scheduled reports](https://github.com/elastic/kibana/issues/1640)
* [Export to PDF](https://github.com/elastic/kibana/issues/509)
* [report generation](https://github.com/elastic/kibana/issues/760)


And there have been a couple of tools that were created to help out:

* [ElasticTab – Elasticsearch to Excel Report](https://github.com/raghavendar-ts/ElasticTab-Elasticsearch-to-Excel-Report)
* [Skedler - Report Scheduler for Kibana](http://guidanz.com/blog/report-scheduler-for-kibana/)
* [elastalert](https://github.com/Yelp/elastalert)

And lastly it sounds like [X-Pack from Elastic](https://www.elastic.co/guide/en/x-pack/current/xpack-introduction.html) will allow for reporting, but it won't be free. You can use it for a 30 day trial but after that you have to purchase a license. Here is nice support table:

![elk-lic](https://raw.githubusercontent.com/elatov/upload/master/kibana-phantomjs/elk-lic.png)

### Screenshot Solutions

It seems some people started using tools to take a screenshot of **Kibana** dashboards:

* [Kibana Reporting Tool?](https://discuss.elastic.co/t/kibana-reporting-tool/27223)
	* This has an example of a **selenium** script in **python**
* [Kibana3 Automated Email Reports Using Windows](http://www.ragingcomputer.com/2014/03/kibana3-automated-email-reports-using-windows)
	* This is an old version of **phantomjs** with **ImageMagick**
* [how can I screen capture kibana 4 including tooltips?](https://groups.google.com/forum/#!topic/phantomjs/yQEIduvuM4w)
	* This has the simplest version of a **phantomjs** script to work with **Kibana** 4
* [Snapshot for Kibana / Grafana](https://github.com/parvez/snapshot)
	* This is nice app, based on **phantomjs** , which can schedule and create screenshots of **Kibana** dashboards.

Actually watching the [From Dashboard to PDF: Generate Reports with the Elastic Stack video from ElastiCon](https://www.elastic.co/elasticon/conf/2016/sf/from-dashboard-to-pdf-generate-reports-with-the-elastic-stack), it mentions that the new export-to-pdf functionality in **x-pack** also depends on **phantomjs**.

### Playing Around with PhantomJS
So I decided to try out **phantomjs** just to see how it works out. Looking over the [download page](http://phantomjs.org/download.html) it looks like for now only the binaries are available for linux, but I did notice that FreeBSD already had it available in the package repos, so I decided to install on my FreeBSD machine. The install is pretty easy:

	$ sudo pkg install phantomjs

Then copying some of the example from above here is the simplest example:

	<> cat l.js
	var url = 'http://kibana:5601/app/kibana#/dashboard/mydashboard/';
	var page = require('webpage').create();
	//wait to load kibana in ms
	var waitTime = 10 * 1000;

	//size of virtual browser window
	page.viewportSize = { width: 1500, height: 1000 };

	page.open(url, function (status) {
	    if (status !== 'success') {
	        console.log('Unable to load the address!');
	        phantom.exit();
	    } else {
	        window.setTimeout(function () {
	       		//page.zoomFactor = 2.0;
	//save as image
	            page.render('kibana.jpg');
	            phantom.exit();
	        }, waitTime);
	    }
	});

Then running the following:

	$ phantomjs l.js

Produced a file called **kibana.jpg** in the same directory and here is how it looked like:

![ph-jpg-ex](https://raw.githubusercontent.com/elatov/upload/master/kibana-phantomjs/ph-jpg-ex.png)

#### Snapshot - Report Generation for ElasticSearch Kibana / Grafana

The [snapshot](https://github.com/parvez/snapshot) project is a very nice project to put all the aspect together so you don't really have to worry about any thing. There is even a **docker** image available if you want to play around with it. The **phantomjs** script in that project has more options (paper size, zoom factor...etc). If you really wanted, just check out the following two files to get an understanding of how it works:

* [helper_generate.js](https://github.com/parvez/snapshot/blob/master/app/helper_generate.js)
* [server.json](https://github.com/parvez/snapshot/blob/master/app/config/server.json)

And if you have **phantomjs** installed you could use those files to generate the **jpg**, **png**, or **pdf** of the dashboards.

#### Phantomjs with Kibana 4 PDF/CSS Issue

I ran into an interesting issue with **phantomjs** and **Kibana** 4 Dashboards when generating pdfs (pngs and jpgs were fine). Basically the top menu bar would not show up it would just show links. I found an issue with **phantomjs** where if the CSS is marked with **!important** it would not parse it (more on that [here](https://github.com/ariya/phantomjs/issues/10669)). I would have to modify **Kibana**'s CSS to fix that, so I just kept using **jpg** for the screenshots.
