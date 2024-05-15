#!/bin/bash

####+BEGIN: bx:dblock:bash:top-of-file :vc "cvs" partof: "bystar" :copyleft "halaal+minimal"

####+END:

####+BEGIN: bx:dblock:lsip:bash:seed-spec :types "seedBleePanelProc.sh"
SEED="
*  /[dblock]/ /Seed/ :: [[file:/opt/public/osmt/bin/seedBleePanelProc.sh]] | 
"
FILE="
*  /This File/ :: /bisos/panels/bisos-model/fileTreeObject-FTO/bleePanelProc.sh 
"
if [ "${loadFiles}" == "" ] ; then
    /opt/public/osmt/bin/seedBleePanelProc.sh -l $0 "$@" 
    exit $?
fi
####+END:



_CommentBegin_
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Cmnd       ::  examplesHookPostExample    [[elisp:(org-cycle)][| ]]
_CommentEnd_

function examplesHookPost {
    cat  << _EOF_
$( examplesSeperatorTopLabel "EXTENSION EXAMPLES" )
_EOF_

    # templatesEvolution
    
    return
}



function templatesEvolution {
    cat  << _EOF_
$( examplesSeperatorSection "ftoProc.sh -- Templates Evolution" )
diff ./ftoProc.sh  /libre/ByStar/InitialTemplates/update/fto/start/commonProc/anyFtoItem/ftoProcNode.sh
cp ./ftoProc.sh  /libre/ByStar/InitialTemplates/update/fto/start/commonProc/anyFtoItem/ftoProcNode.sh
cp /libre/ByStar/InitialTemplates/update/fto/start/commonProc/anyFtoItem/ftoProcNode.sh ./ftoProc.sh  
$( examplesSeperatorSection "commonPanel.org -- Templates Evolution" )
diff ./Panel.org  /libre/ByStar/InitialTemplates/start/fto/commonProc/anyFtoItem/mainPanel.org
cp ./Panel.org /libre/ByStar/InitialTemplates/start/fto/commonProc/anyFtoItem/mainPanel.org
cp /libre/ByStar/InitialTemplates/start/fto/commonProc/anyFtoItem/mainPanel.org ./Panel.org
_EOF_
 return
}



####+BEGIN: bx:dblock:bash:end-of-file :types ""
_CommentBegin_
*  [[elisp:(org-cycle)][| ]]  Common        ::  /[dblock] -- End-Of-File Controls/ [[elisp:(org-cycle)][| ]]
_CommentEnd_
#+STARTUP: showall
#local variables:
#major-mode: sh-mode
#fill-column: 90
# end:
####+END:
