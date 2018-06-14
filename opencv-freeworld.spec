# Tips thanks 
# 1. http://www.linuxfromscratch.org/blfs/view/svn/general/opencv.html
# 2. https://src.fedoraproject.org/rpms/opencv
# 3. https://build.opensuse.org/package/show/openSUSE%3AFactory/opencv

%global abiver  3.4
%bcond_without qt5
%bcond_with cuda

Name:           opencv-freeworld
Version:        3.4.1
Release:        3%{?dist}
Summary:        Collection of algorithms for computer vision
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
BuildRequires:  pkgconfig(libglog)
BuildRequires:	gflags-devel
BuildRequires:	ceres-solver

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
%if %{with cuda}
BuildRequires:  cuda
%endif
BuildRequires:  openblas-devel

BuildRequires:	gcc, gcc-c++
Provides:	opencv = %{version}-%{release}

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package        core
Summary:        OpenCV core libraries
Provides:	opencv-core = %{version}-%{release}
Recommends:	opencv-xfeatures2d = %{version}-%{release}

%description    core
This package contains the OpenCV C/C++ core libraries.


%package        devel
Summary:        Development files for using the OpenCV library
Provides:	opencv-devel = %{version}-%{release}
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       %{name}-contrib%{_isa} = %{version}-%{release}

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
Provides:	opencv-doc = %{version}-%{release}
Obsoletes:      %{name}-devel-docs < %{version}-%{release}

%description    doc
This package contains the OpenCV documentation, samples and examples programs.


%package        -n python2-%{name}
Summary:        Python2 bindings for apps which use OpenCV
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       python2-numpy
%{?python_provide:%python_provide python2-%{srcname}}
# Remove before F30
Provides:       %{name}-python = %{version}-%{release}
Provides:       %{name}-python%{?_isa} = %{version}-%{release}
Provides:	python2-opencv = %{version}-%{release}
Obsoletes:      %{name}-python < %{version}-%{release}

%description    -n python2-%{name}
This package contains Python bindings for the OpenCV library.


%package        -n python3-%{name}
Summary:        Python3 bindings for apps which use OpenCV
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       python3-numpy
%{?python_provide:%python_provide python3-%{srcname}}
# Remove before F30
Provides:       %{name}-python3 = %{version}-%{release}
Provides:       %{name}-python3%{?_isa} = %{version}-%{release}
Provides:	python3-opencv = %{version}-%{release}
Obsoletes:      %{name}-python3 < %{version}-%{release}

%description    -n python3-%{name}
This package contains Python3 bindings for the OpenCV library.


%package        contrib
Summary:        OpenCV contributed functionality
Provides:	opencv-contrib = %{version}-%{release}
Recommends:	opencv-xfeatures2d-devel = %{version}-%{release}

%description    contrib
This package is intended for development of so-called "extra" modules, contributed
functionality. New modules quite often do not have stable API, and they are not
well-tested. Thus, they shouldn't be released as a part of official OpenCV
distribution, since the library maintains binary compatibility, and tries
to provide decent performance and stability.


%package        xfeatures2d
Summary:        xfeatures2d contrib

%description xfeatures2d
xfeatures2d contrib.

%package        xfeatures2d-devel
Summary:        Development files for using the OpenCV library
Requires:	opencv-xfeatures2d = %{version}-%{release}

%description    xfeatures2d-devel
This package contains the OpenCV C/C++ library and header files. It should be installed if you want to develop programs that
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

%cmake -DWITH_OPENCL=ON	               \
      -DWITH_OPENGL=ON	               \
      -DWITH_GSTREAMER=OFF             \
      -DBUILD_WITH_DEBUG_INFO=OFF      \
      -DBUILD_TESTS=OFF                \
      -DBUILD_PERF_TESTS=OFF           \
      -DCMAKE_BUILD_TYPE=Release       \
      -DENABLE_CXX11=ON                \
      -DBUILD_PERF_TESTS=OFF           \
%if %{with qt5}
      -DWITH_QT=ON                     \
%endif
      -DWITH_XINE=ON                   \
      -DBUILD_DOCS=ON                  \
      -DINSTALL_C_EXAMPLES=ON          \
      -DINSTALL_PYTHON_EXAMPLES=ON     \
      -DENABLE_PRECOMPILED_HEADERS=OFF \
      -DCMAKE_SKIP_RPATH=ON            \
      -DBUILD_WITH_DEBUG_INFO=OFF      \
%if %{with cuda}
      -DWITH_CUDA=ON                   \
%endif
%ifarch x86_64
      -DCPU_BASELINE=SSE2              \
      -DCPU_DISPATCH=SSE3,SSE4_1,SSE4_2,AVX,FP16,AVX2 \
%else
      -DCPU_BASELINE_DISABLE=SSE       \
      -DCPU_DISPATCH=SSE,SSE2,SSE3     \
%endif
      -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-%{version}/modules \
%ifarch aarch64
      -DCPU_BASELINE=NEON              \
      -DCPU_DISPATCH=FP16              \
