# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: A =CS-Lib= for Managing RO (Remote Operation) Control File Parameters as a ClsFp
#+end_org """

####+BEGIN: b:py3:cs:file/dblockControls :classification "cs-u"
""" #+begin_org
* [[elisp:(org-cycle)][| /Control Parameters Of This File/ |]] :: dblk ctrls classifications=cs-u
#+BEGIN_SRC emacs-lisp
(setq-local b:dblockControls t) ; (setq-local b:dblockControls nil)
(put 'b:dblockControls 'py3:cs:Classification "cs-u") ; one of cs-mu, cs-u, cs-lib, b-lib, pyLibPure
#+END_SRC
#+RESULTS:
: cs-mu
#+end_org """
####+END:

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
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['ro'], }
csInfo['version'] = '202209130210'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'ro-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/PyFwrk/bisos-pip/bisos.cs/_nodeBase_/fullUsagePanel-en.org][PyFwrk bisos.b.cs Panel For RO]] ||
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

####+BEGIN: b:py3:cs:orgItem/basic :type "=PyImports= " :title "*Py Library IMPORTS*" :comment "-- with classification based framework/imports"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =PyImports=  [[elisp:(outline-show-subtree+toggle)][||]] *Py Library IMPORTS* -- with classification based framework/imports  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
** Imports Based On Classification=cs-u
#+end_org """
from bisos import b
from bisos.b import cs
from bisos.b import b_io

import collections
####+END:

import pathlib
import __main__
import os
import sys
import abc


####+BEGIN: bx:cs:py3:section :title "Service Specification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Service Specification*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:class/decl :className "ROSMU" :superClass "object" :comment "Remote Operations Service Unit" :classType "basic"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-basic  [[elisp:(outline-show-subtree+toggle)][||]] /ROSMU/  superClass=object =Remote Operations Service Unit=   [[elisp:(org-cycle)][| ]]
#+end_org """
class ROSMU(object):
####+END:
    """
** Abstraction of Remote Operations Service Multi-Unit.
"""
####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmuName: str,
            rosmuSpec: str,
    ):
        self._rosmuName = rosmuName  # A named reference to rosmuSpec
        self._rosmuSpec = rosmuSpec  # List Of Units, List Of rosmuStates

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuName" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuName/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuName(
####+END:
            self,
    ):
        return self._rosmuName

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuSpec" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuSpec/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuSpec(
####+END:
            self,
    ):
        """
*** ROS Description. The Contract Specification. Points to a file.
        """
        return self._rosmuSpec


####+BEGIN: bx:cs:py3:section :title "Service Access Point"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Service Access Point*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:


####+BEGIN: b:py3:class/decl :className "RosmuAccessPoint" :superClass "object" :comment "ROSMU Access Point" :classType "basic"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-basic  [[elisp:(outline-show-subtree+toggle)][||]] /RosmuAccessPoint/  superClass=object =ROSMU Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class RosmuAccessPoint(object):
####+END:
    """
** Abstraction of ROSMU Access Point
"""
    rosmuBase = "/bisos/var/gitSh/performer"

####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :comment "rosmu params" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  =rosmu params= deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmu: ROSMU,
            rosmuApName: str,
            performerAddr: str,
            rosmuState: str,
            rosmuFiles: str,
    ):
        self._rosmu = rosmu
        self._rosmuApName = rosmuApName
        self._performerAddr = performerAddr
        self._rosmuState = rosmuState
        self._rosmuFiles = rosmuFiles  # slash root of the file system for this rosmu

####+BEGIN: b:py3:cs:method/typing :methodName "rosmu" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmu/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmu(
####+END:
            self,
    ):
        return self._rosmu

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuApName" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuApName/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuApName(
####+END:
            self,
    ):
        return self._rosmuApName

####+BEGIN: b:py3:cs:method/typing :methodName "performerAddr" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /performerAddr/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def performerAddr(
####+END:
            self,
    ):
        return self._performerAddr


####+BEGIN: b:py3:class/decl :className "GitSh_RosmuAccessPoint" :superClass "RosmuAccessPoint" :comment "ROSMU Access Point" :classType "subed"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-subed  [[elisp:(outline-show-subtree+toggle)][||]] /GitSh_RosmuAccessPoint/  superClass=RosmuAccessPoint =ROSMU Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class GitSh_RosmuAccessPoint(RosmuAccessPoint):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""

    rosmuPerformerBase = "/bisos/var/gitSh/performer"
    rosmuInvokerBase = "/bisos/var/gitSh/invoker"

