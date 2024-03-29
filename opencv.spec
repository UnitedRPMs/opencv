#
# spec file for package opencv
#
# Copyright (c) 2022 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

# Tips thanks 
# 1. http://www.linuxfromscratch.org/blfs/view/svn/general/opencv.html
# 2. https://src.fedoraproject.org/rpms/opencv
# 3. https://build.opensuse.org/package/show/openSUSE%3AFactory/opencv


%global debug_package %{nil}

%undefine _python_bytecompile_extra 

%global _python_bytecompile_extra %{nil}

%undefine __brp_python_bytecompile
%global __brp_python_bytecompile %{nil}

%undefine  py_byte_compile

%global abiver  405
%global dotabiver  4.5.5
%global javaver 455
%bcond_without qt5
%bcond_without freeworld
%bcond_with cuda
%bcond_with clang

Name:           opencv
Version:        4.5.5
Release:        9%{?dist}
Summary:        Collection of algorithms for computer vision
License:        BSD
Url:            http://opencv.org
Source0:	https://github.com/opencv/opencv/archive/%{version}.zip
Source1:        https://github.com/opencv/opencv_contrib/archive/%{version}.tar.gz
Patch:		ffmpeg5.patch
Patch1:		0001-highgui-Fix-unresolved-OpenGL-functions-for-Qt-backe.patch
Patch2:		vtk9.patch

%if %{with clang}
BuildRequires:	clang
%endif
BuildRequires:  libtool
BuildRequires:  cmake 
BuildRequires:  gtk3-devel
BuildRequires:  libwebp-devel
BuildRequires:  chrpath
BuildRequires:  eigen3-devel
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  tbb-devel
BuildRequires:  unzip 
BuildRequires:  ccache

BuildRequires:  openexr-devel >= 3.1.1
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libdc1394-2)
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libv4lconvert)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libglog)
BuildRequires:  gflags-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  fdupes
BuildRequires:  hdf5-devel

%if %{with qt5}
BuildRequires:  qt5-qtbase-devel
BuildRequires:  pkgconfig(Qt5Concurrent) >= 5.2.0
BuildRequires:  pkgconfig(Qt5Gui) >= 5.2.0
BuildRequires:  pkgconfig(Qt5OpenGL) >= 5.2.0
BuildRequires:  pkgconfig(Qt5Test) >= 5.2.0
BuildRequires:  pkgconfig(Qt5Widgets) >= 5.2.0
%else
BuildRequires:  pkgconfig(QtCore)
BuildRequires:  pkgconfig(QtGui)
BuildRequires:  pkgconfig(QtOpenGL)
BuildRequires:  pkgconfig(QtTest)
%endif

BuildRequires:  python2.7
BuildRequires:  python2-numpy
BuildRequires:  python2-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  swig >= 1.3.24
%if %{with freeworld}
BuildRequires:  ffmpeg-devel >= 5.0
BuildRequires:  xine-lib-devel
%endif
%if %{with cuda}
BuildRequires:  cuda
%endif
BuildRequires:  openblas-devel

BuildRequires:  gcc, gcc-c++
%if 0%{?fedora} >= 36
BuildRequires:	annobin-plugin-gcc
%endif
%if 0%{?fedora} >= 29
BuildRequires:	python-unversioned-command
%endif
# java
BuildRequires:  ant
BuildRequires:  java-devel

BuildRequires:	gstreamer1-plugins-base-devel
BuildRequires:	tbb-devel
BuildRequires:	libatomic
#BuildRequires:  ade-devel >= 0.1.0
BuildRequires:  vtk-devel

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package        core
Summary:        OpenCV core libraries
Recommends:     %{name}-xfeatures2d = %{version}-%{release}

%description    core
This package contains the OpenCV C/C++ core libraries.


%package        devel
Summary:        Development files for using the OpenCV library
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-contrib = %{version}-%{release}
Recommends:     %{name}-static = %{version}-%{release}

%description    devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. You should consider installing opencv-doc
package.


