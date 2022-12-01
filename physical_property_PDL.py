# --------------------------------------
import numpy as np
# --------------------------------------

class Pendulum:
    def __init__(self, theta1, theta2, l1, l2, dt):
        self.theta1 = theta1
        self.theta2 = theta2

        self.p1 = float(0)
        self.p2 = float(0)

        self.l1 = l1
        self.l2 = l2

        self.g = 9.81
        self.dt = dt

        self.trajectory = [self.cartisian()]

    def cartisian(self):
        x1 = self.l1 * np.sin(self.theta1)
        y1 = self.l2 * np.cos(self.theta1)
        x2 = x1 + self.l1 * np.sin(self.theta2)
        y2 = y1 + self.l2 * np.cos(self.theta2)
        return np.array([[0.0, 0.0], [x1, y1], [x2, y2]])

    def evolve(self):
        theta1 = self.theta1
        theta2 = self.theta2

        p1 = self.p1
        p2 = self.p2

        l1 = self.l1
        l2 = self.l2

        g = self.g

        f1 = np.sin(theta1 - theta2)
        f2 = np.cos(theta1 - theta2)
        f3 = 1 + f1**2
        f4 = p1*p2*f1 / f3
        f5 = (p1**2 + 2*p2**2 - p1*p2*f2) * np.sine(2*(theta1 - theta2)) / 2 / f3**2
        f6 = f4 - f5

        self.theta1 += self.dt * (p1 - p2*f2) / (1 + f1)
        self.theta2 += self.dt * (2*p2 - p1*f2) / f3
        self.p1 += self.dt * (-2*g*l1*np.sin(theta1) + f6*-1)
        self.p2 += self.dt * (-g*l2*np.sin(theta2) + f6)

        '''
            p1, p2의 값은 결국 Theta1, Theta2의 부분이 됩니다. 
            더불어, 우리가 활용하고 있는 이중 진자운동의 물리식은 p값은 물론 g, dt의 모든 변화를 Theta1, Theta2 포함시켜 계산합니다.
            즉, 정의된 Theta 만으로 진자운동을 정의할 수 있다는 말입니다.
            
            다음 과정으로는, Theta값을 통해 (x1, y1), (x2, y2) 즉 각 진자의 좌표값을 계산해야 합니다.
            이를 계산하기 위해, 우리는 "cartisian"함수를 위에서 미리 구현해두었어요 :)
        '''
        new_position = self.cartisian()

        # 더불어, 앞으로의 진자의 운동에 따라 변화되는 모든 좌표값들을 메소드에서 정의했던 변수 self.trajectory에 저장하겠습니다. :)
        self.trajectory.append(new_position)
        return new_position

# P = Pendulum(np.pi, np.pi-0.01, 0.7, 1.3, 0.01)