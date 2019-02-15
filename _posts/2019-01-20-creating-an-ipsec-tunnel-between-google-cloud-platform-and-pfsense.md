---
published: true
layout: post
title: "Creating an IPSec Tunnel between Google Cloud Platform and PFSense"
author: Karim Elatov
categories: [virtualization,networking]
tags: [gcp,pfsense]
---
### Existing Documentation
As I was trying to create a tunnel between my VPC in Google Cloud Plattform and my [PfSense machine](/2016/10/installing-pfsense-on-pc-engines-apu1d4-netgate-apu4/) at home, I ran into a couple of resources:

- [PFSense IPSec VPN connection to GCP](https://blog.paranoidsoftware.com/pfsense-ipsec-vpn-connection-to-azure-aws-and-google-cloud-2/)
- [Cloud VPN -> Creating a VPN](https://cloud.google.com/vpn/docs/how-to/creating-vpns)
- [Cloud VPN -> Advanced Configurations](https://cloud.google.com/vpn/docs/concepts/advanced)
- [IPsec Troubleshooting](https://doc.pfsense.org/index.php/IPsec_Troubleshooting)
- [Routing internet traffic through a site-to-site IPsec tunnel](https://doc.pfsense.org/index.php/Routing_internet_traffic_through_a_site-to-site_IPsec_tunnel)

These resources helped out tremendously.

### Creating a VPN in GCP
First we can go ahead and create a VPN configuration on the GCP side. In the console go to **Hybrid Connectivity** -> **VPN** and click on **Create**. First it will ask you to define the VPN Gateway:

![gcp-create-vpn-p1.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/gcp-create-vpn-p1.png&raw=1)

The shared key can be generated using the command from the above site:

    <> pwgen -s -N 1 -cn 64

And the **Peer IP Address** is the public IP address of the PfServe machine.

#### Confirm the VPN Tunnel Settings
After creating a VPN Gateway, it will also create a VPN Tunnel automatically and check out the state of the tunnel:

![gcp-create-vpn-p2.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/gcp-create-vpn-p2.png&raw=1)

You will notice the firewall rules will get automatically created on the GCP side.

### Create IPSec Tunnel in PfSense
Now let's create the settings on the PfSense machine. From the admin console go to **VPN** -> **IPsec** -> **Tunnels** -> **Phase 1** and fill out all the settings (most of the settings are covered in the above sites):

![ipsec-create-vpn-p2.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/ipsec-create-vpn-p2.png&raw=1)

#### Adding a Phase 2 Configuration
After the Phase 1 configurations are added, add a Phase 2 configuration and set your settings depending on your setup. Here is how my configuration looked like.

![gcp-create-vpn-p3.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/gcp-create-vpn-p3.png&raw=1)


#### Create Firewall Rules to Allow IPSec
On the WAN interface allow the IPSec ports and protocol:

![ipsec-firewall-rule-pf.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/ipsec-firewall-rule-pf.png&raw=1)

Also don't forget to allow communication between the internal subnets (I kind of went crazy and just allowed all the traffic across the IpSec interface):

![ipsec-firewall-rules-pf-2.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/ipsec-firewall-rules-pf-2.png&raw=1)

After you save your configuration and apply it, the tunnel should get established.

### Confirm the Tunnel is established
From the PfSense side, you can go to **Status** -> **IPsec** -> **Overview** and you should see the tunnel established:

![gcp-create-vpn-p4.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/gcp-create-vpn-p4.png&raw=1)

You can also SSH to the PfSense machine and check out the status:

    [2.4.3-RELEASE][root@pf.kar.int]/root: ipsec status
    Shunted Connections:
       bypasslan:  192.168.56.0/24|/0 === 192.168.56.0/24|/0 PASS
    Routed Connections:
            con1{2}:  ROUTED, TUNNEL, reqid 2
            con1{2}:   192.168.56.0/24|/0 === 10.138.0.0/20|/0
    Security Associations (1 up, 0 connecting):
            con1[28]: ESTABLISHED 10 minutes ago, 161.97.231.112[161.97.231.112]...35.199.169.27[35.199.169.27]
            con1{3}:  INSTALLED, TUNNEL, reqid 2, ESP SPIs: cb52019c_i e918c4b9_o
            con1{3}:   192.168.56.0/24|/0 === 10.138.0.0/20|/0

You can also check out the logs:

    [2.4.3-RELEASE][root@pf.kar.int]/root: clog -f /var/log/ipsec.log
    Apr 22 12:30:32 pf ipsec_starter[67724]: Starting strongSwan 5.6.2 IPsec [starter]...
    Apr 22 12:30:32 pf ipsec_starter[67724]: no netkey IPsec stack detected
    Apr 22 12:30:32 pf ipsec_starter[67724]: no KLIPS IPsec stack detected
    Apr 22 12:30:32 pf ipsec_starter[67724]: no known IPsec stack detected, ignoring!
    Apr 22 12:30:32 pf charon: 00[DMN] Starting IKE charon daemon (strongSwan 5.6.2, FreeBSD 11.1-RELEASE-p7, amd64)
    Apr 22 12:30:32 pf charon: 00[KNL] unable to set UDP_ENCAP: Invalid argument
    Apr 22 12:30:32 pf charon: 00[NET] enabling UDP decapsulation for IPv6 on port 4500 failed
    Apr 22 12:30:32 pf charon: 00[CFG] loading unbound resolver config from '/etc/resolv.conf'
    Apr 22 12:30:32 pf charon: 00[CFG] loading unbound trust anchors from '/usr/local/etc/ipsec.d/dnssec.keys'
    Apr 22 12:30:32 pf charon: 00[CFG] ipseckey plugin is disabled
    Apr 22 12:30:32 pf charon: 00[CFG] loading ca certificates from '/usr/local/etc/ipsec.d/cacerts'
    Apr 22 12:30:32 pf charon: 00[CFG] loading aa certificates from '/usr/local/etc/ipsec.d/aacerts'
    Apr 22 12:30:32 pf charon: 00[CFG] loading ocsp signer certificates from '/usr/local/etc/ipsec.d/ocspcerts'
    Apr 22 12:30:32 pf charon: 00[CFG] loading attribute certificates from '/usr/local/etc/ipsec.d/acerts'
    Apr 22 12:30:32 pf charon: 00[CFG] loading crls from '/usr/local/etc/ipsec.d/crls'
    Apr 22 12:30:32 pf charon: 00[CFG] loading secrets from '/var/etc/ipsec/ipsec.secrets'
    Apr 22 12:30:32 pf charon: 00[CFG]   loaded IKE secret for %any 35.199.169.27
    Apr 22 12:30:32 pf charon: 00[CFG]   loaded IKE secret for gcp-ipsec-shared-key
    Apr 22 12:30:32 pf charon: 00[CFG] opening triplet file /usr/local/etc/ipsec.d/triplets.dat failed: No such file or directory
    Apr 22 12:30:32 pf charon: 00[CFG] loaded 0 RADIUS server configurations
    Apr 22 12:30:32 pf charon: 00[LIB] loaded plugins: charon unbound aes des blowfish rc2 sha2 sha1 md4 md5 random nonce x509 revocation constraints pubkey pkcs1 pkcs7 pkcs8 pkcs12 pgp dnskey sshkey ipseckey pem openssl fips-prf curve25519 xcbc cmac hmac curl attr kernel-pfkey kernel-pfroute resolve socket-default stroke vici updown eap-identity eap-sim eap-md5 eap-mschapv2 eap-dynamic eap-radius eap-tls eap-ttls eap-peap xauth-generic xauth-eap whitelist addrblock counters
    Apr 22 12:30:32 pf charon: 00[JOB] spawning 16 worker threads
    Apr 22 12:30:32 pf ipsec_starter[69708]: charon (69720) started after 80 ms
    Apr 22 12:30:32 pf charon: 01[CFG] received stroke: add connection 'bypasslan'
    Apr 22 12:30:32 pf charon: 01[CFG] conn bypasslan
    Apr 22 12:30:32 pf charon: 01[CFG]   left=%any
    Apr 22 12:30:32 pf charon: 01[CFG]   leftsubnet=192.168.56.0/24
    Apr 22 12:30:32 pf charon: 01[CFG]   right=%any
    Apr 22 12:30:32 pf charon: 01[CFG]   rightsubnet=192.168.56.0/24
    Apr 22 12:30:32 pf charon: 01[CFG]   dpddelay=30
    Apr 22 12:30:32 pf charon: 01[CFG]   dpdtimeout=150
    Apr 22 12:30:32 pf charon: 01[CFG]   sha256_96=no
    Apr 22 12:30:32 pf charon: 01[CFG]   mediation=no
    Apr 22 12:30:32 pf charon: 01[CFG] added configuration 'bypasslan'
    Apr 22 12:30:32 pf charon: 01[CFG] received stroke: route 'bypasslan'
    Apr 22 12:30:32 pf charon: 01[CFG] proposing traffic selectors for us:
    Apr 22 12:30:32 pf charon: 01[CFG]  192.168.56.0/24|/0
    Apr 22 12:30:32 pf charon: 01[CFG] proposing traffic selectors for other:
    Apr 22 12:30:32 pf charon: 01[CFG]  192.168.56.0/24|/0
    Apr 22 12:30:32 pf ipsec_starter[69708]: 'bypasslan' shunt PASS policy installed
    Apr 22 12:30:32 pf ipsec_starter[69708]:
    Apr 22 12:30:32 pf charon: 01[CFG] received stroke: add connection 'con1'
    Apr 22 12:30:32 pf charon: 01[CFG] conn con1
    Apr 22 12:30:32 pf charon: 01[CFG]   left=161.97.231.112
    Apr 22 12:30:32 pf charon: 01[CFG]   leftsubnet=192.168.56.0/24
    Apr 22 12:30:32 pf charon: 01[CFG]   leftauth=psk
    Apr 22 12:30:32 pf charon: 01[CFG]   leftid=161.97.231.112
    Apr 22 12:30:32 pf charon: 01[CFG]   right=35.199.169.27
    Apr 22 12:30:32 pf charon: 01[CFG]   rightsubnet=10.138.0.0/20
    Apr 22 12:30:32 pf charon: 01[CFG]   rightauth=psk
    Apr 22 12:30:32 pf charon: 01[CFG]   rightid=35.199.169.27
    Apr 22 12:30:32 pf charon: 01[CFG]   ike=aes256-sha1-modp2048s256!
    Apr 22 12:30:32 pf charon: 01[CFG]   esp=aes128gcm128-sha1!
    Apr 22 12:30:32 pf charon: 01[CFG]   dpddelay=10
    Apr 22 12:30:32 pf charon: 01[CFG]   dpdtimeout=60
    Apr 22 12:30:32 pf charon: 01[CFG]   dpdaction=3
    Apr 22 12:30:32 pf charon: 01[CFG]   sha256_96=no
    Apr 22 12:30:32 pf charon: 01[CFG]   mediation=no
    Apr 22 12:30:32 pf charon: 01[CFG]   keyexchange=ikev2
    Apr 22 12:30:32 pf charon: 01[CFG] added configuration 'con1'
    Apr 22 12:30:32 pf charon: 01[CFG] received stroke: route 'con1'
    Apr 22 12:30:32 pf charon: 01[CFG] proposing traffic selectors for us:
    Apr 22 12:30:32 pf charon: 01[CFG]  192.168.56.0/24|/0
    Apr 22 12:30:32 pf charon: 01[CFG] proposing traffic selectors for other:
    Apr 22 12:30:32 pf charon: 01[CFG]  10.138.0.0/20|/0
    Apr 22 12:30:32 pf charon: 01[CFG] configured proposals: ESP:AES_GCM_16_128/NO_EXT_SEQ
    Apr 22 12:30:32 pf charon: 01[CHD] CHILD_SA con1{1} state change: CREATED => ROUTED
    Apr 22 12:30:32 pf ipsec_starter[69708]: 'con1' routed
    Apr 22 12:30:32 pf ipsec_starter[69708]:
    Apr 22 12:30:32 pf charon: 01[NET] <1> received packet: from 35.199.169.27[500] to 161.97.231.112[500] (884 bytes)
    Apr 22 12:30:32 pf charon: 01[ENC] <1> parsed IKE_SA_INIT request 0 [ SA KE No N(NATD_S_IP) N(NATD_D_IP) N(HASH_ALG) ]
    Apr 22 12:30:32 pf charon: 01[CFG] <1> looking for an ike config for 161.97.231.112...35.199.169.27
    Apr 22 12:30:32 pf charon: 01[CFG] <1>   candidate: %any...%any, prio 24
    Apr 22 12:30:32 pf charon: 01[CFG] <1>   candidate: 161.97.231.112...35.199.169.27, prio 3100
    Apr 22 12:30:32 pf charon: 01[CFG] <1> found matching ike config: 161.97.231.112...35.199.169.27 with prio 3100
    Apr 22 12:30:32 pf charon: 01[IKE] <1> 35.199.169.27 is initiating an IKE_SA
    Apr 22 12:30:32 pf charon: 01[IKE] <1> IKE_SA (unnamed)[1] state change: CREATED => CONNECTING
    Apr 22 12:30:32 pf charon: 01[CFG] <1> selecting proposal:
    Apr 22 12:30:32 pf charon: 01[CFG] <1>   no acceptable ENCRYPTION_ALGORITHM found
    Apr 22 12:30:32 pf charon: 01[CFG] <1> selecting proposal:
    Apr 22 12:30:32 pf charon: 01[CFG] <1>   proposal matches
    Apr 22 12:30:32 pf charon: 01[CFG] <1> received proposals: IKE:AES_GCM_8_128/AES_GCM_8_192/AES_GCM_8_256/AES_GCM_12_128/AES_GCM_12_192/AES_GCM_12_256/AES_GCM_16_128/AES_GCM_16_192/AES_GCM_16_256/PRF_AES128_XCBC/PRF_AES128_CMAC/PRF_HMAC_SHA1/PRF_HMAC_MD5/PRF_HMAC_SHA2_256/PRF_HMAC_SHA2_384/PRF_HMAC_SHA2_512/MODP_2048/MODP_2048_224/MODP_2048_256/MODP_1536/MODP_3072/MODP_4096/MODP_8192/MODP_1024/MODP_1024_160, IKE:AES_CBC_128/AES_CBC_192/AES_CBC_256/3DES_CBC/AES_XCBC_96/AES_CMAC_96/HMAC_SHA1_96/HMAC_MD5_96/HMAC_SHA2_256_128/HMAC_SHA2_384_192/HMAC_SHA2_512_256/PRF_AES128_XCBC/PRF_AES128_CMAC/PRF_HMAC_SHA1/PRF_HMAC_MD5/PRF_HMAC_SHA2_256/PRF_HMAC_SHA2_384/PRF_HMAC_SHA2_512/MODP_2048/MODP_2048_224/MODP_2048_256/MODP_1536/MODP_3072/MODP_4096/MODP_8192/MODP_1024/MODP_1024_160
    Apr 22 12:30:32 pf charon: 01[CFG] <1> configured proposals: IKE:AES_CBC_256/HMAC_SHA1_96/PRF_HMAC_SHA1/MODP_2048_256
    Apr 22 12:30:32 pf charon: 01[CFG] <1> selected proposal: IKE:AES_CBC_256/HMAC_SHA1_96/PRF_HMAC_SHA1/MODP_2048_256
    Apr 22 12:30:32 pf charon: 01[CFG] <1> received supported signature hash algorithms: sha256 sha384 sha512
    Apr 22 12:30:32 pf charon: 01[IKE] <1> DH group MODP_2048 inacceptable, requesting MODP_2048_256
    Apr 22 12:30:32 pf charon: 01[ENC] <1> generating IKE_SA_INIT response 0 [ N(INVAL_KE) ]
    Apr 22 12:30:32 pf charon: 01[NET] <1> sending packet: from 161.97.231.112[500] to 35.199.169.27[500] (38 bytes)
    Apr 22 12:30:32 pf charon: 01[IKE] <1> IKE_SA (unnamed)[1] state change: CONNECTING => DESTROYING
    Apr 22 12:30:32 pf charon: 01[NET] <2> received packet: from 35.199.169.27[500] to 161.97.231.112[500] (884 bytes)
    Apr 22 12:30:32 pf charon: 01[ENC] <2> parsed IKE_SA_INIT request 0 [ SA KE No N(NATD_S_IP) N(NATD_D_IP) N(HASH_ALG) ]
    Apr 22 12:30:32 pf charon: 01[CFG] <2> looking for an ike config for 161.97.231.112...35.199.169.27
    Apr 22 12:30:32 pf charon: 01[CFG] <2>   candidate: %any...%any, prio 24
    Apr 22 12:30:32 pf charon: 01[CFG] <2>   candidate: 161.97.231.112...35.199.169.27, prio 3100
    Apr 22 12:30:32 pf charon: 01[CFG] <2> found matching ike config: 161.97.231.112...35.199.169.27 with prio 3100
    Apr 22 12:30:32 pf charon: 01[IKE] <2> 35.199.169.27 is initiating an IKE_SA
    Apr 22 12:30:32 pf charon: 01[IKE] <2> IKE_SA (unnamed)[2] state change: CREATED => CONNECTING
    Apr 22 12:30:32 pf charon: 01[CFG] <2> selecting proposal:
    Apr 22 12:30:32 pf charon: 01[CFG] <2>   no acceptable ENCRYPTION_ALGORITHM found
    Apr 22 12:30:32 pf charon: 01[CFG] <2> selecting proposal:
    Apr 22 12:30:32 pf charon: 01[CFG] <2>   proposal matches
    Apr 22 12:30:32 pf charon: 01[CFG] <2> received proposals: IKE:AES_GCM_8_128/AES_GCM_8_192/AES_GCM_8_256/AES_GCM_12_128/AES_GCM_12_192/AES_GCM_12_256/AES_GCM_16_128/AES_GCM_16_192/AES_GCM_16_256/PRF_AES128_XCBC/PRF_AES128_CMAC/PRF_HMAC_SHA1/PRF_HMAC_MD5/PRF_HMAC_SHA2_256/PRF_HMAC_SHA2_384/PRF_HMAC_SHA2_512/MODP_2048/MODP_2048_224/MODP_2048_256/MODP_1536/MODP_3072/MODP_4096/MODP_8192/MODP_1024/MODP_1024_160, IKE:AES_CBC_128/AES_CBC_192/AES_CBC_256/3DES_CBC/AES_XCBC_96/AES_CMAC_96/HMAC_SHA1_96/HMAC_MD5_96/HMAC_SHA2_256_128/HMAC_SHA2_384_192/HMAC_SHA2_512_256/PRF_AES128_XCBC/PRF_AES128_CMAC/PRF_HMAC_SHA1/PRF_HMAC_MD5/PRF_HMAC_SHA2_256/PRF_HMAC_SHA2_384/PRF_HMAC_SHA2_512/MODP_2048/MODP_2048_224/MODP_2048_256/MODP_1536/MODP_3072/MODP_4096/MODP_8192/MODP_1024/MODP_1024_160
    Apr 22 12:30:32 pf charon: 01[CFG] <2> configured proposals: IKE:AES_CBC_256/HMAC_SHA1_96/PRF_HMAC_SHA1/MODP_2048_256
    Apr 22 12:30:32 pf charon: 01[CFG] <2> selected proposal: IKE:AES_CBC_256/HMAC_SHA1_96/PRF_HMAC_SHA1/MODP_2048_256
    Apr 22 12:30:32 pf charon: 01[CFG] <2> received supported signature hash algorithms: sha256 sha384 sha512
    Apr 22 12:30:33 pf charon: 01[CFG] <2> sending supported signature hash algorithms: sha256 sha384 sha512 identity
    Apr 22 12:30:33 pf charon: 01[ENC] <2> generating IKE_SA_INIT response 0 [ SA KE No N(NATD_S_IP) N(NATD_D_IP) N(HASH_ALG) N(MULT_AUTH) ]
    Apr 22 12:30:33 pf charon: 01[NET] <2> sending packet: from 161.97.231.112[500] to 35.199.169.27[500] (456 bytes)
    Apr 22 12:30:33 pf charon: 01[NET] <2> received packet: from 35.199.169.27[500] to 161.97.231.112[500] (332 bytes)
    Apr 22 12:30:33 pf charon: 01[ENC] <2> parsed IKE_AUTH request 1 [ IDi N(INIT_CONTACT) IDr AUTH SA TSi TSr N(MULT_AUTH) N(EAP_ONLY) ]
    Apr 22 12:30:33 pf charon: 01[CFG] <2> looking for peer configs matching 161.97.231.112[161.97.231.112]...35.199.169.27[35.199.169.27]
    Apr 22 12:30:33 pf charon: 01[CFG] <2>   candidate "bypasslan", match: 1/1/24 (me/other/ike)
    Apr 22 12:30:33 pf charon: 01[CFG] <2>   candidate "con1", match: 20/20/3100 (me/other/ike)
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> selected peer config 'con1'
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> authentication of '35.199.169.27' with pre-shared key successful
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> authentication of '161.97.231.112' (myself) with pre-shared key
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> successfully created shared key MAC
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> IKE_SA con1[2] established between 161.97.231.112[161.97.231.112]...35.199.169.27[35.199.169.27]
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> IKE_SA con1[2] state change: CONNECTING => ESTABLISHED
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> scheduling reauthentication in 35397s
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> maximum IKE_SA lifetime 35937s
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> looking for a child config for 0.0.0.0/0|/0 === 0.0.0.0/0|/0
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> proposing traffic selectors for us:
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2>  192.168.56.0/24|/0
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> proposing traffic selectors for other:
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2>  10.138.0.0/20|/0
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2>   candidate "con1" with prio 1+1
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> found matching child config "con1" with prio 2
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> selecting proposal:
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2>   proposal matches
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> received proposals: ESP:AES_GCM_16_128/AES_GCM_16_256/AES_GCM_16_192/AES_GCM_12_128/AES_GCM_8_128/AES_CBC_128/AES_CBC_256/AES_CBC_192/HMAC_SHA1_96/HMAC_SHA2_256_128/HMAC_SHA2_512_256/NO_EXT_SEQ
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> configured proposals: ESP:AES_GCM_16_128/NO_EXT_SEQ
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> selected proposal: ESP:AES_GCM_16_128/NO_EXT_SEQ
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> selecting traffic selectors for us:
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2>  config: 192.168.56.0/24|/0, received: 0.0.0.0/0|/0 => match: 192.168.56.0/24|/0
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2> selecting traffic selectors for other:
    Apr 22 12:30:33 pf charon: 01[CFG] <con1|2>  config: 10.138.0.0/20|/0, received: 0.0.0.0/0|/0 => match: 10.138.0.0/20|/0
    Apr 22 12:30:33 pf charon: 01[CHD] <con1|2> CHILD_SA con1{2} state change: CREATED => INSTALLING
    Apr 22 12:30:33 pf charon: 01[CHD] <con1|2>   using AES_GCM_16 for encryption
    Apr 22 12:30:33 pf charon: 01[CHD] <con1|2> adding inbound ESP SA
    Apr 22 12:30:33 pf charon: 01[CHD] <con1|2>   SPI 0xcc3f46b8, src 35.199.169.27 dst 161.97.231.112
    Apr 22 12:30:33 pf charon: 01[CHD] <con1|2> adding outbound ESP SA
    Apr 22 12:30:33 pf charon: 01[CHD] <con1|2>   SPI 0x59f34fe2, src 161.97.231.112 dst 35.199.169.27
    Apr 22 12:30:33 pf charon: 01[IKE] <con1|2> CHILD_SA con1{2} established with SPIs cc3f46b8_i 59f34fe2_o and TS 192.168.56.0/24|/0 === 10.138.0.0/20|/0
    Apr 22 12:30:33 pf charon: 01[CHD] <con1|2> CHILD_SA con1{2} state change: INSTALLING => INSTALLED
    Apr 22 12:30:33 pf charon: 01[ENC] <con1|2> generating IKE_AUTH response 1 [ IDr AUTH N(ESP_TFC_PAD_N) SA TSi TSr N(AUTH_LFT) ]
    Apr 22 12:30:33 pf charon: 01[NET] <con1|2> sending packet: from 161.97.231.112[500] to 35.199.169.27[500] (220 bytes)


And on the GCP side, if you go check out the VPN details, you will see the Tunnel is established:

![gcp-create-vpn-p5.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/gcp-create-vpn-p5.png&raw=1)

If you have [Stackdriver Logging](https://cloud.google.com/logging/) enabled, you can also check out the logs of the VPN Gateway VM:

![gcp-stackdriver-logs-p1.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/gcp-stackdriver-logs-p1.png&raw=1)

Lastly make sure a machine from the internal network can login to a VM running in GCP:

    <> ssh 10.138.0.6
    Welcome to Ubuntu 16.04.4 LTS (GNU/Linux 4.13.0-1011-gcp x86_64)

     * Documentation:  https://help.ubuntu.com
     * Management:     https://landscape.canonical.com
     * Support:        https://ubuntu.com/advantage

      Get cloud support with Ubuntu Advantage Cloud Guest:
        http://www.ubuntu.com/business/services/cloud

    14 packages can be updated.
    0 updates are security updates.

If you check out **pftop** on the PfSense machine you should see the connection established as well:

![pfsense-pftop.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/gcp-pfsense-ipsec/pfsense-pftop.png&raw=1)

Lastly you can also confirm is going through the tunnel, by doing a **tcpdump** on the tunnel interface:

    [2.4.3-RELEASE][root@pf.kar.int]/root: tcpdump -i enc0
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on enc0, link-type ENC (OpenBSD encapsulated IP), capture size 262144 bytes
    14:11:26.528630 (authentic,confidential): SPI 0xc1a39381: IP 192.168.56.151.32964 > 10.138.0.6.ssh: Flags [S], seq 2935568875, win 29200, options [mss 1460,sackOK,TS val 4255537816 ecr 0,nop,wscale 7], length 0
    14:11:27.560091 (authentic,confidential): SPI 0xc1a39381: IP 192.168.56.151.32964 > 10.138.0.6.ssh: Flags [S], seq 2935568875, win 29200, options [mss 1460,sackOK,TS val 4255538849 ecr 0,nop,wscale 7], length 0
    
That should be it.