%package        doc
Summary:        docs files
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch
Provides:       %{name}-devel-docs = %{version}-%{release}

%description    doc
This package contains the OpenCV documentation, samples and examples programs.


%package        -n python2-%{name}
Summary:        Python2 bindings for apps which use OpenCV
Requires:       %{name} = %{version}-%{release}
Requires:       python2-numpy
# Remove before F30
%if 0%{?fedora} <= 30
Provides:       %{name}-python = %{version}-%{release}
Provides:       %{name}-python%{?_isa} = %{version}-%{release}
%endif

%description    -n python2-%{name}
This package contains Python bindings for the OpenCV library.


%package        -n python3-%{name}
Summary:        Python3 bindings for apps which use OpenCV
Requires:       %{name} = %{version}-%{release}
Requires:       python3-numpy
# Remove before F30
Provides:       %{name}-python3 = %{version}-%{release}
Provides:       %{name}-python3%{?_isa} = %{version}-%{release}


%description    -n python3-%{name}
This package contains Python3 bindings for the OpenCV library.


%package        contrib
Summary:        OpenCV contributed functionality
Recommends:     %{name}-xfeatures2d-devel = %{version}-%{release}

%description    contrib
This package is intended for development of so-called "extra" modules, contributed
functionality. New modules quite often do not have stable API, and they are not
well-tested. Thus, they shouldn't be released as a part of official OpenCV
distribution, since the library maintains binary compatibility, and tries
to provide decent performance and stability.

%if %{with freeworld}
%package        xfeatures2d
Summary:        xfeatures2d contrib

%description xfeatures2d
xfeatures2d contrib.

%package        xfeatures2d-devel
Summary:        Development files for using the OpenCV library
Requires:       %{name}-xfeatures2d = %{version}-%{release}

%description    xfeatures2d-devel
This package contains the OpenCV C/C++ library and header files. It should be installed if you want to develop programs that
will use the OpenCV library. 


%package        static
Summary:        Development static libs for OpenCV

%description    static
This package contains the OpenCV C/C++ static library. It should be installed if you want to develop programs that
will use the static OpenCV library.
%endif

%package 	java
Summary:	Java bindings for apps which use OpenCV
Requires:	java-headless
Requires:	javapackages-filesystem
Requires:	%{name}-core = %{version}-%{release}
Provides:	libopencv_java.so()(64bit)
 
%description 	java
This package contains Java bindings for the OpenCV library.

