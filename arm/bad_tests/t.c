#include <stdio.h>
#include <string.h>
//#include iostream


int main () {
   char command[50];

   strcpy( command, "ls -l" );


   printf("%s\n", command);


   for(int i = 0; i < 50; i++)
   {
       //std::cout << command[i] << "\n";

   }

   system(command);

   return(0);
}
