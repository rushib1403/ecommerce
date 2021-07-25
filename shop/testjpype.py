from jpype import *

startJVM(getDefaultJVMPath(),"-ea")
java.lang.System.out.println("Hello World!!")
Test = JClass('pkg.Test')
Test.speak("hipankudata=psoj")
shutdownJVM()
