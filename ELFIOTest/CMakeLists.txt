cmake_minimum_required(VERSION 3.5.0)
project(elfio-tests LANGUAGES CXX)
if(NOT TARGET elfio::elfio)
  find_package(elfio REQUIRED)
endif()

find_package(Boost REQUIRED COMPONENTS unit_test_framework)

file(GLOB Sources "*.cpp")
add_executable(ELFIOTest ${Sources})
target_link_libraries(ELFIOTest PRIVATE elfio::elfio Boost::unit_test_framework)

enable_testing()
add_test(NAME ELFIOTest COMMAND ELFIOTest WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
