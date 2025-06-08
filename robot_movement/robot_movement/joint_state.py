import math
import numpy as np


class JointStateClass():
    joint_names = ["l_limb_1_to_base_link",
                    "l_limb_2_to_limb_1",
                    "l_limb_3_to_limb_2",
                    "l_limb_4_to_limb_3",
                    "l_limb_5_to_limb_4",
                    "r_limb_1_to_base_link",
                    "r_limb_2_to_limb_1",
                    "r_limb_3_to_limb_2",
                    "r_limb_4_to_limb_3",
                    "r_limb_5_to_limb_4"]
    joint_positions = []
    previous_joint_positions = []
    def __init__(self) -> None:
        pass

    def update_joint_positions(self, degrees):
        self.joint_positions = []
        for i in degrees:
            self.joint_positions.append(math.radians(i-90))

        self.previous_joint_positions = self.joint_positions
        return self.joint_positions
    
    def configure_to_robot_mk1(self, to_convert):
        pass
        
# c = JointStateClass()
# msg = c.update_joint_positions([90,177,40,90,50,
#                                 100,15,115,70,110])
# print(msg)

radian_list = np.array(
              [0.00,
               0.01,
               0.790,
               -1.027,
               0.484,
               0.00,
               0.01,
               0.790,
               -1.027,
               -0.450])


def map_range(value, input_min, input_max, output_min, output_max):
    return (value - input_min) * (output_max - output_min) / (input_max - input_min) + output_min

radian_list_remapped = []
for i in radian_list:
    a = round(math.degrees(i),2)
    radian_list_remapped.append(round(map_range(a, -90, 90, 0, 180),2))

print (radian_list_remapped)


transform_to_motors = np.array([[1,0,0,0,0,0,0,0,0,0],
                                  [0,-1,0,0,0,0,0,0,0,0],
                                  [0,0,1,0,0,0,0,0,0,0],
                                  [0,0,0,-1,0,0,0,0,0,0],
                                  [0,0,0,0,1,0,0,0,0,0],
                                  [0,0,0,0,0,-1,0,0,0,0],
                                  [0,0,0,0,0,0,1,0,0,0],
                                  [0,0,0,0,0,0,0,-1,0,0],
                                  [0,0,0,0,0,0,0,0,-1,0],
                                  [0,0,0,0,0,0,0,0,0,1]])

radian_transformed = np.matmul(radian_list,transform_to_motors)
degree_list = []
for i in radian_transformed:
    degree_list.append((round(math.degrees(i),2) % 180))


# print(degree_list)