####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmu: ROSMU,
            rosmuApName: str,
            performerAddr: str,
    ):
        super().__init__(rosmu, rosmuApName, performerAddr, rosmuState="", rosmuFiles="")

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuAp_invPath" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuAp_invPath/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuAp_invPath(
####+END:
            self,
    ):
        return (
            os.path.join(__class__.rosmuInvokerBase, self.rosmuApName,)
        )


####+BEGIN: b:py3:cs:method/typing :methodName "rosmuAp_perfPath" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuAp_perfPath/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuAp_perfPath(
####+END:
            self,
    ):
        return (
            os.path.join(__class__.rosmuInvokerBase, self.rosmuApName,)
        )

####+BEGIN: b:py3:class/decl :className "RPyC_RosmuAccessPoint" :superClass "RosmuAccessPoint" :comment "ROSMU Access Point" :classType "subed"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-subed  [[elisp:(outline-show-subtree+toggle)][||]] /RPyC_RosmuAccessPoint/  superClass=RosmuAccessPoint =ROSMU Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class RPyC_RosmuAccessPoint(RosmuAccessPoint):
####+END:
    """
** Abstraction of a SAP.
"""

####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmu: ROSMU,
            rosmuApName: str,
            performerAddr: str,
    ):
        super().__init__(rosmu, rosmuApName, performerAddr, rosmuState="", rosmuFiles="")

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuAp_invPath" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuAp_invPath/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuAp_invPath(
####+END:
            self,
    ):
        return (
            #os.path.join(__class__.rosmuInvokerBase, self.rosmuApName,)
        )


####+BEGIN: b:py3:cs:method/typing :methodName "rosmuAp_perfPath" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuAp_perfPath/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuAp_perfPath(
####+END:
            self,
    ):
        return (
            #os.path.join(__class__.rosmuInvokerBase, self.rosmuApName,)
        )


####+BEGIN: bx:cs:py3:section :title "Operations Access Point"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Operations Access Point*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:class/decl :className "OperationAccessPoint" :superClass "abc.ABC" :comment "Operation Access Point" :classType "abs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-abs    [[elisp:(outline-show-subtree+toggle)][||]] /OperationAccessPoint/  superClass=abc.ABC =Operation Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class OperationAccessPoint(abc.ABC):
####+END:
    """
** Abstraction of An Op AP.
"""

####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmuAp: RosmuAccessPoint,
    ):
        self._rosmuAp = rosmuAp

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuAp" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuAp/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuAp(
####+END:
            self,
    ):
        return self._rosmuAp

####+BEGIN: b:py3:cs:method/typing :methodName "invIdCreate" :deco "abc.abstractmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invIdCreate/ deco=abc.abstractmethod  deco=abc.abstractmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @abc.abstractmethod
    def invIdCreate(
####+END:
            self,
    ):
        self._invId = "NOTYET"  # datetag, plus file check

