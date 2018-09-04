#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import random

#define state Walk
class Walk (smach.State):
	def __init__(self):
		smach.State.__init__(self,
							outcomes = ['keep_walking', 'bus_is_near', 'go_home', 'hungry'],
							input_keys = ['time_in'],
							output_keys = ['time_out'])
	
	def execute(self, userdata):
		rospy.loginfo('time : %0f' %userdata.time_in)
		rospy.loginfo('Irmak is walking around')
		if userdata.time_in > 15:

			if userdata.time_in % 3 == 0:
				rospy.loginfo('Irmak got on a bus')
				userdata.time_out = userdata.time_in + 3
				return 'bus_is_near'

			else:
				rospy.loginfo ('Irmak is going home by walking')
				userdata.time_out = userdata.time_in + 4
				return 'go_home'

		elif userdata.time_in > 5:
			rospy.loginfo('Irmak got hungry and she is going to McDonalds by walking')
			userdata.time_out = userdata.time_in + 3
			return 'hungry'

		else:
			userdata.time_out = userdata.time_in + 2
			return 'keep_walking'

#define state Bus
class Bus(smach.State):
	def __init__(self):
		smach.State.__init__(self,
							outcomes = ['go_home', 'hungry'],
							input_keys = ['time_in'],
							output_keys = ['time_out'])
		self.is_hungry = random.randint(0,5)

	def execute(self, userdata):
		rospy.loginfo('time : %f' %userdata.time_in)
		rospy.loginfo('Irmak is in the bus')
		
		if self.is_hungry == 4 | self.is_hungry == 5:
			userdata.time_out = userdata.time_in + 2
			rospy.loginfo('Irmak got hungry and she is going to McDonalds by bus')
			return 'hungry'
		else:
			userdata.time_out = userdata.time_in + 3
			rospy.loginfo('Irmak is going home with bus')
			return 'go_home'

#define state Eating
class Eat(smach.State):
	def __init__ (self):
		smach.State.__init__(self,
							outcomes = ['full'],
							input_keys = ['time_in'],
							output_keys = ['time_out'])

	def execute(self, userdata):
		rospy.loginfo('time : %f' %userdata.time_in)
		rospy.loginfo('Irmak ate and she is full')
		userdata.time_out = userdata.time_in + 3
		return 'full'

def main():
	rospy.init_node('irmak_fsm_example_1')

	sm = smach.StateMachine(outcomes = ['at_home'])
	sm.userdata.time = 0;

	with sm:

		smach.StateMachine.add('WALK', Walk(),
								transitions = {'keep_walking':'WALK',
												'bus_is_near':'BUS',
												'go_home':'at_home',
												'hungry':'EAT',},
								remapping = {'time_in':'time',
											'time_out':'time'})
		smach.StateMachine.add('BUS', Bus(),
								transitions = {'go_home':'at_home',
												'hungry':'EAT'},
								remapping = {'time_in':'time',
											'time_out':'time'})
		smach.StateMachine.add('EAT', Eat(),
								transitions = {'full':'WALK'},
								remapping = {'time_in':'time',
											'time_out':'time'})


		sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
		sis.start()

		outcomes = sm.execute()

		rospy.spin()
		sis.stop()

if __name__ == '__main__':
	main()
