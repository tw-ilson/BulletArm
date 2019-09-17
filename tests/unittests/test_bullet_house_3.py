import unittest
import time
import numpy as np

from helping_hands_rl_envs.envs.house_building_3_env import createHouseBuilding3Env
from helping_hands_rl_envs.envs.pybullet_env import PyBulletEnv

class TestBulletHouse3(unittest.TestCase):
  workspace = np.asarray([[0.35, 0.65],
                          [-0.15, 0.15],
                          [0, 0.50]])
  env_config = {'workspace': workspace, 'max_steps': 1000, 'obs_size': 90, 'render': False, 'fast_mode': True,
                'seed': 0, 'action_sequence': 'pxyr', 'num_objects': 3, 'random_orientation': True,
                'reward_type': 'step_left', 'simulate_grasp': True, 'perfect_grasp': False, 'robot': 'kuka'}


  def testPlanner(self):
    env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
    states, obs = env.reset()
    for i in range(5, -1, -1):
      action = env.getPlan()
      (states_, obs_), rewards, dones = env.step(np.array(action))
      self.assertEqual(rewards, i)


  # def testPlanner2(self):
  #   self.env_config['render'] = True
  #   self.env_config['reward_type'] = 'sparse'
  #   env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
  #   total = 0
  #   s = 0
  #   for i in range(100):
  #     states, obs = env.reset()
  #     for _ in range(10):
  #       action = env.getPlan()
  #       (states_, obs_), rewards, dones = env.step(np.array(action))
  #       if dones:
  #         break
  #     s += int(rewards)
  #     total += 1
  #     print('{}/{}'.format(s, total))

  def testBlockNotValidTriangleOnBrick(self):
    self.env_config['random_orientation'] = False

    env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
    states, obs = env.reset()

    env.saveState()
    position = list(env.getObjectPosition())
    action = [0, position[2][0], position[2][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = [1, position[3][0], position[3][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 8)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 6)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 4)
    env.restoreState()

  def testBlockNotValidBrickOrRoofOnBlock(self):
    self.env_config['random_orientation'] = False

    env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
    states, obs = env.reset()

    env.saveState()
    position = list(env.getObjectPosition())
    action = [0, position[3][0], position[3][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = [1, position[0][0], position[0][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 8)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 6)
    env.restoreState()

    position = list(env.getObjectPosition())
    action = [0, position[2][0], position[2][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = [1, position[0][0], position[0][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 8)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 6)

  def testBlockNotValidRoofOnBrickOnBlock(self):
    self.env_config['random_orientation'] = False

    env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
    states, obs = env.reset()

    env.saveState()
    position = list(env.getObjectPosition())
    action = [0, position[3][0], position[3][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = [1, position[0][0], position[0][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 8)

    position = list(env.getObjectPosition())
    action = [0, position[2][0], position[2][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 9)

    action = [1, position[0][0], position[0][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 10)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 9)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 8)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 7)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 6)

  def testBlockValidTriangleOnBrick(self):
    self.env_config['random_orientation'] = False

    env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
    states, obs = env.reset()

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 4)

    position = list(env.getObjectPosition())
    action = [0, position[2][0], position[2][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = [1, position[3][0], position[3][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 6)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 4)

  def testBlockValidBrickOrRoofOnBlock(self):
    self.env_config['random_orientation'] = False

    env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
    states, obs = env.reset()

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 4)

    env.saveState()
    position = list(env.getObjectPosition())
    action = [0, position[3][0], position[3][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 3)

    action = [1, position[0][0], position[0][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 4)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 3)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 2)
    env.restoreState()

    position = list(env.getObjectPosition())
    action = [0, position[2][0], position[2][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = [1, position[0][0], position[0][1], np.pi / 2]
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 6)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 4)

  def testSuccess(self):
    self.env_config['random_orientation'] = False

    env = createHouseBuilding3Env(PyBulletEnv, self.env_config)()
    states, obs = env.reset()

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 5)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 4)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 3)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 2)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 1)

    action = env.getPlan()
    (states_, obs_), rewards, dones = env.step(np.array(action))
    self.assertEqual(rewards, 0)
