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


.. php:method:: repair_table($table_name)

		:param	string	$table_name:	Name of the table to repair
		:returns:	Array of repair messages or FALSE on failure
		:rtype:	array

		Repairs a database table.

