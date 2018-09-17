from conans import ConanFile, CMake, tools
import os
import re

# parse the version from the configure.ac file
def get_version():
    configureac_path = os.path.join(os.path.dirname(__file__), "configure.ac")
    if not os.path.isfile(configureac_path):
        return None
    with open(configureac_path, 'r') as myfile:
        data = myfile.read()
    version = re.search("AC_INIT\\(\\[ELFIO\\], \\[([0-9\\.]+)\\]\\)", data)
    if version:
        return version.group(1)
    return None

class Elfio(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    name = 'elfio'
    url = 'https://github.com/serge1/ELFIO'
    license = 'MIT'
    version = get_version()
    no_copy_source = True
    scm = {
        "type": "git",
        "url": "https://github.com/niosHD/ELFIO.git",
        "revision": "auto"
    }

    def build(self):
        run_tests = not tools.cross_building(self.settings)

        cmake = CMake(self)
        cmake.definitions["BUILD_EXAMPLES"] = False
        cmake.definitions["BUILD_TESTS"] = run_tests
        cmake.configure()
        cmake.build()
        if run_tests:
            cmake.test()
        cmake.install()

    def package_id(self):
        self.info.header_only()
