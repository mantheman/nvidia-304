# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels akmod
%global debug_package %{nil}

Name:          nvidia-304xx-kmod
Version:       304.137
# Taken over by kmodtool
Release:       101%{?dist}
Summary:       NVIDIA display driver kernel module
Group:         System Environment/Kernel
License:       Redistributable, no modification permitted
URL:           http://www.nvidia.com/
# Source is created from these files:
#ftp://download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}-pkg0.run
#ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-pkg0.run
Source0:       nvidia-kmod-data-%{version}.tar.xz

Source11:      nvidia-304xx-kmodtool-excludekernel-filterfile
# https://anonscm.debian.org/viewvc/pkg-nvidia/packages/nvidia-graphics-drivers-legacy-304xx/trunk/debian/module/debian/patches/disable-mtrr.patch?view=markup
Patch0: disable-warnings.patch
Patch2: 0001-disable-mtrr-4.3.patch
Patch3: 0002-pud-offset-4.12.patch
Patch4: 0003-nvidia-drm-pci-init-4.14.patch
Patch5: 0004-timer-4.15.patch
Patch6: 0005-usercopy-4.16.patch
Patch7: 0006-do_gettimeofday-5.0.patch
Patch8: 0007-subdirs-5.3.patch
Patch9: 0008-on-each-cpu-5.3.patch
Patch10: 0009-remove-drmp-5.5.patch
Patch11: 0010-proc-ops-5.6.patch
Patch12: 0011-kernel-5.7.0-setmemoryarray.patch
Patch13: 0012-kernel5.8.patch
Patch14: 0013-kernel5.9.patch
Patch15: 0014-import-drm_legacy_pci_init-exit-from-src-linux-5.9.1.patch
Patch16: 0015-add-static-and-nv_-prefix-to-copied-drm-legacy-bits.patch
Patch17: 0016-fix-mistake.patch
Patch18: 0016-vmalloc5.9.patch
Patch19: 0017-patch-14-kernel-5.11.patch
Patch20: 0018-kernel5.14.patch
Patch21: 0019-kernel-5.16.patch
Patch22: 0020-kernel-5.17.patch
Patch23: 0021-kernel-5.18.patch
Patch24: 0022-kernel-6.0.patch
Patch25: 0023-kernel-6.2.patch
Patch26: 0024-kernel-6.3.patch
Patch27: 0025-kernel-6.5.patch
Patch28: 0026-gcc14-fix.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i686 x86_64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} --obsolete-name nvidia --obsolete-version "1:304.1000" %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The nvidia %{version} display driver kernel module for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} --obsolete-name nvidia --obsolete-version "1:304.1000" %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T -a 0

# patch loop
for arch in x86 x64
do
pushd nvidiapkg-${arch}
%autopatch -p1
popd
done


for kernel_version  in %{?kernel_versions} ; do
%ifarch %{ix86}
    cp -a nvidiapkg-x86 _kmod_build_${kernel_version%%___*}
%else
    cp -a nvidiapkg-x64 _kmod_build_${kernel_version%%___*}
%endif
done

%build
for kernel_version in %{?kernel_versions}; do
  pushd _kmod_build_${kernel_version%%___*}/kernel/
    make %{?_smp_mflags}  SYSSRC="${kernel_version##*___}" module
  popd
done


%install
rm -rf $RPM_BUILD_ROOT
for kernel_version in %{?kernel_versions}; do
    install -D -m 0755 _kmod_build_${kernel_version%%___*}/kernel/nvidia.ko $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/nvidia.ko
done
%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 304.137-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Feb 13 2018 Nerijus Baliūnas <nerijus@users.sourceforge.net> - 304.137-4
- patch for kernel-4.15

* Wed Dec 06 2017 Nerijus Baliūnas <nerijus@users.sourceforge.net> - 304.137-3
- patch for kernel-4.14

* Fri Sep 22 2017 Nerijus Baliūnas <nerijus@users.sourceforge.net> - 304.137-2
- remove no longer needed 4.12_kernel.patch

* Fri Sep 22 2017 Nerijus Baliūnas <nerijus@users.sourceforge.net> - 304.137-1
- Update to 304.137

* Mon Sep 04 2017 Nerijus Baliūnas <nerijus@users.sourceforge.net> - 304.135-6
- updated patch for kernel-4.12

* Sat Aug 12 2017 Leigh Scott <leigh123linux@googlemail.com> - 304.135-5
- patch for kernel-4.12

* Sun Apr 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 304.135-4
- patch for kernel-4.11rc

* Mon Feb 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 304.135-3
- patch for kernel-4.10

* Wed Feb 15 2017 Leigh Scott <leigh123linux@googlemail.com> - 304.135-2
- remove disable mtrr patch

* Wed Feb 15 2017 Leigh Scott <leigh123linux@googlemail.com> - 304.135-1
- Update to 304.135

* Mon Jan 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 304.134-2
- patch to fix loading module on 4.9 kernel

* Wed Dec 14 2016 leigh scott <leigh123linux@googlemail.com> - 304.134-1
- Update to 304.134

* Tue Sep 27 2016 Leigh Scott <leigh123linux@googlemail.com> - 304.132-1
- Update to 304.132

* Sun Jul 24 2016 leigh scott <leigh123linux@googlemail.com> - 304.131-4
- switch to akmod build

* Fri Jul 01 2016 Leigh Scott <leigh123linux@googlemail.com> - 304.131-3
- patch for kernel-4.6

