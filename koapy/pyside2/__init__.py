# import os
# import PySide2

# Resolve PySide2 plugin issue, should be imported prior to using of PySide2.
# Entire errror message was like the followings:
#
#   qt.qpa.plugin: Could not load the Qt platform plugin "windows" in "" even though it was found.
#   This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
#
#   Available platform plugins are: direct2d, minimal, offscreen, windows.
#
# I think this is happening due to anancodna environment,
# since Qt dlls are added to PATH under an ananconda environment.
#
# if hasattr(PySide2, '__file__'):
#     qt_qpa_platform_plugin_path = os.path.join(os.path.dirname(PySide2.__file__), 'plugins', 'platforms')
#     os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_qpa_platform_plugin_path
