"""
https://matplotlib.org/stable/_downloads/81bc179821dc9808604c256bcb20b3b0/packed_bubbles.py
significantly modified by takefuji
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import subprocess as sp
from pathlib import Path
import sys,os
size=10
L=len(sys.argv)
if L==1:
 file='/var/log/auth.log'
 command="grep Failed /var/log/auth.log|awk -F 'from' '{print $2}'|cut -d ' ' -f 2|sort|uniq -c|sort -nr >IPs"
elif L==2:
 file=Path(sys.argv[1])
 if file.is_file() and os.access(file, os.R_OK):
  command="grep Failed "+str(file)+"|awk -F 'from' '{print $2}'|cut -d ' ' -f 2|sort|uniq -c|sort -nr >IPs"
sp.call(command,shell=True)
d=pd.read_csv('IPs',delim_whitespace=True,header=None)
d.columns=['no','ip']
print(d)
d=d[0:size]
d['name']=d['ip'].astype(str)
for i in range(size):
 command="curl -s -0 ipinfo.io/"+str(d.ip[i])+"|grep country|cut -d \'\"\' -f 4"
 cname=sp.check_output(command,shell=True)
 d.loc[i,'name']=cname.strip().decode('utf-8')+':'+str(d.ip[i])
d.to_csv('r.csv')
d=pd.read_csv('r.csv')

class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)
        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2
        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]
        self.com = self.center_of_mass()
    def center_of_mass(self):
        return np.average(
            self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
        )
    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0],
                        bubble[1] - bubbles[:, 1])
    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - \
            bubbles[:, 2] - self.bubble_spacing
    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])
    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        idx_min = np.argmin(distance)
        return idx_min if type(idx_min) == np.ndarray else [idx_min]
    def collapse(self, n_iterations=50):
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                dir_vec = self.com - self.bubbles[i, :2]

                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        # calculate direction vector
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        # calculate orthogonal vector
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        # test which direction to go
                        new_point1 = (self.bubbles[i, :2] + orth *
                                      self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth *
                                      self.step_dist)
                        dist1 = self.center_distance(
                            self.com, np.array([new_point1]))
                        dist2 = self.center_distance(
                            self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels):
        for i in range(len(self.bubbles)):
            circ = plt.Circle(
                self.bubbles[i, :2], self.bubbles[i, 2])
            ax.add_patch(circ)
            ax.text(*self.bubbles[i, :2], labels[i],
                    horizontalalignment='center', verticalalignment='center')

def main():
 bubble_chart = BubbleChart(area=d['no'],
                           bubble_spacing=0.1)
 bubble_chart.collapse()
 fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
 bubble_chart.plot(
    ax, d['name'])
 ax.axis("off")
 ax.relim()
 ax.autoscale_view()
 ax.set_title('ssh-attacks from malicious IPs')
 plt.savefig('r.png')
 plt.show()
main()