* Mon Feb 15 2016 Orion Poplawski <orion@cora.nwra.com> - 304.131-2
- Add patch for 4.3 kernel

* Thu Nov 19 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.131-1
- Update to 304.131

* Tue Oct 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.128-1.3
- Rebuilt for kernel

* Wed Sep 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.128-1.2
- Rebuilt for kernel

* Wed Sep 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.128-1.1
- Rebuilt for kernel

* Thu Sep 03 2015 Leigh Scott <leigh123linux@googlemail.com> - 304.128-1
- Update to 304.128

* Fri Aug 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.20
- Rebuilt for kernel

* Thu Aug 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.19
- Rebuilt for kernel

* Fri Aug 07 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.18
- Rebuilt for kernel

* Thu Jul 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.17
- Rebuilt for kernel

* Fri Jul 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.16
- Rebuilt for kernel

* Thu Jul 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.15
- Rebuilt for kernel

* Thu Jul 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.14
- Rebuilt for kernel

* Sun Jun 28 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.13
- Rebuilt for kernel

* Wed Jun 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.12
- Rebuilt for kernel

* Tue Jun 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.11
- Rebuilt for kernel

* Sun May 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.10
- Rebuilt for kernel

* Wed May 20 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.9
- Rebuilt for kernel

* Wed May 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.8
- Rebuilt for kernel

* Sat May 09 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.7
- Rebuilt for kernel

* Sat May 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.6
- Rebuilt for kernel

* Wed Apr 22 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.5
- Rebuilt for kernel

* Wed Apr 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.4
- Rebuilt for kernel

* Mon Mar 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.3
- Rebuilt for kernel

* Fri Mar 27 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.2
- Rebuilt for kernel

* Mon Mar 23 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-3.1
- Rebuilt for kernel

* Sat Mar 21 2015 Leigh Scott <leigh123linux@googlemail.com> - 304.125-3
- Patch for 3.19 kernel

* Sat Mar 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-2.2
- Rebuilt for kernel

* Tue Mar 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-2.1
- Rebuilt for kernel

* Thu Mar 05 2015 Leigh Scott <leigh123linux@googlemail.com> - 304.125-2
- Patch for 4.0.0 kernel

* Sat Feb 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.8
- Rebuilt for kernel

* Sun Feb 08 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.7
- Rebuilt for kernel

* Wed Feb 04 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.6
- Rebuilt for kernel

* Mon Feb 02 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.5
- Rebuilt for kernel

* Wed Jan 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.4
- Rebuilt for kernel

* Thu Jan 15 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.3
- Rebuilt for kernel

* Sat Jan 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.2
- Rebuilt for kernel

* Fri Dec 19 2014 Nicolas Chauvet <kwizart@gmail.com> - 304.125-1.1
- Rebuilt for kernel

* Tue Dec 16 2014 Leigh Scott <leigh123linux@googlemail.com> - 304.125-1
- Update to 304.125

* Sun Dec 14 2014 Nicolas Chauvet <kwizart@gmail.com> - 304.123-2.1
- Rebuilt for kernel

* Fri Dec 05 2014 Nicolas Chauvet <kwizart@gmail.com> - 304.123-2
- Rebuilt for f21 final kernel

* Thu Jul 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 304.123-1
- Update to 304.123

* Fri Mar 14 2014 Leigh Scott <leigh123linux@googlemail.com> - 304.121-1
- Update to 304.121

* Fri Jan 24 2014 Leigh Scott <leigh123linux@googlemail.com> - 304.119-1
- Update to 304.119

* Tue Jan 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 304.117-4
- make more changes to 3.13 kernel patch

* Mon Jan 13 2014 Leigh Scott <leigh123linux@googlemail.com> - 304.117-3
- fix 3.13.0 kernel patch for EFI systems with CSM disabled

* Mon Dec 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 304.117-2
- patch for 3.13.0 kernel

* Sat Dec 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.117-1
- Update to 304.117

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.116-4
- Rebuilt for f20 final kernel

* Sat Dec 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.116-3
- Rebuilt for f20 final kernel

* Sun Dec 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.116-2
- Rebuilt for f20 final kernel

* Sun Dec 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 304.116-1
- Update to 304.116

* Wed Nov 06 2013 Leigh Scott <leigh123linux@googlemail.com> - 304.108-4
- use nvidia fix for get_num_physpages

* Wed Sep 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 304.108-3
- patch for 3.12.0 kernel

* Tue Aug 13 2013 Leigh Scott <leigh123linux@googlemail.com> - 304.108-2
- build for akmod

* Tue Aug 13 2013 Leigh Scott <leigh123linux@googlemail.com> - 304.108-1
- Update to 304.108
- patch for 3.11.0 kernel

* Fri Jul 26 2013 Leigh Scott <leigh123linux@googlemail.com> - 304.88-2
- patch for 3.10 kernel

* Fri Jul 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.8
- Rebuilt for kernel

* Sat Jul 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.7
- Rebuilt for kernel

* Sat Jul 06 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.6
- Rebuilt for kernel

* Sun Jun 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.5
- Rebuilt for kernel

* Sat Jun 29 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.4
- Rebuilt for kernel

* Fri Jun 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.3
- Rebuilt for current f19 kernel

* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.2
- Rebuilt for current f19 kernel

* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1.1
- Rebuilt for kernel

* Sun May 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 304.88-1
- Rename to 304xx serie

* Thu Apr 04 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.88-1
- Update to 304.88

* Tue Apr 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-7.5
- Rebuilt for kernel

* Fri Mar 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-7.4
- Rebuilt for kernel

