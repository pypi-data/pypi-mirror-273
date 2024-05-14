# How to install sshanalysis on Linux
This research is under review.

sshanalysis has been downloaded by 484 users worldwide.

<pre>
sshanalysis is available in public and can be installed 
by pip command:
$pip install -U sshanalysis
</pre>

# How to run sshanalysis on Linux
<pre>
$ sshanalysis your_ssh_log_file
or
$ sshanalysis /var/log/auth.log
or
When you run the following command, the file /var/log/auth.log will be used automatically.
$ sshanalysis
</pre>

# Background of sshanalysis
In 2021, 100% of the world’s top 500 supercomputers run on Linux.

96.3% of the world’s top 1 million servers run on Linux.

90% of all cloud infrastructures operate on Linux.

There are well over 1 billion sites on the world wide web.

According to wappalyzer.com, world wide web servers run on Apache 41%, Nginx 39%, IIS 7%, 
and LiteSpeed 5% respectively.

Apache and Nginx are based on open-source software.

Without Linux and open-source software, the Internet would not exist.

In other words, Linux and open source software are indispensable for the Internet.

SSH is now used by almost every data center in the world and more than half of the world's Web servers are managed using SSH.

Malicious attackers have been using true IP (internet protocol) addresses, spoofed IPs, and
springboard hosts's IPs.

Using the mixed IPs can cause DDoS (Distributed Denial of Service) attacks.

Currently it is hard to distinguish true IPs and spoofed IPs.

Therefore, it is hard to mitigate a DDoS attack.

A botnet (short for "robot network") is a network of computers infected 
with malware and under the control of a single attacking party.

There are several general log analysis tools: 
General log analysis tools: Graylog, Nagios, Elastic Stack, LOGalyze, and Fluentd.

There is several open-source tools for analyzing ssh-attacks: 
 "ssh-tracker" or "commons-ssh tracker".
 
This repository introduces a visualization tool, sshanalysis for investigating IPs 
that are attacking a ssh server via ssh.

sshanalysis is a new open-source ssh-tracker tool that visualizes all the IPs 
and country names that are making ssh attacks against a ssh server. 
Top 10 IPs with country names will be displayed on a simplified circle-graph.

In Debian and Ubuntu, /var/log/auth.log is a log file of recorded attacks.

# auth.log analysis
With /var/log/auth.log "read permission", any user can analyze IPs attacking against 
a ssh server.

The following graphs show the number of recorded attacks and top 10 IPs. 
The larger circle, the more number of attacks against a ssh server.
Although, country names were embedded on each graph,
no one knows whether captured IPs are true, spoofed, or springboarded.

sshanalysis can generate all IPs with the number of recorded attacks.
sshanalysis can generate top 10 IPs information associated with locations (country names).

<img src='https://github.com/y-takefuji/sshanalysis/raw/main/neuro.png' width=640 height=480>
<img src='https://github.com/y-takefuji/sshanalysis/raw/main/gpu1.png' width=640 height=480>
<img src='https://github.com/y-takefuji/sshanalysis/raw/main/gpu2.png' width=640 height=480>
<img src='https://github.com/y-takefuji/sshanalysis/raw/main/gpu3.png' width=640 height=480>
<img src='https://github.com/y-takefuji/sshanalysis/raw/main/gpu4.png' width=640 height=480>

# sshanalysis.py
sshanalysis.py consists of three modules. 
The first module generates a csv file containing the number of recorded attacks 
against the sorted IP addresses by using a /var/log/auth.log file or the specified log_file. 
The second module is for generating the country names associated with the captured IP addresses in the specified log_file. 
And the last module is for drawing a circle-graph.

The graph contains top 10 IPs with country names where the radius of the circle 
indicates the number of attacks. 
The larger the circle, the more attacks against the ssh server.

sshanalysis.py can generate an IPs file (all attacking IPs with the number of attacks), 
top 10 r.csv file (the number of attacks, IP address, country name), 
and r.png (circle graph).

We don't know whether captured IPs are true, spoofed, or springboarded.

# auth.log
The maximum size of github file is 25M.

The split command is used to split the auth.log file into multiple files of 20M in size.

$ split -b 20M auth.log auth_log

My auth.log was split into two files: auth_logaa and auth_logab.

To create auth.log, cat auth_log* >auth.log



