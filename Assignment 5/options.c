#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>
#include <immintrin.h>
#include "./options.h"

int checkArguments(int arg_c, char** arg_v, bool* val, long long* n_bytes, struct options* options) {
  *val = false;
  int opt;
  int errflag = 0;
  options->N = false;
  options->bsize = -1;
  options->input = "none";
  while ((opt = getopt(arg_c, arg_v, ":i:o:")) != -1) {
    switch(opt) {
    case 'i':
      // Only possible cases: ./randall -i {input} {bytes} or ./randall -i {input} -o {output} {bytes}
      if (arg_c != 4 && arg_c != 6) {
	errflag = 2;
	break;
      }
      // Update options struct based on input
      if (strcmp("rdrand", optarg) == 0) {
	options->input = "rdrand";
      }
      else if (strcmp("mrand48_r", optarg) == 0) {
	options->input = "mrand48_r";
      }
      else if ('/' == optarg[0]) {
	options->input = "/f";
	options->source = optarg;
      }
      else {
	//	fprintf(stderr, "Invalid input\n");
	errflag = 2;
	break;
      }
      *val = true;
      break;
      
    case 'o':
      if (arg_c != 4 && arg_c != 6) {
	errflag = 3;
	break;
      }
      // Update options struct based on input
      if (strcmp("stdio", optarg) != 0) {
	options->N = true;
	options->bsize = atoi(optarg);
      }
      // Check that N is a valid integer
      if (strcmp("stdio", optarg) != 0) {
      if (strcmp("0", optarg) != 0 && atoi(optarg) <= 0) {
	//	fprintf(stderr, "Must enter a positive integer\n");
	errflag = 3;
        break;
      }
      }
      *val = true;
      break;
      
    case ':':       
      fprintf(stderr, "Option -%c requires an operand\n", optopt);
      if (optopt == 'i') errflag = 2;
      else errflag = 3;
      break;
    case '?':
      fprintf(stderr, "Unrecognized option: '-%c'\n", optopt);
      break;
    default:
      break;
      
    }
}

  if (optind >= arg_c) {return errflag;}

  // Get the number of bytes
  *n_bytes = atol(arg_v[optind]);
  if (*n_bytes > 0) {
    if (!errflag) *val = true;
  }

  return errflag;
}