* Mon Mar 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-7.3
- Rebuilt for kernel

* Fri Mar 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-7.2
- Rebuilt for kernel

* Mon Mar 11 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-7.1
- Rebuilt for kernel

* Fri Mar 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-7
- Modify 3.7 patch for 3.8 kernel

* Thu Feb 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-6.5
- Rebuilt for kernel

* Tue Feb 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-6.4
- Rebuilt for kernel

* Thu Feb 21 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-6.3
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-6.2
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-6.1
- Rebuilt for kernel

* Fri Feb 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-6
- Fix with a better patch from gentoo

* Wed Feb 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-4.1
- Rebuilt for kernel

* Tue Feb 05 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:304.64-4
- Rebuilt as I forgot to change to current

* Tue Feb 05 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:304.64-3
- patch for 3.7.6 kernel compile issue

* Tue Feb 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-2.6
- Rebuilt for kernel

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-2.5
- Rebuilt for updated kernel

* Fri Jan 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-2.4
- Rebuilt for updated kernel

* Thu Jan 17 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-2.3
- Rebuilt for updated kernel

* Mon Jan 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-2.2
- Rebuilt for updated kernel

* Sun Jan 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-2.1
- Rebuilt for updated kernel

* Sun Jan 06 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:304.64-2
- patched and rebuilt for 3.7 kernel

* Thu Jan 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-1.4
- Rebuilt for f18 final kernel

* Fri Dec 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-1.3
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-1.2
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-1.1
- Rebuilt for Fedora 18 Beta kernel

* Thu Nov 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:304.64-1
- Update to 304.64

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.60-1
- Update to 304.60

* Mon Sep 24 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.51-1
- Update to 304.51

* Sat Sep 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.48-1
- Update to 304.48

* Wed Sep 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:304.43-1
- Update to 304.43

* Tue Aug 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.37-1
- Update to 304.37 release

* Sat Aug 04 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.32-2
- build again as the build system lost the first one

* Sat Aug 04 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.32-1
- Update to 304.32

* Tue Jul 31 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.30-2
- add some conditionals to the 3.6 kernel patch

* Tue Jul 31 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.30-1
- Update to 304.30

* Fri Jul 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:304.22-1
- Update to 304.22

* Sat Jun 16 2012 leigh scott <leigh123linux@googlemail.com> - 1:302.17-1
- Update to 302.17

* Tue May 22 2012 leigh scott <leigh123linux@googlemail.com> - 1:302.11-1
- Update to 302.11

* Tue May 22 2012 leigh scott <leigh123linux@googlemail.com> - 1:295.53-1
- Update to 295.53

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.49-1.4
- Rebuilt for release kernel

* Wed May 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.49-1.3
- rebuild for updated kernel

* Sun May 06 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.49-1.2
- rebuild for updated kernel

* Sat May 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.49-1.1
- rebuild for updated kernel

* Thu May 03 2012 leigh scott <leigh123linux@googlemail.com> - 1:295.49-1
- Update to 295.49

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.40-1.5
- rebuild for updated kernel

* Sat Apr 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.40-1.4
- rebuild for updated kernel

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.40-1.3
- rebuild for updated kernel

* Mon Apr 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.40-1.2
- rebuild for updated kernel

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.40-1.1
- rebuild for beta kernel

* Wed Apr 11 2012 leigh scott <leigh123linux@googlemail.com> - 1:295.40-1
- Update to 295.40

* Thu Mar 22 2012 leigh scott <leigh123linux@googlemail.com> - 1:295.33-1
- Update to 295.33

* Thu Mar 22 2012 leigh scott <leigh123linux@googlemail.com> - 1:295.20-2
- patched to build with 3.3.0 kernel

* Tue Feb 14 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.20-1
- Update to 295.20

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.17-1.1
- Rebuild for UsrMove

* Wed Feb 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:295.17-1
- Update to 295.17 (beta)

* Sat Dec 31 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:295.09-1
- Update to 295.09 (beta)

* Tue Nov 22 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:290.10-1
- Update to 290.10

* Wed Nov 09 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:290.06-1
- Update to 290.06 beta

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:285.05.09-1.4
- Rebuild for F-16 kernel

* Tue Nov 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:285.05.09-1.3
- Rebuild for F-16 kernel

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:285.05.09-1.2
- Rebuild for F-16 kernel

* Sun Oct 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:285.05.09-1.1
- Rebuild for F-16 kernel

* Tue Oct 04 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:285.05.09-1
- Update to 285.05.09

* Sat Aug 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:285.03-1
- Update to 285.03
- Remove kernel-xen filter

* Tue Aug 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:280.13-2
- Update to 280.13

* Sun Jul 24 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:280.11-1
- Update to 280.11

* Fri Jul 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:280.04-1
- Update to 280.04 (beta)

* Tue Jun 14 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:275.09.07-1
- Update to 275.09.07

* Wed Jun 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:270.41.19-1
- Update to 270.41.19

* Sat Apr 30 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:270.41.06-1
- Update to 270.41.06

* Tue Apr 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:270.41.03-1
- Update to 270.41.03

* Thu Mar 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:270.30-1
- Update to 270.30

* Tue Mar 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:270.29-1
- Update to 270.29

* Sun Jan 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:270.18-1
- Update to 270.18 beta

* Fri Jan 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:260.19.36-1
- Update to 260.19.36

* Tue Dec 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 1:260.19.29-1
- Update to 260.19.29

