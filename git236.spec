# Pass --without docs to rpmbuild if you don't want the documentation
%bcond_without docs

# Pass --without tests to rpmbuild if you don't want to run the tests
%bcond_without tests

%global gitexecdir          %{_libexecdir}/git-core

# Settings for Fedora >= 34
%if 0%{?fedora} >= 34
%bcond_with                 emacs
%else
%bcond_without              emacs
%endif

# Settings for Fedora
%if 0%{?fedora}
# linkchecker is not available on EL
%bcond_without              linkcheck
%else
%bcond_with                 linkcheck
%endif

# Settings for Fedora and EL >= 9
%if 0%{?fedora} || 0%{?rhel} >= 9
%bcond_without              asciidoctor
%else
%bcond_with                 asciidoctor
%endif

# Settings for Fedora and EL >= 8
%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_with                 python2
%bcond_without              python3
%global gitweb_httpd_conf   gitweb.conf
%global use_glibc_langpacks 1
%global use_perl_generators 1
%global use_perl_interpreter 1
%else
%bcond_without              python2
%bcond_with                 python3
%global build_cflags        %{build_cflags} -fPIC -std=gnu99
%global gitweb_httpd_conf   git.conf
%global use_glibc_langpacks 0
%global use_perl_generators 0
%global use_perl_interpreter 0
%endif

# Settings for Fedora and EL >= 7
%if 0%{?fedora} || 0%{?rhel} >= 7
%global bashcompdir         %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%global bashcomproot        %(dirname %{bashcompdir} 2>/dev/null)
%endif

# Allow cvs subpackage to be toggled via --with/--without
# Disable cvs subpackage by default on EL >= 8
%if 0%{?rhel} >= 8
%bcond_with                 cvs
%else
%bcond_without              cvs
%endif

# Allow credential-libsecret subpackage to be toggled via --with/--without
%bcond_without              libsecret

# Allow p4 subpackage to be toggled via --with/--without
# Disable by default if we lack python2 or python3 support
%if %{with python2} || %{with python3}
%bcond_without              p4
%else
%bcond_with                 p4
%endif

# Hardening flags for EL-7
%if 0%{?rhel} == 7
%global _hardened_build     1
%endif

# Define for release candidates
#global rcrev   .rc0

# Set path to the package-notes linker script
%global _package_note_file  %{_builddir}/%{name}-%{version}%{?rcrev}/.package_note-%{name}-%{version}-%{release}.%{_arch}.ld

Name:           git236
Version:        2.36.6
Release:        1%{?rcrev}%{?dist}
Summary:        Fast Version Control System
License:        GPLv2
URL:            https://git-scm.com/
Source0:        https://www.kernel.org/pub/software/scm/git/%{?rcrev:testing/}git-%{version}%{?rcrev}.tar.xz
Source1:        https://www.kernel.org/pub/software/scm/git/%{?rcrev:testing/}git-%{version}%{?rcrev}.tar.sign

# Junio C Hamano's key is used to sign git releases, it can be found in the
# junio-gpg-pub tag within git.
#
# (Note that the tagged blob in git contains a version of the key with an
# expired signing subkey.  The subkey expiration has been extended on the
# public keyservers, but the blob in git has not been updated.)
#
# https://git.kernel.org/cgit/git/git.git/tag/?h=junio-gpg-pub
# https://git.kernel.org/cgit/git/git.git/blob/?h=junio-gpg-pub&id=7214aea37915ee2c4f6369eb9dea520aec7d855b
Source2:        gpgkey-junio.asc

# Local sources begin at 10 to allow for additional future upstream sources
Source11:       git.xinetd.in
Source12:       git-gui.desktop
Source13:       gitweb-httpd.conf
Source14:       gitweb.conf.in
Source15:       git@.service.in
Source16:       git.socket

# Script to print test failure output (used in %%check)
Source99:       print-failed-test-output

# https://bugzilla.redhat.com/490602
Patch0:         git-cvsimport-Ignore-cvsps-2.2b1-Branches-output.patch

%if %{with docs}
# pod2man is needed to build Git.3pm
BuildRequires:  %{_bindir}/pod2man
%if %{with asciidoctor}
BuildRequires:  docbook5-style-xsl
BuildRequires:  rubygem-asciidoctor
%else
BuildRequires:  asciidoc >= 8.4.1
%endif
# endif with asciidoctor
BuildRequires:  perl(File::Compare)
BuildRequires:  xmlto
%if %{with linkcheck}
BuildRequires:  linkchecker
%endif
# endif with linkcheck
%endif
# endif with docs
BuildRequires:  coreutils
BuildRequires:  desktop-file-utils
BuildRequires:  diffutils
%if %{with emacs}
BuildRequires:  emacs-common
%endif
# endif emacs-common
%if 0%{?rhel} && 0%{?rhel} < 9
# Require epel-rpm-macros for the %%gpgverify macro on EL-7/EL-8, and
# %%build_cflags & %%build_ldflags on EL-7.
BuildRequires:  epel-rpm-macros
%endif
# endif rhel < 9
BuildRequires:  expat-devel
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnupg2
BuildRequires:  libcurl-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  perl(Error)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
%if %{use_perl_generators}
BuildRequires:  perl-generators
%endif
# endif use_perl_generators
%if %{use_perl_interpreter}
BuildRequires:  perl-interpreter
%else
BuildRequires:  perl
%endif
# endif use_perl_interpreter
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  sed
# For macros
BuildRequires:  systemd
BuildRequires:  tcl
BuildRequires:  tk
BuildRequires:  xz
BuildRequires:  zlib-devel >= 1.2

