import numpy as np
import matplotlib.pyplot as plt
import simpleaudio as sa
import time

# Parameters
width, height = 50, 50
num_nodes = 1
max_nodes = 200

# Initialize the network
nodes = [(width // 2, height // 2)]
connections = []

# Generate network
while len(nodes) < max_nodes:
    parent = nodes[np.random.randint(len(nodes))]
    angle = np.random.uniform(0, 2 * np.pi)
    distance = np.random.uniform(1, 3)
    new_node = (int(parent[0] + np.cos(angle) * distance), int(parent[1] + np.sin(angle) * distance))
    
    if 0 <= new_node[0] < width and 0 <= new_node[1] < height:
        nodes.append(new_node)
        connections.append((parent, new_node))

# Mapping node positions to musical notes
min_pitch, max_pitch = 40, 80
min_duration, max_duration = 0.1, 0.5

# Play music as network grows
wave_objects = []
for i, (start, end) in enumerate(connections):
    x, y = end
    pitch = min_pitch + int((y / height) * (max_pitch - min_pitch))
    duration = min_duration + (x / width) * (max_duration - min_duration)

    # Generate sound wave (sine wave)
    frequency = 440.0 * 2 ** ((pitch - 69) / 12.0)
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    audio = (wave * 32767).astype(np.int16)
    wave_objects.append(audio)

# Concatenate and play all sounds
final_wave = np.concatenate(wave_objects)
play_obj = sa.play_buffer(final_wave, 1, 2, sample_rate)

# Visualize network growth
plt.figure()
for (p1, p2) in connections:
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], c='purple')
plt.scatter([n[0] for n in nodes], [n[1] for n in nodes], c='black', s=10)
plt.xlim(0, width)
plt.ylim(0, height)
plt.show()

play_obj.wait_done()
