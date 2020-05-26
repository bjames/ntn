title: Extending C with Python - Preliminaries
published: 
category:
- Programming
author: Brandon James
summary: 


I've been meaning to revist C for a while now. I think having a compiled language in my toolbox is important. As someone who mostly programs in Python, C makes a lot of sense because you can write Python modules using C. This is something you might need to do if you are doing anything computationally intensive and only if it's absolutely necessary. Python is generally fast enough and premature optimization often leads to bugs and difficult to maintain code.  

I haven't touched C since college, but I remember enough of it that most of the online tutorials are overly basic. So I decided an appropriate way to relearn C would be to write a Python Module in C. I started working through the [Python Doc on Extending Python with C](https://docs.python.org/3/extending/extending.html) and I found that it assumes either a whole lot of background on C and the Python/C API or it assumes the reader is willing to spend a significant time doing research as they read through the doc. In this article, I share my notes from working through the example module assuming the reader has little or no background in C. There will be a follow up article where I write a Python module in C that is more applicable to network engineers. In that article I will also compare the running time of the C module and an equivelent native Python module. 

# Breaking Down Hello, World!

Before we start talking about creating Python modules in C, let's do a brief overview of a basic C program.

```
#include <stdio.h>

void main(){

    printf("Hello, World!\n");

}
```

Even if you've never written C before, you've probably created a similar program in some other langauge. Let's break down each component.

## The Building Process

When we write Python code, you don't need to worry about how the interpriter works. In C, the building process can directly impact how your code is executed, so it's important to think about how your code is manipulated when you invoke your compiler. 

1. Preprocess

The preprocessor makes changes to your .c file based on the preprocessor directives mentioned earlier. The code output by the preprocessor is still _human readable_ C code.[^4]

2. Compile

The compiler translates your preprocessed C code into assembly language code[^5]. 

3. Assemble

The assembler translates your compiled code into machine readable object code[^6]. 

4. Link

The compiler then _links_ the object code to any libraries you are using[^7]. What actually happens here differs between operating systems, but broadly speaking code can be either statically linked or dynamically linked. When code is statically linked, the library code is merged with your code. When code is dynamically linked, the libraries continue to exist as seperate pieces of code on your hard drive. These bits of code can be shared with other dynamically linked applications[^8].

Once this process is complete your code is ready to be executed. 

## `<#include>`

In C, any statement begining with `#` is a preprocessor directive[^1]. `#include` tells the preprocessor to inject the code mentioned in the `#include` statement into the file. Unlike Python, C doesn't provide a print function by default. So in order to write to the terminal we need to import `stdio.h`. Just like the name implies, `stdio` is the portion of the standard library that provides IO functions. If you have access to a linux machine, it's very likely you have `stdio.h` sitting in a folder somewhere. You can find it with `locate stdio.h` and peek at the code if you are curious[^2]. 

It should be noted that you won't actually see a printf function instead the header file, instead you'll find a function prototype:

```
extern int printf (const char *__restrict __format, ...);
```

These prototypes exist only to help the compiler verify your use of the function. In the case of C standard library functions, your compiler already has precompiled copies of the code. After your code has been compiled, it is linked to the precompiled library[^3]. When you run your program, it makes calls to these libraries. 

# 

[^1]: You can read more about preprocessor directives [here](https://en.wikibooks.org/wiki/C_Programming/Preprocessor_directives_and_macros). 
[^2]: Alternatively, you can view it on the [web](https://sourceware.org/git/?p=glibc.git;a=blob;f=include/stdio.h;h=9df98b283353e3d5610b8036876833e86a8eeab0;hb=HEAD).
[^3]: The printf function is found in printf.c in the stdlib, you can view it [here](https://sourceware.org/git/?p=glibc.git;a=blob;f=stdio-common/printf.c;h=15f71c1feddf9e8324ab38afb351c7840af5a8fc;hb=9ea3686266dca3f004ba874745a4087a89682617). On Fedora 32, the compiled object file (assuming you are compiling with gcc) is located at /lib/gcc/x86_64-redhat-linux/10/32/libgcc.a. 
[^4]: You can invoke GCC with the -E flag to only run the preprocessing step. In our simple hello world example, this generates a 731 line file. 
[^5]: You can invoke GCC with the -S flag to stop after the compilation step. This generates a .s file contining the assembly langauge code for your program.
[^6]: You can invoke GCC with the -c flag to stop after the assembly step. This generates a .o file continuing object code. Unlike the fully built .out file the .o file will give you an error when you try to run it. My Fedora 32 system says `bash: ./hello.o: cannot execute binary file: Exec format error` ***********Rewrite this*************
[^7]: When using external libraries, you generally need to tell the compiler where to find the library object files. ************Rewrite this***********
[^8]: In Linux this is handled via the Executable and Linkable Format (ELF), which is described in detail [here](http://www.skyfree.org/linux/references/ELF_Format.pdf) or for a brief linking focused overview you can follow this [link](http://csapp.cs.cmu.edu/2e/ch7-preview.pdf). A good start point for Windows DLLs is avaliable [here](https://support.microsoft.com/en-us/help/815065/what-is-a-dll). 