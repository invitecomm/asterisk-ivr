.. Asterisk IVR documentation master file, created by
   sphinx-quickstart on Mon Nov 14 16:14:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   
******************************
Database Connection Settings
******************************

.. automodule:: connection
   
Configuration
******************************

.. autodata:: connection.asterisk_path
.. autodata:: connection.asterisk_conf
.. autodata:: connection.context

Connection Settings
******************************

.. autodata:: connection.config


.. php:class:: CI_FTP

		.. php:method:: connect([$config = array()])

			:param  array   $config: Connection values
			:returns:       TRUE on success, FALSE on failure
			:rtype: bool

			Connects and logs into to the FTP server. Connection preferences are set
			by passing an array to the function, or you can store them in a config
			file.

			Here is an example showing how you set preferences manually::