####+BEGINNOT: b:py3:cs:method/typing :methodName "invId" :deco "property abc.abstractmethod"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Method-    :: /invId/ deco=property abstractmethod  [[elisp:(org-cycle)][| ]]
"""
    @property
    @abc.abstractmethod
    def invId(
####+END:
            self,
    ):
        return self._invId

####+BEGIN: b:py3:cs:method/typing :methodName "invoke" :deco "abc.abstractmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invoke/ deco=abc.abstractmethod  deco=abc.abstractmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @abc.abstractmethod
    def invoke(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:cs:method/typing :methodName "invokeSubmit" :deco "abc.abstractmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeSubmit/ deco=abc.abstractmethod  deco=abc.abstractmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @abc.abstractmethod
    def invokeSubmit(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        pass

####+BEGIN: b:py3:cs:method/typing :methodName "invokeOutcomeRetreive" :deco "abc.abstractmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeOutcomeRetreive/ deco=abc.abstractmethod  deco=abc.abstractmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @abc.abstractmethod
    def invokeOutcomeRetreive(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        pass


####+BEGIN: b:py3:cs:method/typing :methodName "perform" :deco "abc.abstractmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /perform/ deco=abc.abstractmethod  deco=abc.abstractmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @abc.abstractmethod
    def perform(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        pass

####+BEGIN: b:py3:cs:method/typing :methodName "performOutcomeSubmit" :deco "abc.abstractmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /performOutcomeSubmit/ deco=abc.abstractmethod  deco=abc.abstractmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @abc.abstractmethod
    def performOutcomeSubmit(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        pass

####+BEGIN: b:py3:class/decl :className "GitSh_InvokerOpAP" :superClass "OperationAccessPoint" :comment "Operation Access Point" :classType "subed"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-subed  [[elisp:(outline-show-subtree+toggle)][||]] /GitSh_InvokerOpAP/  superClass=OperationAccessPoint =Operation Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class GitSh_InvokerOpAP(OperationAccessPoint):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""


####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmuAp: GitSh_RosmuAccessPoint,
    ):
        self._rosmuAp = rosmuAp


####+BEGIN: b:py3:cs:method/typing :methodName "invokeIdCreate" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeIdCreate/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invokeIdCreate(
####+END:
            self,
    ):
        self._invId = "NOTYET"  # datetag, plus file check
        self._invIdPath = "NOTYET"

####+BEGIN: b:py3:cs:method/typing :methodName "invId" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invId/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invId(
####+END:
            self,
    ):
        return self._invId

####+BEGIN: b:py3:cs:method/typing :methodName "invoke" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invoke/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invoke(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:cs:method/typing :methodName "invokeSubmit" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeSubmit/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invokeSubmit(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:cs:method/typing :methodName "invokeOutcomeRetreive" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeOutcomeRetreive/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invokeOutcomeRetreive(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:class/decl :className "GitSh_PerformerOpAP" :superClass "OperationAccessPoint" :comment "Operation Access Point" :classType "subed"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-subed  [[elisp:(outline-show-subtree+toggle)][||]] /GitSh_PerformerOpAP/  superClass=OperationAccessPoint =Operation Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class GitSh_PerformerOpAP(OperationAccessPoint):
####+END:
    """
** Abstraction of the base ByStar Portable Object
"""

####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmuAp: GitSh_RosmuAccessPoint,
    ):
        self._rosmuAp = rosmuAp

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuAp" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuAp/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuAp(
####+END:
            self,
    ):
        return self._rosmuAp


####+BEGIN: b:py3:cs:method/typing :methodName "invId" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invId/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def invId(
####+END:
            self,
    ):
        return self._invId

####+BEGIN: b:py3:cs:method/typing :methodName "perform" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /perform/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def perform(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:cs:method/typing :methodName "performOutcomeSubmit" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /performOutcomeSubmit/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def performOutcomeSubmit(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")


####+BEGIN: b:py3:class/decl :className "RPyC_InvokerOpAP" :superClass "OperationAccessPoint" :comment "Operation Access Point" :classType "subed"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-subed  [[elisp:(outline-show-subtree+toggle)][||]] /RPyC_InvokerOpAP/  superClass=OperationAccessPoint =Operation Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class RPyC_InvokerOpAP(OperationAccessPoint):
####+END:
    """
** Place holder, unused. Abstraction of Invocation at Operation Access Point.
"""

####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmuAp: GitSh_RosmuAccessPoint,
    ):
        self._rosmuAp = rosmuAp


####+BEGIN: b:py3:cs:method/typing :methodName "invokeIdCreate" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeIdCreate/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invokeIdCreate(
####+END:
            self,
    ):
        self._invId = "NOTYET"  # datetag, plus file check
        self._invIdPath = "NOTYET"

####+BEGIN: b:py3:cs:method/typing :methodName "invId" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invId/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invId(
####+END:
            self,
    ):
        return self._invId

####+BEGIN: b:py3:cs:method/typing :methodName "invoke" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invoke/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invoke(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:cs:method/typing :methodName "invokeSubmit" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeSubmit/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invokeSubmit(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:cs:method/typing :methodName "invokeOutcomeRetreive" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invokeOutcomeRetreive/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def invokeOutcomeRetreive(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:class/decl :className "RPyC_PerformerOpAP" :superClass "OperationAccessPoint" :comment "Operation Access Point" :classType "subed"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-subed  [[elisp:(outline-show-subtree+toggle)][||]] /RPyC_PerformerOpAP/  superClass=OperationAccessPoint =Operation Access Point=   [[elisp:(org-cycle)][| ]]
#+end_org """
class RPyC_PerformerOpAP(OperationAccessPoint):
####+END:
    """
** Place holder, unused. Abstraction of Performance at Operation Access Point.
"""

####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmuAp: GitSh_RosmuAccessPoint,
    ):
        self._rosmuAp = rosmuAp

