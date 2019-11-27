import sys, os


name = "none"
if len(sys.argv) == 2:
	name = sys.argv[1]
else:
	sys.exit()


text = """
#include <stdio.h>
#include <string.h>

int main () {{
   char command[50];

   strcpy( command, "python3 {}.py" );
   system(command);

   return(0);
}}

""".format(name)

print(text)


with open(os.path.join("exs", "run_{}_cpy.c".format(name)), "w") as f:
	f.write(text)


os.system("gcc " + os.path.join("exs","run_{0}_cpy.c -o run_{0}_cpy".format(name)))

# os.system("./run_{}_cpy".format(name))