%endif
      -Wno-dev  ..

%make_build VERBOSE=0

popd

%install
pushd build
%make_install VERBOSE=0
popd

find %{buildroot} -name '*.la' -delete


%ldconfig_scriptlets core

%ldconfig_scriptlets contrib


%files
%doc README.md
%license LICENSE
%{_bindir}/opencv_*
%dir %{_datadir}/OpenCV
%{_datadir}/OpenCV/haarcascades
%{_datadir}/OpenCV/lbpcascades
%{_datadir}/OpenCV/valgrind*

%files core
%{_libdir}/libopencv_core.so.%{abiver}*
%{_libdir}/libopencv_cvv.so.%{abiver}*
%{_libdir}/libopencv_flann.so.%{abiver}*
%{_libdir}/libopencv_hfs.so.%{abiver}*
%{_libdir}/libopencv_highgui.so.%{abiver}*
%{_libdir}/libopencv_imgcodecs.so.%{abiver}*
%{_libdir}/libopencv_imgproc.so.%{abiver}*
%{_libdir}/libopencv_ml.so.%{abiver}*
%{_libdir}/libopencv_objdetect.so.%{abiver}*
%{_libdir}/libopencv_photo.so.%{abiver}*
%{_libdir}/libopencv_shape.so.%{abiver}*
%{_libdir}/libopencv_stitching.so.%{abiver}*
%{_libdir}/libopencv_superres.so.%{abiver}*
%{_libdir}/libopencv_video.so.%{abiver}*
%{_libdir}/libopencv_videoio.so.%{abiver}*
%{_libdir}/libopencv_videostab.so.%{abiver}*
%{_libdir}/libopencv_sfm.so.%{abiver}*
%exclude %{_libdir}/libopencv_xfeatures2d.so.%{abiver}*

%files devel
%{_includedir}/opencv
%{_includedir}/opencv2
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/opencv.pc
%{_libdir}/OpenCV/*.cmake
%exclude %{_includedir}/opencv2/xfeatures2d.hpp
%exclude %{_includedir}/opencv2/xfeatures2d/cuda.hpp
%exclude %{_includedir}/opencv2/xfeatures2d/nonfree.hpp

%files doc
%{_datadir}/OpenCV/samples
%{_datadir}/OpenCV/doc

%files -n python2-%{name}
%{python2_sitearch}/cv2.so

%files -n python3-%{name}
%{python3_sitearch}/cv2.cpython-3*.so

%files contrib
%{_libdir}/libopencv_aruco.so.%{abiver}*
%{_libdir}/libopencv_bgsegm.so.%{abiver}*
%{_libdir}/libopencv_bioinspired.so.%{abiver}*
%{_libdir}/libopencv_calib3d.so.%{abiver}*
%{_libdir}/libopencv_ccalib.so.%{abiver}*
%{_libdir}/libopencv_datasets.so.%%{abiver}*
%{_libdir}/libopencv_dnn.so.%{abiver}*
%{_libdir}/libopencv_dpm.so.%{abiver}*
%{_libdir}/libopencv_face.so.%{abiver}*
%{_libdir}/libopencv_freetype.so.%{abiver}*
%{_libdir}/libopencv_fuzzy.so.%{abiver}*
%{_libdir}/libopencv_hdf.so.%{abiver}*
%{_libdir}/libopencv_img_hash.so.%{abiver}*
%{_libdir}/libopencv_line_descriptor.so.%{abiver}*
%{_libdir}/libopencv_optflow.so.%{abiver}*
%{_libdir}/libopencv_phase_unwrapping.so.%{abiver}*
%{_libdir}/libopencv_plot.so.%{abiver}*
%{_libdir}/libopencv_reg.so.%{abiver}*
%{_libdir}/libopencv_rgbd.so.%{abiver}*
%{_libdir}/libopencv_saliency.so.%{abiver}*
%{_libdir}/libopencv_stereo.so.%{abiver}*
%{_libdir}/libopencv_structured_light.so.%{abiver}*
%{_libdir}/libopencv_surface_matching.so.%{abiver}*
%{_libdir}/libopencv_text.so.%{abiver}*
%{_libdir}/libopencv_tracking.so.%{abiver}*
%{_libdir}/libopencv_ximgproc.so.%{abiver}*
%{_libdir}/libopencv_xobjdetect.so.%{abiver}*
%{_libdir}/libopencv_xphoto.so.%{abiver}*

%files xfeatures2d
%{_libdir}/libopencv_xfeatures2d.so
%{_libdir}/libopencv_xfeatures2d.so.%{abiver}
%{_libdir}/libopencv_xfeatures2d.so.%{abiver}.*

%files xfeatures2d-devel
%{_includedir}/opencv2/xfeatures2d.hpp
%{_includedir}/opencv2/xfeatures2d/cuda.hpp
%{_includedir}/opencv2/xfeatures2d/nonfree.hpp


%changelog

* Thu Jun 07 2018 David Vásquez <davidva AT tuta DOT io> - 3.4.1-3
- Initial build

