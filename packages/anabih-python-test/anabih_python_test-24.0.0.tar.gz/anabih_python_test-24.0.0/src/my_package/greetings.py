
class Greetings:
    def say_hi(self):
        junit_xml = """<?xml version="1.0" encoding="utf-8"?>
            <testsuites time="5.548">
               <testsuite errors="0" failures="0" name="test suite #1" skipped="0" tests="1" time="0.342">
                  <testcase classname="s1 classname test case #1" name="name test case #1" time="0.143">
                      <error message="s1 test case #1 Error #1"/>
                      <failure message="s1 test case #1 Failure #2"/>                      
                  </testcase>
                  <testcase classname="s1 classname test case #2" name="name test case #2" time="0.143">
                      <error message="s1 Error #1"/>
                      <failure message="s1 Failure #2"/>                      
                  </testcase>                  
               </testsuite>
               <testsuite errors="0" failures="0" name="test suite #2" skipped="0" tests="1" time="0.342">
                  <testcase classname="s2 classname test case #1" name="name test case #1" time="0.143">
                      <error message="s2 test case #1 Error #1"/>
                      <failure message="s2 test case #1 Failure #2"/>                      
                  </testcase>
                  <testcase classname="s2 classname test case #2" name="name test case #2" time="0.143">
                      <error message="s2 Error #1"/>
                      <failure message="s2 Failure #2"/>                      
                  </testcase>                  
               </testsuite>              
            </testsuites>
        """
        print(junit_xml)

        f = open("junit-output.xml", "w")
        f.write(junit_xml)
        f.close()
