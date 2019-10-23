typedef struct msg 
{
  char data[20];
} msg;

typedef struct pkt 
{
   int seqnum;
   int acknum;
   int checksum;
   char payload[20];
} pkt;

A_output(msg Message)
{}

B_output(msg Me)