* Thu Nov 11 2010 Nicolas Chauvet <kwizart@gmail.com> - 1:260.19.21-1
- Update to 260.19.21

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 1:260.19.12-1
- Update to 260.19.12

* Thu Oct 07 2010 Nicolas Chauvet <kwizart@gmail.com> - 1:260.19.06-1
- Update to 260.19.06 beta

* Wed Sep 01 2010 Nicolas Chauvet <kwizart@gmail.com> - 1:256.53-1
- Update to 256.53

* Thu Aug 05 2010 Nicolas Chauvet <kwizart@gmail.com> - 1:256.44-1
- Update to 256.44

* Fri Jun 18 2010 Vallimar de Morieve <vallimar@gmail.com> - 1:256.35-1
- update to 256.35

* Thu Jun 17 2010 Nicolas Chaubvet <kwizart@gmail.com> - 1:195.36.31-1
- Update to 195.36.31
- Fix acpi_walk_namespace call with kernel 2.6.33 and later.
  http://bugs.gentoo.org/show_bug.cgi?id=301318 

* Sun Jun 13 2010 Nicolas Chauvet <kwizart@gmail.com> - 1:195.36.24-2
- Backport IOMMU - http://www.nvnews.net/vbulletin/showthread.php?t=151791

* Sat Apr 24 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1:195.36.24-1
- Update to 195.36.24

* Sat Mar 27 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1:195.36.15-1
- Update to 195.36.15

* Fri Mar 12 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1:190.53-3
- Bump Epoch - Fan problem in recent release

* Mon Mar 08 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1:190.53-2
- Revert to 190.53 version 
  http://www.nvnews.net/vbulletin/announcement.php?f=14

* Sat Feb 27 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 195.36.08-1
- Update to 195.36.08

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.53-1.6
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.53-1.5
- rebuild for new kernel

* Thu Feb 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.53-1.4
- rebuild for new kernel

* Wed Feb 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.53-1.3
- rebuild for new kernel

* Sat Jan 30 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.53-1.2
- rebuild for new kernel

* Wed Jan 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.53-1.1
- rebuild for new kernel

* Wed Dec 30 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 190.53-1
- Update to 190.53
- Add patch for VGA_ARB

* Sat Dec 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.9
- rebuild for new kernel

* Thu Dec 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.8
- rebuild for new kernel

* Sun Dec 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.7
- rebuild for new kernel

* Wed Nov 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.6
- rebuild for new kernel

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.5
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.4
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.3
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.2
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 190.42-1.1
- rebuild for new kernels

* Sat Oct 31 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 190.42-1
- Update to 190.42

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.36-1.3
- rebuild for new kernels

* Wed Sep 30 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.36-1.2
- rebuild for new kernels

* Tue Sep 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.36-1.1
- rebuild for new kernels

* Sat Aug 29 2009 kwizart < kwizart at gmail.com > - 185.18.36-1
- Update to 185.18.36 (final)

* Thu Aug 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.14-1.8
- rebuild for new kernels

* Sun Aug 23 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.14-1.7
- rebuild for new kernels

* Sat Aug 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.14-1.6
- rebuild for new kernels

* Sat Aug 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.14-1.5
- rebuild for new kernels

* Fri Aug 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.14-1.4
- rebuild for new kernels

* Fri Aug  7 2009 kwizart < kwizart at gmail.com > - 185.18.14-1.3
- Revert to 185.18.14
- rebuild for new kernels

* Tue Jul 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 185.18.14-1.2
- rebuild for new kernels

* Mon Jun 22 2009 kwizart < kwizart at gmail.com > - 185.18.14-1.1
- rebuild for new kernels

* Fri Jun  5 2009 kwizart < kwizart at gmail.com > - 185.18.14-1
- Update to 185.18.14 (final)

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.8
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.7
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.6
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.5
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.4
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.3
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.2
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.51-1.1
- rebuild for new kernels

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 180.51-1
- Update to 180.51 (stable)
- Don't Obsoletes the beta serie anymore (only the newest)

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.37-2.1
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.37-2
- rebuild for new F11 features

* Mon Mar  9 2009 kwizart < kwizart at gmail.com > - 180.37-1
- Update to 180.37 (prerelease)

* Thu Feb 26 2009 kwizart < kwizart at gmail.com > - 180.35-2
- Handle Obsoletes/Provides in nvidia-kmod for nvidia-beta-kmod

* Wed Feb 25 2009 kwizart < kwizart at gmail.com > - 180.35-1
- Update to 180.35 (prerelease)

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.29-1.1
- rebuild for latest Fedora kernel;

* Tue Feb 10 2009 kwizart < kwizart at gmail.com > - 180.29-1
- Update to 180.29 (stable)
- Reintroduce build for i586 since it will match for SSE without PAE CPU.
 (remember that nvidia main series needs SSE capable CPU).
- Empty the xen exclusion filter.

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.27-1.1
- rebuild for latest Fedora kernel;

* Thu Jan 29 2009 kwizart < kwizart at gmail.com > - 180.27-1
- Update to 180.27 (beta)

* Tue Jan 27 2009 kwizart < kwizart at gmail.com > - 180.25-1
- Update to 180.25 (beta)

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.22-1.3
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.22-1.2
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.22-1.1
- rebuild for latest Fedora kernel;

* Thu Jan  8 2009 kwizart < kwizart at gmail.com > - 180.22-1
- Update to 180.22 (stable)

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.18-1.2
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.18-1.1
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 kwizart < kwizart at gmail.com > - 180.18-1
- Update to 180.18 (beta)

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 180.16-1.1
- rebuild for latest Fedora kernel;

