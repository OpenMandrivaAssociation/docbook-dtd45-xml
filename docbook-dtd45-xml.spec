%define name docbook-dtd45-xml
%define version 1.0
%define release %mkrel 4
%define dtdver 4.5
%define mltyp xml

Name: %{name}
Version: %{version}
Release: %{release}
Group       	: Publishing

Summary     	: XML document type definition for DocBook %{dtdver}

License   	: Artistic style
URL         	: http://www.oasis-open.org/docbook/

Provides        : docbook-dtd-%{mltyp}
Requires(post)  : coreutils
Requires(postun): coreutils
Requires(post)	: sgml-common >= 0.6.3-2mdk
Requires(postun): sgml-common >= 0.6.3-2mdk
Requires(post)  : libxml2-utils
Requires(postun): libxml2-utils

BuildRoot   	: %{_tmppath}/%{name}-%{version}-buildroot

# Zip file downloadable at http://www.oasis-open.org/docbook/%{mltyp}/%{dtdver}
Source0		: docbook-xml-%{dtdver}.tar.bz2 
BuildArch	: noarch  


%define sgmlbase %{_datadir}/sgml

%Description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.


%Prep
%setup -n docbook-xml-%{dtdver} -q 

%Build


%Install
rm -Rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
mkdir -p $DESTDIR
cp -r ent/ $DESTDIR
install -m644 docbook.cat $DESTDIR/catalog
install -m644 catalog.xml $DESTDIR
install -m644 *.dtd $DESTDIR
install -m644 *.mod $DESTDIR
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sgml
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
# looks unnecesary
# touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/catalog


%clean
rm -Rf $RPM_BUILD_ROOT


%Files
%defattr (-,root,root)
%doc README ChangeLog
%dir %{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
# why this?
# %ghost %config(noreplace) %{_sysconfdir}/sgml/catalog


%post
##
## SGML catalog
##
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
if [ -e %{sgmlbase}/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/openjade/catalog
fi

if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/dsssl-stylesheets/catalog
fi
# Symlinks
[ ! -e %{_sysconfdir}/sgml/%{mltyp}-docbook.cat ] && \
	ln -s %{mltyp}-docbook-%{dtdver}.cat %{_sysconfdir}/sgml/%{mltyp}-docbook.cat

##
## XML catalog
##

CATALOG=%{sgmlbase}/docbook/xmlcatalog

%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML V%{dtdver}//EN" \
	"file:///usr/share/sgml/docbook/xml-dtd-%{dtdver}/catalog.xml" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://www.oasis-open.org/docbook/xml/%{dtdver}" \
	"xml-dtd-%{dtdver}" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://www.oasis-open.org/docbook/xml/4.3" \
	"xml-dtd-%{dtdver}" $CATALOG

%Postun
##
## SGML catalog
##
# Do not remove if upgrade
if [ "$1" = "0" ]; then
  if [ -x %{_bindir}/xmlcatalog ]; then 
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog
  fi
 # Symlinks
 [ -e %{_sysconfdir}/sgml/%{mltyp}-docbook.cat ] && \
	 rm -f %{_sysconfdir}/sgml/%{mltyp}-docbook.cat

 if [ -x %{_bindir}/xmlcatalog ]; then

  # The following lines are for the case in which the style sheets
  # were not uninstalled because there is still another DTD
  if [ -e %{sgmlbase}/openjade/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/openjade/catalog
  fi

  if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/docbook/dsssl-stylesheets/catalog
  fi
 fi

##
## XML catalog
##

  CATALOG=%{sgmlbase}/docbook/xmlcatalog

  if [ -w $CATALOG -a -x %{_bindir}/xmlcatalog ]; then
   %{_bindir}/xmlcatalog --noout --del \
  	   "-//OASIS//DTD DocBook XML V%{dtdver}//EN" $CATALOG
   %{_bindir}/xmlcatalog --noout --del \
	   "xml-dtd-%{dtdver}" $CATALOG
  fi
fi


