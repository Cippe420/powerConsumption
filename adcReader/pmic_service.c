
#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define LOGFILE "/var/log/pmic_service.log"
#define DEVICE_FILE_NAME "/dev/vcio"
#define SOCKET_PATH "/run/pmic.sock"
#define MAX_STRING 1024
#define MAJOR_NUM 100
#define MAX_RAILS 32
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

static void log_message(FILE *log_file, const char *message, ...) {
  va_list args;
  time_t now;
  struct tm *tm_info;
  char time_str[26];

  // Get current time
  time(&now);
  tm_info = localtime(&now);
  strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", tm_info);

  // Print to log file
  fprintf(log_file, "[%s] ", time_str);
  va_start(args, message);
  vfprintf(log_file, message, args);
  va_end(args);
  fprintf(log_file, "\n");
  fflush(log_file); // Ensure the log is written immediately
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

typedef struct {
  char name[32];
  double value;
} measurement_t;

int main(int argc, char *argv[]) {

  signal(SIGTERM, sigint_handler);
  signal(SIGINT, sigint_handler);
  FILE *log_file = fopen(LOGFILE, "a");
  if (log_file == NULL) {
    perror("Failed to open log file");
    return 1;
  }

  mb = mbox_open();
  // crea socket locale
  int client_fd, server_fd;
  struct sockaddr_in addr;

  server_fd = socket(AF_INET, SOCK_STREAM, 0);
  if (server_fd < 0) {
    perror("socket");
    return 1;
  }

  unlink(SOCKET_PATH);
  memset(&addr, 0, sizeof(addr));
  addr.sin_family = AF_INET;
  addr.sin_port = htons(12345); // use port 12345 for the socket
  addr.sin_addr.s_addr =
      htonl(INADDR_ANY); // accept connections from any address

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

  client_fd = accept(server_fd, NULL, NULL);
  log_message(log_file, "PMIC service started, waiting for connections...");

  while (!shouldTerminate) {

    char result[MAX_STRING];
    unsigned ret = gencmd(mb, "pmic_read_adc", result, sizeof(result));
    log_message(log_file, result);

    measurement_t currents[MAX_RAILS];
    measurement_t voltages[MAX_RAILS];

    int n_currents = 0;
    int n_voltages = 0;
    char *line = strtok(result, "\n");

    char rail_name[32];
    double rail_value;

    while (line) {
      char *trimmed = line;
      log_message(log_file, "Processing line: [%s]", line);
      int n = sscanf(trimmed, "^\s*([A-Z0-9_]+)_A\s+current\(\d+\)=(\d+\.\d+)A",
                     rail_name, &rail_value);
      if (n == 2) {
        log_message(log_file, "MATCH corrente: rail=%s, value=%.6f\n",
                    rail_name, rail_value);
      } else {
        n = sscanf(trimmed, "^\s*([A-Z0-9_]+)_V\s+volt\(\d+\)=(\d+\.\d+)V",
                   rail_name, &rail_value);
        if (n == 2) {
          log_message(log_file, "MATCH tensione: rail=%s, value=%.6f\n",
                      rail_name, rail_value);
        } else {
          log_message(log_file, "NO MATCH: [%s]\n", trimmed);
        }
      }
      line = strtok(NULL, "\n");
    }

    double total_current = 0.0;
    double total_power = 0.0;

    for (int i = 0; i < MAX_RAILS; i++) {
      double P = voltages[i].value * currents[i].value;
      if (voltages[i].value > 0 && currents[i].value > 0) {
        log_message(log_file,
                    "Rail: %s, Voltage: %.3f V, Current: %.3f A, Power: "
                    "%.3f W",
                    voltages[i].name, voltages[i].value, currents[i].value, P);
        total_current += currents[i].value;
        total_power += P;
      }
    }

    char out[128];
    int len = snprintf(out, sizeof(out), "Current: %.3f A, Power: %.3f W\n",
                       total_current, total_power);

    if (client_fd < 0) {
      client_fd = accept(server_fd, NULL, NULL);
    } else {
      // send the last value to the client
      ssize_t bytes_sent = send(client_fd, out, len, 0);
      if (bytes_sent < 0) {
        perror("send");
        close(client_fd);
        client_fd = accept(server_fd, NULL, NULL);
        continue;
      }
    }

    usleep(1000000); // sleep for 100ms before next read
  }

  close(client_fd);

  // cleanup
  unlink(SOCKET_PATH);
  mbox_close(mb);
  return 0;
}
