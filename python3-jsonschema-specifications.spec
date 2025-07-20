#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	jsonschema-specifications
Summary:	The JSON Schema meta-schemas and vocabularies, exposed as a Registry
Summary(pl.UTF-8):	Metaschematy i słowniki JSON Schema wystawione jako rejestr
Name:		python3-%{module}
Version:	2025.4.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jsonschema-specifications/
Source0:	https://files.pythonhosted.org/packages/source/j/jsonschema-specifications/jsonschema_specifications-%{version}.tar.gz
# Source0-md5:	d3919602b067993ba584fb4fe1662b9d
URL:		https://pypi.org/project/jsonschema-specifications/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling >= 1.27.0
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-referencing >= 0.31.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-pygments-github-lexers
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinxcontrib-spelling > 5
BuildRequires:	python3-sphinxext.opengraph
BuildRequires:	sphinx-pdg-3 > 5
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JSON support files from the JSON Schema Specifications (metaschemas,
vocabularies, etc.), packaged for runtime access from Python as a
referencing-based Schema Registry.

%description -l pl.UTF-8
Pliki wspomagające JSON ze specyfikacji JSON Schema (metaschematy,
słowniki itp.), spakowane w sposób pozwalający na dostęp w czasie
działania programów w Pythonie, jako rejestr schematów oparty na
module referencing.

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

%if %{with tests} || %{with docs}
%{__python3} -m zipfile -e build-3/*.whl build-3-ext
%endif

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-ext" jsonschema_specifications/tests
%endif

%if %{with doc}
# metadata is required
%{__make} -C docs html \
	PYTHONPATH=$PWD/build-3-ext \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/jsonschema_specifications/tests

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
%doc docs/_build/html/{_static,*.html,*.js}
%endif
