import gym
import numpy as np
import torch
from dqn_agent_atari import AtariDQNAgent

from gym.wrappers import AtariPreprocessing, FrameStack

def test_agent(agent, env_id, model_path, episodes=5):
    # 建立和訓練時相同的觀測處理方式
    env = gym.make(env_id, render_mode='human')
    env = AtariPreprocessing(env, screen_size=84, grayscale_obs=True, frame_skip=1)
    env = FrameStack(env, 4)

    total_rewards = []
    
    # 載入訓練好的模型
    agent.behavior_net.load_state_dict(torch.load(model_path, map_location=agent.device))
    agent.behavior_net.eval()

    
    for episode in range(episodes):
        state, _ = env.reset()
        done = False
        episode_reward = 0
        while not done:
            # 使用代理選擇動作（eval_mode=True 使用低 epsilon）
            action = agent.decide_agent_actions(state, epsilon=0.0)
            next_state, reward, done, truncated, _ = env.step(action)
            episode_reward += reward
            state = next_state
            if done or truncated:
                break
        total_rewards.append(episode_reward)
        print(f"Episode {episode + 1}: Reward = {episode_reward}")
    
    env.close()
    print(f"Average Reward over {episodes} episodes: {np.mean(total_rewards):.2f}")

if __name__ == '__main__':
    # 使用與訓練時相同的配置
    config = {
        "gpu": True,
        "training_steps": 1e8,
        "gamma": 0.99,
        "batch_size": 32,
        "eps_min": 0.1,
        "warmup_steps": 20000,
        "eps_decay": 1000000,
        "eval_epsilon": 0.01,
        "replay_buffer_capacity": 100000,
        "logdir": 'log/DQN/',
        "update_freq": 4,
        "update_target_freq": 10000,
        "learning_rate": 0.0000625,
        "eval_interval": 100,
        "eval_episode": 5,
        "env_id": 'ALE/MsPacman-v5',
    }
    
    # 初始化代理
    agent = AtariDQNAgent(config)
    
    # 載入模型並運行測試
    model_path = './Dueling_model.pth'
    # model_9864699_2682 best?
    test_agent(agent, config['env_id'], model_path)