=======================================================================
coap-console: interactive access to serial input/output of CoAP servers
=======================================================================

This Python package provides access
to resources that implement the ``tag:riot-os.org,2021:ser-out`` / ``tag:riot-os.org,2021:ser-in`` interfaces over CoAP.
Those resources can be used to provide log output
or interactive shell access
to CoAP servers (not only) on embedded systems.

It is mainly used together with the `coap-scroll-ring-server Rust crate`_
which implements the server side,
for example as used in the `stdio example`_ on `RIOT OS`_.

It can be run directly from the source repository by running::

    $ ./coap-console 'coap://[2001:db8::1]'

(which discovers a stdout resource or stdin-/out pair of resources on the given IP address)

or installed and run using::

    $ pip install coap_console
    $ coap-console 'coap://[2001:db8::1]'

.. _`coap-scroll-ring-server Rust crate`: https://crates.io/crates/coap-scroll-ring-server
.. _`stdio example`: https://gitlab.com/etonomy/riot-module-examples/-/blob/master/riot-coap-handler-demos/src/stdio.rs?ref_type=heads
.. _`RIOT OS`: https://riot-os.org/
