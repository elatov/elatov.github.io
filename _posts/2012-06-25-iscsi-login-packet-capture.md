---
title: iSCSI Login in a Packet Capture
author: Karim Elatov
layout: post
permalink: /2012/06/iscsi-login-packet-capture/
dsq_thread_id:
  - 1406849705
categories:
  - Networking
  - VMware
tags:
  - iSCSI
  - iSCSI Initiator
  - iSCSI Target
  - packet capture
  - tshark
  - wireshark
---
What is seen in a packet capture when an ESX iSCSI initiator success fully logs into the iSCSI target? Since iSCSI uses TCP, the first thing that we are going to see is a *3-way TCP hand shake* (More information on 3-way TCP handshake can be found [here](http://www.inetdaemon.com/tutorials/internet/tcp/3-way_handshake.shtml)). Now let's follow the packets:


	$ tshark -r iscsi_login.pcap frame.number==4
	4 2012-04-26 16:12:58.174806 10.131.13.11 -> 10.131.13.10 TCP 57956 3260 57956 > iscsi-target [SYN] Seq=0 Win=65535 [TCP CHECKSUM INCORRECT] Len=0 MSS=1460 WS=16 SACK_PERM=1 TSval=54350554 TSecr=0 11.726356 74


So that is the SYN (if you haven't guessed it yet, the iSCSI iniator IP is 10.131.13.11 and the iSCSI target IP is 10.131.13.10). Next we see the SYN/ACK


	$ tshark -r iscsi_login.pcap frame.number==5
	5 2012-04-26 16:12:58.175156 10.131.13.10 -> 10.131.13.11 TCP 3260 57956 iscsi-target > 57956 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1460 SACK_PERM=1 WS=8 TSval=65212169 TSecr=54350554 11.726706 78


and lastly we see the ACK:


	$ tshark -r iscsi_login.pcap frame.number==6
	6 2012-04-26 16:12:58.175199 10.131.13.11 -> 10.131.13.10 TCP 57956 3260 57956 > iscsi-target [ACK] Seq=1 Ack=1 Win=263536 [TCP CHECKSUM INCORRECT] Len=0 TSval=54350554 TSecr=65212169 11.726749 66


Now that we have the TCP connection established, the iSCSI protocol should start to login. From the [iSCSI RFC](http://tools.ietf.org/html/rfc3720) page:

> **10.12. Login Request**
>
> After establishing a TCP connection between an initiator and a target, the initiator MUST start a Login Phase to gain further access to the target's resources.

Looking at the next packet and just looking at the iSCSI information of the packet we see the following


	$ tshark -O iscsi -V -r iscsi_login.pcap frame.number==7
	Frame 7: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 57956 (57956), Dst Port: iscsi-target (3260), Seq: 1, Ack: 1, Len: 48
	iSCSI (Login Command)
	Opcode: Login Command (0x03)
	1... .... = T: Transit to next login stage
	.0.. .... = C: Text is complete
	.... 01.. = CSG: Operational negotiation (0x01)
	.... ..11 = NSG: Full feature phase (0x03)
	VersionMax: 0x00
	VersionMin: 0x00
	TotalAHSLength: 0x00
	DataSegmentLength: 0x000000e7
	ISID: 00023d000000
	00.. .... = ISID_t: IEEE OUI (0x00)
	..00 0000 = ISID_a: 0x00
	ISID_b: 0x023d
	ISID_c: 0x00
	ISID_d: 0x0000
	TSIH: 0x0000
	InitiatorTaskTag: 0x00000000
	CID: 0x0000
	CmdSN: 0x00000001
	ExpStatSN: 0x00000000


So we are getting a Login command with the code of *0x03*. From the iSCSI RFC:

> **10.2.1.2. Opcode**
>
> The Opcode indicates the type of iSCSI PDU the header encapsulates.
>
> The Opcodes are divided into two categories: initiator opcodes and target opcodes. Initiator opcodes are in PDUs sent by the initiator (request PDUs). Target opcodes are in PDUs sent by the target
> (response PDUs). Initiators MUST NOT use target opcodes and targets MUST NOT use initiator opcodes.
>
> Initiator opcodes defined in this specification are:
>
> 0x00 NOP-Out
> 0x01 SCSI Command (encapsulates a SCSI Command Descriptor Block)
> 0x02 SCSI Task Management function request
> 0x03 Login Request
> 0x04 Text Request
> 0x05 SCSI Data-Out (for WRITE operations)
> 0x06 Logout Request
> 0x10 SNACK Request
> 0x1c-0x1e Vendor specific codes

So we sent a *Login Request*, from the RFC:

> **3.5.3.2. Login Request and Login Response**
>
> Login Requests and Responses are used exclusively during the Login Phase of each connection to set up the session and connection parameters. (The Login Phase consists of a sequence of login
> requests and responses carrying the same Initiator Task Tag.) A connection is identified by an arbitrarily selected connection-ID (CID) that is unique within a session. Similar to the Text Requests and Responses, Login Requests/Responses carry key=value text information with a simple syntax in the data segment.
>
> The Login Phase proceeds through several stages (security negotiation, operational parameter negotiation) that are selected with two binary coded fields in the header - the "current stage" (CSG) and the "next stage" (NSG) with the appearance of the latter being signaled by the "transit" flag (T).
>
> The first Login Phase of a session plays a special role, called the leading login, which determines some header fields (e.g., the version number, the maximum number of connections, and the session
> identification).

Also we see that we have the *T* flag set:


	Opcode: Login Command (0x03)
	1... .... = T: Transit to next login stage
	.0.. .... = C: Text is complete


From the RFC:

> 10.12.1. T (Transit) Bit
>
> If set to 1, indicates that the initiator is ready to transit to the next stage.
>
> If the T bit is set to 1 and NSG is FullFeaturePhase, then this also indicates that the initiator is ready for the Final Login Response (see Chapter 5).

So we sent a *Login Request* and we are ready to send more data, now looking at the next packet:


	$ tshark -O data -V -r iscsi_login.pcap frame.number==8
	Frame 8: 298 bytes on wire (2384 bits), 298 bytes captured (2384 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 57956 (57956), Dst Port: iscsi-target (3260), Seq: 49, Ack: 1, Len: 232
	Data (232 bytes)
	0000 49 6e 69 74 69 61 74 6f 72 4e 61 6d 65 3d 69 71 InitiatorName=iq
	0010 6e 2e 31 39 39 38 2d 30 31 2e 63 6f 6d 2e 76 6d n.1998-01.com.vm
	0020 77 61 72 65 3a 77 64 63 2d 74 73 65 2d 68 31 37 ware:wdc-tse-h17
	0030 31 2d 33 63 30 30 64 39 63 65 00 53 65 73 73 69 1-3c00d9ce.Sessi
	0040 6f 6e 54 79 70 65 3d 44 69 73 63 6f 76 65 72 79 onType=Discovery
	0050 00 48 65 61 64 65 72 44 69 67 65 73 74 3d 4e 6f .HeaderDigest=No
	0060 6e 65 00 44 61 74 61 44 69 67 65 73 74 3d 4e 6f ne.DataDigest=No
	0070 6e 65 00 44 65 66 61 75 6c 74 54 69 6d 65 32 57 ne.DefaultTime2W
	0080 61 69 74 3d 30 00 44 65 66 61 75 6c 74 54 69 6d ait=0.DefaultTim
	0090 65 32 52 65 74 61 69 6e 3d 30 00 49 46 4d 61 72 e2Retain=0.IFMar
	00a0 6b 65 72 3d 4e 6f 00 4f 46 4d 61 72 6b 65 72 3d ker=No.OFMarker=
	00b0 4e 6f 00 45 72 72 6f 72 52 65 63 6f 76 65 72 79 No.ErrorRecovery
	00c0 4c 65 76 65 6c 3d 30 00 4d 61 78 52 65 63 76 44 Level=0.MaxRecvD
	00d0 61 74 61 53 65 67 6d 65 6e 74 4c 65 6e 67 74 68 ataSegmentLength
	00e0 3d 33 32 37 36 38 00 00 =32768..
	Data: 496e69746961746f724e616d653d69716e2e313939382d30...
	[Length: 232]


We are now sending the login parameters, from the above packet we can see that we sent the following:

1.  <span style="line-height: 22px;">InitiatorName<br /> </span>
2.  <span style="line-height: 22px;">SessionType</span>
3.  <span style="line-height: 22px;">HeaderDigest</span>
4.  <span style="line-height: 22px;">DataDigest</span>
5.  <span style="line-height: 22px;">DefaultTime2Wait</span>
6.  <span style="line-height: 22px;">IFMarker</span>
7.  <span style="line-height: 22px;">OFMarker</span>
8.  <span style="line-height: 22px;">ErrorRecovery</span>
9.  <span style="line-height: 22px;">MaxRecvDataSegmentLength</span>

More information regarding each parameter can be seen in the RFC:

> 12. Login/Text Operational Text Keys. . . . . . . . . . . . . . . 187
> 12.1. HeaderDigest and DataDigest. . . . . . . . . . . . . . 188
> 12.2. MaxConnections . . . . . . . . . . . . . . . . . . . . 190
> 12.3. SendTargets. . . . . . . . . . . . . . . . . . . . . . 191
> 12.4. TargetName . . . . . . . . . . . . . . . . . . . . . . 191
> 12.5. InitiatorName. . . . . . . . . . . . . . . . . . . . . 192
> 12.6. TargetAlias. . . . . . . . . . . . . . . . . . . . . . 192
> 12.7. InitiatorAlias . . . . . . . . . . . . . . . . . . . . 193
> 12.8. TargetAddress. . . . . . . . . . . . . . . . . . . . . 193
> 12.9. TargetPortalGroupTag . . . . . . . . . . . . . . . . . 194
> 12.10. InitialR2T . . . . . . . . . . . . . . . . . . . . . . 194
> 12.11. ImmediateData. . . . . . . . . . . . . . . . . . . . . 195
> 12.12. MaxRecvDataSegmentLength . . . . . . . . . . . . . . . 196
> 12.13. MaxBurstLength . . . . . . . . . . . . . . . . . . . . 196
> 12.14. FirstBurstLength . . . . . . . . . . . . . . . . . . . 197
> 12.15. DefaultTime2Wait . . . . . . . . . . . . . . . . . . . 197
> 12.16. DefaultTime2Retain . . . . . . . . . . . . . . . . . . 198
> 12.17. MaxOutstandingR2T. . . . . . . . . . . . . . . . . . . 198
> 12.18. DataPDUInOrder . . . . . . . . . . . . . . . . . . . . 198
> 12.19. DataSequenceInOrder. . . . . . . . . . . . . . . . . . 199
> 12.20. ErrorRecoveryLevel . . . . . . . . . . . . . . . . . . 199
> 12.21. SessionType. . . . . . . . . . . . . . . . . . . . . . 200
> 12.22. The Private or Public Extension Key Format . . . . . . 200

After the login request has been sent the iSCSI target then respond with a Login Response:

> The target can answer the login in the following ways:
>
> - Login Response with Login reject. This is an immediate rejection from the target that causes the connection to terminate and the session to terminate if this is the first (or only) connection of a new session. The T bit and the CSG and NSG fields are reserved.
> - Login Response with Login Accept as a final response (T bit set to 1 and the NSG in both request and response are set to FullFeaturePhase). The response includes the protocol version supported by the target and the session ID, and may include iSCSI operational or security parameters (that depend on the current stage).
> - Login Response with Login Accept as a partial response (NSG not set to FullFeaturePhase in both request and response) that indicates the start of a negotiation sequence. The response includes the protocol version supported by the target and either security or iSCSI parameters (when no security mechanism is chosen) supported by the target.

Here is what we see in the packet capture:


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==11
	Frame 11: 290 bytes on wire (2320 bits), 290 bytes captured (2320 bits)
	Ethernet II, Src: Vmware_8c:54:94 (00:50:56:8c:54:94), Dst: Vmware_73:16:b1 (00:50:56:73:16:b1)
	Internet Protocol Version 4, Src: 10.131.13.10 (10.131.13.10), Dst: 10.131.13.11 (10.131.13.11)
	Transmission Control Protocol, Src Port: iscsi-target (3260), Dst Port: 57956 (57956), Seq: 1, Ack: 281, Len: 224
	iSCSI (Login Response)
	Opcode: Login Response (0x23)
	1... .... = T: Transit to next login stage
	.0.. .... = C: Text is complete
	.... 01.. = CSG: Operational negotiation (0x01)
	.... ..11 = NSG: Full feature phase (0x03)
	VersionMax: 0x00
	VersionActive: 0x00
	TotalAHSLength: 0x00
	DataSegmentLength: 0x000000ad
	ISID: 00023d000000
	00.. .... = ISID_t: IEEE OUI (0x00)
	..00 0000 = ISID_a: 0x00
	ISID_b: 0x023d
	ISID_c: 0x00
	ISID_d: 0x0000
	TSIH: 0x000c
	InitiatorTaskTag: 0x00000000
	StatSN: 0x00000000
	ExpCmdSN: 0x00000001
	MaxCmdSN: 0x0000001f
	Status: Success (0x0000)
	Key/Value Pairs
	KeyValue: HeaderDigest=None
	KeyValue: DataDigest=None
	KeyValue: DefaultTime2Wait=2
	KeyValue: DefaultTime2Retain=0
	KeyValue: IFMarker=No
	KeyValue: OFMarker=No
	KeyValue: ErrorRecoveryLevel=0
	KeyValue: TargetPortalGroupTag=1
	KeyValue: MaxRecvDataSegmentLength=65536
	Padding: 000000


We can see that all the key/value pairs were negotiated successfully and this was a *Login Response with Login Accept as a final response*. Next we see a *Text Command*:


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==12
	Frame 12: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 57956 (57956), Dst Port: iscsi-target (3260), Seq: 281, Ack: 225, Len: 48
	iSCSI (Text Command)
	Opcode: Text Command (0x04)
	.0.. .... = I: Queued delivery
	Flags: 0x80
	1... .... = F: Final PDU in sequence
	.0.. .... = C: Text is complete
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000010
	LUN: 0000000000000000
	InitiatorTaskTag: 0x00000001
	TargetTransferTag: 0xffffffff
	CmdSN: 0x00000001
	ExpStatSN: 0x00000001


The *Text Command* is *0x04* and from the above snippet of the RFC we can see that it's a *Text Request*:

> **3.5.3.1. Text Request and Text Response**
>
> Text requests and responses are designed as a parameter negotiation vehicle and as a vehicle for future extension. In the data segment, Text Requests/Responses carry text information using a simple "key=value" syntax.
>
> Text Request/Responses may form extended sequences using the same Initiator Task Tag. The initiator uses the F (Final) flag bit in the text request header to indicate its readiness to terminate a sequence. The target uses the F (Final) flag bit in the text response header to indicate its consent to sequence termination.
>
> Text Request and Responses also use the Target Transfer Tag to indicate continuation of an operation or a new beginning. A target that wishes to continue an operation will set the Target Transfer Tag in a Text Response to a value different from the default 0xffffffff.
>
> An initiator willing to continue will copy this value into the TargetTransfer Tag of the next Text Request. If the initiator wants to restart the current target negotiation (start fresh) will set the Target Transfer Tag to 0xffffffff.
>
> Although a complete exchange is always started by the initiator,specific parameter negotiations may be initiated by the initiator or target.

So now that we have connected to the target we are going to ask some information and that is what a *Text command* does, here is what we see in the next packet:


	$ tshark -r iscsi_login.pcap -x frame.number==13
	13 2012-04-26 16:12:58.176391 10.131.13.11 -> 10.131.13.10 TCP 57956 3260 57956 > iscsi-target [PSH, ACK] Seq=329 Ack=225 Win=263536 [TCP CHECKSUM INCORRECT] Len=16 TSval=54350554 TSecr=65212169 11.727941 82

	0000 00 50 56 8c 54 94 00 50 56 73 16 b1 08 00 45 00 .PV.T..PVs....E.
	0010 00 44 bb f1 40 00 40 06 4f a8 0a 83 0d 0b 0a 83 .D..@.@.O.......
	0020 0d 0a e2 64 0c bc 14 8c e5 11 e2 d8 78 e2 80 18 ...d........x...
	0030 40 57 2f 51 00 00 01 01 08 0a 03 3d 52 da 03 e3 @W/Q.......=R...
	0040 0f 09 53 65 6e 64 54 61 72 67 65 74 73 3d 41 6c ..SendTargets=Al
	0050 6c 00 l.


For our *Text Request* we have sent a *SendTargets=All*:

> **3.3. iSCSI Session Types**
>
> iSCSI defines two types of sessions:
>
> a) Normal operational session - an unrestricted session.
> b) Discovery-session - a session only opened for target discovery. The target MUST ONLY accept text requests with the SendTargets key and a logout request with the reason "close the session". All other requests MUST be rejected.
> ...
> ...
> **Appendix D. SendTargets Operation**
>
> To reduce the amount of configuration required on an initiator, iSCSI provides the SendTargets text request. The initiator uses the SendTargets request to get a list of targets to which it may have access, as well as the list of addresses (IP address and TCP port) on which these targets may be accessed.
>
> To make use of SendTargets, an initiator must first establish one of two types of sessions. If the initiator establishes the session using the key "SessionType=Discovery", the session is a discovery session, and a target name does not need to be specified. Otherwise, the session is a normal, operational session. The end Targets command MUST only be sent during the Full Feature Phase of a normal or discovery session.
> ...
> ...
> A SendTargets command consists of a single Text request PDU. This PDU contains exactly one text key and value. The text key MUST be SendTargets. The expected response depends upon the value, as well as whether the session is a discovery or operational session.
>
> The value must be one of:
>
> All
>
> The initiator is requesting that information on all relevant targets known to the implementation be returned. This value MUST be supported on a discovery session, and MUST NOT be supported on an operational session.

Since I am using a discovery session (In ESX "Dynamic Discovery"), this makes perfect sense. Next we get a *Text Response*


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==15
	Frame 15: 202 bytes on wire (1616 bits), 202 bytes captured (1616 bits)
	Ethernet II, Src: Vmware_8c:54:94 (00:50:56:8c:54:94), Dst: Vmware_73:16:b1 (00:50:56:73:16:b1)
	Internet Protocol Version 4, Src: 10.131.13.10 (10.131.13.10), Dst: 10.131.13.11 (10.131.13.11)
	Transmission Control Protocol, Src Port: iscsi-target (3260), Dst Port: 57956 (57956), Seq: 225, Ack: 345, Len: 136
	iSCSI (Text Response)
	Opcode: Text Response (0x24)
	Flags: 0x80
	1... .... = F: Final PDU in sequence
	.0.. .... = C: Text is complete
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000056
	LUN: 0000000000000000
	InitiatorTaskTag: 0x00000001
	TargetTransferTag: 0xffffffff
	StatSN: 0x00000001
	ExpCmdSN: 0x00000002
	MaxCmdSN: 0x00000020
	Key/Value Pairs
	KeyValue: TargetName=iqn.1992-05.com.emc:bb0050568c51390000-2
	KeyValue: TargetAddress=10.131.13.10:3260,1
	Padding: 0000


We can see that in the response we received the *TargetName* and *TargetAddress* of what our iSCSI initiator has access to, and this is also expected; per the RFC:

> The response to this command (SendTargets=All) is a text response that contains a list of zero or more targets and, optionally, their addresses. Each target is returned as a target record. A target record begins with the TargetName text key, followed by a list of TargetAddress text keys, and bounded by the end of the text response or the next TargetName key, which begins a new record. No text keys other than TargetName and TargetAddress are permitted within a SendTargets response.
> ...
> ...
> Examples:
>
> This example is the SendTargets response from a single target that has no other interface ports.
>
> Initiator sends text request that contains:
>
> SendTargets=All
>
> Target sends a text response that contains:
>
> TargetName=iqn.1993-11.com.example:diskarray.sn.8675309
>
> All the target had to return in the simple case was the target name. It is assumed by the initiator that the IP address and TCP port for this target are the same as used on the current connection to the
> default iSCSI target.

We got our targets, and now we actually send a *Logout Request*:


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==16
	Frame 16: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 57956 (57956), Dst Port: iscsi-target (3260), Seq: 345, Ack: 361, Len: 48
	iSCSI (Logout Command)
	Opcode: Logout Command (0x06)
	.1.. .... = I: Immediate delivery
	.000 0000 = Reason: Close session (0x00)
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000000
	InitiatorTaskTag: 0x00000002
	CID: 0x0000
	CmdSN: 0x00000002
	ExpStatSN: 0x00000002


From the RFC:

> **10.14. Logout Request**
>
> The Logout Request is used to perform a controlled closing of a connection. An initiator MAY use a Logout Request to remove a connection from a session or to close an entire session. After sending the Logout Request PDU, an initiator MUST NOT send any new iSCSI requests on the closing connection. If the Logout Request is intended to close the session, new iSCSI requests MUST NOT be sent on any of the connections participating in the session. When receiving a Logout Request with the reason code of "close the connection" or "close the session", the target MUST terminate all pending commands, whether acknowledged via ExpCmdSN or not, on that connection or session respectively. When receiving a Logout Request with the reason code "remove connection for recovery", the target MUST discard all requests not yet acknowledged via ExpCmdSN that were issued on the specified connection, and suspend all data/status/R2T transfers on behalf of pending commands on the specified connection.

Why did we get a *Logout Request*? since this was the first login this makes sense:

> The first Login Phase of a session plays a special role, called the leading login, which determines some header fields (e.g., the version number, the maximum number of connections, and the session identification). The CmdSN initial value is also set by the leading login. StatSN for each connection is initiated by the connection login. A login request may indicate an implied logout (cleanup) of the connection to be logged in (a connection restart) by using the same Connection ID (CID) as an existing connection, as well as the same session identifying elements of the session to which the old connection was associated.

After the *Logout Request* we see a *Logout Response*:


	$ tshark -r iscsi -V -O iscsi_login.pcap frame.number==17
	Frame 17: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_8c:54:94 (00:50:56:8c:54:94), Dst: Vmware_73:16:b1 (00:50:56:73:16:b1)
	Internet Protocol Version 4, Src: 10.131.13.10 (10.131.13.10), Dst: 10.131.13.11 (10.131.13.11)
	Transmission Control Protocol, Src Port: iscsi-target (3260), Dst Port: 57956 (57956), Seq: 361, Ack: 393, Len: 48
	iSCSI (Logout Response)
	Opcode: Logout Response (0x26)
	Response: Connection closed successfully (0x00)
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000000
	InitiatorTaskTag: 0x00000002
	StatSN: 0x00000002
	ExpCmdSN: 0x00000002
	MaxCmdSN: 0x00000020
	Time2Wait: 0x0002
	Time2Retain: 0x0000


And we can see that our logout (connection close) was successful. After that we see a TCP connection tear-down and a reset:

> **3.2.5. iSCSI Connection Termination**
>
> An iSCSI connection may be terminated by use of a transport connection shutdown or a transport reset. Transport reset is assumed to be an exceptional event. Graceful TCP connection shutdowns are done by sending TCP FINs. A graceful transport connection shutdown SHOULD only be initiated by either party when the connection is not in iSCSI Full Feature Phase. A target MAY terminate a Full Feature Phase connection on internal exception events, but it SHOULD announce the fact through an Asynchronous Message PDU. Connection termination with outstanding commands may require recovery actions.

From the packet capture we see this:


	$ tshark -r iscsi_login.pcap frame.number==18
	18 2012-04-26 16:12:58.183649 10.131.13.10 > 10.131.13.11 TCP 3260 57956 iscsi-target > 57956 [FIN, ACK] Seq=409 Ack=393 Win=196608 Len=0 TSval=65212169 TSecr=54350554 11.735199 66
	$ tshark -r iscsi_login.pcap frame.number==19
	19 2012-04-26 16:12:58.183667 10.131.13.11 -> 10.131.13.10 TCP 57956 3260 57956 > iscsi-target [ACK] Seq=393 Ack=410 Win=263488 [TCP CHECKSUM INCORRECT] Len=0 TSval=54350555 TSecr=65212169 11.735217 66
	$ tshark -r iscsi_login.pcap frame.number==20
	20 2012-04-26 16:12:58.183698 10.131.13.11 -> 10.131.13.10 TCP 57956 3260 57956 > iscsi-target [RST, ACK] Seq=393 Ack=410 Win=263536 [TCP CHECKSUM INCORRECT] Len=0 TSval=54350555 TSecr=65212169 11.735248 66


Since we are actually not done, we keep the connection alive by using the *NOP-out* and *NOP-in* packets:

> **3.5.3.6. NOP-Out Request and NOP-In Response**
>
> This request/response pair may be used by an initiator and target as a "ping" mechanism to verify that a connection/session is still active and all of its components are operational. Such a ping may be
> triggered by the initiator or target. The triggering party indicates that it wants a reply by setting a value different from the default 0xffffffff in the corresponding Initiator/Target Transfer Tag.
>
> NOP-In/NOP-Out may also be used "unidirectional" to convey to the initiator/target command, status or data counter values when there is no other "carrier" and there is a need to update the initiator/
> target.

Again from the packet capture:


	$ tshark -r iscsi_login.pcap frame.number==21
	21 2012-04-26 16:13:01.622104 10.131.13.11 -> 10.131.13.10 iSCSI 57742 3260 NOP Out 15.173654 114
	$ tshark -r iscsi frame.number==22
	22 2012-04-26 16:13:01.622613 10.131.13.10 -> 10.131.13.11 iSCSI 3260 57742 NOP In 15.174163 114


Then we do the same thing all over again. First re-establish the 3-way tcp handshake:


	$ tshark -r iscsi_login.pcap frame.number==24
	24 2012-04-26 16:13:02.758405 10.131.13.11 -> 10.131.13.10 TCP 58219 3260 58219 > iscsi-target [SYN] Seq=0 Win=65535 [TCP CHECKSUM INCORRECT] Len=0 MSS=1460 WS=16 SACK_PERM=1 TSval=54351012 TSecr=0 16.309955 74
	$ tshark -r iscsi_login.pcap frame.number==25
	25 2012-04-26 16:13:02.758775 10.131.13.10 -> 10.131.13.11 TCP 3260 58219 iscsi-target > 58219 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1460 SACK_PERM=1 WS=8 TSval=65212192 TSecr=54351012 16.310325 78
	$ tshark -r iscsi_login.pcap frame.number==26
	26 2012-04-26 16:13:02.758838 10.131.13.11 -> 10.131.13.10 TCP 58219 3260 58219 > iscsi-target [ACK] Seq=1 Ack=1 Win=263536 [TCP CHECKSUM INCORRECT] Len=0 TSval=54351012 TSecr=65212192 16.310388 66


We then see the *Login Request* with the login parameters:


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==27
	Frame 27: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 58219 (58219), Dst Port: iscsi-target (3260), Seq: 1, Ack: 1, Len: 48
	iSCSI (Login Command)
	Opcode: Login Command (0x03)
	1... .... = T: Transit to next login stage
	.0.. .... = C: Text is complete
	.... 01.. = CSG: Operational negotiation (0x01)
	.... ..11 = NSG: Full feature phase (0x03)
	VersionMax: 0x00
	VersionMin: 0x00
	TotalAHSLength: 0x00
	DataSegmentLength: 0x000000e7
	ISID: 00023d000000
	00.. .... = ISID_t: IEEE OUI (0x00)
	..00 0000 = ISID_a: 0x00
	ISID_b: 0x023d
	ISID_c: 0x00
	ISID_d: 0x0000
	TSIH: 0x0000
	InitiatorTaskTag: 0x00000000
	CID: 0x0000
	CmdSN: 0x00000001
	ExpStatSN: 0x00000000

	$ tshark -r iscsi_login.pcap -V -O data frame.number==28
	Frame 28: 298 bytes on wire (2384 bits), 298 bytes captured (2384 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 58219 (58219), Dst Port: iscsi-target (3260), Seq: 49, Ack: 1, Len: 232
	Data (232 bytes)

	0000 49 6e 69 74 69 61 74 6f 72 4e 61 6d 65 3d 69 71 InitiatorName=iq
	0010 6e 2e 31 39 39 38 2d 30 31 2e 63 6f 6d 2e 76 6d n.1998-01.com.vm
	0020 77 61 72 65 3a 77 64 63 2d 74 73 65 2d 68 31 37 ware:wdc-tse-h17
	0030 31 2d 33 63 30 30 64 39 63 65 00 53 65 73 73 69 1-3c00d9ce.Sessi
	0040 6f 6e 54 79 70 65 3d 44 69 73 63 6f 76 65 72 79 onType=Discovery
	0050 00 48 65 61 64 65 72 44 69 67 65 73 74 3d 4e 6f .HeaderDigest=No
	0060 6e 65 00 44 61 74 61 44 69 67 65 73 74 3d 4e 6f ne.DataDigest=No
	0070 6e 65 00 44 65 66 61 75 6c 74 54 69 6d 65 32 57 ne.DefaultTime2W
	0080 61 69 74 3d 30 00 44 65 66 61 75 6c 74 54 69 6d ait=0.DefaultTim
	0090 65 32 52 65 74 61 69 6e 3d 30 00 49 46 4d 61 72 e2Retain=0.IFMar
	00a0 6b 65 72 3d 4e 6f 00 4f 46 4d 61 72 6b 65 72 3d ker=No.OFMarker=
	00b0 4e 6f 00 45 72 72 6f 72 52 65 63 6f 76 65 72 79 No.ErrorRecovery
	00c0 4c 65 76 65 6c 3d 30 00 4d 61 78 52 65 63 76 44 Level=0.MaxRecvD
	00d0 61 74 61 53 65 67 6d 65 6e 74 4c 65 6e 67 74 68 ataSegmentLength
	00e0 3d 33 32 37 36 38 00 00 =32768..

	Data: 496e69746961746f724e616d653d69716e2e313939382d30...
	[Length: 232]


Then we get the *Login Response*:


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==31
	Frame 31: 290 bytes on wire (2320 bits), 290 bytes captured (2320 bits)
	Ethernet II, Src: Vmware_8c:54:94 (00:50:56:8c:54:94), Dst: Vmware_73:16:b1 (00:50:56:73:16:b1)
	Internet Protocol Version 4, Src: 10.131.13.10 (10.131.13.10), Dst: 10.131.13.11 (10.131.13.11)
	Transmission Control Protocol, Src Port: iscsi-target (3260), Dst Port: 58219 (58219), Seq: 1, Ack: 281, Len: 224
	iSCSI (Login Response)
	Opcode: Login Response (0x23)
	1... .... = T: Transit to next login stage
	.0.. .... = C: Text is complete
	.... 01.. = CSG: Operational negotiation (0x01)
	.... ..11 = NSG: Full feature phase (0x03)
	VersionMax: 0x00
	VersionActive: 0x00
	TotalAHSLength: 0x00
	DataSegmentLength: 0x000000ad
	ISID: 00023d000000
	00.. .... = ISID_t: IEEE OUI (0x00)
	..00 0000 = ISID_a: 0x00
	ISID_b: 0x023d
	ISID_c: 0x00
	ISID_d: 0x0000
	TSIH: 0x000d
	InitiatorTaskTag: 0x00000000
	StatSN: 0x00000000
	ExpCmdSN: 0x00000001
	MaxCmdSN: 0x0000001f
	Status: Success (0x0000)
	Key/Value Pairs
	KeyValue: HeaderDigest=None
	KeyValue: DataDigest=None
	KeyValue: DefaultTime2Wait=2
	KeyValue: DefaultTime2Retain=0
	KeyValue: IFMarker=No
	KeyValue: OFMarker=No
	KeyValue: ErrorRecoveryLevel=0
	KeyValue: TargetPortalGroupTag=1
	KeyValue: MaxRecvDataSegmentLength=65536
	Padding: 000000


After that the initiator sends *Text Request* to get all the available targets with a *SendTargets=All* command:


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==32
	Frame 32: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 58219 (58219), Dst Port: iscsi-target (3260), Seq: 281, Ack: 225, Len: 48
	iSCSI (Text Command)
	Opcode: Text Command (0x04)
	.0.. .... = I: Queued delivery
	Flags: 0x80
	1... .... = F: Final PDU in sequence
	.0.. .... = C: Text is complete
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000010
	LUN: 0000000000000000
	InitiatorTaskTag: 0x00000001
	TargetTransferTag: 0xffffffff
	CmdSN: 0x00000001
	ExpStatSN: 0x00000001

	$ tshark -r iscsi_login.pcap -x frame.number==33
	33 2012-04-26 16:13:02.760053 10.131.13.11 -> 10.131.13.10 TCP 58219 3260 58219 > iscsi-target [PSH, ACK] Seq=329 Ack=225 Win=263536 [TCP CHECKSUM INCORRECT] Len=16 TSval=54351012 TSecr=65212192 16.311603 82

	0000 00 50 56 8c 54 94 00 50 56 73 16 b1 08 00 45 00 .PV.T..PVs....E.
	0010 00 44 bc 8b 40 00 40 06 4f 0e 0a 83 0d 0b 0a 83 .D..@.@.O.......
	0020 0d 0a e3 6b 0c bc fa d4 92 15 e2 e2 3c e2 80 18 ...k........<...
	0030 40 57 2f 51 00 00 01 01 08 0a 03 3d 54 a4 03 e3 @W/Q.......=T...
	0040 0f 20 53 65 6e 64 54 61 72 67 65 74 73 3d 41 6c . SendTargets=Al
	0050 6c 00 l.


Then we get a *Text Response* from the *Text Request* with the available targets:


	Frame 35: 202 bytes on wire (1616 bits), 202 bytes captured (1616 bits)
	Ethernet II, Src: Vmware_8c:54:94 (00:50:56:8c:54:94), Dst: Vmware_73:16:b1 (00:50:56:73:16:b1)
	Internet Protocol Version 4, Src: 10.131.13.10 (10.131.13.10), Dst: 10.131.13.11 (10.131.13.11)
	Transmission Control Protocol, Src Port: iscsi-target (3260), Dst Port: 58219 (58219), Seq: 225, Ack: 345, Len: 136
	iSCSI (Text Response)
	Opcode: Text Response (0x24)
	Flags: 0x80
	1... .... = F: Final PDU in sequence
	.0.. .... = C: Text is complete
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000056
	LUN: 0000000000000000
	InitiatorTaskTag: 0x00000001
	TargetTransferTag: 0xffffffff
	StatSN: 0x00000001
	ExpCmdSN: 0x00000002
	MaxCmdSN: 0x00000020
	Key/Value Pairs
	KeyValue: TargetName=iqn.1992-05.com.emc:bb0050568c51390000-2
	KeyValue: TargetAddress=10.131.13.10:3260,1
	Padding: 0000


Then we logout:


	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==36
	Frame 36: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_73:16:b1 (00:50:56:73:16:b1), Dst: Vmware_8c:54:94 (00:50:56:8c:54:94)
	Internet Protocol Version 4, Src: 10.131.13.11 (10.131.13.11), Dst: 10.131.13.10 (10.131.13.10)
	Transmission Control Protocol, Src Port: 58219 (58219), Dst Port: iscsi-target (3260), Seq: 345, Ack: 361, Len: 48
	iSCSI (Logout Command)
	Opcode: Logout Command (0x06)
	.1.. .... = I: Immediate delivery
	.000 0000 = Reason: Close session (0x00)
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000000
	InitiatorTaskTag: 0x00000002
	CID: 0x0000
	CmdSN: 0x00000002
	ExpStatSN: 0x00000002

	$ tshark -r iscsi_login.pcap -V -O iscsi frame.number==37
	Frame 37: 114 bytes on wire (912 bits), 114 bytes captured (912 bits)
	Ethernet II, Src: Vmware_8c:54:94 (00:50:56:8c:54:94), Dst: Vmware_73:16:b1 (00:50:56:73:16:b1)
	Internet Protocol Version 4, Src: 10.131.13.10 (10.131.13.10), Dst: 10.131.13.11 (10.131.13.11)
	Transmission Control Protocol, Src Port: iscsi-target (3260), Dst Port: 58219 (58219), Seq: 361, Ack: 393, Len: 48
	iSCSI (Logout Response)
	Opcode: Logout Response (0x26)
	Response: Connection closed successfully (0x00)
	TotalAHSLength: 0x00
	DataSegmentLength: 0x00000000
	InitiatorTaskTag: 0x00000002
	StatSN: 0x00000002
	ExpCmdSN: 0x00000002
	MaxCmdSN: 0x00000020
	Time2Wait: 0x0002
	Time2Retain: 0x0000


Then finally we see the tear down of the TCP connection:


	 Seq=409 Ack=393 Win=196608 Len=0 TSval=65212192 TSecr=54351013 16.319255 66
	$ tshark -r iscsi frame.number==39
	39 2012-04-26 16:13:02.767712 10.131.13.11 -> 10.131.13.10 TCP 58219 3260 58219 > iscsi-target [ACK] Seq=393 Ack=410 Win=263488 [TCP CHECKSUM INCORRECT] Len=0 TSval=54351013 TSecr=65212192 16.319262 66
	$ tshark -r iscsi frame.number==40
	40 2012-04-26 16:13:02.767751 10.131.13.11 -> 10.131.13.10 TCP 58219 3260 58219 > iscsi-target [RST, ACK] Seq=393 Ack=410 Win=263536 [TCP CHECKSUM INCORRECT] Len=0 TSval=54351013 TSecr=65212192 16.319301 66


At this point we have gone through a successful login phase and now we will see commands pertaining to LUN characteristics. They will look something like this:


	$ tshark -r iscsi frame.number==41
	41 2012-04-26 16:13:02.794032 10.131.13.11 -> 10.131.13.10 iSCSI 57742 3260 SCSI: Report LUNs LUN: 0x00 16.345582 114
	$ tshark -r iscsi frame.number==42
	42 2012-04-26 16:13:02.794557 10.131.13.10 -> 10.131.13.11 iSCSI 3260 57742 SCSI: Data In LUN: 0x00 (Report LUNs Response Data) SCSI: Response LUN: 0x00 (Report LUNs) (Good) 16.346107 130


At this point the iSCSI protocol will get pretty chatty and if you loaded the packet capture into wireshark, it will look something like this:

![iscsi_1](https://github.com/elatov/uploads/raw/master/2012/04/iscsi_1.png)

![iscsi_2](https://github.com/elatov/uploads/raw/master/2012/04/iscsi_2.png)

You can also get a summary of all the iSCSI commands in a packet capture using tshark (starting with version [1.6](http://www.wireshark.org/news/20110607.html) ):


	$ tshark -r iscsi_login.pcap -q -z scsi,srt,0,ip.addr==10.131.13.10

	===========================================================
	SCSI SBC (disk) SRT Statistics:
	Filter: ip.addr==10.131.13.10
	Procedure Calls Min SRT Max SRT Avg SRT
	Test Unit Ready 1 0.000379 0.000379 0.000379
	Inquiry 18 0.000321 0.001858 0.000524
	Reserve(6) 4 0.000321 0.000365 0.000346
	Release(6) 4 0.000336 0.000373 0.000357
	Mode Sense(6) 6 0.000333 0.000409 0.000361
	Read Capacity(10) 5 0.000359 0.000486 0.000401
	Read(10) 30 0.001031 0.137482 0.012604
	Write(10) 11 0.001825 0.009923 0.007988
	Report LUNs 1 0.000525 0.000525 0.000525
	===========================================================


For anyone that is interested, here is a [link](https://github.com/elatov/uploads/raw/master/2012/06/iscsi_login.pcap) to the packet capture that I grabbed during the iSCSI login process.

### Related Posts

- [HTTP Based Data Transfers from Windows 8 VM to Linux Physical Machine are Corrupted](/2013/01/http-based-data-transfer-from-windows-8-vm-to-linux-physical-machine-gets-corrupted/)