%if %{with tests}
# Test suite requirements
BuildRequires:  acl
%if 0%{?fedora} || 0%{?rhel} >= 8
# Needed by t5540-http-push-webdav.sh
BuildRequires: apr-util-bdb
%endif
# endif fedora or rhel >= 8
BuildRequires:  bash
%if %{with cvs}
BuildRequires:  cvs
BuildRequires:  cvsps
%endif
# endif with cvs
%if %{use_glibc_langpacks}
# glibc-all-langpacks and glibc-langpack-is are needed for GETTEXT_LOCALE and
# GETTEXT_ISO_LOCALE test prereq's, glibc-langpack-en ensures en_US.UTF-8.
BuildRequires:  glibc-all-langpacks
BuildRequires:  glibc-langpack-en
BuildRequires:  glibc-langpack-is
%endif
# endif use_glibc_langpacks
%if 0%{?fedora} || 0%{?rhel} >= 9
BuildRequires:  gnupg2-smime
%endif
# endif fedora or el >= 9
%if 0%{?fedora} || ( 0%{?rhel} >= 7 && ( "%{_arch}" == "ppc64le" || "%{_arch}" == "x86_64" ) )
BuildRequires:  highlight
%endif
# endif fedora or el7+ (ppc64le/x86_64)
%if 0%{?fedora} >= 37
BuildRequires:  httpd-core
%else
BuildRequires:  httpd
%endif
# endif fedora >= 37
%if 0%{?fedora} && ! ( 0%{?fedora} >= 35 || "%{_arch}" == "i386" || "%{_arch}" == "s390x" )
BuildRequires:  jgit
%endif
# endif fedora (except i386 and s390x)
BuildRequires:  mod_dav_svn
BuildRequires:  openssh-clients
BuildRequires:  perl(App::Prove)
BuildRequires:  perl(CGI)
BuildRequires:  perl(CGI::Carp)
BuildRequires:  perl(CGI::Util)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(filetest)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(IO::Pty)
BuildRequires:  perl(JSON)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(Mail::Address)
BuildRequires:  perl(Memoize)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
%if %{with python3}
BuildRequires:  python3-devel
%else
%if %{with python2}
BuildRequires:  python2-devel
%endif
# endif with python2
%endif
# endif with python3
BuildRequires:  subversion
BuildRequires:  subversion-perl
BuildRequires:  tar
BuildRequires:  time
BuildRequires:  zip
%endif
# endif with tests

Requires:       git-core = %{version}-%{release}
Requires:       git-core-doc = %{version}-%{release}
%if ! %{defined perl_bootstrap}
Requires:       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap
Requires:       perl-Git = %{version}-%{release}

%if %{with emacs} && %{defined _emacs_version}
Requires:       emacs-filesystem >= %{_emacs_version}
%endif
# endif with emacs && defined _emacs_version

# safe replacement
Provides:       git = %{version}-%{release}
Provides:       git%{?_isa} = %{version}-%{release}
Conflicts:      git < %{version}-%{release}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs common set of tools which are usually using with
small amount of dependencies. To install all git packages, including
tools for integrating with other SCMs, install the git-all meta-package.

%package all
Summary:        Meta-package to pull in all git tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%if %{with libsecret}
Requires:       git-credential-libsecret = %{version}-%{release}
%endif
# endif with libsecret
%if %{with cvs}
Requires:       git-cvs = %{version}-%{release}
%endif
# endif with cvs
Requires:       git-daemon = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
%if %{with p4}
Requires:       git-p4 = %{version}-%{release}
%endif
# endif with p4
Requires:       git-subtree = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-instaweb = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}
%if ! %{defined perl_bootstrap}
Requires:       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap
# safe replacement
Provides:       git-all = %{version}-%{release}
Conflicts:      git-all < %{version}-%{release}
%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package core
Summary:        Core package of git with minimal functionality
Requires:       less
Requires:       openssh-clients
Requires:       zlib >= 1.2
# safe replacement
Provides:       git-core = %{version}-%{release}
Provides:       git-core%{?_isa} = %{version}-%{release}
Conflicts:      git-core < %{version}-%{release}
%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.
To install all git packages, including tools for integrating with
other SCMs, install the git-all meta-package.

%package core-doc
Summary:        Documentation files for git-core
BuildArch:      noarch
Requires:       git-core = %{version}-%{release}
# safe replacement
Provides:       git-core-doc = %{version}-%{release}
Conflicts:      git-core-doc < %{version}-%{release}
%description core-doc
Documentation files for git-core package including man pages.

%if %{with libsecret}
%package credential-libsecret
Summary:        Git helper for accessing credentials via libsecret
BuildRequires:  libsecret-devel
Requires:       git = %{version}-%{release}
# safe replacement
Provides:       git-credential-libsecret = %{version}-%{release}
Provides:       git-credential-libsecret%{?_isa} = %{version}-%{release}
Conflicts:      git-credential-libsecret < %{version}-%{release}
%description credential-libsecret
%{summary}.
%endif
# endif with libsecret

%if %{with cvs}
%package cvs
Summary:        Git tools for importing CVS repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       cvs
Requires:       cvsps
Requires:       perl(DBD::SQLite)
# safe replacement
Provides:       git-cvs = %{version}-%{release}
Conflicts:      git-cvs < %{version}-%{release}
%description cvs
%{summary}.
%endif
# endif with cvs

%package daemon
Summary:        Git protocol daemon
Requires:       git-core = %{version}-%{release}
Requires:       systemd
Requires(post): systemd
Requires(preun):  systemd
Requires(postun): systemd
# safe replacement
Provides:       git-daemon = %{version}-%{release}
Provides:       git-daemon%{?_isa} = %{version}-%{release}
Conflicts:      git-daemon < %{version}-%{release}
%description daemon
The git daemon for supporting git:// access to git repositories

%package email
Summary:        Git tools for sending patches via email
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Authen::SASL)
Requires:       perl(Cwd)
Requires:       perl(Email::Valid)
Requires:       perl(File::Spec)
Requires:       perl(File::Spec::Functions)
Requires:       perl(File::Temp)
Requires:       perl(IO::Socket::SSL)
Requires:       perl(Mail::Address)
Requires:       perl(MIME::Base64)
Requires:       perl(MIME::QuotedPrint)
Requires:       perl(Net::Domain)
Requires:       perl(Net::SMTP)
Requires:       perl(Net::SMTP::SSL)
Requires:       perl(POSIX)
Requires:       perl(Sys::Hostname)
Requires:       perl(Term::ANSIColor)
Requires:       perl(Term::ReadLine)
Requires:       perl(Text::ParseWords)
# safe replacement
Provides:       git-email = %{version}-%{release}
Conflicts:      git-email < %{version}-%{release}
%description email
%{summary}.

%package gitk
Summary:        Git repository browser
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
Requires:       tk >= 8.4
# safe replacement
Provides:       gitk = %{version}-%{release}
Conflicts:      gitk < %{version}-%{release}
%description gitk
%{summary}.

%package gitweb
Summary:        Simple web interface to git repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
# safe replacement
Provides:       gitweb = %{version}-%{release}
Conflicts:      gitweb < %{version}-%{release}
%description gitweb
%{summary}.

