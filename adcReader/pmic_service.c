
#include <fcntl.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <time.h>
#include <unistd.h>

#define DEVICE_FILE_NAME "/dev/vcio"
#define SOCKET_PATH "/run/pmic.sock"
#define MAX_STRING 1024
#define MAJOR_NUM 100
#define IOCTL_MBOX_PROPERTY _IOWR(MAJOR_NUM, 0, char *)
#define GET_GENCMD_RESULT 0x00030080
int mb;
char last_value[MAX_STRING] = "uninitialized";

static int mbox_open() {
  int file_desc;

  // open a char device file used for communicating with kernel mbox driver
  file_desc = open(DEVICE_FILE_NAME, 0);
  if (file_desc < 0) {
    printf("Can't open device file: %s\n", DEVICE_FILE_NAME);
    printf("Try creating a device file with: sudo mknod %s c %d 0\n",
           DEVICE_FILE_NAME, MAJOR_NUM);
    exit(-1);
  }
  return file_desc;
}

static void mbox_close(int file_desc) { close(file_desc); }

static int mbox_property(int file_desc, void *buf) {
  int ret_val = ioctl(file_desc, IOCTL_MBOX_PROPERTY, buf);

  if (ret_val < 0) {
    printf("ioctl_set_msg failed:%d\n", ret_val);
  }
  return ret_val;
}

static unsigned gencmd(int file_desc, const char *command, char *result,
                       int result_len) {
  int i = 0;
  unsigned p[(MAX_STRING >> 2) + 7];
  int len = strlen(command);
  // maximum length for command or response
  if (len + 1 >= MAX_STRING) {
    fprintf(stderr, "gencmd length too long : %d\n", len);
    return -1;
  }
  p[i++] = 0;          // size
  p[i++] = 0x00000000; // process request

  p[i++] = GET_GENCMD_RESULT; // (the tag id)
  p[i++] = MAX_STRING;        // buffer_len
  p[i++] = 0;                 // request_len (set to response length)
  p[i++] = 0;                 // error repsonse

  memcpy(p + i, command, len + 1);
  i += MAX_STRING >> 2;

  p[i++] = 0x00000000;  // end tag
  p[0] = i * sizeof *p; // actual size

  mbox_property(file_desc, p);
  result[0] = 0;
  strncat(result, (const char *)(p + 6), result_len);

  return p[5];
}

static volatile int shouldTerminate = 0;

void sigint_handler(int sig) {
  shouldTerminate = 1;
  unlink(SOCKET_PATH);
  mbox_close(mb);
  exit(0);
}

int main(int argc, char *argv[]) {

  signal(SIGTERM, sigint_handler);
  signal(SIGINT, sigint_handler);

  mb = mbox_open();
  // crea socket locale
  int client_fd, server_fd;
  struct sockaddr_un addr;

  server_fd = socket(AF_UNIX, SOCK_STREAM, 0);
  if (server_fd < 0) {
    perror("socket");
    return 1;
  }

  unlink(SOCKET_PATH);
  memset(&addr, 0, sizeof(addr));
  addr.sun_family = AF_UNIX;
  strncpy(addr.sun_path, SOCKET_PATH, sizeof(addr.sun_path) - 1);

  if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("bind");
    close(server_fd);
    return 1;
  }

  if (listen(server_fd, 5) < 0) {
    perror("listen");
    close(server_fd);
    return 1;
  }

  // start polling the values
  while (!shouldTerminate) {
    char result[MAX_STRING];
    if (gencmd(mb, "pmic_read_adc", result, sizeof(result)) == 0) {
      strncpy(last_value, result, sizeof(last_value) - 1);
    }

    struct timeval tv = {0, 0};
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(server_fd, &fds);
    int ret = select(server_fd + 1, &fds, NULL, NULL, &tv);
    if (ret > 0 && FD_ISSET(server_fd, &fds)) {
      client_fd = accept(server_fd, NULL, NULL);
      if (client_fd > 0) {
        write(client_fd, last_value, strlen(last_value));
        write(client_fd, "\n", 1);
        close(client_fd);
      }
    }
    // obsoleta, should use nanosleep
    usleep(500000);
  }

  // cleanup
  unlink(SOCKET_PATH);
  mbox_close(mb);
  return 0;
}
