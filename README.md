# saltstack-circusctl
saltstack execution module for circusctl 

Instructions:
1 - vagrant up
2 - vagrant ssh master
3 - salt * state.highstate
4 - salt minion1 cmd.exec_code bash 'initctl reload-configuration'