####+BEGIN: b:py3:cs:method/typing :methodName "rosmuAp" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /rosmuAp/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def rosmuAp(
####+END:
            self,
    ):
        return self._rosmuAp


####+BEGIN: b:py3:cs:method/typing :methodName "invId" :deco "property"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /invId/ deco=property  deco=property   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @property
    def invId(
####+END:
            self,
    ):
        return self._invId

####+BEGIN: b:py3:cs:method/typing :methodName "perform" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /perform/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def perform(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")

####+BEGIN: b:py3:cs:method/typing :methodName "performOutcomeSubmit" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /performOutcomeSubmit/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def performOutcomeSubmit(
####+END:
            self,
            opName: str,
            opParams: str,
    ):
        """
*** Look into rosmuSpec, subject opName to access control, then invoke
        """
        print(f"{opName}{opParams}")


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CSU" :anchor ""  :extraInfo "Command Services Section"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CSU_: |]]  Command Services Section  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


####+BEGIN: b:py3:cs:func/typing :funcName "examples_csu" :funcType "eType" :retType "" :deco "default" :argsList ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-eType  [[elisp:(outline-show-subtree+toggle)][||]] /examples_csu/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def examples_csu(
####+END:
        sectionTitle: typing.AnyStr = '',
) -> None:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ] Examples of Service Access Instance Commands.
    #+end_org """

    def cpsInit(): return collections.OrderedDict()
    def menuItem(verbosity): cs.examples.cmndInsert(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'

    if sectionTitle == 'default':
        cs.examples.menuChapter('*Remote Operations Management*')

    icmWrapper = ""
    cmndName = "ro_sapCreate"
    cps = cpsInit() ; cps['perfName'] = "localhost" ; cps['rosmu'] = "csB2Examples.cs"
    cmndArgs = "" ;

    cs.examples.cmndInsert(cmndName, cps, cmndArgs, verbosity='none', icmWrapper=icmWrapper)

    #cmndName = "pyCmndInvOf_parsArgsStdinCmndResult" ; cps = cpsInit() ; cmndArgs = "" ;
    #menuItem(verbosity='none')

    cs.examples.menuChapter('FileParams Access And Management*')

    icmWrapper = ""
    cmndName = "ro_fps"
    cps = cpsInit() ; cps['perfName'] = "localhost" ; cps['rosmu'] = "csB2Examples.cs"
    cmndArgs = "list" ;
    cs.examples.cmndInsert(cmndName, cps, cmndArgs, verbosity='none', icmWrapper=icmWrapper)

    icmWrapper = ""
    cmndName = "ro_fps"
    cps = cpsInit() ; cps['perfName'] = "localhost" ; cps['rosmu'] = "csB2Examples.cs"
    cmndArgs = "menu" ;
    cs.examples.cmndInsert(cmndName, cps, cmndArgs, verbosity='none', icmWrapper=icmWrapper)

####+BEGIN: b:py3:cs:func/args :funcName "commonParamsSpecify" :comment "Params Spec for: --aipxBase --aipxRoot" :funcType "FmWrk" :retType "Void" :deco "" :argsList "icmParams"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-A-FmWrk  [[elisp:(outline-show-subtree+toggle)][||]] /commonParamsSpecify/ deco=   [[elisp:(org-cycle)][| ]] =Params Spec for: --aipxBase --aipxRoot=   [[elisp:(org-cycle)][| ]]
#+end_org """
def commonParamsSpecify(
    icmParams,
):
####+END:
    """
** --rosmu (Remote Operations Service Unit. Name of the ROS)
    """

    SapBase_FPs.fps_asIcmParamsAdd(icmParams,)

    icmParams.parDictAdd(
        parName='perfName',
        parDescription="Performer Name. In Bx, A container name.",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--perfName',
    )
    icmParams.parDictAdd(
        parName='perfModel',
        parDescription="Performer Model. For now just rpyc.",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--perfModel',
    )
    icmParams.parDictAdd(
        parName='roSapPath',
        parDescription="Path to FPs base.",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--roSapPath',
    )
    icmParams.parDictAdd(
        parName='perfAuSel',
        parDescription="Performer Authentication Unit Selector",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--perfAuSel',
    )
    icmParams.parDictAdd(
        parName='perfAuAddr',
        parDescription="Performer Authentication Unit Address",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--perfAuAddr',
    )
    icmParams.parDictAdd(
        parName='rosmu',
        parDescription="Remote Operations Service Multi-Unit. Name of the ROS",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--rosmu',
    )
    icmParams.parDictAdd(
        parName='rosmuSel',
        parDescription="rosmu SAP Selector.",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--rosmuSel',
    )
    icmParams.parDictAdd(
        parName='rosmuAp',
        parDescription="Combination of perfAuAddr+rosmu+rosmuSel",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--rosmuAp',
    )
    icmParams.parDictAdd(
        parName='rosmuApPath',
        parDescription="A path to rosmuAp is available as FPs",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--rosmuApPath',
    )
    icmParams.parDictAdd(
        parName='invId',
        parDescription="Remote Operations Service Unit. Name of the ROS",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.ICM_ParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--invId',
    )


####+BEGIN: bx:dblock:python:class :className "SapBase_FPs" :superClass "b.fpCls.BaseDir" :comment "" :classType "basic"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Cls-basic  [[elisp:(outline-show-subtree+toggle)][||]] /SapBase_FPs/ b.fpCls.BaseDir  [[elisp:(org-cycle)][| ]]
#+end_org """
class SapBase_FPs(b.fpCls.BaseDir):
####+END:
    """
** Abstraction of the PalsBase for LiveTargets
"""
####+BEGIN: b:py3:cs:method/typing :methodName "__init__" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /__init__/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def __init__(
####+END:
            self,
            rosmu: str="",
            perfName: str="",
            perfModel: str="",
            rosmuSel: str="",
            roSapPath: str="",
            fpBase: str="",
    ):
        self.rosmu = rosmu
        self.perfName = perfName
        self.perfModel = perfModel
        self.rosmuSel = rosmuSel
        self.roSapPath = roSapPath

        if fpBase:
            self.roSapPath = fpBase
            fileSysPath = fpBase
        elif roSapPath:
            if rosmu or perfModel or perfName or rosmuSel:
                b_io.eh.eh_problem_usageError("conflict with roSapPath")
            fileSysPath = roSapPath
        else:
            fileSysPath = self.basePath_obtain()

        super().__init__(fileSysPath,)


