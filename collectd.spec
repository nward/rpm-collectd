Summary: Statistics collection daemon for filling RRD files
Name: collectd
Version: 5.2.0
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Daemons
URL: http://collectd.org/

Source: http://collectd.org/files/%{name}-%{version}.tar.bz2
Source1: collectd-httpd.conf
Source2: collection.conf
Source3: collectd.service
Patch1: %{name}-include-collectd.d.patch
Patch2: fixperlinstall.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%ifnarch ppc ppc64 sparc sparc64
BuildRequires: libvirt-devel
BuildRequires: lm_sensors-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: rrdtool-devel
BuildRequires: curl-devel
%if 0%{?fedora} >= 8
BuildRequires: perl-libs, perl-devel
%else
BuildRequires: perl
%endif
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: net-snmp-devel
BuildRequires: libpcap-devel
BuildRequires: mysql-devel
BuildRequires: OpenIPMI-devel
BuildRequires: postgresql-devel
%ifnarch s390 s390x
BuildRequires: nut-devel
%endif
BuildRequires: iptables-devel
BuildRequires: liboping-devel
BuildRequires: python-devel
BuildRequires: libgcrypt-devel
BuildRequires: librabbitmq-devel
%if 0%{?fedora} >= 15
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%endif


%description
collectd is a small daemon written in C for performance.  It reads various
system  statistics  and updates  RRD files,  creating  them if necessary.
Since the daemon doesn't need to startup every time it wants to update the
files it's very fast and easy on the system. Also, the statistics are very
fine grained since the files are updated every 10 seconds.


%package apache
Summary:       Apache plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description apache
This plugin collects data provided by Apache's 'mod_status'.

%package amqp
Summary:       AMQP plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description amqp
This plugin collects data from AMQP with the RabbitMQ client.

%package dns
Summary:       DNS traffic analysis module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description dns
This plugin collects DNS traffic data.


%package email
Summary:       Email plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}, spamassassin
%description email
This plugin collects data provided by spamassassin.


%package ipmi
Summary:       IPMI module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description ipmi
This plugin for collectd provides IPMI support.


%package mysql
Summary:       MySQL module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description mysql
MySQL querying plugin. This plugins provides data of issued commands,
called handlers and database traffic.


%package nginx
Summary:       Nginx plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description nginx
This plugin gets data provided by nginx.


%ifnarch s390 s390x
%package nut
Summary:       Network UPS Tools module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description nut
This plugin for collectd provides Network UPS Tools support.
%endif


%package -n perl-Collectd
Summary:       Perl bindings for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%description -n perl-Collectd
This package contains Perl bindings and plugin for collectd.


%package ping
Summary:       Ping module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description ping
This plugin for collectd provides network latency statistics.


%package postgresql
Summary:       PostgreSQL module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description postgresql
PostgreSQL querying plugin. This plugins provides data of issued commands,
called handlers and database traffic.


%package rrdtool
Summary:       RRDTool module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}, rrdtool
%description rrdtool
This plugin for collectd provides rrdtool support.


%ifnarch ppc ppc64 sparc sparc64
%package sensors
Summary:       Libsensors module for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}, lm_sensors
%description sensors
This plugin for collectd provides querying of sensors supported by
lm_sensors.
%endif

%package snmp
Summary:        SNMP module for collectd
Group:          System Environment/Daemons
Requires:       collectd = %{version}-%{release}, net-snmp
%description snmp
This plugin for collectd provides querying of net-snmp.


%package web
Summary:        Contrib web interface to viewing rrd files
Group:          System Environment/Daemons
Requires:       collectd = %{version}-%{release}
Requires:       collectd-rrdtool = %{version}-%{release}
Requires:       perl-HTML-Parser, perl-Regexp-Common, rrdtool-perl, httpd
%description web
This package will allow for a simple web interface to view rrd files created by
collectd.

%ifnarch ppc ppc64 sparc sparc64
%package virt
Summary:       Libvirt plugin for collectd
Group:         System Environment/Daemons
Requires:      collectd = %{version}-%{release}
%description virt
This plugin collects information from virtualized guests.
%endif

%prep
%setup -q
%patch1
%patch2

sed -i.orig -e 's|-Werror||g' Makefile.in */Makefile.in


%build
%configure CFLAGS="%{optflags} -DLT_LAZY_OR_NOW='RTLD_LAZY|RTLD_GLOBAL'" \
    --disable-static \
    --disable-ascent \
    --disable-apple_sensors \
    --disable-curl_json  \
    --disable-dbi  \
    --disable-gmond \
    --disable-ipvs \
    --disable-java \
    --disable-memcachec \
    --disable-modbus \
    --disable-netapp \
    --disable-netlink \
    --disable-notify_desktop \
    --disable-notify_email \
    --disable-onewire \
    --disable-oracle \
    --disable-pinba \
    --disable-routeros \
    --disable-rrdcached \
    --disable-tape \
    --disable-tokyotyrant \
    --disable-xmms \
    --disable-zfs_arc \
    --enable-apache \
    --enable-amqp \
    --enable-apcups \
    --enable-battery \
    --enable-bind \
    --enable-conntrack \
    --enable-contextswitch \
    --enable-cpu \
    --enable-cpufreq \
    --enable-csv \
    --enable-curl \
    --enable-curl_xml \
    --enable-df \
    --enable-disk \
    --enable-dns \
    --enable-email \
    --enable-entropy \
    --enable-exec \
    --enable-filecount \
    --enable-fscache \
    --enable-hddtemp \
    --enable-interface \
    --enable-ipmi \
    --enable-iptables \
    --enable-irq \
    --enable-libvirt \
    --enable-load \
    --enable-logfile \
    --enable-madwifi \
    --enable-match_empty_counter \
    --enable-match_hashed \
    --enable-match_regex \
    --enable-match_timediff \
    --enable-match_value \
    --enable-mbmon \
    --enable-memcached \
    --enable-memory \
    --enable-multimeter \
    --enable-mysql \
    --enable-network \
    --enable-nfs \
    --enable-nginx \
    --enable-ntpd \
%ifnarch s390 s390x
    --enable-nut \
%else
    --disable-nut \
%endif
    --enable-olsrd \
    --enable-openvpn \
    --enable-perl \
    --enable-ping \
    --enable-postgresql \
    --enable-powerdns \
    --enable-processes \
    --enable-protocols \
    --enable-python \
    --enable-rrdtool \
%ifnarch ppc ppc64 sparc sparc64
    --enable-sensors \
%endif
    --enable-serial \
    --enable-snmp \
    --enable-swap \
    --enable-syslog \
    --enable-table \
    --enable-tail \
    --enable-target_notification \
    --enable-target_replace \
    --enable-target_scale \
    --enable-target_set \
    --enable-tcpconns \
    --enable-teamspeak2 \
    --enable-ted \
    --enable-thermal \
    --enable-unixsock \
    --enable-uptime \
    --enable-users \
    --enable-uuid \
    --enable-vmem \
    --enable-vserver \
    --enable-wireless \
    --enable-write_http \
    --with-libiptc \
    --with-python \
    --with-perl-bindings=INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__rm} -rf contrib/SpamAssassin
%{__make} install DESTDIR="%{buildroot}"

%{__install} -Dp -m0644 src/collectd.conf %{buildroot}%{_sysconfdir}/collectd.conf
%if 0%{?fedora} >= 15
%{__install} -Dp -m0644 %{SOURCE3} %{buildroot}%{_unitdir}/collectd.service
%else
%{__install} -Dp -m0755 contrib/fedora/init.d-collectd %{buildroot}%{_initrddir}/collectd
%endif