%package gui
Summary:        Graphical interface to Git
BuildArch:      noarch
Requires:       gitk = %{version}-%{release}
Requires:       tk >= 8.4
# safe replacement
Provides:       git-gui = %{version}-%{release}
Conflicts:      git-gui < %{version}-%{release}
%description gui
%{summary}.

%package instaweb
Summary:        Repository browser in gitweb
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       gitweb = %{version}-%{release}
%if 0%{?rhel} >= 9
Requires:       httpd
%else
Requires:       lighttpd
%endif
# safe replacement
Provides:       git-instaweb = %{version}-%{release}
Conflicts:      git-instaweb < %{version}-%{release}

%description instaweb
A simple script to set up gitweb and a web server for browsing the local
repository.

%if %{with p4}
%package p4
Summary:        Git tools for working with Perforce depots
BuildArch:      noarch
%if %{with python3}
BuildRequires:  python3-devel
%else
%if %{with python2}
BuildRequires:  python2-devel
%endif
# endif with python2
%endif
# endif with python3
Requires:       git = %{version}-%{release}
# safe replacement
Provides:       git-p4 = %{version}-%{release}
Conflicts:      git-p4 < %{version}-%{release}
%description p4
%{summary}.
%endif
# endif with p4

%package perl-Git
Summary:        Perl interface to Git
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# safe replacement
Provides:       perl-Git = %{version}-%{release}
Conflicts:      perl-Git < %{version}-%{release}
%description perl-Git
%{summary}.

%package perl-Git-SVN
Summary:        Perl interface to Git::SVN
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# safe replacement
Provides:       perl-Git-SVN = %{version}-%{release}
Conflicts:      perl-Git-SVN < %{version}-%{release}
%description perl-Git-SVN
%{summary}.

%package subtree
Summary:        Git tools to merge and split repositories
Requires:       git-core = %{version}-%{release}
# safe replacement
Provides:       git-subtree = %{version}-%{release}
Provides:       git-subtree%{?_isa} = %{version}-%{release}
Conflicts:      git-subtree < %{version}-%{release}
%description subtree
Git subtrees allow subprojects to be included within a subdirectory
of the main project, optionally including the subproject's entire
history.

%package svn
Summary:        Git tools for interacting with Subversion repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Digest::MD5)
%if ! %{defined perl_bootstrap}
Requires:       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap
Requires:       subversion
# safe replacement
Provides:       git-svn = %{version}-%{release}
Conflicts:      git-svn < %{version}-%{release}
%description svn
%{summary}.

%prep
# Verify GPG signatures
xz -dc '%{SOURCE0}' | %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data=-

%autosetup -p1 -n git-%{version}%{?rcrev}

# Install print-failed-test-output script
install -p -m 755 %{SOURCE99} print-failed-test-output

# Remove git-archimport from command list
sed -i '/^git-archimport/d' command-list.txt

%if %{without cvs}
# Remove git-cvs* from command list
sed -i '/^git-cvs/d' command-list.txt
%endif
# endif without cvs

%if %{without p4}
# Remove git-p4 from command list
sed -i '/^git-p4/d' command-list.txt
%endif
# endif without p4

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
# Pipe to tee to aid confirmation/verification of settings.
cat << \EOF | tee config.mak
V = 1
CFLAGS = %{build_cflags}
LDFLAGS = %{build_ldflags}
USE_LIBPCRE = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
INSTALL_SYMLINKS = 1
GITWEB_PROJECTROOT = %{_localstatedir}/lib/git
GNU_ROFF = 1
NO_PERL_CPAN_FALLBACKS = 1
%if 0%{?rhel} && 0%{?rhel} < 8
NO_UNCOMPRESS2 = 1
%endif
%if %{with python3}
PYTHON_PATH = %{__python3}
%else
%if %{with python2}
PYTHON_PATH = %{__python2}
%else
NO_PYTHON = 1
%endif
%endif
%if %{with asciidoctor}
USE_ASCIIDOCTOR = 1
%endif
htmldir = %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
prefix = %{_prefix}
perllibdir = %{perl_vendorlib}
gitwebdir = %{_localstatedir}/www/git

# Test options
DEFAULT_TEST_TARGET = prove
GIT_PROVE_OPTS = --verbose --normalize %{?_smp_mflags} --formatter=TAP::Formatter::File
GIT_TEST_OPTS = -x --verbose-log
EOF

# Filter bogus perl requires
# packed-refs comes from a comment in contrib/hooks/update-paranoid
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(packed-refs\\)
%if ! %{defined perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Term::ReadKey\\)
%endif
# endif ! defined perl_bootstrap

# Remove Git::LoadCPAN to ensure we use only system perl modules.  This also
# allows the dependencies to be automatically processed by rpm.
rm -rf perl/Git/LoadCPAN{.pm,/}
grep -rlZ '^use Git::LoadCPAN::' | xargs -r0 sed -i 's/Git::LoadCPAN:://g'

# Update gitweb default home link string
sed -i 's@"++GITWEB_HOME_LINK_STR++"@$ENV{"SERVER_NAME"} ? "git://" . $ENV{"SERVER_NAME"} : "projects"@' \
    gitweb/gitweb.perl

# Move contrib/{contacts,subtree} docs to Documentation so they build with the
# proper asciidoc/docbook/xmlto options
mv contrib/{contacts,subtree}/git-*.txt Documentation/

%build
# Improve build reproducibility
export TZ=UTC
export SOURCE_DATE_EPOCH=$(date -r version +%%s 2>/dev/null)

%make_build all %{?with_docs:doc}

%make_build -C contrib/contacts/ all

%if %{with libsecret}
%make_build -C contrib/credential/libsecret/
%endif
# endif with libsecret

%make_build -C contrib/credential/netrc/

%make_build -C contrib/diff-highlight/

%make_build -C contrib/subtree/ all

# Fix shebang in a few places to silence rpmlint complaints
%if %{with python2}
sed -i -e '1s@#! */usr/bin/env python$@#!%{__python2}@' \
    contrib/fast-import/import-zips.py
%else
# Remove contrib/fast-import/import-zips.py which requires python2.
rm -rf contrib/fast-import/import-zips.py
%endif
# endif with python2

# Use python3 to avoid an unnecessary python2 dependency, if possible.
%if %{with python3}
sed -i -e '1s@#!\( */usr/bin/env python\|%{__python2}\)$@#!%{__python3}@' \
    contrib/hg-to-git/hg-to-git.py
%endif
# endif with python3

%install
%make_install %{?with_docs:install-doc}

%make_install -C contrib/contacts

