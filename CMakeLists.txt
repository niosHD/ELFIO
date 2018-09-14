cmake_minimum_required(VERSION 3.5.0)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(forceOutOfSourceBuild)

# Parse the library version from the configure.ac file
file(READ "configure.ac" CONFIGURE_AC)
if(NOT CONFIGURE_AC MATCHES "AC_INIT\\(\\[ELFIO\\], \\[([0-9\\.]+)\\]\\)")
  message(FATAL_ERROR "Version could not be parsed.")
else()
  set(VERSION_STRING "${CMAKE_MATCH_1}")
endif()

project(elfio VERSION "${VERSION_STRING}" LANGUAGES CXX)

add_library(elfio INTERFACE)
add_library(elfio::elfio ALIAS elfio)
target_include_directories(elfio INTERFACE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                                           $<INSTALL_INTERFACE:include>)
target_compile_features(elfio INTERFACE cxx_std_11)

# Determine if project is built as a subproject (using add_subdirectory)
# or if it is the master project.
if (PROJECT_NAME STREQUAL CMAKE_PROJECT_NAME)
  enable_testing()
  option(BUILD_EXAMPLES "Build examples by default." ON)
  if(BUILD_EXAMPLES)
    add_subdirectory(examples)
  else()
    add_subdirectory(examples EXCLUDE_FROM_ALL)
  endif()

  option(BUILD_TESTS "Build tests by default." ON)
  if(BUILD_TESTS)
    add_subdirectory(ELFIOTest)
  else()
    add_subdirectory(ELFIOTest EXCLUDE_FROM_ALL)
  endif()

  #----------------------------------------------------------------------------
  # Installation and export configuration
  #----------------------------------------------------------------------------
  # Setup variables with the paths and targets that should be installed.
  # Using cached variables to permit overriding them from the command line.
  include(GNUInstallDirs)
  set(CONFIG_FILE_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/elfio" CACHE STRING
      "Installation directory for cmake files, relative to CMAKE_INSTALL_PREFIX.")
  set(LIB_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}" CACHE STRING
      "Installation directory for libraries, relative to CMAKE_INSTALL_PREFIX.")
  set(INCLUDE_INSTALL_DIR "${CMAKE_INSTALL_INCLUDEDIR}" CACHE STRING
      "Installation directory for include files, relative to CMAKE_INSTALL_PREFIX.")

  set(version_config "${PROJECT_BINARY_DIR}/elfio-config-version.cmake")
  set(project_config "${PROJECT_BINARY_DIR}/elfio-config.cmake")
  set(targets_export_name "elfio-targets")
  set(install_targets "elfio")
  set(namespace "elfio::")

  # Generate the version, config and target files into the build directory.
  include(CMakePackageConfigHelpers)
  write_basic_package_version_file("${version_config}"
                                   VERSION "${PROJECT_VERSION}"
                                   COMPATIBILITY "AnyNewerVersion")
  configure_package_config_file("${PROJECT_SOURCE_DIR}/cmake/elfio-config.cmake.in"
                                "${project_config}"
                                INSTALL_DESTINATION "${CONFIG_FILE_INSTALL_DIR}")
  export(TARGETS ${install_targets}
         NAMESPACE "${namespace}"
         FILE "${PROJECT_BINARY_DIR}/${targets_export_name}.cmake")

  # Install version, config and target files.
  install(FILES "${project_config}" "${version_config}"
          DESTINATION "${CONFIG_FILE_INSTALL_DIR}")
  install(EXPORT "${targets_export_name}"
          DESTINATION "${CONFIG_FILE_INSTALL_DIR}"
          NAMESPACE "${namespace}")

  # Install the library and headers.
  install(TARGETS ${install_targets}
          EXPORT "${targets_export_name}"
          DESTINATION "${LIB_INSTALL_DIR}")
  install(DIRECTORY "elfio"
          DESTINATION "${INCLUDE_INSTALL_DIR}"
          FILES_MATCHING
          PATTERN "*.h"
          PATTERN "*.hpp")

  #----------------------------------------------------------------------------
  # Simple packaging support
  #----------------------------------------------------------------------------
  set(CPACK_PACKAGE_VERSION_MAJOR "${PROJECT_VERSION_MAJOR}")
  set(CPACK_PACKAGE_VERSION_MINOR "${PROJECT_VERSION_MINOR}")
  set(CPACK_PACKAGE_VERSION_PATCH "${PROJECT_VERSION_PATCH}")
  set(CPACK_SOURCE_GENERATOR ZIP)
  set(CPACK_SOURCE_PACKAGE_FILE_NAME "elfio-${PROJECT_VERSION}")
  set(CPACK_PACKAGE_NAME "elfio")
  set(CPACK_RESOURCE_FILE_README "${PROJECT_SOURCE_DIR}/README")
  include(CPack)
endif ()
