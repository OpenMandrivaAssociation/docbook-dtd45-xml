%define dtdver	4.5
%define mltyp	xml
%define sgmlbase %{_datadir}/sgml

Summary:	XML document type definition for DocBook %{dtdver}
Name:		docbook-dtd45-xml
Version:	1.0
Release:	22
Group:		Publishing
License:	Artistic style
Url:		http://www.oasis-open.org/docbook/
# Zip file downloadable at http://www.oasis-open.org/docbook/%{mltyp}/%{dtdver}
Source0:	docbook-xml-%{dtdver}.tar.bz2 
BuildArch:	noarch  
Provides:	docbook-dtd-%{mltyp}
Requires(post,postun):	coreutils
Requires(post,postun):	libxml2-utils
Requires(post,postun):	sgml-common

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.

%prep
%setup -n docbook-xml-%{dtdver} -q 

%build

%install
DESTDIR=%{buildroot}%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
mkdir -p $DESTDIR
cp -r ent/ $DESTDIR
install -m644 docbook.cat $DESTDIR/catalog
install -m644 catalog.xml $DESTDIR
install -m644 *.dtd $DESTDIR
install -m644 *.mod $DESTDIR
mkdir -p %{buildroot}%{_sysconfdir}/sgml
touch %{buildroot}%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat

%files
%doc README ChangeLog
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
	"http://www.oasis-open.org/docbook/xml/4.5" \
	"xml-dtd-%{dtdver}" $CATALOG

%postun
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

