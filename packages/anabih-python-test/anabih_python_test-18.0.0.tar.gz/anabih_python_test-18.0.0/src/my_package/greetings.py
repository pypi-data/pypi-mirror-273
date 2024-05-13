
class Greetings:
    def say_hi(self):
        junit_xml = """<?xml version="1.0" encoding="utf-8"?>
            <testsuites time="5.548">
               <testsuite errors="0" failures="2" name="my-test-suite" skipped="0" tests="1" time="0.342">
                  <testcase classname="my classname" name="my name" time="0.143">
                      <failure message="file 1 not found"/>
                      <failure message="file 2 not found"/>
                  </testcase>
               </testsuite>
            </testsuites>
        """
        print(junit_xml)

        f = open("junit-output.xml", "w")
        f.write(junit_xml)
        f.close()
