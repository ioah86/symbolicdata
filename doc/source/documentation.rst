==================================================
Documentation on SDEval
==================================================

:Author:
   Albert Heinle<aheinle@uwaterloo.ca>
:UPDATED:
   Tue Apr 14 11:04:12 EDT 2015


--------------------
Abstract
--------------------
This document serves the purpose to provide a complete documentation
on the SDEval project. This document splits in two different parts:

1. User documentation for SDEval
2. Developer documentation for SDEval

In the user documentation, we will outline different scenarios in which the
one can use the tools in the SDEval project.

In the developer documentation, we will discuss the general structure
of the scripts written in SDEval, so that a potential developer has
the chance to extend the functionality of these tools to his/her
purposes.

--------------------
Table of Contents
--------------------
.. contents::

--------------------
User Documentation
--------------------

Scope of SDEval
=========================

SDEval aims two address two different types of users. The first type
of user is a developer of software for problems in the field of computer algebra,
who wishes to compare his/her implementation with already available
ones. The second type of user is the researcher, who is interested in
the solution to a certain problem, and seeks the assistance of
computer algebra systems. His/her problem may be solved by one particular
computer algebra system in a feasible
amount of time, while another one fails to produce an output fast
enough. Similarly, the outputs of the different systems may
differ. Hence, s/he may be interested to run as many of the systems as
possible.

It is a fair assumption that both types of users are not familiar
with all computer algebra systems out there. Hence, a way to translate
a problem instance of a certain algorithmic problem into executable code is a
desirable functionality to have. SDEval provides this functionality,
and makes it as user-friendly as possible.

But also after the executable code is available, there are more needs,
especially for the developer. There needs to be a way to assess the
performance of software in a fair and reproducible way. SDEval
provides an environment, where the user can run, monitor and quit
one's calculations. This environment is given by a folder structure
with included scripts; we envision these folders to be shared as
tar-balls with publications, so that other users can verify
the results of the user in an as easy as possible way.

SDEval is designed to be as flexible as possible, while maintaining
simplicity for the user. We are extending the system on a
regular basis
with new supported computation problems and supported computer algebra
systems for these problems. The running- and monitoring routines are
even independent from the creation-part. This means that they can be
used to run and monitor computations which may not even be related to computer
algebra. In this way, SDEval provides tools which can be used across
scientific communities.

System Requirements
=========================

SDEval consists of a selection of scripts, which assist the user
in **(i) creating benchmarks** and **(ii) running these benchmarks and
monitoring the computations**. The system requirements for both parts
are varying, as the authors assume that the user mainly does part (i)
on his/her desktop computer, and part (ii) is mainly done on computing
machines, where the user has ssh-access to.

Hence, we distinguish system requirements for part (i) and (ii).

**Ad (i): System Requirements For Creating Benchmarks**

:OS Requirements:
   Any operating system you can install Python 2.7x on.
:Necessary Software (Packages):
   - Python 2.7x.
   - TKinter for Python (only if you want to use the GUI to create
     benchmarks, i.e. ``create_tasks_gui.py``); usually included in
     the Python-distribution.

**Ad (ii): System Requirements For Running and Monitoring Benchmarks**

:OS Requirements:
   Any Unix-like operating system (Linux and Mac OS X).
:Necessary Software (Packages):
   - Python 2.7x.
   - A tool to measure the consumed time of a process, which provides an output compatible with IEEE Std 1003.2-1992
     ("POSIX.2"). Usually provided with the Unix-like operating
     system (command: ``time``).
..
   General outline
   - Creating a task
     - Features (i.a. the tasks and computer algebra systems which are
        currently  supported.)
     - GUI vs. terminal version
     - Changing a task
       - Machinesettings
       - TaskInfo
       - Output interpretation scripts
       - providing manual scripts which the respective computer algebra
         systems can access (like our maple wrapper, or ncfactor.lib)
       - Stability requirements, such that runTask does not run into
         problems:
         - Existence of executable files in the respective locations
         - name of problem instances line up with names of folders in
           casResources
         - name of computer algebra systems are the same as in taskInfo
         - Machinesettings names need to have the same denotations for
           computer algebra systems as the taskInfo file.
         - time command, if different from standard linux time command,
           needs to support the POSIX 2 standard (IEEE Std 1003.2-1992) for time output.
         - All files need to be there
     - Features planned for the future
   - Running a task
     - Features
       - Fail -- Resume
       - Different parallel processes
       - Resource limitations
     - Interventions which not harm the stability of the running process:
       - kill a computer algebra system which is currently running.
     - Interventions that harm the stability of the running process
       - Deleting/locking any files
     - Features planned for the future
