:py:mod:`koapy.cli.commands.generate.grpc.ssl_credentials`
==========================================================

.. py:module:: koapy.cli.commands.generate.grpc.ssl_credentials


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.commands.generate.grpc.ssl_credentials.generate_self_signed_key_cert
   koapy.cli.commands.generate.grpc.ssl_credentials.generate_key_cert_signed_by_authority
   koapy.cli.commands.generate.grpc.ssl_credentials.ssl_credentials



.. py:function:: generate_self_signed_key_cert(organization_name, common_name, key_filename=None, cert_filename=None, key_password=None, country_name=None, state_or_province_name=None, locality_name=None, valid_days=None)


.. py:function:: generate_key_cert_signed_by_authority(organization_name, common_name, alternative_dns_names=None, key_filename=None, csr_filename=None, cert_filename=None, key_password=None, country_name=None, state_or_province_name=None, locality_name=None, valid_days=None, authority_key_filename=None, authority_cert_filename=None, authority_key_password=None)


.. py:function:: ssl_credentials()


