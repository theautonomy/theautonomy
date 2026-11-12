```console
wei@github:~$ whoami
██╗    ██╗ ███████╗ ██╗      ██╗      ██╗
██║    ██║ ██╔════╝ ██║      ██║      ██║
██║ █╗ ██║ █████╗   ██║      ██║      ██║
██║███╗██║ ██╔══╝   ██║      ██║      ██║
╚███╔███╔╝ ███████╗ ██║      ███████╗ ██║
 ╚══╝╚══╝  ╚══════╝ ╚═╝      ╚══════╝ ╚═╝
```

```console
wei@github:~$ jshell --startup ~/me.jsh
|  Welcome to JShell -- Version 25
jshell> me
me ==> Developer[
          handle    = "theautonomy",
          speaks    = [Java, Spring, SQL, Bash, a little JS],
          lives_in  = "the Spring ecosystem, usually one release ahead",
          builds    = "small, runnable examples that explain one idea well",
          blog      = "https://byweili.com"
        ]
```

<!-- streak:start -->
```console
wei@github:~$ ./streak.sh

  waiting for the first run of .github/workflows/streak.yml ...
```
<!-- streak:end -->

```console
wei@github:~$ mvn -q verify
[INFO] Tests run: ∞, Failures: 0, Errors: 0, Skipped: sleep
[INFO] BUILD SUCCESS — see you in the next commit
```
