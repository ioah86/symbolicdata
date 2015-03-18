Documentation on SDEval
==================================================

:Author:
   Albert Heinle<aheinle@uwaterloo.ca>
:UPDATED:
   Thu Feb  5 14:34:42 EST 2015


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

Table of Contents
--------------------
.. contents::

User Documentation
--------------------

..
   General outline
   - System requirements.
   - Scope of SDEval
     - Mathematicians not familiar with computer algebra systems
     - People writing papers and running certain computations.
     - What are currently the biggest problems with computations
        mentioned in papers?
     - Reproducibility
     - Creating benchmarks easily
     - Running benchmarks easily and providing ways to interpret data.
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
