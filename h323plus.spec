# TODO:
# - separate plugins to subpackages
# - gsm-amr plugin (using system amrnb if possible)
# - use system libilbc or at least use optflags for plugins/audio/iLBC
# - configure: Skipping tests for RFC 2190 H.263 support
# - configure: Disabled non-RFC2190 H.263 using ffmpeg
# - configure: Disabled H.263 using VIC

%define		fver	%(echo %{version} | tr . _)
Summary:	H.323 Plus Library
Summary(pl.UTF-8):	Biblioteka OpenH323
Name:		h323plus
Version:	1.24.0
Release:	0.1
License:	MPL 1.0
Group:		Libraries
Source0:	http://www.h323plus.org/source/download/%{name}-v%{fver}.tar.gz
# Source0-md5:	459d527c3b52dc34837c9530899f556a
Patch0:		%{name}-configure.patch
Patch1:		%{name}-ptlib-version.patch
Patch2:		%{name}-mak-paths.patch
Patch3:		%{name}-gcc47.patch
Patch4:		%{name}-celt051.patch
URL:		http://www.h323plus.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	celt051-devel
BuildRequires:	ffmpeg-devel >= 0.4.6
BuildRequires:	libgsm-devel >= 1.0.10
BuildRequires:	libstdc++-devel
BuildRequires:	lpc10-devel >= 1.5
BuildRequires:	ptlib-devel >= 2.10.1
BuildRequires:	sed >= 4.0
BuildRequires:	speex-devel >= 1:1.1.5
Requires:	speex >= 1:1.1.5
Obsoletes:	openh323 < %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenH323 project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%description -l pl.UTF-8
Celem projektu OpenH323 jest stworzenie w pełni funkcjonalnej i
wyposażonej implementacji protokołu telekonferencyjnego ITU H.323,
który może być używany przez użytkowników prywatnych i komercyjnych
bez opłat.

%package devel
Summary:	OpenH323 development files
Summary(pl.UTF-8):	Pliki dla developerów OpenH323
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ffmpeg-devel
Requires:	ptlib-devel >= 2.10.1
Obsoletes:	openh323-devel < %{version}-%{release}

%description devel
Header files and libraries for developing applications that use
OpenH323.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki konieczne do rozwoju aplikacji
używających OpenH323.

%package static
Summary:	OpenH323 static libraries
Summary(pl.UTF-8):	Biblioteki statyczne OpenH323
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	openh323-ststic < %{version}-%{release}

%description static
OpenH323 static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenH323.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__autoconf}
%configure \
	--enable-localspeex=no \
	--enable-plugins

BUILDDIR=$(pwd)
%{__make} %{?debug:debug}%{!?debug:opt}shared \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}" \
	OPENH323DIR=$BUILDDIR \
	OH323_INCDIR=$BUILDDIR/include \
	OH323_LIBDIR=$BUILDDIR/%{_lib}

%{__make} -C plugins %{?debug:debug}%{!?debug:opt}shared \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}" \
	OPENH323DIR=$BUILDDIR \
	OH323_INCDIR=$BUILDDIR/include \
	OH323_LIBDIR=$BUILDDIR/%{_lib}

%{__make} -C samples/simple \
	CC="%{__cc}" \
	CPLUS="%{__cxx}" \
	OPTCCFLAGS="%{rpmcflags} %{!?debug:-DNDEBUG}" \
	OPENH323DIR=$BUILDDIR \
	OH323_INCDIR=$BUILDDIR/include \
	OH323_LIBDIR=$BUILDDIR/%{_lib}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}

%{__make} install \
	OH323_LIBDIR=%{_lib} \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}

%{__make} -C plugins install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}

# using cp as install won't preserve links
cp -pd %{_lib}/lib*.a $RPM_BUILD_ROOT%{_libdir}
install -p samples/simple/obj_*/simph323 $RPM_BUILD_ROOT%{_bindir}
cp -a version.h $RPM_BUILD_ROOT%{_includedir}/openh323

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libh323.so.*.*.*
%dir %{_libdir}/opal-%{version}/codecs
%dir %{_libdir}/opal-%{version}/codecs/audio
%dir %{_libdir}/opal-%{version}/codecs/video
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/audio/*.so
%attr(755,root,root) %{_libdir}/opal-%{version}/codecs/video/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libh323.so
%{_includedir}/openh323
%{_datadir}/openh323

%files static
%defattr(644,root,root,755)
%{_libdir}/libh323_s.a
