import numpy as np
import matplotlib.pyplot as plt   

x = np.arange(1,53)/10

mean_reward_list = []
for i in range(1,53):
	filename = "reward/Compo4_p1.5_PPOsb1.4_nsteps512_dump{:04d}.npy".format(int(i))
	r = np.load(filename)
	mean_reward = np.mean(r)
	print(f"reward:{mean_reward}")
	mean_reward_list.append(mean_reward)
 
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, mean_reward_list, lw=2, color = 'darkslateblue', marker = 'o')
ax.set_xlabel("million steps")
ax.set_ylabel("Reward of PPO")
plt.title('Reward over every 100k timesteps')
plt.savefig('RewardPPO_test.png')