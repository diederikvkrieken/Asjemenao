import basebehavior.behaviorimplementation

import time
import almath

class ApproachBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        self.idling = False

        self.nao = self.body.nao(0)
        self.nao.set_cam_vars()
        self.nao.say("Approach the ball, we shall")

        self.last_ball_recogtime = 0
        self.ball_last_seen = time.time()

        self.is_looking_horizontal = True


    def implementation_update(self):
        if self.idling:
            return

        # If the ball is seen but not close enough, just walk towards it:
        if (self.m.n_occurs("combined_red") > 0):
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_ball_recogtime:
                detectionlist = obs['sorted_contours']
                max_blob = detectionlist[0]
                print "red: x=%d, y=%d, size=%f" % (max_blob['x'], max_blob['y'], max_blob['surface'])
                self.last_ball_recogtime = recogtime
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if max_blob['surface'] > 50:
                    print "Ik zie de bal"
                    self.ball_last_seen = time.time()
                    #Is the ball in the correct location?:
                    if max_blob['y'] > 75 and max_blob['x'] > 60 and max_blob['x'] < 100 and not self.is_looking_horizontal:
                        # If the ball is seen close enough, use self.m.add_item('ball_approached',time.time(),{}) to finish this behavior.
                        self.m.add_item('ball_approached', time.time(),{}) 
                        print "Ik ben dicht genoeg bij de bal."
                        return
                    if not self.nao.isWalking():
                        #Make sure that the ball is in the center of the camera:
                        if max_blob['x'] < 60:
                            self.nao.walkNav(0, 0, 0.1)
                            pass
                        elif max_blob['x'] > 100:
                            self.nao.walkNav(0, 0, -0.1)
                            pass
                    if not self.nao.isWalking():
                        #Walk a bit if the ball is not really close:
                        if max_blob['y'] < 80:
                            self.nao.walkNav(0.05, 0, 0)
                            pass
                        elif self.is_looking_horizontal:
                            self.nao.look_down()
                            self.is_looking_horizontal = False
        
        # Timeout after 10 seconds if the ball is not seen anymore:
        if (time.time() - self.ball_last_seen) > 10:
            self.nao.say("To the dark side, the ball is!")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            self.idling = True
