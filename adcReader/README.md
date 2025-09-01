## pmic_service

This repository contains the source code for the `pmic_service`, a service designed retrieve the PMIC (Power Management Integrated Circuit) information from the system and expose it through a TCP socket.


### Features
- Listens on a specified TCP port for incoming connections.
- Retrieves PMIC information using the `pmic_read_adc` command and determines the power consumption.
- Sends the information back to the connected client.


### Code Structure

- mbox_open()
    open the "DEVICE_FILE_NAME" file and return the file descriptor.

- mbox_close()
    close the file descriptor.

- log_message()
    log the message to the syslog.

- mbox_property()
    ioctl wrapper that sends a property request to the mailbox.

- gencmd()
    constructs a "property message" to execute a general command, here it is used to call "pmic_read_adc".
    uses an array p[] to store and send the header of the property buffer.


- find_or_create_rail(), strip_suffix()
    helper functions to calculate the power consumption after retrieving the PMIC information.


- main()
    - sets up a TCP socket to listen for incoming connections on a specified port.
    - when a client connects, it retrieves the PMIC information using the `gencmd` function.
    - processes the retrieved data to calculate power consumption.
    - sends the PMIC information and power consumption back to the client.