%if %{with emacs}
%global elispdir %{_emacs_sitelispdir}/git
pushd contrib/emacs >/dev/null
for el in *.el ; do
    # Note: No byte-compiling is done.  These .el files are one-line stubs
    # which only serve to point users to better alternatives.
    install -Dpm 644 $el %{buildroot}%{elispdir}/$el
    rm -f $el # clean up to avoid cruft in git-core-doc
done
popd >/dev/null
%endif
# endif with emacs

%if %{with libsecret}
install -pm 755 contrib/credential/libsecret/git-credential-libsecret \
    %{buildroot}%{gitexecdir}
%endif
# endif with libsecret
install -pm 755 contrib/credential/netrc/git-credential-netrc \
    %{buildroot}%{gitexecdir}
# temporarily move contrib/credential/netrc aside to prevent it from being
# deleted in the docs preparation, so the tests can be run in %%check
mv contrib/credential/netrc .

%make_install -C contrib/subtree

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -pm 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
sed "s|@PROJECTROOT@|%{_localstatedir}/lib/git|g" \
    %{SOURCE14} > %{buildroot}%{_sysconfdir}/gitweb.conf

# install contrib/diff-highlight and clean up to avoid cruft in git-core-doc
install -Dpm 0755 contrib/diff-highlight/diff-highlight \
    %{buildroot}%{_datadir}/git-core/contrib/diff-highlight
rm -rf contrib/diff-highlight/{Makefile,diff-highlight,*.perl,t}

# Remove contrib/scalar to avoid cruft in the git-core-doc docdir
rm -rf contrib/scalar

# Clean up contrib/subtree to avoid cruft in the git-core-doc docdir
rm -rf contrib/subtree/{INSTALL,Makefile,git-subtree*,t}

# git-archimport is not supported
find %{buildroot} Documentation -type f -name 'git-archimport*' -exec rm -f {} ';'

%if %{without cvs}
# Remove git-cvs* and gitcvs*
find %{buildroot} Documentation \( -type f -o -type l \) \
    \( -name 'git-cvs*' -o -name 'gitcvs*' \) -exec rm -f {} ';'
%endif
# endif without cvs

%if %{without p4}
# Remove git-p4* and mergetools/p4merge
find %{buildroot} Documentation -type f -name 'git-p4*' -exec rm -f {} ';'
rm -f %{buildroot}%{gitexecdir}/mergetools/p4merge
%endif
# endif without p4

# Remove unneeded git-remote-testsvn so git-svn can be noarch
rm -f %{buildroot}%{gitexecdir}/git-remote-testsvn