* Wed Dec 17 2008 kwizart < kwizart at gmail.com > - 180.16-1
- Update to 180.16

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.82-1.5
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.82-1.4
- rebuilt

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.82-1.3
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.82-1.2
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.82-1.1
- rebuild for latest Fedora kernel;

* Thu Nov 13 2008 kwizart < kwizart at gmail.com > - 177.82-1
- Update to 177.82

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.80-1.4
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.80-1.3
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.80-1.2
- rebuild for latest rawhide kernel

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.80-1.1
- rebuild for latest rawhide kernel

* Mon Oct 13 2008 kwizart < kwizart at gmail.com > - 177.80-1
- Update to 177.80

* Sun Oct 5 2008 Stewart Adam <s.adam at diffingo.com> - 177.78-3
- Disable EXTRA_LDFLAGS in patches

* Sun Oct 05 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 177.78-2.1
- rebuild for rpm fusion

* Wed Oct 1 2008 Stewart Adam < s.adam at diffingo.com > - 177.78-1
- Update to 177.78 beta

* Mon Sep 15 2008 Stewart Adam < s.adam at diffingo.com > - 177.70-1
- Update to 177.70
- Skip all Xen sanity checks

* Thu Jul 31 2008 kwizart < kwizart at gmail.com > - 173.14.12-1
- Update to 173.14.12

* Tue Jun 17 2008 kwizart < kwizart at gmail.com > - 173.14.09-1
- Update to 173.14.09
- Remove i586 (driver needs CPU to have SSE)

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 173.14.05-2
- Add NVIDIA_kernel-173.14.05-2419292.diff.txt

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 173.14.05-1
- Update to 173.14.05

* Thu Apr 10 2008 kwizart < kwizart at gmail.com > - 173.08-1
- Update to 173.08 (beta) - Fedora 9 experimental support
  See: http://www.nvnews.net/vbulletin/showthread.php?t=111460

* Wed Mar 19 2008 kwizart < kwizart at gmail.com > - 171.06-2
- Add Patch for 2.6.25rc kernels

* Fri Mar  7 2008 kwizart < kwizart at gmail.com > - 171.06-1
- Update to 171.06 (beta)

* Wed Feb 27 2008 kwizart < kwizart at gmail.com > - 169.12-1
- Update to 169.12

* Sun Feb  3 2008 kwizart < kwizart at gmail.com > - 169.09-5
- typo fixes

* Sat Feb  2 2008 kwizart < kwizart at gmail.com > - 169.09-3
- Reenable debuginfo
- Disable xen check properly (still not working)
- Remove the smbus patch (uneeded).

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 169.09-2
- rebuild for new kmodtools, akmod adjustments

* Wed Jan 23 2008 Stewart Adam <s.adam AT diffingo DOT com> - 169.09-1
- Update to 169.09
- Fix License tag

* Sun Jan 20 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 169.07-2
- build akmods package

* Sat Dec 22 2007 Stewart Adam < s.adam AT diffingo DOT com > - 169.07-1
- Update to 169.07
- Don't build debug to fix BuildID error

* Mon Nov 05 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-17
- rebuilt for F8 kernels

* Wed Oct 31 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-16
- rebuilt for latest kernels

* Tue Oct 30 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-15
- rebuilt for latest kernels

* Sun Oct 28 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-14
- rebuilt for latest kernels
- adjust to rpmfusion and new kmodtool

* Sat Oct 27 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-13
- rebuilt for latest kernels

* Tue Oct 23 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-12
- rebuilt for latest kernels

* Mon Oct 22 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-11
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-10
- rebuilt for latest kernels

* Thu Oct 18 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-9
- rebuilt for latest kernels

* Fri Oct 12 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-8
- rebuilt for latest kernels

* Thu Oct 11 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-7
- rebuilt for latest kernels

* Wed Oct 10 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 100.14.19-6
- rebuilt for latest kernels

* Tue Oct 09 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 100.14.19-5
- rebuilt for latest kernels

* Sun Oct 07 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> 
- build for rawhide kernels as of today

* Thu Oct 04 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 100.14.19-3
- fix typo

* Wed Oct 03 2007 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 100.14.19-2
- update for new kmod-helper stuff
- build for newest kernels

* Thu Sep 20 2007 kwizart < kwizart at gmail.com > - 100.14.19-1
- Update to Final 100.14.19

* Sun Sep 09 2007 Thorsten Leemhuis < fedora AT leemhuis DOT info > - 100.14.11-4
- Build for latest only

* Sun Sep 09 2007 Thorsten Leemhuis < fedora AT leemhuis DOT info > - 100.14.11-3
- Convert to new kmods stuff from livna
- Rebuild for F8T2 and rawhide

* Fri Aug 10 2007 Stewart Adam < s.adam AT diffingo DOT com > - 100.14.11-2
- Add patch from nvnews for 2.6.23rc2 support
- Rebuild for F8T1

* Thu Jun 21 2007 Stewart Adam < s.adam AT diffingo DOT com > - 100.14.11-1
- Update to 100.14.11
- Drop unneeded patches

* Sun Jun 10 2007 kwizart < kwizart at gmail.com > - 100.14.09-1
- Update to Final 100.14.09

* Sun May 27 2007 kwizart < kwizart at gmail.com > - 1.0.9762-1
- Update to 1.0.9762

* Fri Apr 27 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9755-3
- Rebuild for F7T4 (fixed kversion)
- Fix changelog dates

