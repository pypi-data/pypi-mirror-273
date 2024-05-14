from setuptools import setup

name = "types-hvac"
description = "Typing stubs for hvac"
long_description = '''
## Typing stubs for hvac

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`hvac`](https://github.com/hvac/hvac) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`hvac`.

This version of `types-hvac` aims to provide accurate annotations
for `hvac==2.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/hvac. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `3195f9fb1b4275144177441815e8132d4a600c83` and was tested
with mypy 1.10.0, pyright 1.1.362, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.1.0.20240514",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/hvac.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-requests'],
      packages=['hvac-stubs'],
      package_data={'hvac-stubs': ['__init__.pyi', 'adapters.pyi', 'api/__init__.pyi', 'api/auth_methods/__init__.pyi', 'api/auth_methods/approle.pyi', 'api/auth_methods/aws.pyi', 'api/auth_methods/azure.pyi', 'api/auth_methods/cert.pyi', 'api/auth_methods/gcp.pyi', 'api/auth_methods/github.pyi', 'api/auth_methods/jwt.pyi', 'api/auth_methods/kubernetes.pyi', 'api/auth_methods/ldap.pyi', 'api/auth_methods/legacy_mfa.pyi', 'api/auth_methods/oidc.pyi', 'api/auth_methods/okta.pyi', 'api/auth_methods/radius.pyi', 'api/auth_methods/token.pyi', 'api/auth_methods/userpass.pyi', 'api/secrets_engines/__init__.pyi', 'api/secrets_engines/active_directory.pyi', 'api/secrets_engines/aws.pyi', 'api/secrets_engines/azure.pyi', 'api/secrets_engines/consul.pyi', 'api/secrets_engines/database.pyi', 'api/secrets_engines/gcp.pyi', 'api/secrets_engines/identity.pyi', 'api/secrets_engines/kv.pyi', 'api/secrets_engines/kv_v1.pyi', 'api/secrets_engines/kv_v2.pyi', 'api/secrets_engines/pki.pyi', 'api/secrets_engines/rabbitmq.pyi', 'api/secrets_engines/ssh.pyi', 'api/secrets_engines/transform.pyi', 'api/secrets_engines/transit.pyi', 'api/system_backend/__init__.pyi', 'api/system_backend/audit.pyi', 'api/system_backend/auth.pyi', 'api/system_backend/capabilities.pyi', 'api/system_backend/health.pyi', 'api/system_backend/init.pyi', 'api/system_backend/key.pyi', 'api/system_backend/leader.pyi', 'api/system_backend/lease.pyi', 'api/system_backend/mount.pyi', 'api/system_backend/namespace.pyi', 'api/system_backend/policies.pyi', 'api/system_backend/policy.pyi', 'api/system_backend/quota.pyi', 'api/system_backend/raft.pyi', 'api/system_backend/seal.pyi', 'api/system_backend/system_backend_mixin.pyi', 'api/system_backend/wrapping.pyi', 'api/vault_api_base.pyi', 'api/vault_api_category.pyi', 'aws_utils.pyi', 'constants/__init__.pyi', 'constants/approle.pyi', 'constants/aws.pyi', 'constants/azure.pyi', 'constants/client.pyi', 'constants/gcp.pyi', 'constants/identity.pyi', 'constants/transit.pyi', 'exceptions.pyi', 'utils.pyi', 'v1/__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
