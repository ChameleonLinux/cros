title: Welcome to Taiga!
datetime: 2016-02-01 15:00

Thanks for installing __Taiga__!

* [Documentation](https://crosdoc.wolflinux.org/)
* [GitHub](https://github.com/ProjectCros)

You can create new pages by adding new file with filenames like __*date*-*title*.md__. Pages are just files, ok?
You may need to study basic Markdown syntax.

> The purpose of our lives is to be happy.

__Taiga__ is just extension for __cros__. Extensions are written in Python and mostly are based on __hooks__.

You can also use *CGI* scripts for dynamic pages. They are not as powerful as extensions but are easier and can be in every language.
Scripts can be compiled - they are executed like programs. You will just need to create rule to run them properly.


*c++ example. hello.compiled*

    #include <iostream>

    int main() {
      std::cout << "Content-Type: text/plain" << endl;
      std::cout << endl;
      std::cout << "Hello, world!" << endl;
    }
