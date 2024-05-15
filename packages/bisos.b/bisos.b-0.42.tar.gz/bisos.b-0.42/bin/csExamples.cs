#!/bin/env python
# -*- coding: utf-8 -*-
"""\
* *[Summary]* :: A /library/ Beginning point for development of new ICM oriented libraries.
"""

import typing

csInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Description:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]

**  [[elisp:(org-cycle)][| ]]   Model and Terminology                                      :Overview:
*** concept             -- Desctiption of concept
**      [End-Of-Description]
"""], }

csInfo['moduleUsage'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Usage:* | ]]

**      How-Tos:
**      [End-Of-Usage]
"""

csInfo['moduleStatus'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
** TODO [[elisp:(org-cycle)][| ]]  Current     :: For now it is an ICM. Turn it into ICM-Lib. [[elisp:(org-cycle)][| ]]
**      [End-Of-Status]
"""

"""
*  [[elisp:(org-cycle)][| *ICM-INFO:* |]] :: Author, Copyleft and Version Information
"""
####+BEGIN: bx:cs:py:name :style "fileName"
csInfo['moduleName'] = "csExamples"
####+END:

####+BEGIN: bx:cs:py:version-timestamp :style "date"
csInfo['version'] = "202209052608"
####+END:

####+BEGIN: bx:cs:py:status :status "Production"
csInfo['status']  = "Production"
####+END:

csInfo['credits'] = ""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/csInfo-mbNedaGplByStar.py"
csInfo['authors'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
csInfo['copyright'] = "Copyright 2017, [[http://www.neda.com][Neda Communications, Inc.]]"
csInfo['licenses'] = "[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"
csInfo['maintainers'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
csInfo['contacts'] = "[[http://mohsen.1.banan.byname.net/contact]]"
csInfo['partOf'] = "[[http://www.by-star.net][Libre-Halaal ByStar Digital Ecosystem]]"
####+END:

csInfo['panel'] = "{}-Panel.org".format(csInfo['moduleName'])
csInfo['groupingType'] = "IcmGroupingType-pkged"
csInfo['cmndParts'] = "IcmCmndParts[common] IcmCmndParts[param]"


####+BEGIN: bx:cs:python:top-of-file :partof "bystar" :copyleft "halaal+minimal"
""" #+begin_org
*  This file:/bisos/git/auth/bxRepos/bisos-pip/bpf/py3/bin/csExamples.cs :: [[elisp:(org-cycle)][| ]]
 is part of The Libre-Halaal ByStar Digital Ecosystem. http://www.by-star.net
 *CopyLeft*  This Software is a Libre-Halaal Poly-Existential. See http://www.freeprotocols.org
 A Python Interactively Command Module (PyICM).
 Best Developed With COMEEGA-Emacs And Best Used With Blee-ICM-Players.
 *WARNING*: All edits wityhin Dynamic Blocks may be lost.
#+end_org """
####+END:

####+BEGIN: bx:cs:python:topControls :partof "bystar" :copyleft "halaal+minimal"
""" #+begin_org
*  [[elisp:(org-cycle)][|/Controls/| ]] :: [[elisp:(org-show-subtree)][|=]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
#+end_org """
####+END:
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/pyWorkBench.org"
"""
*  /Python Workbench/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
"""
####+END:

####+BEGIN: bx:cs:python:icmItem :itemType "=Imports=" :itemTitle "*IMPORTS*"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =Imports=  [[elisp:(outline-show-subtree+toggle)][||]] *IMPORTS*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:


# import os
import collections

####+BEGINNOT: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/importUcfIcmBleepG.py"
from bisos import cs
from bisos import io
from bisos import bpf

#G = cs.globalContext.get()

from blee.icmPlayer import bleep
####+END:

import collections

""" #+begin_org

#+BEGIN_SRC emacs-lisp
(setq  b:py:cs:csuList
  (list
   "blee.icmPlayer.bleep"
   "bisos.examples.pattern_csu"
   "bisos.examples.pyRunAs_csu"
   "bisos.examples.io_csu"
   "bisos.examples.parsArgsStdinCmndResult_csu"
   "bisos.examples.subProcOps_csu"
   "bisos.examples.platformConfigs_csu"
 ))
#+END_SRC

#+RESULTS:
| blee.icmPlayer.bleep | bisos.examples.pattern_csu | bisos.examples.pyRunAs_csu | bisos.examples.io_csu | bisos.examples.parsArgsStdinCmndResult_csu | bisos.examples.subProcOps_csu | bisos.examples.platformConfigs_csu |

*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] /csuList emacs-list Specifications/  [[elisp:(blee:org:code-block/above-run)][Eval Above:]] [[elisp:(org-cycle)][| ]]

#+end_org """


####+BEGIN: b:py:cs:framework/csuListProc :pyImports t :csuImports t :csuParams t
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] ~Process CSU List~ with 7 in csuList pyImports=t csuImports=t csuParams=t
#+end_org """

