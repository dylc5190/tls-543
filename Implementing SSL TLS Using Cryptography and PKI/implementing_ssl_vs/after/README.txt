This distribution contains the contents of each chapter after the
 chapter is complete.  Each
chapter has it's own Microsoft Visual Studio "solution" file, each of which contains multiple projects;
one for each executable developed within the chapter.  Most projects refer to files in other chapter's
directories, so you may want to pay close attention to the dependencies here.  This was tested with
Visual Studio 2005, and should build correctly on any version later than this.
All of the executables from this book are designed to be invoked from the command line; you can open
up a command prompt and navigate to the "Debug" directory after building (this will be created by
Visual Studio) and run them from there.
Alternatively, if you don't have access to Visual Studio, you can download the "_gcc" distribution
which includes Makefiles designed for command-line builds.