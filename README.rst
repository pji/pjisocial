*****************************************
How do I install pywebview macOS Big Sur?
*****************************************
If you are getting an error when trying to install `pywebview` when
running on macOS Big Sur, try running the following before the
install::

    export SYSTEM_VERSION_COMPAT=1

Big Sur changed the major version number for macOS from ten to eleven,
which seems to cause a problem for some versions of `pip` and `numpy`.
Setting the `SYSTEM_VERSION_COMPAT` environment variable to one tells
macOS to report its version as `10.16` rather than `11.0`.