from blee.icmPlayer import bleep
from bisos.examples import pattern_csu
from bisos.examples import pyRunAs_csu
from bisos.examples import io_csu
from bisos.examples import parsArgsStdinCmndResult_csu
from bisos.examples import subProcOps_csu
from bisos.examples import platformConfigs_csu


csuList = [ 'blee.icmPlayer.bleep', 'bisos.examples.pattern_csu', 'bisos.examples.pyRunAs_csu', 'bisos.examples.io_csu', 'bisos.examples.parsArgsStdinCmndResult_csu', 'bisos.examples.subProcOps_csu', 'bisos.examples.platformConfigs_csu', ]

g_importedCmndsModules = cs.csuList_importedModules(csuList)

def g_extraParams():
    csParams = cs.param.CmndParamDict()
    cs.csuList_commonParamsSpecify(csuList, csParams)
    cs.argsparseBasedOnCsParams(csParams)

####+END:

####+BEGINNOT: b:py3:cs:cmnd/classHead :cmndName "examples" :comment "FrameWrk: ICM Examples" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc    [[elisp:(outline-show-subtree+toggle)][||]] <<example>> =FrameWrk: ICM Examples= parsMand= parsOpt= argsMin=0 argsMax=0 asFunc= interactive=  [[elisp:(org-cycle)][| ]]
#+end_org """
class examples(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @io.track.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: bpf.op.Outcome,
    ) -> bpf.op.Outcome:
        cmndOutcome = self.getOpOutcome()
        if rtInv.outs:
            if not self.cmndLineValidate(outcome=cmndOutcome):
                return cmndOutcome

        callParamsDict = {}
        if not cs.cmndCallParamsValidate(callParamsDict, rtInv, outcome=cmndOutcome):
            return cmndOutcome

        """FrameWrk: ICM Examples"""
