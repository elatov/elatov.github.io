---
published: true
layout: post
title: "NGINX Ingress with Alertmanager and Prometheus"
author: Karim Elatov
categories: [containers]
tags: [nginx-ingress,prometheus]
---
I installed the [nginx-ingress controller](https://kubernetes.github.io/ingress-nginx/) a while back and that setup is covered in my previous post ([Using the Nginx Ingress Controller with Kubernetes](/2018/08/using-the-nginx-ingress-controller-with-kubernetes/)). Now let's use the existing deployment to add some [ingress resources](https://kubernetes.io/docs/concepts/services-networking/ingress/#what-is-ingress). I found a couple of sites that got me started:

* [Exposing Prometheus and Alertmanager](https://github.com/coreos/prometheus-operator/blob/master/Documentation/user-guides/exposing-prometheus-and-alertmanager.md)
* [Howto expose prometheus, grafana and alertmanager with nginx ingress #11471](https://github.com/helm/charts/issues/11471)

### Exposing Prometheus
I ended using the following ingress configuation:

```bash
> cat ingress.yaml 
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: prometheus
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: "/$2"
spec:
  tls:
  - hosts:
    - "ub"
    secretName: tls-secret
  rules:
  - host: ub
    http:
      paths:
      - path: "/prom(/|$)(.*)"
        backend:
          serviceName: prometheus
          servicePort: 9090
```
Then I had to modify the **prometheus** deployment to accept traffic on the new *path* (**/prom**). This was covered in the [Securing Prometheus API and UI Endpoints Using Basic Auth](https://prometheus.io/docs/guides/basic-auth/#nginx-configuration) documentation:

```
> grep web deploy.yaml 
            - "--web.enable-lifecycle"
            - "--web.route-prefix=/"
            - "--web.external-url=http://ub/prom"
```

Then applying (`kubectl apply`) those settings, allowed me to visit the host and getting to the prometheus UI:

![prom-with-nginx.png](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/nginx-ingress-prom/prom-with-nginx.png)

If you want you can also enable **http-auth** through the **nginx-ingress** controller. The insturctions are covered at [Basic Authentication](https://kubernetes.github.io/ingress-nginx/examples/auth/basic/) and the steps are the following:

```bash
$ htpasswd -c auth admin
$ kubectl create secret generic basic-auth --from-file=auth
```

Then modify the config and point to the new **secret**:

```bash
> cat ingress.yaml 
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: prometheus
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: "/$2"
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - Prometheus'
spec:
  tls:
  - hosts:
    - "ub"
    secretName: tls-secret
  rules:
  - host: ub
    http:
      paths:
      - path: "/prom(/|$)(.*)"
        backend:
          serviceName: prometheus
          servicePort: 9090
```

Now if you try to visit the page it will give you a warning:

```bash
> curl -kI https://ub/prom/
HTTP/2 401 
server: nginx/1.17.7
date: Sun, 26 Jan 2020 22:12:14 GMT
content-type: text/html
content-length: 179
www-authenticate: Basic realm="Authentication Required - Prometheus"
strict-transport-security: max-age=15724800; includeSubDomains
```

Simple and gets the job done.

### Exposing Alertmanager
Very similar approach with [Alertmanager](https://prometheus.io/docs/alerting/alertmanager/) as with **prometheus** (no changes to **ingress** other than the *path*). I just had to modify the deployment to make sure the application is serving behind a different *path*:

```bash
 > grep web deploy.yaml 
            - --web.external-url=http://localhost:9093/alerts
            - --web.route-prefix=/
```

Not too shabby.