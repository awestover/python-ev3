
#include <stdio.h>
#include <string.h>

int main () {
   char command[50];

   strcpy( command, "python3 test.py" );
   system(command);

   return(0);
}