* Fri Apr 27 2007 kwizart < kwizart at gmail.com > - 1.0.9755-2
- Build for Fedora test4 kernel

* Thu Mar 8 2007 kwizart < kwizart at gmail.com > - 1.0.9755-1
- Update to 1.0.9755
- Build to current 2.6.20-1.2967.fc7

* Sun Mar 4 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9746-7
- kdump for non-i686
- Fix dates in changelog

* Sat Mar 3 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9746-6
- No kdump
- New kernel

* Fri Mar 2 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9746-5
- New kernel
- Make Source0 a URL

* Sat Feb 24 2007 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9746-4
- Standardize all summaries and descriptions with other nvidia and fglrx
  packages
- Move paths from nvidia-glx to nvidia

* Wed Feb 7 2007 kwizart < kwizar at gmail.com > - 1.0.9746-3
- Disable xen variant

* Wed Feb 7 2007 kwizart < kwizar at gmail.com > - 1.0.9746-2
- Rebuild for Fedora Core 7 test1

* Tue Dec 26 2006 kwizart < kwizart at gmail.com > - 1.0.9746-1
- Update to release 1.0.9746 (Final).
- Standard version do not support xen kernel.
- Update xen patch: patch-nv-1.0-9625-xenrt.txt

* Thu Nov 23 2006 Stewart Adam < s.adam AT diffingo DOT com > - 1.0.9742-2
- Change %%description, as NV30 and below no longer supported
- Update nvidia desktop file

* Mon Nov 20 2006 kwizart < kwiart at gmail.com > - 1.0.9742-1
- Update to release 1.0.9742

* Tue Nov 07 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.9629-1
- update to release 1.0.9629
- include xen patch (thx to Bob Richmond)

* Wed Nov 01 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.9626-2
- include patch from 
  http://www.nvnews.net/vbulletin/showpost.php?p=996233&postcount=20

* Sun Oct 22 2006 Stewart Adam <s.adam AT diffingo DOT com> - 1.0.9626-1
- update to release 1.0.9626

* Sat Oct 07 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8774-2
- sed-away the config.h include

* Thu Aug 24 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8774-1
- update to release 1.0.8774

* Thu Aug 10 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-5
- update for kernel 2.6.17-1.2174_FC5

* Mon Aug 07 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-4
- forgot to update release field

* Fri Aug 04 2006 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 1.0.8762-3
- minor changes to spacing, removal of random tabs, re-arrangements

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.8762-2
- Invoke kmodtool with bash instead of sh.

* Wed May 24 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8762-1
- update to 1.0.8762