####+BEGIN: b:py3:cs:method/typing :methodName "fps_asCsParamsAdd" :deco "staticmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /fps_asCsParamsAdd/  deco=staticmethod  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @staticmethod
    def fps_asCsParamsAdd(
####+END:
            icmParams,
    ):
        """staticmethod: takes in icmParms and augments it with fileParams. returns icmParams."""
        icmParams.parDictAdd(
            parName='perfIpAddr',
            parDescription="",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            #parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--perfIpAddr',
        )
        icmParams.parDictAdd(
            parName='perfPortNu',
            parDescription="",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            #parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--perfPortNu',
        )
        icmParams.parDictAdd(
            parName='accessControl',
            parDescription="",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            #parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--accessControl',
        )

        return icmParams


####+BEGIN: b:py3:cs:method/typing :methodName "fps_asIcmParamsAdd" :deco "staticmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /fps_asIcmParamsAdd/ deco=staticmethod  deco=staticmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @staticmethod
    def fps_asIcmParamsAdd(
####+END:
            icmParams,
    ):
        """staticmethod: takes in icmParms and augments it with fileParams. returns icmParams."""
        icmParams.parDictAdd(
            parName='perfIpAddr',
            parDescription="",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            #parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--perfIpAddr',
        )
        icmParams.parDictAdd(
            parName='perfPortNu',
            parDescription="",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            #parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--perfPortNu',
        )
        icmParams.parDictAdd(
            parName='accessControl',
            parDescription="",
            parDataType=None,
            parDefault=None,
            parChoices=list(),
            #parScope=icm.ICM_ParamScope.TargetParam,  # type: ignore
            argparseShortOpt=None,
            argparseLongOpt='--accessControl',
        )

        return icmParams

####+BEGIN: b:py3:cs:method/typing :methodName "perfNameToRoSapPath" :deco "staticmethod"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /perfNameToRoSapPath/ deco=staticmethod  deco=staticmethod   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @staticmethod
    def perfNameToRoSapPath(
####+END:
            perfName,
            rosmu=None,
            rosmuSel=None,
            perfModel=None,
    ):
        """."""

        if rosmu == None:
            rosmu=cs.G.icmMyName()

        if rosmuSel == None:
            rosmuSel="default"

        if perfModel == None:
            perfModel="rpyc"

        sapBaseFps = b.pattern.sameInstance(SapBase_FPs, rosmu=rosmu, perfName=perfName, perfModel=perfModel, rosmuSel=rosmuSel)

        roSapPath = sapBaseFps.fps_absBasePath()

        return roSapPath

