################################################################################
# oops/hosts/juno/junocam/gold_master.py: Backplane gold master tester for
# JunoCam
################################################################################
import oops.backplane.gold_master as gm
from oops.hosts.juno.junocam import standard_obs

if __name__ == '__main__':
    gm.execute_as_command()

################################################################################
