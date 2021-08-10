:py:mod:`koapy.cli.extensions.verbose_option`
=============================================

.. py:module:: koapy.cli.extensions.verbose_option


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.cli.extensions.verbose_option.VerboseOption



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.extensions.verbose_option.verbose_option



.. py:class:: VerboseOption(*decls, **attrs)

   Bases: :py:obj:`click.Option`

   Options are usually optional values on the command line and
   have some extra features that arguments don't have.

   All other parameters are passed onwards to the parameter constructor.

   :param show_default: controls if the default value should be shown on the
                        help page. Normally, defaults are not shown. If this
                        value is a string, it shows the string instead of the
                        value. This is particularly useful for dynamic options.
   :param show_envvar: controls if an environment variable should be shown on
                       the help page.  Normally, environment variables
                       are not shown.
   :param prompt: if set to `True` or a non empty string then the user will be
                  prompted for input.  If set to `True` the prompt will be the
                  option name capitalized.
   :param confirmation_prompt: Prompt a second time to confirm the
       value if it was prompted for. Can be set to a string instead of
       ``True`` to customize the message.
   :param prompt_required: If set to ``False``, the user will be
       prompted for input only when the option was specified as a flag
       without a value.
   :param hide_input: if this is `True` then the input on the prompt will be
                      hidden from the user.  This is useful for password
                      input.
   :param is_flag: forces this option to act as a flag.  The default is
                   auto detection.
   :param flag_value: which value should be used for this flag if it's
                      enabled.  This is set to a boolean automatically if
                      the option string contains a slash to mark two options.
   :param multiple: if this is set to `True` then the argument is accepted
                    multiple times and recorded.  This is similar to ``nargs``
                    in how it works but supports arbitrary number of
                    arguments.
   :param count: this flag makes an option increment an integer.
   :param allow_from_autoenv: if this is enabled then the value of this
                              parameter will be pulled from an environment
                              variable in case a prefix is defined on the
                              context.
   :param help: the help string.
   :param hidden: hide this option from help outputs.

   .. versionchanged:: 8.0.1
       ``type`` is detected from ``flag_value`` if given.

   .. py:method:: _match_long_opt(self, opt, explicit_value, state)


   .. py:method:: _match_short_opt(self, arg, state)


   .. py:method:: _get_value_from_state(self, option_name, option, state)


   .. py:method:: _patch_parser(self, parser)


   .. py:method:: add_to_parser(self, parser, ctx)



.. py:function:: verbose_option(dest=None, default=None, flag_value=None, expose_value=None, callback=None)