####+BEGIN: b:py3:cs:method/typing :methodName "fps_manifestDict" :deco ""
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /fps_manifestDict/ deco=    [[elisp:(org-cycle)][| ]]
    #+end_org """
    def fps_manifestDictBuild(
####+END:
            self,
    ):
        """ ConcreteMethod based on abstract pattern
        """
        csParams = cs.G.icmParamDictGet()
        self._manifestDict = {}
        paramsList = [
                'perfIpAddr',
                'perfPortNu',
                'accessControl',
                'perfName',
                'perfModel',
                'rosmu',
                'rosmuSel',
        ]
        for eachParam in paramsList:
            thisCsParam = csParams.parNameFind(eachParam)   # type: ignore
            thisFpCmndParam = b.fpCls.FpCmndParam(
                cmndParam=thisCsParam,
                fileParam=None,
            )
            self._manifestDict[eachParam] = thisFpCmndParam
        #
        # Assign subBases -- Nested Params -- Not Implemented
        #
        #self._manifestDict[eachParam] = FpCsParamsBase_name

        return self._manifestDict


####+BEGIN: bx:icm:py3:method :methodName "fps_namesWithRelPath_NOT" :deco "classmethod"
    """
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-       :: /fps_namesWithRelPath_NOT/ deco=classmethod  [[elisp:(org-cycle)][| ]]
#+end_org """
    @classmethod
    def fps_namesWithRelPath_NOT(
####+END:
            cls,
    ):
        """classmethod: returns a dict with fp names as key and relBasePath as value.
        The names refer to icmParams.parDictAdd(parName) of fps_asIcmParamsAdd
        """
        relBasePath = "."
        return (
            {
                'perfIpAddr': relBasePath,
                'perfPortNu': relBasePath,
                'accessControl': relBasePath,
                'perfName': relBasePath,
                'perfModel': relBasePath,
                'rosmu': relBasePath,
                'rosmuSel': relBasePath,
            }
        )



####+BEGIN: b:py3:cs:method/typing :methodName "fps_absBasePath" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /fps_absBasePath/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_absBasePath(
####+END:
           self,
    ):
        return typing.cast(str, self.basePath_obtain())



####+BEGIN: b:py3:cs:method/typing :methodName "basePath_obtain" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /basePath_obtain/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def basePath_obtain(
####+END:
           self,
    ) -> pathlib.Path:
        return (
            pathlib.Path(
                os.path.join(
                    "/bisos/var/cs/ro/sap",
                    self.rosmu,
                    self.perfName,
                    self.perfModel,
                    self.rosmuSel,
                )
            )
        )


####+BEGIN: b:py3:cs:method/typing :methodName "basePath_update" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /basePath_update/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def basePath_update(
####+END:
           self,
    ) -> pathlib.Path:
        basePath = self.basePath_obtain()
        basePath.mkdir(parents=True, exist_ok=True)
        return basePath


####+BEGIN: b:py3:cs:method/typing :methodName "fps_baseMake" :deco "default"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-     [[elisp:(outline-show-subtree+toggle)][||]] /fps_baseMake/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def fps_baseMake(
####+END:
            self,
    ):
        #palsControlPath = self.basePath_obtain()
        #fpsPath = self.basePath_obtain()
        #self.fpsBaseInst = repoLiveParams.PalsRepo_LiveParams_FPs(
        #    fpsPath,
        #)
        #return self.fpsBaseInst
        pass


####+BEGIN: bx:cs:py3:section :title "CS ro_sap Cmnds"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CS ro_sap Cmnds*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGINNOT: b:py3:cs:cmnd/classHead :cmndName "ro_sapCreate" :ro "noCli" :comment "" :parsMand "perfName rosmu" :parsOpt "perfModel rosmuSel" :argsMin 0 :argsMax 0
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<ro_sapCreate>>parsMand=perfName rosmu parsOpt=perfModel rosmuSel argsMin=0 argsMax=0 ro=noCli pyInv=
#+end_org """
class ro_sapCreate(cs.Cmnd):
    cmndParamsMandatory = [ 'perfName', 'rosmu', ]
    cmndParamsOptional = [ 'perfModel', 'rosmuSel', ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}
    rtInvConstraints = cs.rtInvoker.RtInvoker.new_noRo() # NO RO From CLI

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             perfName: typing.Optional[str]=None,  # Cs Mandatory Param
             rosmu: typing.Optional[str]=None,  # Cs Mandatory Param
             perfModel: typing.Optional[str]=None,  # Cs Optional Param
             rosmuSel: typing.Optional[str]=None,  # Cs Optional Param
    ) -> b.op.Outcome:

