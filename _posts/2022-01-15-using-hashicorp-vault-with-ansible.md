---
published: true
layout: post
title: "Using Hashicorp Vault with Ansible"
author: Karim Elatov
categories: [security,automation,containers]
tags: [vault, ansible]
---
I found my self storing credentials for applications I was deploying with Ansible.
I then ran into [Handling secrets in your Ansible playbooks](https://www.redhat.com/sysadmin/ansible-playbooks-secrets)
which gave a lot of different approaches and I wanted to give it a shot.

## Setting up Vault
[My previous post](/2021/09/using-hashicorp-vault-on-kubernetes/) describes how you can deploy Vault really quick on Kubernetes. There is also a [cloud offering from Hashicorp](https://cloud.hashicorp.com/products/vault/pricing) and they have a trial. After it's deployed we can login and configure it:

```bash
> kubectl exec -it vault-0 -- /bin/ash
/ $ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    5
Threshold       3
Version         1.9.2
Storage Type    file
Cluster Name    vault-cluster-9ff92283
Cluster ID      93572f29-2xxxxx
HA Enabled      false
```

If you would like, you can also connect remotely. First install the cli, in my case I was using Fedora (From [Install Vault](https://learn.hashicorp.com/tutorials/vault/getting-started-install#install-vault)):

```bash
> sudo dnf install -y dnf-plugins-core
> sudo dnf config-manager --add-repo https://rpm.releases.hashicorp.com/fedora/hashicorp.repo
> sudo dnf -y install vault
```

Then we configure the creds and url:

```bash
export VAULT_ADDR="http://vault.kar.int:8200"
export VAULT_TOKEN="s.7z1Vxxxxx"
vault status
```

## Configuring Token for Ansible
Now we can create a token for ansible.

### Change Default max_lease_ttl
I wanted to create a token that was valid for a year and we could refresh every 30 days (There are a lot of different tokens you can create and they are all covered in the [Tokens](https://www.vaultproject.io/docs/concepts/tokens) page). By default the maximum TTL for a token is 32 days:

```bash
~ $ vault read sys/auth/token/tune
Key                  Value
---                  -----
default_lease_ttl    768h
description          token based credentials
force_no_cache       false
max_lease_ttl        768h
token_type           default-service
```

So let's go ahead and increase that:

```bash
~ $ vault write sys/auth/token/tune max_lease_ttl=8760h
Success! Data written to: sys/auth/token/tune
```

### Enable kv-v2 Secrets Engine and Create a secret
Now let's enable the kv-v2 secret engine:

```bash
~ $ vault secrets enable -path=apps kv-v2
Success! Enabled the kv-v2 secrets engine at: apps/
```

Now let's put some creds in there:

```bash
~ $ vault kv put apps/my-app username="user"
~ $ vault kv patch apps/my-app password="password"
```

You can then see both values:

```bash
~ $ vault kv get apps/my-app
======= Metadata =======
Key                Value
---                -----
created_time       2021-12-24T19:44:38.586835116Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            3

====== Data ======
Key         Value
---         -----
username    user
password    password
```

Or you can get one field at a time:

```bash
~ $ vault kv get -field=username apps/my-app
user
~ $ vault kv get -field=password apps/my-app
password
```

### Create a Policy
Now let's create a policy to allow to read the secret:

```bash
~ $ cat app-policy.hcl
path "apps/*" {
  capabilities = ["read"]
}
```

Now let's apply it:

```bash
~ $ vault policy write app-reader app-policy.hcl
Success! Uploaded policy: app-reader
```

### Create a Token and attach to a Policy
Now let's create a token and make sure it's attached to the above policy:

```bash
~ $ vault token create -display-name app-reader -explicit-max-ttl 8760h -policy app-reader -ttl 720h -renewable
Key                  Value
---                  -----
token                s.7z1Vxxx
token_accessor       RJb1xxx
token_duration       720h
token_renewable      true
token_policies       ["app-reader" "default"]
identity_policies    []
policies             ["app-reader" "default"]
```

You can also confirm you can read the secret:

```bash
~ $ vault token capabilities s.7z1xxxx apps/my-app
read
```

## Get Secret from Vault with Ansible
Reading over the [new documentation](https://docs.ansible.com/ansible/latest//collections/community/hashi_vault/hashi_vault_lookup.html) from Ansible, I ended up with the following line to get the secret:

{% raw %}
```bash
"{{ lookup('hashi_vault', 'secret=apps/data/my-app token=s.7z1Vxxx url=https://vault.kar.int')['data']['username'] }}"
```
{% endraw %}

And it actually worked out :) I needed to install a python module but other than that it was good to go:

```bash
pip3 install hvac --user
```