* Sun May 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.8756-3
- Require version >= of nvidia-kmod-common.
- Provide nvidia-kmod instead of kmod-nvidia to fix upgrade woes (#970).

* Thu Apr 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.8756-2
- Provide "kernel-modules" instead of "kernel-module" to match yum's config.

* Sat Apr 08 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8756-1
- Update to 8756
- drop patch

* Thu Mar 23 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-6
- disable xen0 for now

* Wed Mar 22 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-5
- build for 2.6.16-1.2069_FC5

* Wed Mar 22 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-4
- allow to pass kversion and kvariants via command line

* Sat Mar 18 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.8178-3
- drop 0.lvn
- use kmodtool from svn
- hardcode kernel and variants

* Mon Jan 30 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.2
- Some minor fixes
- new kmodtool

* Sun Jan 22 2006 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 1.0.8178-0.lvn.1
- split into packages for userland and kmod
- rename to nvidia-kmod

* Thu Dec 22 2005 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 0:1.0.8178-0.lvn.2
- change nvidia-glx.sh and nvidia-glx.csh to point to README.txt rather than README
- reference xorg.conf rather than XF86Config in the init script
- improve readability of instructions and comments, fix some typos
- drop epoch, as it seems to be affecting dependencies according to rpmlint
- tweak the nvidia-settings desktop file so it always shows up on the
  menu in the right location
- add the manual pages for nvidia-settings and nvidia-xconfig
- remove header entries from the nvidia-glx files list. they belong in -devel
- fix changelog entries to refer to 7676 not 7176 (though there was a 7176 x86_64
  release prior to 7174)
- add libXvMCNVIDIA.so
- update to 8178

* Wed Dec 07 2005 Niko Mirthes (straw) <nmirthes AT gmail DOT com> - 0:1.0.8174-0.lvn.1
- add the manual pages for nvidia-settings and nvidia-xconfig
- install the new nvidia-xconfig utility and associated libs

* Mon Dec 05 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.8174-0.lvn.1
- Update to 8174
- desktop entry now Categories=Settings (#665)
- Ship bug-reporting tool in doc (#588)
- Things from Bug 635, Niko Mirthes (straw) <nmirthes AT gmail DOT com>:
-- avoid changing time stamps on libs where possible
-- only add /etc/modprobe.conf entries if they aren't already there
-- add /etc/modprobe.conf entries one at a time
-- only remove /etc/modprobe.conf entries at uninstall, not during upgrade
-- avoid removing any modprobe.conf entries other than our own
-- match Xorg's install defaults where it makes sense (0444)
-- a few other minor tweaks to the files lists

* Sun Sep 04 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.3
- Conflics with nvidia-glx-legacy
- Integrate some minor correction suggested by Niko Mirthes
  <nmirthes AT gmail DOT com> in #475

* Fri Aug 26 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.2
- Rename src5: nvidia.init to nvidia-glx-init
- Fix correct servicename in nvidia-glx-init
- Run nvidia-glx-init before gdm-early-login; del and readd the script
  during post

* Sun Aug 21 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7676-0.lvn.1
- Update to 7676
- Lots of cleanup from me and Niko Mirthes <nmirthes AT gmail DOT com>
- add NVreg_ModifyDeviceFiles=0 to modprobe.conf (Niko)
- Drop support for FC2
- Nearly proper Udev-Support with workarounds around FC-Bug 151527

* Fri Jun 17 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.5
- Slight change of modprobe.conf rexexp

* Thu Jun 16 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.4
- Fixed a critical bug in modprobe.conf editing where all lines starting with alias and
  ending with then a word starting with any of the letters n,v,i,d,i,a,N,V,r,e is removed.

* Mon Jun 13 2005 Thorsten Leemhuis <fedora AT leemhuis DOT info> - 0:1.0.7174-0.lvn.3
- Adjust kenrnel-module-stuff for FC4
- Ship both x86 and x64 in the SRPM

* Sun Jun 12 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.2
- Only create 16 devices
- Put libXvMCNVIDIA.a in -devel
- Don't remove nvidia options in /etc/modprobe.conf
- Make ld.so.conf file config(noreplace)
- Use same directory permissions as the kernel

* Sat Apr 2 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7174-0.lvn.1
- New upstream release, 7174

* Wed Mar 30 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.5
- Added x86_64 support patch from Thorsten Leemhuis

* Wed Mar 23 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.4
- Fix kernel module permissions again (644)
- Only create 16 /dev/nvidia* devices, 256 is unnecessary

* Fri Mar 18 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.3
- Fixed kernel-module permissions

* Thu Mar 17 2005 Dams <anvil[AT]livna.org> 0:1.0.7167-0.lvn.2
- Removed provides on kernel-module and kernel-modules

* Sat Mar 05 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.7167-0.lvn.1
- New upstream release 1.0.7167
- Added patch from http://www.nvnews.net/vbulletin/showthread.php?t=47405
- Removed old patch against 2.6.9

* Sat Feb 05 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.7
- Added a number of post-6629 patches from http://www.minion.de/files/1.0-6629
- Fixed permissions of nvidia/nvidia.ko

* Fri Jan 21 2005 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.6
- Fix incorrect MAKDEV behaviour and dependency

* Tue Nov 30 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.4
- Fixed creation of /dev/nvidia* on FC2

* Sat Nov 27 2004 Dams <anvil[AT]livna.org> - 0:1.0.6629-0.lvn.3
- Dont try to print kvariant in description when it's not defined.

* Sun Nov 21 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:1.0.6629-0.lvn.2
- resulting kernel-module package now depends again on /root/vmlinuz-<kernelver>
- Use rpmbuildtags driverp and kernelp

* Sat Nov 06 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6629-0.lvn.1
- New upstream version, 1.0-6629
- Build without kernel-module-devel by default

* Fri Oct 29 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.6
- Make n-c-display handle misc problems in a better way
- Fixed wrong icon file name in .desktop file
- Re-added the mysteriously vanished sleep line in the init script
  when kernel module wasn't present

* Fri Oct 22 2004 Thorsten Leemhuis <fedora at leemhuis dot info> - 0:1.0.6111-0.lvn.5
- Use fedora-kmodhelper in the way ntfs or ati-fglrx use it
- Allow rpm to strip the kernel module. Does not safe that much space ATM but
  might be a good idea
- Allow to build driver and kernel-module packages independent of each other
- Some minor spec-file changes

* Thu Oct 21 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.4
- udev fixes
- Incorporated fix for missing include line in ld.so.conf from ati-fglrx spec (T Leemhuis)

* Sun Sep 19 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.3
- Remove FC1/kernel 2.4 compability
- Rename srpm to nvidia-glx
- Build with kernel-module-devel

* Sun Aug 15 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.2
- Restore ldsoconfd macro
- Disable autoamtic removal of scripted installation for now; needs testing

* Sat Aug 14 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6111-0.lvn.1
- Upstream release 6111
- Fixed init script (again)

* Tue Aug  3 2004 Dams <anvil[AT]livna.org> 0:1.0.6106-0.lvn.4
- ld.so.conf.d directory detected by spec file
- Using nvidialibdir in nvidia-glx-devel files section
- Got rid of yarrow and tettnang macros
- libGL.so.1 symlink in tls directory always present

* Mon Jul 19 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.3
- Fixed script bug that would empty prelink.conf
- Added symlink to non-tls libGL.so.1 on FC1

* Tue Jul 13 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.3
- Updated init script to reflect name change -xfree86 -> -display

* Mon Jul 12 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.2
- Fixed backup file naming

* Sun Jul 11 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2.1
- Restore working macros
- Always package the gui tool

* Sun Jul 11 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.2
- Renamed nvidia-config-xfree86 to nvidia-config-display
- Fixed symlinks
- Use ld.so.conf.d on FC2
- Remove script installation in pre
- Use system-config-display icon for nvidia-settings
- 2 second delay in init script when kernel module not found
- Make nvidia-config-display fail more gracefully
- Add blacklist entry to prelink.conf on FC1

* Mon Jul 05 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.6106-0.lvn.1
- New upstream release
- First attempt to support FC2
- Dropped dependency on XFree86

* Mon Feb 09 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.5336-0.lvn.3
- Use pkg0

* Sun Feb 08 2004 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.5336-0.lvn.2
- New Makefile variable SYSSRC to point to kernel sources.
- kmodhelper fixes.

* Fri Jan 30 2004 Keith G. Robertson-Turner <nvidia-devel[AT]genesis-x.nildram.co.uk> 0:1.0.5336-0.lvn.1
- New upstream release
- Removed (now obsolete) kernel-2.6 patch
- Install target changed upstream, from "nvidia.o" to "module"
- Linked nv/Makefile.kbuild to (now missing) nv/Makefile

* Sun Jan 25 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.18
- Updated nvidia-config-display
- Now requiring pyxf86config

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.17
- Added nvidiasettings macro to enable/disable gui packaging

* Mon Jan 19 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.16
- Updated minion.de patches
- Added some explicit requires
- Test nvidia-config-xfree86 presence in kernel-module package
  scriptlets

* Mon Jan 12 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.15
- Updated Readme.fedora
- nvidia-glx-devel package

* Sat Jan  3 2004 Dams <anvil[AT]livna.org> 0:1.0.5328-0.lvn.14
- Hopefully fixed kernel variant thingy

* Fri Jan  2 2004 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.13
- Support for other kernel variants (bigmem, etc..)
- Changed URL in Source0

* Tue Dec 30 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.13
- Dropped nvidia pkgX information in release tag.

* Tue Dec 30 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.12.pkg0
- Renamed kernel module package in a kernel-module-nvidia-`uname -r` way
- Using fedora.us kmodhelper for kernel macro
- Using nvidia pkg0 archive

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.11.pkg1
- kernel-module-nvidia package provides kernel-module
- We wont own devices anymore. And we wont re-create them if they are
  already present

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.10.pkg1
- Yet another initscript update. Really.
- Scriptlets updated too

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.9.pkg1
- Fixed alias in modprobe.conf for 2.6

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.8.pkg1
- Another initscript update

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.7.pkg1
- kernel module requires kernel same kversion
- initscript updated again
- Dont conflict, nor obsolete XFree86-Mesa-libGL. Using ld.so.conf to
  make libGL from nvidia first found. Hope Mike Harris will appreciate.

* Sun Dec 21 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.6.pkg1
- kernel-module-nvidia requires kernel same version-release

* Sat Dec 20 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.6.pkg1
- Updated initscript

* Fri Dec 19 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.lvn.5.pkg1
- lvn repository tag

* Fri Dec 19 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.5.pkg1
- Added initscript to toggle nvidia driver according to running kernel
  and installed kernel-module-nvidia packages
- Updated scriptlets

* Thu Dec 18 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.4.pkg1
- Arch detection
- Url in patch0

* Tue Dec 16 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.3.pkg1
- Desktop entry for nvidia-settings
- s/kernel-module-{name}/kernel-module-nvidia
- nvidia-glx doesnt requires kernel-module-nvidia-driver anymore
- Using modprobe.conf for 2.6 kernel
- Hopefully fixed symlinks

* Mon Dec 15 2003 Dams <anvil[AT]livna.org> 0:1.0.4620-0.fdr.2.pkg1
- Building kernel module for defined kernel
- kernel module for 2.6 is nvidia.ko
- Patch not to install kernel module on make install
- Updated patch for 2.6
- depmod in scriptlet for defined kernel
- nvidia-glx conflicting XFree86-Mesa-libGL because we 0wn all its
  symlink now
- Dont override libGL.so symlink because it belongs to XFree86-devel
- Added nvidia 'pkgfoo' info to packages release
- Spec file cleanup

* Fri Dec 12 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4620-0.fdr.2
- Fixed repairing of a link in post-uninstall
- Obsolete Mesa instead of Conflict with it, enables automatic removal.

* Mon Dec 08 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4620-0.fdr.1
- Added support for 2.6 kernels
- Cleaned up build section, removed the need for patching Makefiles.
- Added missing BuildReq gcc32
- Don't package libs twice, only in /usr/lib/tls/nvidia
- Made config cript executable and put it into /usr/sbin
- Moved kernel module to kernel/drivers/video/nvidia/
- Fixed libGL.so and libGLcore.so.1 links to allow linking against OpenGL libraries

* Mon Dec 08 2003 Keith G. Robertson-Turner <nvidia-devel at genesis-x.nildram.co.uk> - 0:1.0.4620-0.fdr.0
- New beta 4620 driver
- New GUI control panel
- Some minor fixes

* Thu Nov 20 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.10.1
- Finally fixed SMP builds.

* Wed Nov 19 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.9
- Don't make nvidia-glx depend on kernel-smp

* Tue Nov 18 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.8
- Some build fixes

* Tue Nov 11 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.7
- Added CC=gcc32
- Fixed upgrading issue
- Added driver switching capabilities to config script.

* Fri Nov 07 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.4
- Added conflict with XFree86-Mesa-libGL.
- Disabled showing of the README.Fedora after installation.

* Sun Oct 12 2003 Peter Backlund <peter dot backlund at home dot se> - 0:1.0.4496-0.fdr.3
- Added NVidia configuration script written in Python.
- Some cleanup of files section
- For more info, see https://bugzilla.fedora.us/show_bug.cgi?id=402

* Tue Jul 08 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> - 0:1.0.4363-0.fdr.2
- renamed /sbin/makedevices.sh /sbin/nvidia-makedevices.sh ( noticed by
  Panu Matilainen )
- Fixed name problem
* Sun Jun 22 2003 Andreas Bierfert (awjb) <andreas.bierfert[AT]awbsworld.de> - 0:1.0.4363-0.fdr.1
- Initial RPM release, still some ugly stuff in there but should work..