####+END:
        """\
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]] Creates path for ro_sap and updates FPs
        """

        # if not (perfName is None or roSapPath is None):
        #     return b_io.eh.eh_problem_usageError("Either perfName or roSapPath should be specified")

        # if perfName and roSapPath:
        #     return b_io.eh.eh_problem_usageError("Both perfName and roSapPath should be specified")

        if not rosmuSel:
            rosmuSel = "default"

        if not perfModel:
            perfModel = "rpyc"

        #cmndArgs = list(self.cmndArgsGet("0&1", cmndArgsSpecDict, effectiveArgsList)) # type: ignore

        sapBaseFps = b.pattern.sameInstance(SapBase_FPs, rosmu=rosmu, perfName=perfName, perfModel=perfModel, rosmuSel=rosmuSel)

        sapBaseFps.fps_setParam('perfIpAddr', "127.0.0.1")
        sapBaseFps.fps_setParam('perfPortNu', "123456")
        sapBaseFps.fps_setParam('accessControl', "placeholder")
        sapBaseFps.fps_setParam('perfName', perfName)
        sapBaseFps.fps_setParam('perfModel', perfModel)
        sapBaseFps.fps_setParam('rosmu', rosmu)
        sapBaseFps.fps_setParam('rosmuSel', rosmuSel)

        return(cmndOutcome)

####+BEGIN: bx:cs:py3:section :title "CS Performer"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CS Performer*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGINNOT: b:py3:cs:cmnd/classHead :cmndName "csPerformer" :comment "" :parsMand "" :parsOpt "roSapPath perfName" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<csPerformer>>parsMand= parsOpt=roSapPath perfName argsMin=0 argsMax=0 pyInv=
#+end_org """
class csPerformer(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ 'roSapPath', 'perfName', ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}
    rtInvConstraints = cs.rtInvoker.RtInvoker.new_noRo()

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             roSapPath: typing.Optional[str]=None,  # Cs Optional Param
             perfName: typing.Optional[str]=None,  # Cs Optional Param
    ) -> b.op.Outcome:

####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  A starting point command.
        #+end_org """)

        #print("JJ")
        #b_io.pr(perfName)
        #b_io.pr(roSapPath)

        if not (roSapPath or perfName):
            # both are None
            return b_io.eh.eh_problem_usageError(f"either perfName or roSapPath must be specified.")

        if roSapPath and perfName:
            # neither are None
            return (
                b_io.eh.eh_problem_usageError(f"both perfName and roSapPath can not be specified.")
            )

        #b_io.pr(perfName)

        if perfName:
            roSapPath = SapBase_FPs.perfNameToRoSapPath(perfName)

        #b_io.pr(roSapPath)

        # read file params, based on perfModel, invoke appropriate performer.
        sapBaseFps = b.pattern.sameInstance(SapBase_FPs, roSapPath=roSapPath)

        #sapBaseFps.fps_setParam('perfIpAddr', "127.0.0.1")
        portNu = sapBaseFps.fps_getParam('perfPortNu')
        #sapBaseFps.fps_setParam('accessControl', "placeholder")

        b_io.pr(f"Performer at::  portNu=${portNu} -- roSapPath={roSapPath}")

        cs.rpyc.csPerform(portNu.parValueGet())

        return(cmndOutcome)


