---
published: true
layout: post
title: "Migrating from nginx ingress to K8S Gateway API"
author: Karim Elatov
categories: [networking, containers]
tags: [kubernetes, nginx-ingress, istio, oauth2-proxy, k8s_gateway_api]
---
I ran into [Ingress NGINX Retirement: What You Need to Know](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/) and I decided it's time to migrate to the [Gateway API](https://gateway-api.sigs.k8s.io/). 
I decided to use the `istio` gateway controller, since I was planning on using the auth methods. Also this encouraged me: [Gateway API Benchmarks](https://github.com/howardjohn/gateway-api-bench)

### Installing Gateway CRDs

Since I want to use `tlsroute`, I need to install the experimental CRDs:

```
> kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/experimental-install.yaml
customresourcedefinition.apiextensions.k8s.io/backendtlspolicies.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/gatewayclasses.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/gateways.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/grpcroutes.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/httproutes.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/referencegrants.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/tcproutes.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/tlsroutes.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/udproutes.gateway.networking.k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/xbackendtrafficpolicies.gateway.networking.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/xlistenersets.gateway.networking.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/xmeshes.gateway.networking.x-k8s.io serverside-applied
```

### Installing Istio Gateway Controller

We need `istiod` and `istio-base` else it will fail to install because of [this](https://github.com/istio/istio/issues/46307):

```
helm install istio-base istio/base -n istio-system --create-namespace 
helm install istiod istio/istiod -n istio-system --set pilot.env.PILOT_ENABLE_ALPHA_GATEWAY_API=true
helm install istio-ingress istio/gateway -n istio-ingress --create-namespace --set service.type=ClusterIP
```

The `pilot.env.PILOT_ENABLE_ALPHA_GATEWAY_API=true` is required to use `TLSRoute` (this is discussed [here](https://github.com/istio/istio/discussions/48807)) and `--set service.type=ClusterIP` is useful to save a LoadBalancer IP since the `gateway` resource will get it's own IP anyways:

```
> k get gateway
NAME          CLASS   ADDRESS         PROGRAMMED   AGE
web-gateway   istio   192.168.1.204   True         135m
```

After the installation `istio` will install it's own `gatewayclass`:

```
> kubectl get gatewayclass
NAME           CONTROLLER                    ACCEPTED   AGE
istio          istio.io/gateway-controller   True       3m29s
istio-remote   istio.io/unmanaged-gateway    True       3m29s
```

One other random note, when I was installing the `helm` charts with `argocd`, I ran into this issue where the `istiod` and `base` charts kept overwriting each other's `validatingwebhookconfiguration`. The issue was captured in [ValidationWebhook 'failurePolicy' is changed to 'Fail' after deployment](https://github.com/istio/istio/issues/52785) and the fix is in there as well. Add the following to both of the argocd applications and the issue was fixed.

```
spec:
  ignoreDifferences:
    - group: admissionregistration.k8s.io
      kind: ValidatingWebhookConfiguration
      name: istio-validator-istio-system
      jsonPointers:
        - /webhooks/0/failurePolicy
    - group: admissionregistration.k8s.io
      kind: ValidatingWebhookConfiguration
      name: istiod-default-validator
      jsonPointers:
        - /webhooks/0/failurePolicy
```        

### Converting Ingress to httproute and tlsroute

There is a conversion script that can be used: [ingress2gateway](https://github.com/kubernetes-sigs/ingress2gateway):

```
./ingress2gateway print -A --providers ingress-nginx
```

I would say it's a good starting point, but for any custom configurations (ssl passthrough, authentication, or http rewrites) you have to update or create the resources your self.

#### Reviewing the istio configurations
To check how the gateway is programmed:

```
## get the gateway pod
> k get po -l gateway.networking.k8s.io/gateway-name=web-gateway
NAME                                 READY   STATUS    RESTARTS   AGE
web-gateway-istio-5f77df989f-zk29t   1/1     Running   0          167m

## then use istioctl
> istioctl pc listener web-gateway-istio-5f77df989f-zk29t
ADDRESSES PORT  MATCH                                DESTINATION
0.0.0.0   80    ALL                                  Route: http.80
0.0.0.0   443   SNI: *.kar.int                       Route: https.443.default.web-gateway~istio-autogenerated-k8s-gateway~https-ext.default
0.0.0.0   443   SNI: kubeapi.kar.int                 Cluster: outbound|443||kubernetes.default.svc.cluster.local
0.0.0.0   15021 ALL                                  Inline Route: /healthz/ready*
0.0.0.0   15090 ALL                                  Inline Route: /stats/prometheus*
```

We can see that the `httproutes` end up getting a `route` configuration, while the `tlsroute` which is doing passthrough is just forwarding the traffic to the service (which is expected). Breaking it down further we can also look at the `route` and confirm which `service` it's forwarding to:

```
> istioctl pc routes web-gateway-istio-5f77df989f-zk29t --name http.80 -o yaml | yq '.[].virtualHosts[] | select(.domains[] | . == "ceph.kar.int")' | yq '{domains: .domains, name: .name, cluster: .routes[0].route.cluster}'
{
  "domains": [
    "ceph.kar.int"
  ],
  "name": "ceph.kar.int:80",
  "cluster": "outbound|8080||rook-ceph-mgr-dashboard.rook-ceph.svc.cluster.local"
}
```

I did run into an interesting issue where Multiplexing hasn't been finalized  [Conflicting SNI's between HTTPRoute & TLSRoute](https://github.com/kubernetes-sigs/gateway-api/issues/623). So if you have an `httproute` and `tlsroute` on the same port, unless you create a separate `listener` on both side, it's going to have unexpected results. I am hoping we can add multiple `hostnames` to the gateway listener and that way we can control it by SNI. Right now the `gateway` allows only for 1 hostname (but we can do wild cards), while the `httproute` or `tlsroute` allows for multiple `hostnames`. If both allowed multiple `hostnames` I think it will give more flexibility.

### Authentication with the Istio Gateway

I was lazy for some of my applications and didn't enable authentication on the application side initially. But at this moment I took the opportunity and enabled **Basic Auth** on `alertmanager`, it included a lot of changes but they are all covered [here](https://github.com/prometheus-community/helm-charts/issues/3701)

#### Configuring oauth2-proxy with istio

If you want to get fancy and integrate OIDC, here are some nice guides:

- [External Authorization](https://istio.io/latest/docs/tasks/security/authorization/authz-custom/)
- [Istio OIDC Authentication with OAuth2-Proxy](https://medium.com/@lucario/istio-external-oidc-authentication-with-oauth2-proxy-5de7cd00ef04)
- [Istio OIDC authn + authz with oauth2-proxy](https://www.ventx.de/blog/post/istio_oauth2_proxy/index.html)
- [Authenticate applications on Kubernetes: Okta(OIDC), Istio, and OAuth2-Proxy integration](https://seifrajhi.github.io/blog/authenticate-apps-on-k8s-okta-istio-oauth2/)

I used the [helm chart for oauth2-proxy](https://artifacthub.io/packages/helm/oauth2-proxy/oauth2-proxy) and here is the `values.yaml` file I ended up using:

```
> cat values.yaml
config:
  # these are from your IDP
  clientSecret: "xxx"
  clientID: "xxx"
  # local to this server
  cookieSecret: "xxx"
  httpAddress: "0.0.0.0:4180"

  configFile: |
    provider = "oidc"
    oidc_issuer_url = "YOUR_IDP_ISSUER_URL"
    redirect_url = "https://oauth.YOUR_DOMAIN/oauth2/callback"
    cookie_domains = [ ".YOUR_DOMAIN" ]
    scope = "openid email profile"
    # Headers to forward from the proxy to the upstream upon successful auth
    set_xauthrequest = "true"
    pass_authorization_header = "true"
    pass_host_header = "true"
    reverse_proxy = "true"
    whitelist_domains = [ ".YOUR_DOMAIN" ]
    upstreams =  "static://200" # Dummy upstream, as Istio handles final routing
    skip_provider_button = "true"

extraObjects:
- apiVersion: v1
  kind: ConfigMap
  metadata:
    name: oauth2-proxy-accesslist 
    labels:
      app: oauth2-proxy
  data:
    restricted_users.txt: |
      you@mail.com

extraVolumes:
  - name: custom-emails-volume
    configMap:
      name: oauth2-proxy-accesslist

extraVolumeMounts:
  - name: custom-emails-volume
    mountPath: /etc/oauth2-proxy/custom-config/ # Define a new path for clarity
    readOnly: true

extraArgs:
  authenticated-emails-file: /etc/oauth2-proxy/custom-config/restricted_users.txt
```

In this setup I have an `httproute` resource for each the `oauth2-proxy` and the application it self. For `istiod` I had the following `values.yaml`:

```
> cat values.yaml
pilot:
  env:
    PILOT_ENABLE_ALPHA_GATEWAY_API: "true"
meshConfig:
  extensionProviders:
  - name: oauth2-proxy-extauthz
    envoyExtAuthzHttp:
      service: oauth2-proxy.default.svc.cluster.local
      port: 80
      headersToUpstreamOnAllow:
      - path
      - x-auth-request-email
      - x-auth-request-preferred-username
      headersToDownstreamOnDeny:
      - content-type
      - set-cookie
      includeRequestHeadersInCheck:
      - authorization
      - cookie
      - x-auth-request-groups
      includeAdditionalHeadersInCheck:
        X-Auth-Request-Redirect: 'https://%REQ(:authority)%%REQ(:path)%'
```

And lastly here is the `authorizationpolicy`:

```
 > cat authpolicy-ext-authz.yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: enforce-oauth2-proxy
spec:
  selector:
    matchLabels:
      gateway.networking.k8s.io/gateway-name: web-gateway
  action: CUSTOM
  provider:
    name: "oauth2-proxy-extauthz"
  rules:
  - to:
    - operation:
        hosts: ["APP.YOUR_DOMAIN"]%
```        

It's quite as setup, from one of the above guides here how the traffic will flow:

![istio-oauth2-proxy-flow](https://res.cloudinary.com/elatov/image/upload/v1765075768/blog-pics/nginx-ingress-to-gateway-api/istio-oauth2-proxy-flow-mermaid.png)

For troubleshooting it helps to enable debug logs to review how the authorization and routing is working on the istio gateway side:

```
istioctl proxy-config log web-gateway-istio-7cf44d7f5b-2px8c --level debug
```

Then look at the logs of the `web-gateway-istio` pod:

```
kubectl logs -l gateway.networking.k8s.io/gateway-name=web-gateway
```

To reset:

```
istioctl proxy-config log web-gateway-istio-7cf44d7f5b-2px8c -r
```

And with that I was able to completely migrate from [nginx-ingress](https://github.com/kubernetes/ingress-nginx) to [istio gateway api](https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/).