####+END:
        def cpsInit(): return collections.OrderedDict()
        def menuItem(verbosity): cs.examples.cmndInsert(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
        #def execLineEx(cmndStr): cs.examples.execInsert(execLine=cmndStr)

        #logControler = io.log.Control()
        #logControler.loggerSetLevel(20)

        cs.examples.myName(cs.G.icmMyName(), cs.G.icmMyFullName())

        cs.examples.commonBrief()

        bleep.examples_icmBasic()

        cs.examples.menuChapter('=Misc=  *Facilities*')

        cmndName = "dirCreateExamples" ; cmndArgs = "" ;
        cps=cpsInit() ;
        menuItem(verbosity='little')

        cmndName = "exceptionExamples" ; menuItem(verbosity='little')

        cmndName = "subProcOpsExamples" ; menuItem(verbosity='little')

        pattern_csu.examples_csu(sectionTitle="default")

        pyRunAs_csu.examples_csu(sectionTitle="default")

        io_csu.examples_csu(sectionTitle="default")

        parsArgsStdinCmndResult_csu.examples_csu(sectionTitle="default")

        subProcOps_csu.examples_csu(sectionTitle="default")

        platformConfigs_csu.examples_csu(sectionTitle="default")

        cs.examples.menuChapter('=Tests=  *All Examples As Tests*')
        cmndName = "allExamplesAsTests" ; menuItem(verbosity='none')

        return(cmndOutcome)



####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "examplesOld" :comment "FrameWrk: ICM Examples" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<examplesOld>> =FrameWrk: ICM Examples=parsMand= parsOpt= argsMin=0 argsMax=0 pyInv=
#+end_org """
class examplesOld(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @io.track.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: bpf.op.Outcome,
    ) -> bpf.op.Outcome:
        """FrameWrk: ICM Examples"""
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return io.eh.badOutcome(cmndOutcome)
####+END:
        def cpsInit(): return collections.OrderedDict()
        def menuItem(verbosity): cs.examples.cmndInsert(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
        #def execLineEx(cmndStr): cs.examples.execInsert(execLine=cmndStr)

        #logControler = io.log.Control()
        #logControler.loggerSetLevel(20)

        cs.examples.myName(cs.G.icmMyName(), cs.G.icmMyFullName())

        cs.examples.commonBrief()

        bleep.examples_icmBasic()


        cs.examples.menuChapter('=Misc=  *Facilities*')

        cmndName = "dirCreateExamples" ; cmndArgs = "" ;
        cps=cpsInit() ;
        menuItem(verbosity='little')

        cmndName = "exceptionExamples" ; menuItem(verbosity='little')

        cmndName = "subProcOpsExamples" ; menuItem(verbosity='little')

        pattern_csu.examples_csu(sectionTitle="default")

        pyRunAs_csu.examples_csu(sectionTitle="default")

        io_csu.examples_csu(sectionTitle="default")

        parsArgsStdinCmndResult_csu.examples_csu(sectionTitle="default")

        subProcOps_csu.examples_csu(sectionTitle="default")

        platformConfigs_csu.examples_csu(sectionTitle="default")

        cs.examples.menuChapter('=Tests=  *All Examples As Tests*')
        cmndName = "allExamplesAsTests" ; menuItem(verbosity='none')

        return(cmndOutcome)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "dirCreateExamples" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<dirCreateExamples>>parsMand= parsOpt= argsMin=0 argsMax=0 pyInv=
#+end_org """
class dirCreateExamples(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @io.track.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: bpf.op.Outcome,
    ) -> bpf.op.Outcome:

        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return io.eh.badOutcome(cmndOutcome)
####+END:
        docStr = """
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]] Various examples for creation of directories.
- examples and smoke unit test for file: ../bisos/bpf/dir.py
        """
        if self.docStrClassSet(docStr,): return cmndOutcome

        bpf.dir.createIfNotThere("/tmp/t1")

        return cmndOutcome



####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "exceptionExamples" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<exceptionExamples>>parsMand= parsOpt= argsMin=0 argsMax=0 pyInv=
#+end_org """
class exceptionExamples(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @io.track.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: bpf.op.Outcome,
    ) -> bpf.op.Outcome:

        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return io.eh.badOutcome(cmndOutcome)
####+END:

        bpf.exception.terminate("PREV-Term", "NEXT-Term", "Some Termination Message")

        # terminate, terminates. So, below is unreachable.
        #

        try:
            raise bpf.exception.TransitionError("PREV", "NEXT", "Some Message")
        except bpf.exception.TransitionError as inst:
            print(inst)

        return cmndOutcome



####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "allExamplesAsTests" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<allExamplesAsTests>>parsMand= parsOpt= argsMin=0 argsMax=0 pyInv=
#+end_org """
class allExamplesAsTests(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @io.track.subjectToTracking(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: bpf.op.Outcome,
    ) -> bpf.op.Outcome:

        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return io.eh.badOutcome(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org \
** [[elisp:(org-cycle)][| *CmndDesc:* | ]] This is an example of a CmndSvc with lots of features.
        #+end_org """)

        myName = cs.G.icmMyName()

        verbosity = " -v 20 "

        if bpf.subProc.WOpW(invedBy=self, log=1).bash(
                f"""{myName}  {verbosity} -i sameInstanceEx""",
        ).isProblematic():  return(io.eh.badOutcome(cmndOutcome))

        if bpf.subProc.WOpW(invedBy=self, log=1).bash(
                f"""{myName}  {verbosity} -i runAsUser""",
        ).isProblematic():  return(io.eh.badOutcome(cmndOutcome))

        if bpf.subProc.WOpW(invedBy=self, log=1).bash(
                f"""{myName}  {verbosity} -i outStreamsExamples""",
        ).isProblematic():  return(io.eh.badOutcome(cmndOutcome))

        # if bpf.subProc.WOpW(invedBy=self, log=1).bash(
        #         f"""{myName}  {verbosity} -i subProcOpsWithArgs echo this and that""",
        # ).isProblematic():  return(io.eh.badOutcome(cmndOutcome))

        if bpf.subProc.WOpW(invedBy=self, log=1).bash(
                f"""{myName}  {verbosity} --par1Example="par1Mantory" --par2Example="par2Optional" -i parsArgsStdinCmndResult""",
        ).isProblematic():  return(io.eh.badOutcome(cmndOutcome))

        if bpf.subProc.WOpW(invedBy=self, log=1).bash(
                f"""{myName}  {verbosity} -i pyCmndInvOf_parsArgsStdinCmndResult""",
        ).isProblematic():  return(io.eh.badOutcome(cmndOutcome))

        return cmndOutcome


####+BEGIN: b:py3:cs:framework/main :csInfo "csInfo" :noCmndEntry "examples" :extraParamsHook "g_extraParams" :importedCmndsModules "g_importedCmndsModules"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] ~g_icmMain~ (csInfo, _examples_, g_extraParams, g_importedCmndsModules)
#+end_org """

if __name__ == '__main__':
    cs.main.g_csMain(
        csInfo=csInfo,
        noCmndEntry=examples,  # specify a Cmnd name
        extraParamsHook=g_extraParams,
        importedCmndsModules=g_importedCmndsModules,
    )

####+END:

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