####+BEGINNOT: b:py3:cs:cmnd/classHead :cmndName "ro_fps" :comment ""  :extent "noVerify" :ro "noCli" :parsMand "" :parsOpt "roSapPath perfName rosmu rosmuSel perfModel" :argsMin 1 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<ro_fps>>  =verify= parsOpt=roSapPath perfName rosmu rosmuSel perfModel argsMin=1 argsMax=9999 ro=noCli   [[elisp:(org-cycle)][| ]]
#+end_org """
class ro_fps(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ 'roSapPath', 'perfName', 'rosmu', 'rosmuSel', 'perfModel', ]
    cmndArgsLen = {'Min': 1, 'Max': 9999,}
    rtInvConstraints = cs.rtInvoker.RtInvoker.new_noRo() # NO RO From CLI

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             roSapPath: typing.Optional[str]=None,  # Cs Optional Param
             perfName: typing.Optional[str]=None,  # Cs Optional Param
             rosmu: typing.Optional[str]=None,  # Cs Optional Param
             rosmuSel: typing.Optional[str]=None,  # Cs Optional Param
             perfModel: typing.Optional[str]=None,  # Cs Optional Param
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  A starting point command.
        #+end_org """)

        if not (roSapPath or perfName):
            # both are None
            return b_io.eh.eh_problem_usageError(f"either perfName or roSapPath must be specified.")

        if roSapPath and perfName:
            # neither are None
            return (
                b_io.eh.eh_problem_usageError(f"both perfName and roSapPath can not be specified.")
            )

        cmndArgsSpecDict = self.cmndArgsSpec()

        action = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        actionArgs = self.cmndArgsGet("1&9999", cmndArgsSpecDict, argsList)

        # actionArgsStr = ""
        # for each in actionArgs:
        #     actionArgsStr = actionArgsStr + " " + each

        # actionAndArgs = f"""{action} {actionArgsStr}"""

        b.comment.orgMode(""" #+begin_org
*****  [[elisp:(org-cycle)][| *Note:* | ]] Next we take in stdin, when interactive.
After that, we print the results and then provide a result in =cmndOutcome=.
        #+end_org """)

        if perfName:
            roSapPath = SapBase_FPs.perfNameToRoSapPath(perfName, rosmu=rosmu, rosmuSel=rosmuSel, perfModel=perfModel)

        sapBaseFps = b.pattern.sameInstance(SapBase_FPs, roSapPath=roSapPath)

        if action == "list":
            print(f"With fpBase={roSapPath} and cls={SapBase_FPs} name={sapBaseFps.__class__.__name__}.")
            if b.fpCls.fpParamsReveal(cmndOutcome=cmndOutcome).cmnd(
                    rtInv=rtInv,
                    cmndOutcome=cmndOutcome,
                    fpBase=roSapPath,
                    cls=sapBaseFps.__class__.__name__,
                    argsList=['getExamples'],
            ).isProblematic(): return(icm.EH_badOutcome(cmndOutcome))

        elif action == "menu":
            print(f"With fpBase={roSapPath} and cls={SapBase_FPs} NOTYET.")
        else:
            print(f"bad input {action}")

        return(cmndOutcome)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default   [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """  #+begin_org
** [[elisp:(org-cycle)][| *cmndArgsSpec:* | ]]
        #+end_org """

        cmndArgsSpecDict = cs.arg.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="action",
            argChoices=['list', 'menu',],
            argDescription="Action to be specified by rest"
        )
        cmndArgsSpecDict.argsDictAdd(
            argPosition="1&9999",
            argName="actionArgs",
            argChoices=[],
            argDescription="Rest of args for use by action"
        )

        return cmndArgsSpecDict


####+BEGIN: b:py3:cs:func/typing :funcName "roInvokeCmndAtSap" :comment "~Name of Box File Params~"  :funcType "eType" :deco "track"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-eType  [[elisp:(outline-show-subtree+toggle)][||]] /roInvokeCmndAtSap/  ~Name of Box File Params~ deco=track  [[elisp:(org-cycle)][| ]]
#+end_org """
@cs.track(fnLoc=True, fnEntry=True, fnExit=True)
def roInvokeCmndAtSap(
####+END:
        roSapPath: typing.Optional[str],  # RO pyInv Sap Path
        rtInv,
        cmndOutcome,
        cmndClass,
        ** cmndKwArgs,
) -> b.op.Outcome:
    """ #+begin_org
** [[elisp:(org-cycle)][| *DocStr | ]
    #+end_org """

    sapBaseFps = b.pattern.sameInstance(cs.ro.SapBase_FPs, roSapPath=roSapPath)
    portNu = sapBaseFps.fps_getParam('perfPortNu')
    ipAddr = sapBaseFps.fps_getParam('perfIpAddr')
    cmndKwArgs.update({'rtInv': rtInv})
    cmndKwArgs.update({'cmndOutcome': cmndOutcome})
    print(f"roInvokeCmndAtSap at {roSapPath} of {cmndClass.__name__} with {cmndKwArgs}", file=sys.stderr)
    rpycInvResult = cs.rpyc.csInvoke(
        ipAddr.parValueGet(),
        portNu.parValueGet(),
        cmndClass,
        **cmndKwArgs,
    )
    return rpycInvResult




####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* *[[elisp:(org-cycle)][| ~End-Of-Editable-Text~ |]]* :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
