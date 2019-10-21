# Tips thanks 
# 1. http://www.linuxfromscratch.org/blfs/view/svn/general/opencv.html
# 2. https://src.fedoraproject.org/rpms/opencv
# 3. https://build.opensuse.org/package/show/openSUSE%3AFactory/opencv

%global debug_package %{nil}
%global abiver 4.1
%global javaver 412
%bcond_without qt5
%bcond_without freeworld
%bcond_with cuda
%bcond_with clang

Name:           opencv
Version:        4.1.2
Release:        7%{?dist}
Summary:        Collection of algorithms for computer vision
License:        BSD
Url:            http://opencv.org
Source0:	https://github.com/opencv/opencv/archive/%{version}.zip
Source1:        https://github.com/opencv/opencv_contrib/archive/%{version}.tar.gz

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
# java
BuildRequires:  ant
BuildRequires:  java-devel

BuildRequires:	gstreamer1-plugins-base-devel
BuildRequires:	tbb-devel

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

# Necessary Modules 
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
pushd build

# cmake macro fails build

cmake -DCMAKE_INSTALL_PREFIX=/usr      \
      -DCMAKE_BUILD_TYPE=Release       \
      -DENABLE_CXX11=ON                \
      -DBUILD_PERF_TESTS=OFF           \
      -DWITH_XINE=ON                   \
      -DBUILD_TESTS=OFF                \
      -DENABLE_PRECOMPILED_HEADERS=OFF \
      -DCMAKE_SKIP_RPATH=ON            \
      -DBUILD_WITH_DEBUG_INFO=OFF      \
      -DOPENCV_GENERATE_PKGCONFIG=ON   \
      -DBUILD_DOCS=ON                  \
      -DINSTALL_C_EXAMPLES=ON          \
      -DINSTALL_PYTHON_EXAMPLES=ON     \
      -DOPENCV_ENABLE_NONFREE=ON       \
      -DBUILD_opencv_cvv=ON            \
      -DOPENCV_PYTHON2_INSTALL_PATH=%{python2_sitearch} \
      -DOPENCV_PYTHON3_INSTALL_PATH=%{python3_sitearch} \
      -Wno-dev  ..

make  VERBOSE=0

popd

%install

pushd build
%make_install VERBOSE=0
popd

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
#{_libdir}/libopencv_cvv.so.{abiver}*
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
%{_libdir}/libopencv_features2d.so.%{abiver}*

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
%{_libdir}/libopencv_aruco.so.%{abiver}*
%{_libdir}/libopencv_bgsegm.so.%{abiver}*
%{_libdir}/libopencv_bioinspired.so.%{abiver}*
%{_libdir}/libopencv_calib3d.so.%{abiver}*
%{_libdir}/libopencv_ccalib.so.%{abiver}*
%{_libdir}/libopencv_datasets.so.%%{abiver}*
%{_libdir}/libopencv_dnn.so.%{abiver}*
%{_libdir}/libopencv_dnn_objdetect.so.%{abiver}*
%{_libdir}/libopencv_dnn_superres.so.%{abiver}*
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
%{_libdir}/libopencv_gapi.so.%{abiver}*
%{_libdir}/libopencv_quality.so.%{abiver}*

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
