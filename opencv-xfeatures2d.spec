# Tips thanks 
# 1. http://www.linuxfromscratch.org/blfs/view/svn/general/opencv.html

%global __requires_exclude ^(%{_libdir})\\.so*|^(%{_includedir}/opencv2)\\.hpp

%bcond_without qt5

Name:           opencv-xfeatures2d
Version:        3.4.1
Release:        1%{?dist}
Summary:        xfeatures2d contrib
License:        BSD
Url:            http://opencv.org
Source0:        https://github.com/opencv/opencv/archive/%{version}.zip
Source1:	https://github.com/opencv/opencv_contrib/archive/%{version}.tar.gz
Source2:	https://raw.githubusercontent.com/opencv/opencv_3rdparty/dfe3162c237af211e98b8960018b564bc209261d/ippicv/ippicv_2017u3_lnx_intel64_general_20170822.tgz

# Patches from Fedora
Patch:		opencv-3.4.1-cmake_paths.patch
Patch3:		opencv-3.4.1-cmake_va_intel_fix.patch

# Thanks openSuse
Patch1:		opencv-3.2.0-gcc-6.0.patch
Patch2:		opencv-3.4.1-compilation-C-mode.patch

BuildRequires:  libtool
BuildRequires:  cmake 
BuildRequires:  gtk3-devel
BuildRequires:	libwebp-devel
BuildRequires:  chrpath
BuildRequires:  eigen3-devel
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  tbb-devel
BuildRequires:	unzip 
BuildRequires:	ccache

BuildRequires:  pkgconfig(IlmBase)
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(libdc1394-2)
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libv4lconvert)
BuildRequires:  pkgconfig(zlib)

%if %{with qt5}
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

BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  swig >= 1.3.24
BuildRequires:  ffmpeg-devel 
BuildRequires:  xine-lib-devel
BuildRequires:  openblas-devel

BuildRequires:	gcc, gcc-c++

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.

%package        devel
Summary:        Development files for using the OpenCV library
Supplements:	opencv-contrib
Requires:	%{name} = %{version}-%{release}

%description    devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. 


%prep
%setup -n opencv-%{version} -a 1
%patch -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

ipp_file=%{S:2} 
ipp_dir=.cache/ippicv                           

mkdir -p $ipp_dir &&
cp -f %{S:2} $ipp_dir/


%build
mkdir -p build
pushd build

%cmake -DCMAKE_INSTALL_PREFIX=/usr     \
      -DWITH_OPENCL=ON	               \
      -DWITH_OPENGL=ON	               \
      -DWITH_GSTREAMER=OFF             \
      -DBUILD_WITH_DEBUG_INFO=OFF      \
      -DBUILD_TESTS=OFF                \
      -DBUILD_PERF_TESTS=OFF           \
      -DCMAKE_BUILD_TYPE=Release       \
      -DENABLE_CXX11=ON                \
      -DBUILD_PERF_TESTS=OFF           \
      -DWITH_XINE=ON                   \
      -DBUILD_TESTS=OFF                \
      -DENABLE_PRECOMPILED_HEADERS=OFF \
      -DCMAKE_SKIP_RPATH=ON            \
      -DBUILD_WITH_DEBUG_INFO=OFF      \
%ifarch x86_64
      -DCPU_BASELINE=SSE2 \
      -DCPU_DISPATCH=SSE3,SSE4_1,SSE4_2,AVX,FP16,AVX2 \
%else
      -DCPU_BASELINE_DISABLE=SSE \
      -DCPU_DISPATCH=SSE,SSE2,SSE3 \
%endif
      -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-%{version}/modules \
      -Wno-dev  ..

%make_build VERBOSE=0

popd

%install
pushd build
%make_install VERBOSE=0
popd

rm -rf %{buildroot}/%{_datadir}/
rm -rf %{buildroot}/%{_bindir}/

%files
%exclude %{_libdir}/*
%exclude %{_includedir}/opencv/*
%exclude %{_includedir}/opencv2/*
%exclude %dir %{_includedir}/opencv/
%exclude %dir %{_includedir}/opencv2/
%exclude %dir %{_libdir}/
%{_libdir}/libopencv_xfeatures2d.so
%{_libdir}/libopencv_xfeatures2d.so.3.4
%{_libdir}/libopencv_xfeatures2d.so.3.4.1

%files devel
%{_includedir}/opencv2/xfeatures2d.hpp
%{_includedir}/opencv2/xfeatures2d/cuda.hpp
%{_includedir}/opencv2/xfeatures2d/nonfree.hpp


%changelog

* Thu Jun 07 2018 David Vásquez <davidva AT tuta DOT io> - 3.4.1-1
- Initial build

