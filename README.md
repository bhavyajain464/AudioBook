# AudioBook
AudioBook using kivy interface in python (only read pdf files for now)

Steps to build your own AudioBook:
1) First clone the repository and go to the root directory of the app.
2) Install the requirements using pip install -r requirement.txt.
3) Then run "buildozer android debug deploy run" to build the apk file.
4) Copy the apk file created in bin folder in the root directory to the phone and install it.


Note:
1) To debug just run "python3 main.py" after installing all the requirements
2) If you are getting error in running that "android" module not found.Then comment out two lines "from android.permissions import request_permissions, Permission" and "request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])".These lines are required to ask storage permission from the user and these lines must be uncommented before building the apk file.
3) If you want to change some specifications and permissions regarding the app buildozer.spec file can be changed.
4) If the change is not reflected in the build apk then first run buildozer android clean to run the build from scratch.