%prep
%setup -n opencv-%{version} -a 1 
%patch -p1
%patch1 -p1
%patch2 -p1
# Necessary Modules 
rm -rf modules/cudabgsegm
mv -f opencv_contrib-%{version}/modules/* modules/
cp opencv_contrib-%{version}/LICENSE LICENSE.contrib

# Remove Windows specific files
rm -f doc/packaging.txt


%build

%if %{with clang}
export CC=clang
export CXX=clang++
%else
export CC=gcc 
export CXX=g++
%endif

mkdir -p build

# cmake macro fails build

%cmake -B build                        \
      -DCMAKE_BUILD_TYPE=Release       \
      -DENABLE_CXX11=ON                \
      -DBUILD_PERF_TESTS=OFF           \
      -DWITH_XINE=ON                   \
      -DBUILD_TESTS=OFF                \
      -DWITH_QT=ON                     \
      -DENABLE_PRECOMPILED_HEADERS=OFF \
      -DCMAKE_SKIP_RPATH=ON            \
      -DBUILD_WITH_DEBUG_INFO=OFF      \
      -DOPENCV_GENERATE_PKGCONFIG=ON   \
      -DBUILD_DOCS=ON                  \
      -DINSTALL_C_EXAMPLES=ON          \
      -DINSTALL_PYTHON_EXAMPLES=ON     \
      -DOPENCV_ENABLE_NONFREE=ON       \
      -DBUILD_opencv_cvv=ON            \
      -DWITH_ADE=OFF                   \
      -DWITH_opencv_gapi=OFF           \
      -DOPENCV_PYTHON2_INSTALL_PATH=%{python2_sitearch} \
      -DOPENCV_PYTHON3_INSTALL_PATH=%{python3_sitearch} \
      -DCMAKE_CXX_FLAGS=-latomic \
      -DOPENCV_EXTRA_EXE_LINKER_FLAGS=-latomic \
      -Wno-dev  
      

make -C build VERBOSE=0


%install
%make_install -C build VERBOSE=0

mkdir -p %{buildroot}%{_docdir}/%{name}-doc
mv %{buildroot}/%{_datadir}/opencv4/samples %{buildroot}/%{_docdir}/%{name}-doc/examples

# Java
mv %{buildroot}/usr/share/java/opencv4/libopencv_java%{javaver}.so %{buildroot}/%{_libdir}
ln -sf %{_libdir}/libopencv_java%{javaver}.so %{buildroot}/%{_libdir}/libopencv_java.so
mkdir -p %{buildroot}/%{_jnidir}
mv %{buildroot}/usr/share/java/opencv4/opencv-%{javaver}.jar %{buildroot}/%{_jnidir}/
ln -sf %{_jnidir}/opencv-%{javaver}.jar %{buildroot}/%{_jnidir}/opencv.jar

# Fix rpmlint warning "doc-file-dependency"
chmod 644 %{buildroot}%{_docdir}/%{name}-doc/examples/python/*.py

%fdupes -s %{buildroot}/%{_docdir}/%{name}-doc/examples
%fdupes -s %{buildroot}/%{_includedir}

find %{buildroot} -name '*.la' -delete

rm -rf %{buildroot}/%{_datadir}/OpenCV/licenses/

# Compatibility
pushd %{buildroot}/%{_includedir}/
ln -sf opencv4/opencv2 opencv2
popd

pushd %{buildroot}/%{_libdir}/pkgconfig
ln -sf opencv4.pc opencv.pc
popd


sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/usr/bin/setup_vars_opencv4.sh



%ldconfig_scriptlets core

%ldconfig_scriptlets contrib


%files
%doc README.md
%license LICENSE
%{_datadir}/licenses/opencv4/
%{_bindir}/opencv_*
%dir %{_datadir}/opencv4
%{_datadir}/opencv4/haarcascades
%{_datadir}/opencv4/lbpcascades
%{_datadir}/opencv4/valgrind*
%{_datadir}/opencv4/quality/

%files core
%{_libdir}/libopencv_core.so.%{abiver}*
/usr/lib64/libopencv_core.so.%{dotabiver}
%{_libdir}/libopencv_flann.so.%{abiver}*
%{_libdir}/libopencv_flann.so.%{dotabiver}
%{_libdir}/libopencv_highgui.so.%{abiver}*
%{_libdir}/libopencv_highgui.so.%{dotabiver}
%{_libdir}/libopencv_imgcodecs.so.%{abiver}*
%{_libdir}/libopencv_imgcodecs.so.%{dotabiver}
%{_libdir}/libopencv_imgproc.so.%{abiver}*
%{_libdir}/libopencv_imgproc.so.%{dotabiver}
%{_libdir}/libopencv_ml.so.%{abiver}*
%{_libdir}/libopencv_ml.so.%{dotabiver}
%{_libdir}/libopencv_objdetect.so.%{abiver}*
%{_libdir}/libopencv_objdetect.so.%{dotabiver}
%{_libdir}/libopencv_photo.so.%{abiver}*
%{_libdir}/libopencv_photo.so.%{dotabiver}
%{_libdir}/libopencv_stitching.so.%{abiver}*
%{_libdir}/libopencv_stitching.so.%{dotabiver}
%{_libdir}/libopencv_video.so.%{abiver}*
%{_libdir}/libopencv_video.so.%{dotabiver}
%{_libdir}/libopencv_videoio.so.%{abiver}*
%{_libdir}/libopencv_videoio.so.%{dotabiver}
%{_libdir}/libopencv_sfm.so.%{abiver}*
%{_libdir}/libopencv_features2d.so.%{abiver}*
%{_libdir}/libopencv_features2d.so.%{dotabiver}
#{_libdir}/libopencv_gapi.so.%{abiver}*
%{_libdir}/libopencv_calib3d.so.%{abiver}*
%{_libdir}/libopencv_calib3d.so.%{dotabiver}
%{_libdir}/libopencv_dnn.so.%{abiver}*
%{_libdir}/libopencv_dnn.so.%{dotabiver}
%{_libdir}/libopencv_viz.so.%{dotabiver}
%{_libdir}/libopencv_viz.so.%{abiver}*

%files devel
%{_includedir}/opencv4
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/opencv4.pc
%{_libdir}/pkgconfig/opencv.pc
%{_libdir}/cmake/opencv4/*.cmake
%exclude %{_includedir}/opencv4/opencv2/xfeatures2d.hpp
%exclude %{_includedir}/opencv4/opencv2/xfeatures2d/cuda.hpp
%exclude %{_includedir}/opencv4/opencv2/xfeatures2d/nonfree.hpp
%{_includedir}/opencv2

%files doc
%{_docdir}/%{name}-doc/

%files -n python2-%{name}
%{python2_sitearch}/cv2/

%files -n python3-%{name}
%{python3_sitearch}/cv2/
%{_bindir}/setup_vars_opencv4.sh

%files contrib
%{_libdir}/libopencv_alphamat.so.%{abiver}*
%{_libdir}/libopencv_aruco.so.%{abiver}*
%{_libdir}/libopencv_bgsegm.so.%{abiver}*
%{_libdir}/libopencv_barcode.so.%{abiver}*
%{_libdir}/libopencv_bioinspired.so.%{abiver}*
%{_libdir}/libopencv_ccalib.so.%{abiver}*
%{_libdir}/libopencv_cvv.so.%{abiver}*
%{_libdir}/libopencv_datasets.so.%{abiver}*
%{_libdir}/libopencv_dnn_objdetect.so.%{abiver}*
%{_libdir}/libopencv_dnn_superres.so.%{abiver}*
%{_libdir}/libopencv_dpm.so.%{abiver}*
%{_libdir}/libopencv_face.so.%{abiver}*
%{_libdir}/libopencv_freetype.so.%{abiver}*
%{_libdir}/libopencv_fuzzy.so.%{abiver}*
%{_libdir}/libopencv_hdf.so.%{abiver}*
%{_libdir}/libopencv_hfs.so.%{abiver}*
%{_libdir}/libopencv_img_hash.so.%{abiver}*
%{_libdir}/libopencv_intensity_transform.so.%{abiver}*
%{_libdir}/libopencv_line_descriptor.so.%{abiver}*
%{_libdir}/libopencv_mcc.so.%{abiver}*
%{_libdir}/libopencv_optflow.so.%{abiver}*
%{_libdir}/libopencv_phase_unwrapping.so.%{abiver}*
%{_libdir}/libopencv_plot.so.%{abiver}*
%{_libdir}/libopencv_quality.so.%{abiver}*
%{_libdir}/libopencv_rapid.so.%{abiver}*
%{_libdir}/libopencv_reg.so.%{abiver}*
%{_libdir}/libopencv_rgbd.so.%{abiver}*
%{_libdir}/libopencv_saliency.so.%{abiver}*
%{_libdir}/libopencv_shape.so.%{abiver}*
%{_libdir}/libopencv_stereo.so.%{abiver}*
%{_libdir}/libopencv_structured_light.so.%{abiver}*
%{_libdir}/libopencv_superres.so.%{abiver}*
%{_libdir}/libopencv_surface_matching.so.%{abiver}*
%{_libdir}/libopencv_text.so.%{abiver}*
%{_libdir}/libopencv_tracking.so.%{abiver}*
%{_libdir}/libopencv_videostab.so.%{abiver}*
%{_libdir}/libopencv_wechat_qrcode.so.%{abiver}*
%{_libdir}/libopencv_ximgproc.so.%{abiver}*
%{_libdir}/libopencv_xobjdetect.so.%{abiver}*
%{_libdir}/libopencv_xphoto.so.%{abiver}*

# Wtf? Why redundant?
%{_libdir}/libopencv_alphamat.so.%{dotabiver}
%{_libdir}/libopencv_aruco.so.%{dotabiver}
%{_libdir}/libopencv_barcode.so.%{dotabiver}
%{_libdir}/libopencv_bgsegm.so.%{dotabiver}
%{_libdir}/libopencv_bioinspired.so.%{dotabiver}
%{_libdir}/libopencv_ccalib.so.%{dotabiver}
%{_libdir}/libopencv_cvv.so.%{dotabiver}
%{_libdir}/libopencv_datasets.so.%{dotabiver}
%{_libdir}/libopencv_dnn_objdetect.so.%{dotabiver}
%{_libdir}/libopencv_dnn_superres.so.%{dotabiver}
%{_libdir}/libopencv_dpm.so.%{dotabiver}
%{_libdir}/libopencv_face.so.%{dotabiver}
%{_libdir}/libopencv_freetype.so.%{dotabiver}
%{_libdir}/libopencv_fuzzy.so.%{dotabiver}
#{_libdir}/libopencv_gapi.so.%{dotabiver}
%{_libdir}/libopencv_hdf.so.%{dotabiver}
%{_libdir}/libopencv_hfs.so.%{dotabiver}

%{_libdir}/libopencv_img_hash.so.%{dotabiver}
%{_libdir}/libopencv_intensity_transform.so.%{dotabiver}
%{_libdir}/libopencv_line_descriptor.so.%{dotabiver}
%{_libdir}/libopencv_mcc.so.%{dotabiver}
%{_libdir}/libopencv_optflow.so.%{dotabiver}
%{_libdir}/libopencv_phase_unwrapping.so.%{dotabiver}
%{_libdir}/libopencv_plot.so.%{dotabiver}
%{_libdir}/libopencv_quality.so.%{dotabiver}
%{_libdir}/libopencv_rapid.so.%{dotabiver}
%{_libdir}/libopencv_reg.so.%{dotabiver}
%{_libdir}/libopencv_rgbd.so.%{dotabiver}
%{_libdir}/libopencv_saliency.so.%{dotabiver}
%{_libdir}/libopencv_sfm.so.%{dotabiver}
%{_libdir}/libopencv_shape.so.%{dotabiver}
%{_libdir}/libopencv_stereo.so.%{dotabiver}
%{_libdir}/libopencv_structured_light.so.%{dotabiver}
%{_libdir}/libopencv_superres.so.%{dotabiver}
%{_libdir}/libopencv_surface_matching.so.%{dotabiver}
%{_libdir}/libopencv_text.so.%{dotabiver}
%{_libdir}/libopencv_tracking.so.%{dotabiver}
%{_libdir}/libopencv_videostab.so.%{dotabiver}
%{_libdir}/libopencv_wechat_qrcode.so.%{dotabiver}
%{_libdir}/libopencv_xfeatures2d.so.%{dotabiver}
%{_libdir}/libopencv_ximgproc.so.%{dotabiver}
%{_libdir}/libopencv_xobjdetect.so.%{dotabiver}
%{_libdir}/libopencv_xphoto.so.%{dotabiver}


%if %{with freeworld}
%files xfeatures2d
%{_libdir}/libopencv_xfeatures2d.so
%{_libdir}/libopencv_xfeatures2d.so.%{abiver}*

%files xfeatures2d-devel
%{_includedir}/opencv4/opencv2/xfeatures2d.hpp
%{_includedir}/opencv4/opencv2/xfeatures2d/cuda.hpp
%{_includedir}/opencv4/opencv2/xfeatures2d/nonfree.hpp

%files static
%{_libdir}/opencv4/3rdparty/libcorrespondence.a
%{_libdir}/opencv4/3rdparty/libmultiview.a
%{_libdir}/opencv4/3rdparty/libnumeric.a
%{_libdir}/opencv4/3rdparty/libsimple_pipeline.a
%endif

%files java
%{_libdir}/libopencv_java*.so
%{_jnidir}/opencv-*.jar
%{_jnidir}/opencv.jar

%changelog

* Sat May 28 2022 David Va <davidva AT tuta DOT io> - 4.5.5-9
- Rebuilt

* Sat Apr 30 2022 David Va <davidva AT tuta DOT io> - 4.5.5-8
- disabled ade

* Sat Jan 22 2022 David Va <davidva AT tuta DOT io> - 4.5.5-7
- Updated to 4.5.5

* Mon Nov 01 2021 David Va <davidva AT tuta DOT io> - 4.5.4-7
- Updated to 4.5.4

* Mon Aug 02 2021 David Va <davidva AT tuta DOT io> - 4.5.3-7
- Updated to 4.5.3

* Sat Apr 17 2021 David Vásquez <davidva AT tuta DOT io> - 4.5.2-7
- Updated to 4.5.2

* Tue Feb 09 2021 David Vásquez <davidva AT tuta DOT io> - 4.5.1-8
- Rebuilt

* Fri Jan 22 2021 David Vásquez <davidva AT tuta DOT io> - 4.5.1-7
- Updated to 4.5.1

* Sun Nov 01 2020 David Vásquez <davidva AT tuta DOT io> - 4.5.0-7
- Updated to 4.5.0

* Sat Aug 08 2020 David Vásquez <davidva AT tuta DOT io> - 4.4.0-8
- Fix compatibility

* Sat Aug 08 2020 David Vásquez <davidva AT tuta DOT io> - 4.4.0-7
- Updated to 4.4.0

* Sun May 31 2020 David Vásquez <davidva AT tuta DOT io> - 4.3.0-9
- Rebuilt for python3.9

* Wed Apr 08 2020 David Vásquez <davidva AT tuta DOT io> - 4.3.0-8
- Updated to 4.3.0

* Thu Feb 20 2020 David Vásquez <davidva AT tuta DOT io> - 4.2.0-8
- Rebuilt for compatibility

* Sat Dec 28 2019 David Vásquez <davidva AT tuta DOT io> - 4.2.0-7
- Updated to 4.2.0

* Mon Oct 21 2019 David Vásquez <davidva AT tuta DOT io> - 4.1.2-7
- Updated to 4.1.2

* Fri Aug 02 2019 David Vásquez <davidva AT tuta DOT io> - 4.1.1-7
- Updated to 4.1.1

* Fri May 31 2019 David Vásquez <davidva AT tuta DOT io> - 4.1.0-9
- opencv-java provides change

* Thu May 30 2019 David Vásquez <davidva AT tuta DOT io> - 4.1.0-8
- Compatibility transitional

* Tue May 21 2019 David Vásquez <davidva AT tuta DOT io> - 4.1.0-7
- Updated to 4.1.0-7

* Mon May 20 2019 David Vásquez <davidva AT tuta DOT io> - 3.4.6-8
- Updated to 3.4.6-8

* Sat May 18 2019 David Vásquez <davidva AT tuta DOT io> - 3.4.4-8
- Rebuilt for libHalf libIex libIlmImf libIlmThread libImath

* Wed Apr 10 2019 David Vásquez <davidva AT tuta DOT io> - 3.4.4-7
- Updated to 3.4.4-7

* Sun Oct 07 2018 David Vásquez <davidva AT tuta DOT io> - 3.4.3-7
- Updated to 3.4.3
- Conditional clang 

* Wed Jul 04 2018 David Vásquez <davidva AT tuta DOT io> - 3.4.1-8
- Rebuilt for python3.7

* Thu Jun 07 2018 David Vásquez <davidva AT tuta DOT io> - 3.4.1-7
- Initial build