exclude_re="archimport|email|git-(citool|credential-libsecret|cvs|daemon|gui|instaweb|p4|subtree|svn)|gitk|gitweb|p4merge"
(find %{buildroot}{%{_bindir},%{_libexecdir}} -type f -o -type l | grep -vE "$exclude_re" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}{%{_bindir},%{_libexecdir}} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
(find %{buildroot}%{perl_vendorlib} -type f | sed -e s@^%{buildroot}@@) > perl-git-files
(find %{buildroot}%{perl_vendorlib} -mindepth 1 -type d | sed -e 's@^%{buildroot}@%dir @') >> perl-git-files
# Split out Git::SVN files
grep Git/SVN perl-git-files > perl-git-svn-files
sed -i "/Git\/SVN/ d" perl-git-files
%if %{with docs}
(find %{buildroot}%{_mandir} -type f | grep -vE "$exclude_re|Git" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf %{buildroot}%{_mandir}
%endif
# endif with docs

mkdir -p %{buildroot}%{_localstatedir}/lib/git
install -Dp -m 0644 %{SOURCE16} %{buildroot}%{_unitdir}/git.socket
perl -p \
    -e "s|\@GITEXECDIR\@|%{gitexecdir}|g;" \
    -e "s|\@BASE_PATH\@|%{_localstatedir}/lib/git|g;" \
    %{SOURCE15} > %{buildroot}%{_unitdir}/git@.service

# Setup bash completion
install -Dpm 644 contrib/completion/git-completion.bash %{buildroot}%{bashcompdir}/git
ln -s git %{buildroot}%{bashcompdir}/gitk

# Install tcsh completion
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-completion.tcsh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# Move contrib/hooks out of %%docdir
mkdir -p %{buildroot}%{_datadir}/git-core/contrib
mv contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
pushd contrib > /dev/null
ln -s ../../../git-core/contrib/hooks
popd > /dev/null

# Install git-prompt.sh
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-prompt.sh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# install git-gui .desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE12}

# symlink git-citool to git-gui if they are identical
pushd %{buildroot}%{gitexecdir} >/dev/null
if cmp -s git-gui git-citool 2>/dev/null; then
    ln -svf git-gui git-citool
fi
popd >/dev/null

# find translations
%find_lang git git.lang
cat git.lang >> bin-man-doc-files

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
chmod a-x %{buildroot}%{gitexecdir}/git-mergetool--lib
# These files probably are not needed
find . -regex '.*/\.\(git\(attributes\|ignore\)\|perlcriticrc\)' -delete
chmod a-x Documentation/technical/api-index.sh
find contrib -type f -print0 | xargs -r0 chmod -x

# Split core files
not_core_re="git-(add--interactive|contacts|credential-netrc|filter-branch|instaweb|request-pull|send-mail)|gitweb"
grep -vE "$not_core_re|%{_mandir}" bin-man-doc-files > bin-files-core
touch man-doc-files-core
%if %{with docs}
grep -vE "$not_core_re" bin-man-doc-files | grep "%{_mandir}" > man-doc-files-core
%endif
# endif with docs
grep -E  "$not_core_re" bin-man-doc-files > bin-man-doc-git-files

##### DOC
# place doc files into %%{_pkgdocdir} and split them into expected packages
# contrib
not_core_doc_re="(git-(cvs|gui|citool|daemon|instaweb|subtree))|p4|svn|email|gitk|gitweb"
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -pr CODE_OF_CONDUCT.md README.md Documentation/*.txt Documentation/RelNotes contrib %{buildroot}%{_pkgdocdir}/
# Remove contrib/ files/dirs which have nothing useful for documentation
rm -rf %{buildroot}%{_pkgdocdir}/contrib/{contacts,credential}/
cp -p gitweb/INSTALL %{buildroot}%{_pkgdocdir}/INSTALL.gitweb
cp -p gitweb/README %{buildroot}%{_pkgdocdir}/README.gitweb

%if %{with docs}
cp -pr Documentation/*.html Documentation/docbook-xsl.css %{buildroot}%{_pkgdocdir}/
cp -pr Documentation/{howto,technical} %{buildroot}%{_pkgdocdir}/
find %{buildroot}%{_pkgdocdir}/{howto,technical} -type f \
    |grep -o "%{_pkgdocdir}.*$" >> man-doc-files-core
%endif
# endif with docs

{
    find %{buildroot}%{_pkgdocdir} -type f -maxdepth 1 \
        | grep -o "%{_pkgdocdir}.*$" \
        | grep -vE "$not_core_doc_re"
    find %{buildroot}%{_pkgdocdir}/{contrib,RelNotes} -type f \
        | grep -o "%{_pkgdocdir}.*$"
    find %{buildroot}%{_pkgdocdir} -type d | grep -o "%{_pkgdocdir}.*$" \
        | sed "s/^/\%dir /"
} >> man-doc-files-core
##### #DOC

%check
%if %{without tests}
echo "*** Skipping tests"
exit 0
%endif
# endif without tests

%if %{with docs} && %{with linkcheck}
# Test links in HTML documentation
find %{buildroot}%{_pkgdocdir} -name "*.html" -print0 | xargs -r0 linkchecker
%endif
# endif with docs && with linkcheck

# Tests to skip on all releases and architectures
GIT_SKIP_TESTS=""

%ifarch aarch64 %{arm} %{power64}
# Skip tests which fail on aarch64, arm, and ppc
#
# The following 2 tests use run_with_limited_cmdline, which calls ulimit -s 128
# to limit the maximum stack size.
# t5541.36 'push 2000 tags over http'
# t5551.25 'clone the 2,000 tag repo to check OS command line overflow'
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t5541.36 t5551.25"
%endif
# endif aarch64 %%{arm} %%{power64}

%ifarch %{power64}
# Skip tests which fail on ppc
#
# t9115-git-svn-dcommit-funky-renames is disabled because it frequently fails.
# The port it uses (9115) is already in use.  It is unclear if this is
# due to an issue in the test suite or a conflict with some other process on
# the build host.  It only appears to occur on ppc-arches.
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t9115"
%endif
# endif %%{power64}

%ifarch s390x && 0%{?rhel} == 8
# Skip tests which fail on s390x on rhel-8
#
# The following tests fail on s390x & el8.  The cause should be investigated.
# However, it's a lower priority since the same tests work consistently on
# s390x with Fedora and RHEL-9.  The failures seem to originate in t5300.
#
# t5300.10 'unpack without delta'
# t5300.12 'unpack with REF_DELTA'
# t5300.14 'unpack with OFS_DELTA'
# t5303.5  'create corruption in data of first object'
# t5303.7  '... and loose copy of second object allows for partial recovery'
# t5303.11 'create corruption in data of first delta'
# t6300.35 'basic atom: head objectsize:disk'
# t6300.91 'basic atom: tag objectsize:disk'
# t6300.92 'basic atom: tag *objectsize:disk'
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t5300.{10,12,14} t5303.{5,7,11} t6300.{35,91,92}"
%endif
# endif s390x && rhel == 8

export GIT_SKIP_TESTS

# Set LANG so various UTF-8 tests are run
export LANG=en_US.UTF-8

# Explicitly enable tests which may be skipped opportunistically
# Check for variables set via test_bool_env in the test suite:
#   git grep 'test_bool_env GIT_' -- t/{lib-,t[0-9]}*.sh |
#       sed -r 's/.* (GIT_[^ ]+) .*/\1/g' | sort -u
export GIT_TEST_GIT_DAEMON=true
export GIT_TEST_HTTPD=false
export GIT_TEST_SVNSERVE=true
export GIT_TEST_SVN_HTTPD=false

# Create tmpdir for test output and update GIT_TEST_OPTS
# Also update GIT-BUILD-OPTIONS to keep make from any needless rebuilding
testdir=$(mktemp -d -p /tmp git-t.XXXX)
sed -i "s@^GIT_TEST_OPTS = .*@& --root=$testdir@" config.mak
touch -r GIT-BUILD-OPTIONS ts
sed -i "s@\(GIT_TEST_OPTS='.*\)'@\1 --root=$testdir'@" GIT-BUILD-OPTIONS
touch -r ts GIT-BUILD-OPTIONS

# Run the tests
%__make -C t all || ./print-failed-test-output

# Run contrib/credential/netrc tests
mkdir -p contrib/credential
mv netrc contrib/credential/
%make_build -C contrib/credential/netrc/ test || \
%make_build -C contrib/credential/netrc/ testverbose

# Clean up test dir
rmdir --ignore-fail-on-non-empty "$testdir"

%post daemon
%systemd_post git.socket

%preun daemon
%systemd_preun git.socket

%postun daemon
%systemd_postun_with_restart git.socket

%files -f bin-man-doc-git-files
%if %{with emacs}
%{elispdir}
%endif
# endif with emacs
%{_datadir}/git-core/contrib/diff-highlight
%{_datadir}/git-core/contrib/hooks/update-paranoid
%{_datadir}/git-core/contrib/hooks/setgitperms.perl
%{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%{_datadir}/git-core/templates/hooks/pre-rebase.sample
%{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample

%files all
# No files for you!

%files core -f bin-files-core
#NOTE: this is only use of the %%doc macro in this spec file and should not
#      be used elsewhere
%{!?_licensedir:%global license %doc}
%license COPYING
# exclude is best way here because of troubles with symlinks inside git-core/
%exclude %{_datadir}/git-core/contrib/diff-highlight
%exclude %{_datadir}/git-core/contrib/hooks/update-paranoid
%exclude %{_datadir}/git-core/contrib/hooks/setgitperms.perl
%exclude %{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%exclude %{_datadir}/git-core/templates/hooks/pre-rebase.sample
%exclude %{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%{bashcomproot}
%{_datadir}/git-core/

%files core-doc -f man-doc-files-core
%if 0%{?rhel} && 0%{?rhel} <= 7
# .py files are only bytecompiled on EL <= 7
%exclude %{_pkgdocdir}/contrib/*/*.py[co]
%endif
# endif rhel <= 7
%{_pkgdocdir}/contrib/hooks

%if %{with libsecret}
%files credential-libsecret
%{gitexecdir}/git-credential-libsecret
%endif
# endif with libsecret

%if %{with cvs}
%files cvs
%{_pkgdocdir}/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{gitexecdir}/*cvs*
%{?with_docs:%{_mandir}/man1/*cvs*.1*}
%{?with_docs:%{_pkgdocdir}/*git-cvs*.html}
%endif
# endif with cvs

%files daemon
%{_pkgdocdir}/git-daemon*.txt
%{_unitdir}/git.socket
%{_unitdir}/git@.service
%{gitexecdir}/git-daemon
%{_localstatedir}/lib/git
%{?with_docs:%{_mandir}/man1/git-daemon*.1*}
%{?with_docs:%{_pkgdocdir}/git-daemon*.html}

%files email
%{_pkgdocdir}/*email*.txt
%{gitexecdir}/*email*
%{?with_docs:%{_mandir}/man1/*email*.1*}
%{?with_docs:%{_pkgdocdir}/*email*.html}

%files gitk
%{_pkgdocdir}/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk
%{?with_docs:%{_mandir}/man1/*gitk*.1*}
%{?with_docs:%{_pkgdocdir}/*gitk*.html}

%files gitweb
%{_pkgdocdir}/*.gitweb
%{_pkgdocdir}/gitweb*.txt
%{?with_docs:%{_mandir}/man1/gitweb.1*}
%{?with_docs:%{_mandir}/man5/gitweb.conf.5*}
%{?with_docs:%{_pkgdocdir}/gitweb*.html}
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
%{_localstatedir}/www/git/

%files gui
%{gitexecdir}/git-gui*
%{gitexecdir}/git-citool
%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui/
%{_pkgdocdir}/git-gui.txt
%{_pkgdocdir}/git-citool.txt
%{?with_docs:%{_mandir}/man1/git-gui.1*}
%{?with_docs:%{_pkgdocdir}/git-gui.html}
%{?with_docs:%{_mandir}/man1/git-citool.1*}
%{?with_docs:%{_pkgdocdir}/git-citool.html}

%files instaweb
%{gitexecdir}/git-instaweb
%{_pkgdocdir}/git-instaweb.txt
%{?with_docs:%{_mandir}/man1/git-instaweb.1*}
%{?with_docs:%{_pkgdocdir}/git-instaweb.html}

%if %{with p4}
%files p4
%{gitexecdir}/*p4*
%{gitexecdir}/mergetools/p4merge
%{_pkgdocdir}/*p4*.txt
%{?with_docs:%{_mandir}/man1/*p4*.1*}
%{?with_docs:%{_pkgdocdir}/*p4*.html}
%endif
# endif with p4

%files perl-Git -f perl-git-files
%{?with_docs:%{_mandir}/man3/Git.3pm*}

%files perl-Git-SVN -f perl-git-svn-files

%files subtree
%{gitexecdir}/git-subtree
%{_pkgdocdir}/git-subtree.txt
%{?with_docs:%{_mandir}/man1/git-subtree.1*}
%{?with_docs:%{_pkgdocdir}/git-subtree.html}

%files svn
%{gitexecdir}/git-svn
%{_pkgdocdir}/git-svn.txt
%{?with_docs:%{_mandir}/man1/git-svn.1*}
%{?with_docs:%{_pkgdocdir}/git-svn.html}

%changelog
* Tue May 2 2023 James Kennedy <github@9815.ca> - 2.36.6-1
- Update to version 2.36.6
- Fixes CVE-2023-25652, CVS-2023-25815, and CVE-2023-29007

* Wed Feb 15 2023 Danilo Braband <dbraband@gmail.com> - 2.36.5-1
- Update to version 2.36.5
- Fixes CVE-2023-23946 and CVE-2023-22490

* Fri Jan 20 2023 Danilo Braband <dbraband@gmail.com> - 2.36.4-1
- Update to version 2.36.4
- Fixes CVE-2022-23521 and CVE-2022-41903

* Tue Nov 22 2022 Jeff Sheltren <jeff@tag1consulting.com> - 2.36.3-1
- Update to version 2.36.3
- Fixes CVE-2022-39253 and CVE-2022-39260

* Fri Sep 30 2022 Carl George <carl@george.computer> - 2.36.2-1
- Update to version 2.36.2
- Fixes CVE-2022-29187

* Mon May 09 2022 Carl George <carl@george.computer> - 2.36.1-2
- Port from Fedora to IUS

* Fri May 06 2022 Todd Zullinger <tmz@pobox.com> - 2.36.1-1
- update to 2.36.1

* Mon Apr 18 2022 Todd Zullinger <tmz@pobox.com> - 2.36.0-1
- update to 2.36.0

* Thu Apr 14 2022 Todd Zullinger <tmz@pobox.com> - 2.36.0-0.3.rc2
- usability improvements on top of CVE-2022-24765

* Wed Apr 13 2022 Todd Zullinger <tmz@pobox.com> - 2.36.0-0.2.rc2
- update to 2.36.0-rc2 (CVE-2022-24765)
- disable failing tests on s390x on EL8

* Fri Apr 08 2022 Todd Zullinger <tmz@pobox.com> - 2.36.0-0.1.rc1
- update to 2.36.0-rc1

* Tue Apr 05 2022 Todd Zullinger <tmz@pobox.com> - 2.36.0-0.0.rc0
- update to 2.36.0-rc0
- use httpd-core for tests on Fedora >= 37

* Sat Jan 29 2022 Todd Zullinger <tmz@pobox.com> - 2.35.1-1
- update to 2.35.1

* Mon Jan 24 2022 Todd Zullinger <tmz@pobox.com> - 2.35.0-1
- update to 2.35.0
- set path to linker script in %%_package_note_file

* Sat Jan 22 2022 Todd Zullinger <tmz@pobox.com> - 2.35.0-0.2.rc2.3
- remove contrib/scalar to avoid cruft in git-core-doc

* Fri Jan 21 2022 Todd Zullinger <tmz@pobox.com> - 2.35.0-0.2.rc2.2
- fix compilation on EL7

* Thu Jan 20 2022 Todd Zullinger <tmz@pobox.com> - 2.35.0-0.2.rc2.1
- checkout: avoid BUG() when hitting a broken repository (rhbz#2042920)

* Wed Jan 19 2022 Todd Zullinger <tmz@pobox.com> - 2.35.0-0.2.rc2
- update to 2.35.0-rc2

* Sat Jan 15 2022 Todd Zullinger <tmz@pobox.com> - 2.35.0-0.1.rc1
- update to 2.35.0-rc1

* Mon Jan 10 2022 Todd Zullinger <tmz@pobox.com> - 2.35.0-0.0.rc0
- update to 2.35.0-rc0

* Thu Nov 25 2021 Todd Zullinger <tmz@pobox.com> - 2.34.1-1
- update to 2.34.1
- fix gpgsm issues with gnupg-2.3

* Mon Nov 15 2021 Todd Zullinger <tmz@pobox.com> - 2.34.0-1
- update to 2.34.0

* Sun Nov 14 2021 Todd Zullinger <tmz@pobox.com> - 2.33.1-3
- add more git-email perl dependencies
- Resolves: rhbz#2020487

* Thu Nov 11 2021 Ondřej Pohořelský <opohorel@redhat.com> - 2.33.1-2
- add Perl requires to git-email
- Resolves: rhbz#2020487

* Wed Oct 13 2021 Todd Zullinger <tmz@pobox.com> - 2.33.1-1
- update to 2.33.1

* Mon Sep 27 2021 Ondřej Pohořelský <opohorel@redhat.com> - 2.33.0-1
- update to 2.33.0
- contrib/hooks/multimail is no longer distributed with git

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.32.0-1.2
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 06 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-1
- update to 2.32.0
- add perl(File::Compare) BuildRequires
- fix var to enable git-svn tests with httpd
- remove %%changelog entries prior to 2019

* Thu Jun 03 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.5.rc3
- drop jgit on Fedora >= 35
  Resolves: rhbz#1965808

* Wed Jun 02 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.4.rc3
- update to 2.32.0-rc3

* Fri May 28 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.3.rc2
- update to 2.32.0-rc2

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.32.0-0.2.rc1
- Perl 5.34 re-rebuild of bootstrapped packages

* Sat May 22 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.1.rc1
- update to 2.32.0-rc1
- rearrange python2/python3 conditionals
- re-enable git-p4 with python3
- add coreutils BuildRequires
- remove unneeded NEEDS_CRYPTO_WITH_SSL

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.31.1-3.1
- Perl 5.34 rebuild

* Mon May 17 2021 Todd Zullinger <tmz@pobox.com> - 2.32.0-0.0.rc0
- update to 2.32.0-rc0

* Sun May 16 2021 Todd Zullinger <tmz@pobox.com>
- clean up various dist conditionals

* Wed Apr 21 2021 Todd Zullinger <tmz@pobox.com> - 2.31.1-3
- apply upstream patch to fix clone --bare segfault
  Resolves: rhbz#1952030

* Tue Apr 06 2021 Todd Zullinger <tmz@pobox.com> - 2.31.1-2
- remove two stray %%defattr macros from %%files sections

* Sat Mar 27 2021 Todd Zullinger <tmz@pobox.com> - 2.31.1-1
- update to 2.31.1

* Fri Mar 19 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-2
- fix git bisect with annotaged tags

* Mon Mar 15 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-1
- update to 2.31.0

* Tue Mar 09 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-0.2.rc2
- update to 2.31.0-rc2

* Wed Mar 03 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-0.1.rc1
- update to 2.31.0-rc1

* Tue Mar 02 2021 Todd Zullinger <tmz@pobox.com> - 2.31.0-0.0.rc0
- update to 2.31.0-rc0

* Tue Mar 02 2021 Todd Zullinger <tmz@pobox.com> - 2.30.1-3
- use %%{gpgverify} macro to verify tarball signature

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.30.1-2.1
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Thu Feb 18 2021 Ondřej Pohořelský <opohorel@redhat.com - 2.30.1-2
- include git-daemon in git-all meta-package

* Thu Feb 18 2021 Todd Zullinger <tmz@pobox.com>
- re-enable t7812-grep-icase-non-ascii on s390x

* Tue Feb 09 2021 Todd Zullinger <tmz@pobox.com> - 2.30.1-1
- update to 2.30.1

* Mon Feb 08 2021 Ondřej Pohořelský <opohorel@redhat.com> - 2.30.0-2
- add rhel 9 conditional to require httpd instead of lighttpd in git-instaweb

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 28 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-1
- update to 2.30.0

* Wed Dec 23 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-0.2.rc2
- update to 2.30.0-rc2

* Sat Dec 19 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-0.1.rc1
- update to 2.30.0-rc1

* Mon Dec 14 2020 Todd Zullinger <tmz@pobox.com> - 2.30.0-0.0.rc0
- update to 2.30.0-rc0

* Sun Dec 06 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-4
- move git-difftool to git-core, it does not require perl

* Wed Nov 25 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-3
- apply upstream patch to resolve git fast-import memory leak (#1900335)
- add epel-rpm-macros BuildRequires on EL-7 (#1872865)

* Sat Nov 07 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-2
- apply upstream patch to resolve git log segfault (#1791810)

* Thu Oct 29 2020 Todd Zullinger <tmz@pobox.com> - 2.29.2-1
- update to 2.29.2

* Sat Oct 24 2020 Todd Zullinger <tmz@pobox.com> - 2.29.1-1
- update to 2.29.1
- fix bugs in am/rebase handling of committer ident/date

* Mon Oct 19 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-1
- update to 2.29.0

* Thu Oct 15 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-0.2.rc2
- update to 2.29.0-rc2

* Fri Oct 09 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-0.1.rc1
- update to 2.29.0-rc1
- drop emacs-git stub for fedora >= 34 (#1882360)
- adjust python hashbang in contrib/hg-to-git, it supports python3

* Mon Oct 05 2020 Todd Zullinger <tmz@pobox.com> - 2.29.0-0.0.rc0
- update to 2.29.0-rc0

* Mon Jul 27 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-1
- update to 2.28.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.0-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-0.2.rc2
- update to 2.28.0-rc2

* Sat Jul 18 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-0.1.rc1
- update to 2.28.0-rc1

* Thu Jul 09 2020 Todd Zullinger <tmz@pobox.com> - 2.28.0-0.0.rc0
- update to 2.28.0-rc0

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.27.0-1.2
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.27.0-1.1
- Perl 5.32 rebuild

* Mon Jun 01 2020 Todd Zullinger <tmz@pobox.com> - 2.27.0-1
- update to 2.27.0

* Tue May 26 2020 Todd Zullinger <tmz@pobox.com> - 2.27.0-0.2.rc2
- update to 2.27.0-rc2

* Thu May 21 2020 Todd Zullinger <tmz@pobox.com> - 2.27.0-0.1.rc1
- update to 2.27.0-rc1

* Thu May 21 2020 Merlin Mathesius <mmathesi@redhat.com> - 2.26.2-2
- Minor conditional fixes for ELN

* Mon Apr 20 2020 Todd Zullinger <tmz@pobox.com> - 2.26.2-1
- update to 2.26.2 (CVE-2020-11008)

* Tue Apr 14 2020 Todd Zullinger <tmz@pobox.com> - 2.26.1-1
- update to 2.26.1 (CVE-2020-5260)

* Sat Apr 04 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-2
- fix issue with fast-forward rebases when rebase.abbreviateCommands is set
- fix/quiet rpmlint issues from libsecret split

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 2.26.0-1.1
- Fix string quoting for rpm >= 4.16

* Sun Mar 22 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-1
- update to 2.26.0

* Mon Mar 16 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.3.rc2
- update to 2.26.0-rc2

* Thu Mar 12 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.2.rc1
- remove s390x gcc10 workaround (#1799408)

* Tue Mar 10 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.1.rc1
- update to 2.26.0-rc1
- adjust make test options
- add missing build deps for tests

* Fri Mar 06 2020 Todd Zullinger <tmz@pobox.com> - 2.26.0-0.0.rc0
- update to 2.26.0-rc0

* Wed Feb 26 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-4
- use Asciidoctor to build documentation when possible

* Sat Feb 22 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-3
- work around issue on s390x with gcc10 (#1799408)

* Wed Feb 19 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-2
- split libsecret credential helper into a subpackage (#1804741)
- consolidate macros for Fedora/EPEL
- remove unneeded gnome-keyring obsoletes

* Mon Feb 17 2020 Todd Zullinger <tmz@pobox.com> - 2.25.1-1
- update to 2.25.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Tom Stellard <tstellar@redhat.com> - 2.25.0-2
- Use make_build macro when running tests

* Tue Jan 14 2020 Todd Zullinger <tmz@pobox.com> - 2.25.0-1
- update to 2.25.0

* Thu Jan 09 2020 Todd Zullinger <tmz@pobox.com> - 2.25.0-0.2.rc2
- update to 2.25.0-rc2

* Fri Jan 03 2020 Todd Zullinger <tmz@pobox.com> - 2.25.0-0.1.rc1
- update to 2.25.0-rc1
- only add highlight test BR for ppc64le/x86_64 on EL7+

* Wed Dec 25 2019 Todd Zullinger <tmz@pobox.com> - 2.25.0-0.0.rc0
- update to 2.25.0-rc0

* Thu Dec 19 2019 Todd Zullinger <tmz@pobox.com> - 2.24.1-2
- fix git-daemon systemd scriptlets (#1785088)

* Tue Dec 10 2019 Todd Zullinger <tmz@pobox.com> - 2.24.1-1
- update to 2.24.1 (CVE-2019-1348, CVE-2019-1349, CVE-2019-1350, CVE-2019-1351,
  CVE-2019-1352, CVE-2019-1353, CVE-2019-1354, and CVE-2019-1387)

* Wed Dec 04 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-2
- restore jgit BR for use in tests

* Mon Nov 04 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-1
- update to 2.24.0

* Thu Oct 31 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.2.rc2
- update to 2.24.0-rc2

* Sun Oct 27 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.1.rc1.1
- disable linkchecker on all EL releases

* Thu Oct 24 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.1.rc1
- update to 2.24.0-rc1
- skip failing test in t7812-grep-icase-non-ascii on s390x
- gitk: add Requires: git-gui (#1765113)

* Sat Oct 19 2019 Todd Zullinger <tmz@pobox.com> - 2.24.0-0.0.rc0
- update to 2.24.0-rc0
- fix t0500-progress-display on big-endian arches

* Fri Aug 16 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-1
- Update to 2.23.0

* Sun Aug 11 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.2.rc2
- Update to 2.23.0-rc2

* Fri Aug 02 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.1.rc1
- Update to 2.23.0-rc1

* Mon Jul 29 2019 Todd Zullinger <tmz@pobox.com> - 2.23.0-0.0.rc0
- Update to 2.23.0-rc0

* Thu Jul 25 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-2
- completion: do not cache if --git-completion-helper fails
- avoid trailing comments in spec file
- drop jgit on Fedora > 30

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-1
- Update to 2.22.0

* Tue Jun 04 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.7.rc3
- Perl 5.30 re-rebuild updated packages

* Mon Jun 03 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.6.rc3
- Update to 2.22.0-rc3

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.5.rc2
- Perl 5.30 re-rebuild of bootstrapped packages

* Sat Jun 01 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.22.0-0.4.rc2
- Perl 5.30 rebuild

* Thu May 30 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.3.rc2
- Update to 2.22.0-rc1

* Fri May 24 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.2.rc1
- Apply upstream fixes for diff-parseopt issues on s390x

* Sun May 19 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.1.rc1
- Update to 2.22.0-rc1

* Mon May 13 2019 Todd Zullinger <tmz@pobox.com> - 2.22.0-0.0.rc0
- Update to 2.22.0-rc0
- Ensure a consistent format for test output
- Improve JGIT test prereq (jgit on Fedora >= 30 is broken)
- Add perl(JSON::PP) BuildRequires for trace2 tests

* Sun Feb 24 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-1
- Update to 2.21.0
- Move gitweb manpages to gitweb package
- Link git-citool to git-gui if they are identical

* Tue Feb 19 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.2.rc2
- Update to 2.21.0.rc2

* Fri Feb 15 2019 Todd Zullinger <tmz@pobox.com>
- Set SOURCE_DATE_EPOCH and TZ to improve build reproducibility

* Wed Feb 13 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.1.rc1
- Update to 2.21.0.rc1

* Thu Feb 07 2019 Todd Zullinger <tmz@pobox.com> - 2.21.0-0.0.rc0
- Update to 2.21.0.rc0
- Remove %%changelog entries prior to 2017

* Thu Jan 31 2019 Todd Zullinger <tmz@pobox.com> - 2.20.1-2
- Remove extraneous pcre BuildRequires
- Add additional BuildRequires for i18n locales used in tests
- Replace gitweb home-link with inline sed
- Add gnupg2-smime and perl JSON BuildRequires for tests
- Work around gpg-agent issues in the test suite
- Drop gnupg BuildRequires on fedora >= 30
- Fix formatting of contrib/{contacts,subtree} docs
- Use %%{build_cflags} and %%{build_ldflags}
- Drop unneeded TEST_SHELL_PATH make variable

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.20.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