%{__install} -d -m0755 %{buildroot}%{_localstatedir}/lib/collectd/rrd
%{__install} -d -m0755 %{buildroot}/%{_datadir}/collectd/collection3/
%{__install} -d -m0755 %{buildroot}/%{_sysconfdir}/httpd/conf.d/


# Convert docs to UTF-8
find contrib/ -type f -exec %{__chmod} a-x {} \;
for f in contrib/README ChangeLog ; do
  mv $f $f.old; iconv -f iso-8859-1 -t utf-8 < $f.old > $f; rm $f.old
done

# Remove Perl hidden .packlist files.
find %{buildroot} -name .packlist -exec rm {} \;
# Remove Perl temporary file perllocal.pod
find %{buildroot} -name perllocal.pod -exec rm {} \;

# copy web interface
cp -ad contrib/collection3/* %{buildroot}/%{_datadir}/collectd/collection3/
rm -f %{buildroot}/%{_datadir}/collectd/collection3/etc/collection.conf
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/collectd.conf
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/collection.conf
ln -s %{_sysconfdir}/collection.conf %{buildroot}/%{_datadir}/collectd/collection3/etc/collection.conf
chmod +x %{buildroot}/%{_datadir}/collectd/collection3/bin/*.cgi

# Move the Perl examples to a separate directory.
mkdir perl-examples
find contrib -name '*.p[lm]' -exec mv {} perl-examples/ \;

# Move config contribs
mkdir -p %{buildroot}/etc/collectd.d/
cp contrib/redhat/apache.conf %{buildroot}/etc/collectd.d/apache.conf
cp contrib/redhat/email.conf %{buildroot}/etc/collectd.d/email.conf
cp contrib/redhat/mysql.conf %{buildroot}/etc/collectd.d/mysql.conf
cp contrib/redhat/nginx.conf %{buildroot}/etc/collectd.d/nginx.conf
cp contrib/redhat/sensors.conf %{buildroot}/etc/collectd.d/sensors.conf
cp contrib/redhat/snmp.conf %{buildroot}/etc/collectd.d/snmp.conf

# configs for subpackaged plugins
%ifnarch s390 s390x
for p in dns ipmi libvirt nut perl ping postgresql rrdtool
%else
for p in dns ipmi libvirt perl ping postgresql rrdtool
%endif
do
%{__cat} > %{buildroot}/etc/collectd.d/$p.conf <<EOF
LoadPlugin $p
EOF
done
%{__cat} >> %{buildroot}/etc/collectd.d/rrdtool.conf <<EOF
<Plugin rrdtool>
       DataDir "/var/lib/collectd/rrd"
       CacheTimeout 120
       CacheFlush   900
</Plugin>
EOF


# *.la files shouldn't be distributed.
rm -f %{buildroot}/%{_libdir}/{collectd/,}*.la


%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    # Initial installation
%if 0%{?fedora} >= 15
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add collectd
%endif
fi


%preun
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
%if 0%{?fedora} >= 15
    /bin/systemctl --no-reload disable collectd.service > /dev/null 2>&1 || :
    /bin/systemctl stop collectd.service > /dev/null 2>&1 || :
%else
    /sbin/service collectd stop &>/dev/null || :
    /sbin/chkconfig --del collectd
%endif
fi


%postun
/sbin/ldconfig
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
%if 0%{?fedora} >= 15
    /bin/systemctl try-restart collectd.service >/dev/null 2>&1 || :
%else
    /sbin/service collectd condrestart &>/dev/null || :
%endif
fi


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, -)

%config(noreplace) %{_sysconfdir}/collectd.conf
%config(noreplace) %{_sysconfdir}/collectd.d/
%exclude %{_sysconfdir}/collectd.d/apache.conf
%exclude %{_sysconfdir}/collectd.d/dns.conf
%exclude %{_sysconfdir}/collectd.d/email.conf
%exclude %{_sysconfdir}/collectd.d/ipmi.conf
%exclude %{_sysconfdir}/collectd.d/libvirt.conf
%exclude %{_sysconfdir}/collectd.d/mysql.conf
%exclude %{_sysconfdir}/collectd.d/nginx.conf
%ifnarch s390 s390x
%exclude %{_sysconfdir}/collectd.d/nut.conf
%endif
%exclude %{_sysconfdir}/collectd.d/perl.conf
%exclude %{_sysconfdir}/collectd.d/ping.conf
%exclude %{_sysconfdir}/collectd.d/postgresql.conf
%exclude %{_datadir}/collectd/postgresql_default.conf
%exclude %{_sysconfdir}/collectd.d/rrdtool.conf
%exclude %{_sysconfdir}/collectd.d/sensors.conf
%exclude %{_sysconfdir}/collectd.d/snmp.conf

%if 0%{?fedora} >= 15
%{_unitdir}/collectd.service
%else
%{_initrddir}/collectd
%endif
%{_bindir}/collectd-nagios
%{_bindir}/collectdctl
%{_bindir}/collectd-tg
%{_sbindir}/collectd
%{_sbindir}/collectdmon
%dir %{_localstatedir}/lib/collectd/

%dir %{_libdir}/collectd
%{_libdir}/collectd/apcups.so
%{_libdir}/collectd/battery.so
%{_libdir}/collectd/contextswitch.so
%{_libdir}/collectd/cpu.so
%{_libdir}/collectd/cpufreq.so
%{_libdir}/collectd/csv.so
%{_libdir}/collectd/curl_xml.so
%{_libdir}/collectd/df.so
%{_libdir}/collectd/disk.so
%{_libdir}/collectd/entropy.so
%{_libdir}/collectd/exec.so
%{_libdir}/collectd/filecount.so
%{_libdir}/collectd/hddtemp.so
%{_libdir}/collectd/interface.so
%{_libdir}/collectd/iptables.so
%{_libdir}/collectd/irq.so
%{_libdir}/collectd/load.so
%{_libdir}/collectd/logfile.so
%{_libdir}/collectd/madwifi.so
%{_libdir}/collectd/match_empty_counter.so
%{_libdir}/collectd/match_hashed.so
%{_libdir}/collectd/mbmon.so
%{_libdir}/collectd/memcached.so
%{_libdir}/collectd/memory.so
%{_libdir}/collectd/multimeter.so
%{_libdir}/collectd/network.so
%{_libdir}/collectd/nfs.so
%{_libdir}/collectd/ntpd.so
%{_libdir}/collectd/olsrd.so
%{_libdir}/collectd/powerdns.so
%{_libdir}/collectd/processes.so
%{_libdir}/collectd/python.so
%{_libdir}/collectd/serial.so
%{_libdir}/collectd/swap.so
%{_libdir}/collectd/syslog.so
%{_libdir}/collectd/tail.so
%{_libdir}/collectd/target_scale.so
%{_libdir}/collectd/target_v5upgrade.so
%{_libdir}/collectd/tcpconns.so
%{_libdir}/collectd/teamspeak2.so
%{_libdir}/collectd/thermal.so
%{_libdir}/collectd/threshold.so
%{_libdir}/collectd/unixsock.so
%{_libdir}/collectd/users.so
%{_libdir}/collectd/uuid.so
%{_libdir}/collectd/vmem.so
%{_libdir}/collectd/vserver.so
%{_libdir}/collectd/wireless.so
%{_libdir}/collectd/write_http.so

%{_libdir}/collectd/bind.so
%{_libdir}/collectd/conntrack.so
%{_libdir}/collectd/curl.so
%{_libdir}/collectd/fscache.so
%{_libdir}/collectd/match_regex.so
%{_libdir}/collectd/match_timediff.so
%{_libdir}/collectd/match_value.so
%{_libdir}/collectd/openvpn.so
%{_libdir}/collectd/protocols.so
%{_libdir}/collectd/table.so
%{_libdir}/collectd/target_notification.so
%{_libdir}/collectd/target_replace.so
%{_libdir}/collectd/target_set.so
%{_libdir}/collectd/ted.so
%{_libdir}/collectd/uptime.so
%{_libdir}/collectd/aggregation.so
%{_libdir}/collectd/ethstat.so
%{_libdir}/collectd/md.so
%{_libdir}/collectd/numa.so
%{_libdir}/collectd/write_graphite.so

%{_datadir}/collectd/types.db

# collectdclient - TBD reintroduce -devel subpackage?
%{_libdir}/libcollectdclient.so
%{_libdir}/libcollectdclient.so.1
%{_libdir}/libcollectdclient.so.1.0.0
%{_libdir}/pkgconfig/libcollectdclient.pc
%{_includedir}/collectd/client.h
%{_includedir}/collectd/lcc_features.h
%{_includedir}/collectd/network.h
%{_includedir}/collectd/network_buffer.h

%doc AUTHORS ChangeLog COPYING README
%doc %{_mandir}/man1/collectd.1*
%doc %{_mandir}/man1/collectdctl.1*
%doc %{_mandir}/man1/collectd-nagios.1*
%doc %{_mandir}/man1/collectdmon.1*
%doc %{_mandir}/man5/collectd.conf.5*
%doc %{_mandir}/man5/collectd-exec.5*
%doc %{_mandir}/man5/collectd-java.5*
%doc %{_mandir}/man5/collectd-python.5*
%doc %{_mandir}/man5/collectd-threshold.5*
%doc %{_mandir}/man5/collectd-unixsock.5*
%doc %{_mandir}/man5/types.db.5*

%files apache
%defattr(-, root, root, -)
%{_libdir}/collectd/apache.so
%config(noreplace) %{_sysconfdir}/collectd.d/apache.conf


%files amqp
%defattr(-, root, root, -)
%{_libdir}/collectd/amqp.so


%files dns
%defattr(-, root, root, -)
%{_libdir}/collectd/dns.so
%config(noreplace) %{_sysconfdir}/collectd.d/dns.conf


%files email
%defattr(-, root, root, -)
%{_libdir}/collectd/email.so
%config(noreplace) %{_sysconfdir}/collectd.d/email.conf
%doc %{_mandir}/man5/collectd-email.5*


%files ipmi
%defattr(-, root, root, -)
%{_libdir}/collectd/ipmi.so
%config(noreplace) %{_sysconfdir}/collectd.d/ipmi.conf


%files mysql
%defattr(-, root, root, -)
%{_libdir}/collectd/mysql.so
%config(noreplace) %{_sysconfdir}/collectd.d/mysql.conf


%files nginx
%defattr(-, root, root, -)
%{_libdir}/collectd/nginx.so
%config(noreplace) %{_sysconfdir}/collectd.d/nginx.conf


%ifnarch s390 s390x
%files nut
%defattr(-, root, root, -)
%{_libdir}/collectd/nut.so
%config(noreplace) %{_sysconfdir}/collectd.d/nut.conf
%endif


%files -n perl-Collectd
%defattr(-, root, root, -)
%doc perl-examples/*
%{_libdir}/collectd/perl.so
%{perl_vendorlib}/Collectd.pm
%{perl_vendorlib}/Collectd/
%config(noreplace) %{_sysconfdir}/collectd.d/perl.conf
%doc %{_mandir}/man5/collectd-perl.5*
%doc %{_mandir}/man3/Collectd::Unixsock.3pm*


%files ping
%defattr(-, root, root, -)
%{_libdir}/collectd/ping.so
%config(noreplace) %{_sysconfdir}/collectd.d/ping.conf


%files postgresql
%defattr(-, root, root, -)
%{_libdir}/collectd/postgresql.so
%config(noreplace) %{_sysconfdir}/collectd.d/postgresql.conf
%{_datadir}/collectd/postgresql_default.conf


%files rrdtool
%defattr(-, root, root, -)
%{_libdir}/collectd/rrdtool.so
%config(noreplace) %{_sysconfdir}/collectd.d/rrdtool.conf


%ifnarch ppc ppc64 sparc sparc64
%files sensors
%defattr(-, root, root, -)
%{_libdir}/collectd/sensors.so
%config(noreplace) %{_sysconfdir}/collectd.d/sensors.conf
%endif

%files snmp
%defattr(-, root, root, -)
%{_libdir}/collectd/snmp.so
%config(noreplace) %{_sysconfdir}/collectd.d/snmp.conf
%doc %{_mandir}/man5/collectd-snmp.5*


%files web
%defattr(-, root, root, -)
%{_datadir}/collectd/collection3/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/collectd.conf
%config(noreplace) %{_sysconfdir}/collection.conf

%ifnarch ppc ppc64 sparc sparc64
%files virt
%defattr(-, root, root, -)
%{_libdir}/collectd/libvirt.so
%config(noreplace) %{_sysconfdir}/collectd.d/libvirt.conf
%endif

%changelog
* Mon Nov 26 2012 Alan Pevec <apevec@redhat.com> 5.2.0-1
- update to 5.2.0 from Steve Traylen rhbz#877721

* Wed Nov 21 2012 Alan Pevec <apevec@redhat.com> 5.1.1-1
- update to 5.1.1
- spec cleanups from Ruben Kerkhof
- fix postgresql_default.conf location rhbz#681615
- fix broken configuration for httpd 2.4 rhbz#871385

* Mon Nov 19 2012 Alan Pevec <apevec@redhat.com> 5.0.5-1
- new upstream version 5.0.5
  http://mailman.verplant.org/pipermail/collectd/2012-November/005465.html

* Mon Sep 17 2012 Alan Pevec <apevec@redhat.com> 5.0.4-1
- New upstream release, version bump to 5 (#743894) from Andrew Elwell

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 4.10.7-2
- Perl 5.16 rebuild

* Tue Apr 03 2012 Alan Pevec <apevec@redhat.com> 4.10.7-1
- new upstream release 4.10.7
  http://mailman.verplant.org/pipermail/collectd/2012-April/005045.html

* Wed Feb 29 2012 Alan Pevec <apevec@redhat.com> 4.10.6-1
- new upstream release 4.10.6
  http://mailman.verplant.org/pipermail/collectd/2012-February/004932.html

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Alan Pevec <apevec@redhat.com> 4.10.4-1
- new upstream version 4.10.4
  http://mailman.verplant.org/pipermail/collectd/2011-October/004777.html
- collectd-web config file DataDir value wrong rhbz#719809
- Python plugin doesn't work rhbz#739593
- Add systemd service file. (thanks Paul P. Komkoff Jr) rhbz#754460

* Fri Jul 29 2011 Kevin Fenzi <kevin@scrye.com> - 4.10.3-8
- Rebuild for new snmp again.

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 4.10.3-7
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 4.10.3-6
- Perl mass rebuild

* Fri Jul 08 2011 Kevin Fenzi <kevin@scrye.com> - 4.10.3-5
- Rebuild for new snmp

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.10.3-4
- Perl mass rebuild

* Tue May 03 2011 Dan Horák <dan@danny.cz> - 4.10.3-3
- fix build on s390(x)

* Tue Apr 19 2011 Alan Pevec <apevec@redhat.com> 4.10.3-2
- re-enable nut plugin rhbz#465729 rhbz#691380

* Tue Mar 29 2011 Alan Pevec <apevec@redhat.com> 4.10.3-1
- new upstream version 4.10.3
  http://collectd.org/news.shtml#news87
- disable nut 2.6 which fails collectd check:
  libupsclient  . . . . no (symbol upscli_connect not found)

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 4.10.2-4
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 07 2011 Dan Horák <dan[at]danny.cz> 4.10.2-2
- no nut on s390(x)

* Thu Dec 16 2010 Alan Pevec <apevec@redhat.com> 4.10.2-1
- New upstream version 4.10.2
- http://collectd.org/news.shtml#news86
- explicitly disable/enable all plugins, fixes FTBFS bz#660936

* Thu Nov 04 2010 Alan Pevec <apevec@redhat.com> 4.10.1-1
- New upstream version 4.10.1
  http://collectd.org/news.shtml#news85

* Sat Oct 30 2010 Richard W.M. Jones <rjones@redhat.com> 4.10.0-3
- Bump and rebuild for updated libnetsnmp.so.

* Wed Sep 29 2010 jkeating - 4.10.0-2
- Rebuilt for gcc bug 634757

* Sun Sep 19 2010 Robert Scheck <robert@fedoraproject.org> 4.10.0-1
- New upstream version 4.10.0 (thanks to Mike McGrath)

* Tue Jun 08 2010 Alan Pevec <apevec@redhat.com> 4.9.2-1
- New upstream version 4.9.2
  http://collectd.org/news.shtml#news83

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.9.1-3
- Mass rebuild with perl-5.12.0

* Fri Mar 26 2010 Alan Pevec <apevec@redhat.com> 4.9.1-2
- enable ping plugin bz#541744

* Mon Mar 08 2010 Lubomir Rintel <lkundrak@v3.sl> 4.9.1-1
- New upstream version 4.9.1
  http://collectd.org/news.shtml#news81

* Tue Feb 16 2010 Alan Pevec <apevec@redhat.com> 4.8.3-1
- New upstream version 4.8.3
  http://collectd.org/news.shtml#news81
- FTBFS bz#564943 - system libiptc is not usable and owniptc fails to compile:
  add a patch from upstream iptables.git to fix owniptc compilation

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 4.8.1-3
- rebuild against perl 5.10.1

* Fri Nov 27 2009 Alan Pevec <apevec@redhat.com> 4.8.1-2
- use Fedora libiptc, owniptc in collectd sources fails to compile

* Wed Nov 25 2009 Alan Pevec <apevec@redhat.com> 4.8.1-1
- update to 4.8.1 (Florian La Roche) bz# 516276
- disable ping plugin until liboping is packaged bz# 541744

* Fri Sep 11 2009 Tom "spot" Callaway <tcallawa@redhat.com> 4.6.5-1
- update to 4.6.5
- disable ppc/ppc64 due to compile error

* Wed Sep 02 2009 Alan Pevec <apevec@redhat.com> 4.6.4-1
- fix condrestart: on upgrade collectd is not restarted, bz# 516273
- collectd does not re-connect to libvirtd, bz# 480997
- fix unpackaged files https://bugzilla.redhat.com/show_bug.cgi?id=516276#c4
- New upstream version 4.6.4
  http://collectd.org/news.shtml#news69

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.6.2-5
- rebuilt with new openssl

* Thu Aug  6 2009 Richard W.M. Jones <rjones@redhat.com> - 4.6.2-4
- Force rebuild to test FTBFS issue.
- lib/collectd/types.db seems to have moved to share/collectd/types.db

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 20 2009 Alan Pevec <apevec@redhat.com> 4.6.2-1
- New upstream version 4.6.2
  http://collectd.org/news.shtml#news64

* Tue Mar 03 2009 Alan Pevec <apevec@redhat.com> 4.5.3-2
- patch for strict-aliasing issue in liboping.c

* Mon Mar 02 2009 Alan Pevec <apevec@redhat.com> 4.5.3-1
- New upstream version 4.5.3
- fixes collectd is built without iptables plugin, bz# 479208
- list all expected plugins explicitly to avoid such bugs

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 4.5.1-3
- Rebuild against new mysql client.

* Sun Dec 07 2008 Alan Pevec <apevec@redhat.com> 4.5.1-2.1
- fix subpackages, bz# 475093

* Sun Nov 30 2008 Alan Pevec <apevec@redhat.com> 4.5.1-2
- workaround for https://bugzilla.redhat.com/show_bug.cgi?id=468067

* Wed Oct 22 2008 Alan Pevec <apevec@redhat.com> 4.5.1-1
- New upstream version 4.5.1, bz# 470943
  http://collectd.org/news.shtml#news59
- enable Network UPS Tools (nut) plugin, bz# 465729
- enable postgresql plugin
- spec cleanup, bz# 473641

* Fri Aug 01 2008 Alan Pevec <apevec@redhat.com> 4.4.2-1
- New upstream version 4.4.2.

* Thu Jul 03 2008 Lubomir Rintel <lkundrak@v3.sk> 4.4.1-4
- Fix a typo introduced by previous change that prevented building in el5

* Thu Jul 03 2008 Lubomir Rintel <lkundrak@v3.sk> 4.4.1-3
- Make this compile with older perl package
- Turn dependencies on packages to dependencies on Perl modules
- Add default attributes for files

* Thu Jun 12 2008 Alan Pevec <apevec@redhat.com> 4.4.1-2
- Split rrdtool into a subpackage (Chris Lalancette)
- cleanup subpackages, split dns plugin, enable ipmi
- include /etc/collectd.d (bz#443942)

* Mon Jun 09 2008 Alan Pevec <apevec@redhat.com> 4.4.1-1
- New upstream version 4.4.1.
- plugin changes: reenable iptables, disable ascent

* Tue May 27 2008 Alan Pevec <apevec@redhat.com> 4.4.0-2
- disable iptables/libiptc

* Mon May 26 2008 Alan Pevec <apevec@redhat.com> 4.4.0-1
- New upstream version 4.4.0.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-9
- Added {?dist} to release number (thanks Alan Pevec).

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-8
- Bump release number so we can tag this in Rawhide.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-6
- Exclude perl.so from the main package.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-5
- Put the perl bindings and plugin into a separate perl-Collectd
  package.  Note AFAICT from the manpage, the plugin and Collectd::*
  perl modules must all be packaged together.

* Wed Apr 16 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-4
- Remove -devel subpackage.
- Add subpackages for apache, email, mysql, nginx, sensors,
  snmp (thanks Richard Shade).
- Add subpackages for perl, libvirt.

* Tue Apr 15 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-2
- Install Perl bindings in vendor dir not site dir.

* Tue Apr 15 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-1
- New upstream version 4.3.2.
- Create a -devel subpackage for development stuff, examples, etc.
- Use .bz2 package instead of .gz.
- Remove fix-hostname patch, now upstream.
- Don't mark collectd init script as config.
- Enable MySQL, sensors, email, apache, Perl, unixsock support.
- Don't remove example Perl scripts.
- Package types.db(5) manpage.
- Fix defattr.
- Build in koji to find the full build-requires list.

* Mon Apr 14 2008 Richard W.M. Jones <rjones@redhat.com> - 4.2.3.100.g79b0797-2
- Prepare for Fedora package review:
- Clarify license is GPLv2 (only).
- Setup should be quiet.
- Spelling mistake in original description fixed.
- Don't include NEWS in doc - it's an empty file.
- Convert some other doc files to UTF-8.
- config(noreplace) on init file.

* Thu Jan 10 2008 Chris Lalancette <clalance@redhat.com> - 4.2.3.100.g79b0797.1.ovirt
- Update to git version 79b0797
- Remove *.pm files so we don't get a bogus dependency
- Re-enable rrdtool; we will need it on the WUI side anyway

* Mon Oct 29 2007 Dag Wieers <dag@wieers.com> - 4.2.0-1 - 5946+/dag
- Updated to release 4.2.0.

* Mon Oct 29 2007 Dag Wieers <dag@wieers.com> - 3.11.5-1
- Initial package. (using DAR)
