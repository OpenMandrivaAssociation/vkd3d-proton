%global optflags %{optflags} -fno-strict-aliasing

Name:		vkd3d-proton
Version:	3.0
Release:	1
Summary:	D3D12 implementation for Wine/Proton that translates D3D to Vulkan

License:	LGPLv2+
URL:		https://github.com/HansKristian-Work/vkd3d-proton/
Source0:	https://github.com/HansKristian-Work/vkd3d-proton/archive/refs/tags/v%{version}.tar.gz
# Get the correct revisions from
# https://github.com/HansKristian-Work/vkd3d-proton/tree/v%{version}/khronos
Source1:	https://github.com/KhronosGroup/SPIRV-Headers/archive/3b9447dc98371e96b59a6225bd062a9867e1d203.tar.gz
Source2:	https://github.com/KhronosGroup/Vulkan-Headers/archive/b39ab380a44b6c8df462c34e976ea9ce2d2c336b.tar.gz
Source3:	https://github.com/HansKristian-Work/dxil-spirv/archive/4e36bab794afdb7d78f56b866971009ca894fe9c.tar.gz
Source4:	https://github.com/KhronosGroup/SPIRV-Cross/archive/4b7bcb7e5cf71015b3299088d22004bfe4e13a5e.tar.gz
Source5:	https://github.com/KhronosGroup/SPIRV-Tools/archive/e9a8ceeddbf7e3aaadac2ab6f8a6ab6437872e88.tar.gz
Source6:	https://github.com/doitsujin/dxbc-spirv/archive/a38b5d78ed29f5fe44c2a2e157d5f7c2516df6e5.tar.gz

BuildArch:	noarch
BuildRequires:	meson
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  perl-JSON
BuildRequires:  perl-open
BuildRequires:	glslang
BuildRequires:	pkgconfig(xcb)
BuildRequires:	spirv-headers
BuildRequires:	pkgconfig(SPIRV-Tools)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xcb-icccm)
# For widl
BuildRequires:	mingw
BuildRequires:	cross-x86_64-w64-mingw32-binutils
BuildRequires:	cross-x86_64-w64-mingw32-gcc
BuildRequires:	cross-i686-w64-mingw32-binutils
BuildRequires:	cross-i686-w64-mingw32-gcc

Provides:	direct3d12-implementation
# For dxgi
Requires:	direct3d-implementation
Recommends:	dxvk

%description
The vkd3d project includes libraries, shaders, utilities, and demos for
translating D3D12 to Vulkan.

%prep
%autosetup -p1
cd khronos
rmdir SPIRV-Headers Vulkan-Headers
tar xf %{S:1}
tar xf %{S:2}
mv SPIRV-Headers-* SPIRV-Headers
mv Vulkan-Headers-* Vulkan-Headers
cd ../subprojects
rmdir dxil-spirv
tar xf %{S:3}
mv dxil-spirv-* dxil-spirv
cd dxil-spirv/third_party
rmdir spirv-headers
ln -s ../../../khronos/SPIRV-Headers spirv-headers
rmdir SPIRV-Cross SPIRV-Tools
tar xf %{S:4}
tar xf %{S:5}
mv SPIRV-Cross-* SPIRV-Cross
mv SPIRV-Tools-* SPIRV-Tools
cd ../subprojects
rmdir dxbc-spirv
tar xf %{S:6}
mv dxbc-spirv-* dxbc-spirv
cd dxbc-spirv/submodules
rmdir spirv_headers
ln -s ../../../../../khronos/SPIRV-Headers spirv_headers

%conf
%meson \
	--cross-file=build-win64.txt

%meson32 \
	--cross-file=build-win32.txt

%build
%ninja_build -C build

%ninja_build -C build32

%install
mkdir -p %{buildroot}%{_libdir}/wine/x86_64-windows %{buildroot}%{_prefix}/lib/wine/i386-windows
cp build/libs/*/*.dll %{buildroot}%{_libdir}/wine/x86_64-windows/
cp build32/libs/*/*.dll %{buildroot}%{_prefix}/lib/wine/i386-windows/

%files
%{_libdir}/wine/x86_64-windows/d3d12core.dll
%{_libdir}/wine/x86_64-windows/d3d12.dll
%{_prefix}/lib/wine/i386-windows/d3d12core.dll
%{_prefix}/lib/wine/i386-windows/d3d12.dll
