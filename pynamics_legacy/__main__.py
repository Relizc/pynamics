from launcher import LaunchEnv, launch

import sys
env = LaunchEnv(sys.argv)

launch(env.path, env.vars)



