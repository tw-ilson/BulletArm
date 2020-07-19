import time
import pybullet as pb
from copy import deepcopy
import numpy.random as npr
import numpy as np
from itertools import combinations
from helping_hands_rl_envs.envs.pybullet_tilt_deconstruct_env import PyBulletEnv, PyBulletTiltDeconstructEnv
from helping_hands_rl_envs.simulators import constants


def createTiltImproviseHouseBuilding5DeconstructEnv(simulator_base_env, config):
  class TiltImproviseHouseBuilding5DeconstructEnv(PyBulletTiltDeconstructEnv):
    ''''''
    def __init__(self, config):
      if simulator_base_env is PyBulletEnv:
        super().__init__(config)
      else:
        raise ValueError('Bad simulator base env specified.')
      self.simulator_base_env = simulator_base_env
      self.random_orientation = config['random_orientation'] if 'random_orientation' in config else False
      self.num_obj = config['num_objects'] if 'num_objects' in config else 1
      self.reward_type = config['reward_type'] if 'reward_type' in config else 'sparse'
      self.tilt_min_dist = 0.04

      pb.setPhysicsEngineParameter(numSubSteps=0, numSolverIterations=200, solverResidualThreshold=1e-7,
                                   constraintSolverType=pb.CONSTRAINT_SOLVER_LCP_SI)

    def step(self, action):
      reward = 1.0 if self.checkStructure() else 0.0
      self.takeAction(action)
      self.wait(100)
      obs = self._getObservation(action)
      motion_primative, x, y, z, rot = self._decodeAction(action)
      done = motion_primative and self._checkTermination()

      if not done:
        done = self.current_episode_steps >= self.max_steps or not self.isSimValid()
      self.current_episode_steps += 1

      return obs, reward, done

    def reset(self):
      ''''''
      super(TiltImproviseHouseBuilding5DeconstructEnv, self).reset()
      self.generateImproviseH5()

      while not self.checkStructure():
        super(TiltImproviseHouseBuilding5DeconstructEnv, self).reset()
        self.generateImproviseH5()

      return self._getObservation()

    def _checkTermination(self):
      if self.current_episode_steps < 8:
        return False
      obj_combs = combinations(self.objects, 2)
      for (obj1, obj2) in obj_combs:
        dist = np.linalg.norm(np.array(obj1.getXYPosition()) - np.array(obj2.getXYPosition()))
        if dist < 2.2*self.min_block_size:
          return False
      return True

    def checkStructure(self):
      rand_objs = list(filter(lambda x: self.object_types[x] == constants.RANDOM, self.objects))
      roofs = list(filter(lambda x: self.object_types[x] == constants.ROOF, self.objects))
      if roofs[0].getZPosition() <  2.1 * self.min_block_size:
        return False

      rand_obj_combs = combinations(rand_objs, 2)
      for (obj1, obj2) in rand_obj_combs:
        if self._checkOnTop(obj1, roofs[0]) and self._checkOnTop(obj2, roofs[0]) and self.isPosOffTilt(obj1.getXYPosition()) and self.isPosOffTilt(obj2.getXYPosition()):
          return True
      return False

  def _thunk():
    return TiltImproviseHouseBuilding5DeconstructEnv(config)

  return _thunk
