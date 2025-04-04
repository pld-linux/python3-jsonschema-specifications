# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	jsonschema-specifications
Summary:	The JSON Schema meta-schemas and vocabularies, exposed as a Registry
Name:		python3-%{module}
Version:	2024.10.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jsonschema-specifications/
Source0:	https://files.pythonhosted.org/packages/source/j/jsonschema-specifications/jsonschema_specifications-%{version}.tar.gz
# Source0-md5:	e8f726a5b9647031d9ee8b922cf9b56f
URL:		https://pypi.org/project/jsonschema-specifications/
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-build
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-referencing
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-sphinxext.opengraph
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JSON support files from the JSON Schema Specifications (metaschemas,
vocabularies, etc.), packaged for runtime access from Python as a
referencing-based Schema Registry.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n jsonschema_specifications-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" jsonschema_specifications/tests
%endif

%if %{with doc}
%{__python3} -m zipfile -e build-3/*.whl build-3-docs
%{__make} -C docs html \
	PYTHONPATH=$PWD/build-3-docs \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%dir %{py3_sitescriptdir}/jsonschema_specifications
%{py3_sitescriptdir}/jsonschema_specifications/*.py
%{py3_sitescriptdir}/jsonschema_specifications/__pycache__
%{py3_sitescriptdir}/jsonschema_specifications/schemas
%{py3_sitescriptdir}/jsonschema_specifications-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
