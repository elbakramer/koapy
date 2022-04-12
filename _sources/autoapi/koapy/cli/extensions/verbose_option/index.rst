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

   koapy.cli.extensions.verbose_option.verbose_flag_option
   koapy.cli.extensions.verbose_option.no_verbose_flag_option
   koapy.cli.extensions.verbose_option.verbose_option



.. py:class:: VerboseOption(*decls, **attrs)

   Bases: :py:obj:`click.Option`

   Options are usually optional values on the command line and
   have some extra features that arguments don't have.

   All other parameters are passed onwards to the parameter constructor.

   :param show_default: Show the default value for this option in its
       help text. Values are not shown by default, unless
       :attr:`Context.show_default` is ``True``. If this value is a
       string, it shows that string in parentheses instead of the
       actual value. This is particularly useful for dynamic options.
       For single option boolean flags, the default remains hidden if
       its value is ``False``.
   :param show_envvar: Controls if an environment variable should be
       shown on the help page. Normally, environment variables are not
       shown.
   :param prompt: If set to ``True`` or a non empty string then the
       user will be prompted for input. If set to ``True`` the prompt
       will be the option name capitalized.
   :param confirmation_prompt: Prompt a second time to confirm the
       value if it was prompted for. Can be set to a string instead of
       ``True`` to customize the message.
   :param prompt_required: If set to ``False``, the user will be
       prompted for input only when the option was specified as a flag
       without a value.
   :param hide_input: If this is ``True`` then the input on the prompt
       will be hidden from the user. This is useful for password input.
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

   .. versionchanged:: 8.1.0
       Help text indentation is cleaned here instead of only in the
       ``@option`` decorator.

   .. versionchanged:: 8.1.0
       The ``show_default`` parameter overrides
       ``Context.show_default``.

   .. versionchanged:: 8.1.0
       The default of a single option boolean flag is not shown if the
       default value is ``False``.

   .. versionchanged:: 8.0.1
       ``type`` is detected from ``flag_value`` if given.

   .. py:method:: add_to_parser(self, parser, ctx)



.. py:function:: verbose_flag_option(default=0, flag_value=1, show_default=False, metavar='[0...5]', help='Set verbosity level.')


.. py:function:: no_verbose_flag_option(help='Force zero verbosity.')


.. py:function:: verbose_option(dest='verbose', default=0, flag_value=1, callback=None, expose_value=False, show_default=False)


