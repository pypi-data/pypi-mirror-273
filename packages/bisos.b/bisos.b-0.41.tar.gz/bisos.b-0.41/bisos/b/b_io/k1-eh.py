# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: A =CS-Lib= for creating and managing BPO's gpg and encryption/decryption.
#+end_org """

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of Blee ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Libre-Halaal Foundation. Subject to AGPL.
** It is not part of Emacs. It is part of Blee.
** Best read and edited  with Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: NOTYET
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:python:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['eh'], }
csInfo['version'] = '202209082757'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'eh-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/PyFwrk/bisos.crypt/_nodeBase_/fullUsagePanel-en.org][PyFwrk bisos.crypt Panel]]
Module description comes here.
** Relevant Panels:
** Status: In use with BISOS
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO complete fileName in particulars.
#+end_org """

####+BEGIN: b:prog:file/orgTopControls :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Controls |]] :: [[elisp:(delete-other-windows)][(1)]] | [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
#+end_org """
####+END:

####+BEGIN: b:python:file/workbench :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Workbench |]] :: [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: bx:cs:python:icmItem :itemType "=PyImports= " :itemTitle "*Py Library IMPORTS*"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =PyImports=  [[elisp:(outline-show-subtree+toggle)][||]] *Py Library IMPORTS*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

import sys

from bisos import b
from bisos.b import b_io

import logging

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "EH: ICM Error Handling On Top Of Python Exceptions" :anchor "" :extraInfo " (io.eh. Module)"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _EH: ICM Error Handling On Top Of Python Exceptions_: |]]   (io.eh. Module)  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END

####+BEGIN: bx:cs:py3:func :funcName "critical_cmndArgsPositional" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /critical_cmndArgsPositional/  [[elisp:(org-cycle)][| ]]
#+end_org """
def critical_cmndArgsPositional(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )
    #raise RuntimeError()

####+BEGIN: bx:cs:py3:func :funcName "critical_cmndArgsOptional" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /critical_cmndArgsOptional/  [[elisp:(org-cycle)][| ]]
#+end_org """
def critical_cmndArgsOptional(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )
    #raise RuntimeError()

####+BEGIN: bx:cs:py3:func :funcName "critical_usageError" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /critical_usageError/  [[elisp:(org-cycle)][| ]]
#+end_org """
def critical_usageError(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('io.eh.usageError: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )
    return(ReturnCode.UsageError)
    #raise RuntimeError()

####+BEGIN: bx:cs:py3:func :funcName "problem_notyet" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /problem_notyet/  [[elisp:(org-cycle)][| ]]
#+end_org """
def problem_notyet(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('io.eh.NotYet: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )
    #raise RuntimeError()

####+BEGIN: bx:cs:py3:func :funcName "problem_info" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /problem_info/  [[elisp:(org-cycle)][| ]]
#+end_org """
def problem_info(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    logger.critical('io.eh.Info: ' + format(*v, **k) + ' -- ' + b.ast.stackFrameInfoGet(2) )

    return

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('io.eh.Info: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )

####+BEGIN: bx:cs:py3:func :funcName "problem_usageError" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /problem_usageError/  [[elisp:(org-cycle)][| ]]
#+end_org """
def problem_usageError(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )

    return (
        eh_problem_usageError(b.op.Outcome(), *v, **k)
    )

    #raise RuntimeError()


####+BEGIN: bx:cs:py3:func :funcName "eh_problem_usageError" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /eh_problem_usageError/  [[elisp:(org-cycle)][| ]]
#+end_org """
def eh_problem_usageError(
####+END:
        outcome,
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    errStr='io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2)
    return(outcome.set(
        opError=b.op.OpError.UsageError,
        opErrInfo=errStr,
    ))


####+BEGIN: bx:cs:py3:func :funcName "critical_unassigedError" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /critical_unassigedError/  [[elisp:(org-cycle)][| ]]
#+end_org """
def critical_unassigedError(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.critical('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )
    #raise RuntimeError()

####+BEGIN: bx:cs:py3:func :funcName "critical_oops" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /critical_oops/  [[elisp:(org-cycle)][| ]]
#+end_org """
def critical_oops(
####+END:
        *v,
        **k,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    print(('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) ))
    logger.critical('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )

    traceback.print_stack()


    #raise RuntimeError()

####+BEGIN: bx:cs:py3:func :funcName "critical_exception" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /critical_exception/  [[elisp:(org-cycle)][| ]]
#+end_org """
def critical_exception(
####+END:
        e,
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] Usage Example:
    try: m=2/0
    except Exception as e: io.eh.critical_exception(e)
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    #fn = FUNC_currentGet()

    outString = format(e)

    logger.critical('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )

    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logger.critical(
        "io.eh.: {exc_type} {fname} {lineno}"
        .format(
            exc_type=exc_type,
            fname=fname,
            lineno=exc_tb.tb_lineno
        )
    )

    logging.exception(e)

    # Or any of the
    #logger.error("io.eh.critical_exception", exc_info=True)
    #print(traceback.format_exc())

####+BEGIN: bx:cs:py3:func :funcName "badOutcome" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /badOutcome/  [[elisp:(org-cycle)][| ]]
#+end_org """
def badOutcome(
####+END:
        outcome,
):
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    print((
        "io.eh.badOutcome: InvokedBy {invokerName}, Operation Failed: Stdcmnd={stdcmnd} Error={status} -- {errInfo}".
        format(invokerName=outcome.invokerName,
               stdcmnd=outcome.stdcmnd,
               status=outcome.error,
               errInfo=outcome.errInfo,
        )))
    print(('io.eh.: ' + ' -- ' + b.ast.stackFrameInfoGet(2) ))

    return outcome

####+BEGIN: bx:cs:py3:func :funcName "badLastOutcome" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /badLastOutcome/  [[elisp:(org-cycle)][| ]]
#+end_org """
def badLastOutcome(
####+END:
):
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """
    return (
        io.eh.badOutcome(
            cs.G.lastOpOutcome
        ))

####+BEGIN: bx:cs:py3:func :funcName "eh_badLastOutcome" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /eh_badLastOutcome/  [[elisp:(org-cycle)][| ]]
#+end_org """
def eh_badLastOutcome(
####+END:
):
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    return (
            cs.G.lastOpOutcome
    )


####+BEGIN: bx:cs:py3:func :funcName "runTime" :funcType "extTyped" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-extTyped [[elisp:(outline-show-subtree+toggle)][||]] /runTime/  [[elisp:(org-cycle)][| ]]
#+end_org """
def runTime(
####+END:
        *v,
        **k,
):
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    logControler = b_io.log.Control()
    logger = logControler.loggerGet()

    fn = b.ast.FUNC_currentGet()
    argsLength =  b.ast.FUNC_argsLength(fn, v, k)

    if argsLength == 2:   # empty '()'
        outString = ''
    else:
        outString = format(*v, **k)

    logger.error('io.eh.: ' + outString + ' -- ' + b.ast.stackFrameInfoGet(2) )
    raise RuntimeError()



####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :title " ~End Of Editable Text~ "
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _ ~End Of Editable Text~ _: |]]    [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:


####+BEGIN: b:prog:file/endOfFile :extraParams nil
""" #+begin_org
* *[[elisp:(org-cycle)][| END-OF-FILE |]]* :: emacs and org variables and control parameters
#+end_org """
### local variables:
### no-byte-compile: t
### end:
####+END:
