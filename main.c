// C library headers
#include <stdio.h>
#include <string.h>
#include <errno.h>

// Linux headers
#include <fcntl.h> // Contains file controls like O_RDWR
#include <errno.h> // Error integer and strerror() function
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h> // write(), read(), close()

int main()
{
    
    // open serial port
    int serial_port = open("/dev/ttyUSB0", O_RDWR);

    // check for errors
    if(serial_port < 0)
    {
        printf("Error %i opening serial_port: %s\n", errno, strerror(errno));
    }

    /*
    struct termios {
    tcflag_t c_iflag;       input mode flags 
    tcflag_t c_oflag;       output mode flags 
    tcflag_t c_cflag;       control mode flags 
    tcflag_t c_lflag;       local mode flags 
    cc_t c_line;            line discipline 
    cc_t c_cc[NCCS];        control characters 
    };*/

    struct termios tty;

    // get the FD state
    if (tcgetattr(serial_port, &tty) != 0)
    {
        printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
        return EIO;
    }       
    
    /*
    eventually change settings
    */

    // with everything set, read and write into port it's possible

    // buf length can vary
    unsigned char read_buf[256];

    int n = read(serial_port, &read_buf, sizeof(read_buf));


    if (n!=0)
    {
        // hopefully i will be recieveing 

    }

    // cast value to float (?) , is it watts?
    


    close(serial_port);

    return 0;




}