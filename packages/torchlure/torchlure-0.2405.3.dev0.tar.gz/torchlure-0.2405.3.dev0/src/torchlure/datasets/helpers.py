import asyncio
import time

import gymnasium as gym
import minari

from .minari_ext import AsyncDataCollector, D4RLDataset


async def collect_episode(env, policy=None):
    """Collect a single episode using the specified environment and policy."""
    env.reset()
    done = False
    while not done:
        action = env.action_space.sample() if policy is None else policy()
        obs, rew, terminated, truncated, info = env.step(action)
        done = terminated or truncated


async def worker(env, queue, policy, start_time, print_every, total_episodes):
    collected = 0
    while True:
        episode_idx = await queue.get()
        if episode_idx is None:
            break
        await collect_episode(env, policy)
        collected += 1

        # Calculate and print ETA
        if collected % print_every == 0:
            elapsed_time = time.time() - start_time
            episodes_done = episode_idx + 1
            episodes_left = total_episodes - episodes_done
            eta = (
                (elapsed_time / episodes_done) * episodes_left
                if episodes_done > 0
                else float("inf")
            )
            eta_minutes, eta_seconds = divmod(eta, 60)
            print(
                f"Collected {episodes_done} episodes. ETA: {int(eta_minutes)}m {int(eta_seconds)}s"
            )


async def collect_samples_async(
    env_id, num_episodes, dataset_id, policy=None, num_envs=4, print_every=1000
):
    """Collect samples asynchronously using multiple environments."""
    start_time = time.time()

    # Initialize environments
    envs = [
        AsyncDataCollector(gym.make(env_id), record_infos=True) for _ in range(num_envs)
    ]

    # Create a queue for managing episode collection
    queue = asyncio.Queue()

    # Enqueue episode indices
    for i in range(num_episodes):
        queue.put_nowait(i)

    # Add termination signals to the queue for each worker
    for _ in range(num_envs):
        queue.put_nowait(None)

    # Start workers
    tasks = [
        worker(env, queue, policy, start_time, print_every, num_episodes)
        for env in envs
    ]
    await asyncio.gather(*tasks)

    # Create the dataset using the first environment
    dataset = envs[0].create_dataset(dataset_id)

    # Add data from other environments to the dataset
    for i, env in enumerate(envs[1:], start=2):
        try:
            env.add_to_dataset(dataset)
        except Exception as e:
            print(f"Error adding data from environment {i}: {e}")

    # Close all environments
    for env in envs:
        env.close()

    # Print total time taken
    total_time = time.time() - start_time
    total_minutes, total_seconds = divmod(total_time, 60)
    print(f"Total time taken: {int(total_minutes)}m {int(total_seconds)}s")

    return dataset
