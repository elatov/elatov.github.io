---
published: true
layout: post
title: "Distributed Systems Design - WhatsApp"
author: Karim Elatov
categories: [distributed systems design]
tags: [whatsapp,websockets, message queue]
---

Let's keep chugging along with our distributed systems design.

## Existing Material
Here is some existing stuff:

* [How to Develop Chat System Design like Facebook Messenger, Whatsapp](https://www.cronj.com/blog/how-to-develop-chat-system-design-like-facebook-messenger/)
* [Design a chat system](https://systeminterview.com/design-a-chat-system.php)
* [The WhatsApp Architecture Facebook Bought For $19 Billion](http://highscalability.com/blog/2014/2/26/the-whatsapp-architecture-facebook-bought-for-19-billion.html)

And here are some YouTube Videos:

* [Whatsapp System Design: Chat Messaging Systems for Interviews](https://www.youtube.com/watch?v=vvhC64hQZMk)
* [System Design: Messenger service like Whatsapp or WeChat - Interview Question](https://www.youtube.com/watch?v=5m0L0k8ZtEs)
* [Whatsapp System design or software architecture](https://www.youtube.com/watch?v=L7LtmfFYjc4)

And here are some sample architecture diagrams from the above sites:

* ![whatsapp-design-1.png](https://res.cloudinary.com/elatov/image/upload/v1611970217/blog-pics/dsd-whatsapp/whatsapp-design-1.png)
* ![whatsapps-design-2.png](https://res.cloudinary.com/elatov/image/upload/v1611970217/blog-pics/dsd-whatsapp/whatsapps-design-2.png)
* ![whatsapp-design-3.png](https://res.cloudinary.com/elatov/image/upload/v1611970217/blog-pics/dsd-whatsapp/whatsapp-design-3.png)

## Sending Messages
Watching over some videos it looks like there are usually a cluster of services which have a message queue running on them for each user. If the users are live then the messages are added to queue and pulled by the correspending receivers. Also it sounds like as soon as a message is delived to the receiver it is removed from the queue to make space for the next one. You can add a loadbalancer to spread the intial request across multiple machines or you can have a dedicated microservice acting as a gateway and have it forward the request to the *chat*/*queue* servers accordingly. 

### Websockets
Websockets are used to create a persistent connection between the client and the servers. There are two typical approaches to this: Polling and Websockets. Polling is a technique where the client periodically asks the server if there are messages available. Depending on polling frequency, polling could be resource intensive. It could consume server resources where nothing in the queue resides. 

WebSocket is a common solution for sending asynchronous updates from server to client. WebSocket connection is initiated by the client. It is bi-directional and persistent. It starts as a HTTP connection and could be *enhanced* by some well-defined handshake to a WebSocket connection. Through this persistent connection, a server could send updates to a client. 

## Storing Messages
If the user is not live then the message is pulled from the queue and is stored in some temperary storage. Depending on the volume you can could store it in a NoSQL datastore and scale as necessary. If even further performace is required using Redis as a cache will help as well. If you are supporting media, then uploading those object to a Blob storage would be advantages for durability, availability, and also offloading that component to a well know blob storage supported by a cloud provider.

## Custom Setup
Reading over the awesome [The WhatsApp Architecture Facebook Bought For $19 Billion](http://highscalability.com/blog/2014/2/26/the-whatsapp-architecture-facebook-bought-for-19-billion.html) page it talks about all the custom FreeBSD and Erlang patches that WhatsApp used to reach their scale and it's an awesome example of great engineering. In the beginning I was thinking one could probably use kafka as a distributed messaging queue but I think with amount of performance they were able to squeeze out of those servers it would be difficult to achieve the same with anything else. 