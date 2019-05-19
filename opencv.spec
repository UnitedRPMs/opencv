# Tips thanks 
# 1. http://www.linuxfromscratch.org/blfs/view/svn/general/opencv.html
# 2. https://src.fedoraproject.org/rpms/opencv
# 3. https://build.opensuse.org/package/show/openSUSE%3AFactory/opencv

%global debug_package %{nil}
%global abiver 3.4
%bcond_without qt5
%bcond_without freeworld
%bcond_with cuda
%bcond_with clang

Name:           opencv
Version:        3.4.4
Release:        8%{?dist}
Summary:        Collection of algorithms for computer vision
License:        BSD
Url:            http://opencv.org
Source0:	https://github.com/opencv/opencv/archive/%{version}.zip
Source1:        https://github.com/opencv/opencv_contrib/archive/%{version}.tar.gz
Source2:        https://github.com/opencv/opencv_3rdparty/raw/ippicv/master_20180723/ippicv/ippicv_2019_lnx_intel64_general_20180723.tgz

# Patches from Fedora
Patch1:         opencv-3.4.1-cmake_paths.patch
Patch11:        https://github.com/opencv/opencv_contrib/pull/1905/commits/c4419e4e65a8d9e0b5a15e9a5242453f261bee46.patch
Patch12:        https://github.com/opencv/opencv/pull/13254/commits/ad35b79e3f98b4ce30481e0299cca550ed77aef0.patch

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
BuildRequires:  gflags-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  fdupes
BuildRequires:  hdf5-devel

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

BuildRequires:  python2-devel
BuildRequires:  python2-numpy
BuildRequires:  python2-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  swig >= 1.3.24
%if %{with freeworld}
BuildRequires:  ffmpeg-devel 
BuildRequires:  xine-lib-devel
%endif
%if %{with cuda}
BuildRequires:  cuda
%endif
BuildRequires:  openblas-devel

BuildRequires:  gcc, gcc-c++
%if 0%{?fedora} >= 29
BuildRequires:	python-unversioned-command
%endif

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
Obsoletes:      %{name}-devel-docs < %{version}-%{release}

%description    doc
This package contains the OpenCV documentation, samples and examples programs.


%package        -n python2-%{name}
Summary:        Python2 bindings for apps which use OpenCV
Requires:       %{name} = %{version}-%{release}
Requires:       python2-numpy
%{?python_provide:%python_provide python2-%{srcname}}
# Remove before F30
Provides:       %{name}-python = %{version}-%{release}
Provides:       %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-python < %{version}-%{release}

%description    -n python2-%{name}
This package contains Python bindings for the OpenCV library.


%package        -n python3-%{name}
Summary:        Python3 bindings for apps which use OpenCV
Requires:       %{name} = %{version}-%{release}
Requires:       python3-numpy
%{?python_provide:%python_provide python3-%{srcname}}
# Remove before F30
Provides:       %{name}-python3 = %{version}-%{release}
Provides:       %{name}-python3%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-python3 < %{version}-%{release}

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

%prep
%setup -n opencv-%{version} -a 1 

%patch1 -p1 -b .cmake_paths

pushd %{name}_contrib-%{version}
%patch11 -p1 -b .cvv_repair_build
popd
%patch12 -p1 -b .fix_install_of_python_bindings

%if %{with freeworld}
ipp_file=%{S:2} 
ipp_dir=.cache/ippicv                           

mkdir -p $ipp_dir &&
cp -f %{S:2} $ipp_dir/
%endif

%build

%if %{with clang}
export CC=clang
export CXX=clang++
%endif

mkdir -p build
pushd build

# cmake macro fails build


cmake -DCMAKE_INSTALL_PREFIX=/usr      \
      -DLIB_INSTALL_DIR:PATH=%{_libdir} \
      -DLIB_SUFFIX=64                  \
      -DCMAKE_BUILD_TYPE=Release       \
      -DWITH_OPENCL=ON                 \
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
%if %{with freeworld}
      -DWITH_XINE=ON                   \
%else
      -DWITH_IPP=OFF                   \
      -DWITH_XINE=OFF                  \
      -DWITH_FFMPEG=OFF                \
%endif
      -DBUILD_DOCS=ON                  \
      -DINSTALL_C_EXAMPLES=ON          \
      -DINSTALL_PYTHON_EXAMPLES=ON     \
      -DENABLE_PRECOMPILED_HEADERS=OFF \
      -DCMAKE_SKIP_RPATH=ON            \
%if %{with cuda}
      -DWITH_CUDA=ON                   \
%else
      -DWITH_CUDA=OFF                  \
%endif
%ifarch x86_64
      -DCPU_BASELINE_DISABLE=SSE3      \
      -DCPU_BASELINE_REQUIRE=SSE2      \
%else
      -DCPU_BASELINE_DISABLE=SSE       \
      -DCPU_DISPATCH=SSE,SSE2,SSE3     \
%endif
      -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-%{version}/modules \
      -DOpenGL_GL_PREFERENCE=GLVND     \
      -DVERBOSE=0 \
      -DPYTHON2_EXECUTABLE=%{__python2} \
      -DPYTHON3_EXECUTABLE=%{__python3} \
      -DPYTHON2_PACKAGES_PATH=%{python2_sitearch} \
      -DPYTHON3_PACKAGES_PATH=%{python3_sitearch} \
      -DOPENCV_PYTHON2_INSTALL_PATH=%{python2_sitearch} \
      -DOPENCV_PYTHON3_INSTALL_PATH=%{python3_sitearch} \
      -DOPENCV_SKIP_PYTHON_LOADER=ON \
      -DOPENCV_ENABLE_NONFREE=ON ..

%make_build VERBOSE=0

popd

%install

%if %{with clang}
export CC=clang
export CXX=clang++
%endif

pushd build
%make_install VERBOSE=0
popd

mkdir -p %{buildroot}%{_docdir}/%{name}-doc
mv %{buildroot}%{_datadir}/OpenCV/samples %{buildroot}%{_docdir}/%{name}-doc/examples

# Fix rpmlint warning "doc-file-dependency"
chmod 644 %{buildroot}%{_docdir}/%{name}-doc/examples/python/*.py

%fdupes -s %{buildroot}%{_docdir}/%{name}-doc/examples
%fdupes -s %{buildroot}%{_includedir}

find %{buildroot} -name '*.la' -delete

rm -rf %{buildroot}%{_datadir}/OpenCV/licenses/

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
%{_libdir}/libopencv_dnn_objdetect.so.%{abiver}*
%{_libdir}/libopencv_features2d.so.%{abiver}*

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
%{_docdir}/%{name}-doc/

%files -n python2-%{name}
%{python2_sitearch}/cv2.so

%files -n python3-%{name}
%{python3_sitearch}/cv2.cpython-3*.so
%{_bindir}/setup_vars_opencv3.sh

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

%if %{with freeworld}
%files xfeatures2d
%{_libdir}/libopencv_xfeatures2d.so
%{_libdir}/libopencv_xfeatures2d.so.%{abiver}*

%files xfeatures2d-devel
%{_includedir}/opencv2/xfeatures2d.hpp
%{_includedir}/opencv2/xfeatures2d/cuda.hpp
%{_includedir}/opencv2/xfeatures2d/nonfree.hpp

%files static
%{_libdir}/OpenCV/3rdparty/lib64/libcorrespondence.a
%{_libdir}/OpenCV/3rdparty/lib64/libmultiview.a
%{_libdir}/OpenCV/3rdparty/lib64/libnumeric.a
%{_libdir}/OpenCV/3rdparty/lib64/libsimple_pipeline.a
%endif

%changelog

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
