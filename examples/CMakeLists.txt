cmake_minimum_required(VERSION 3.5.0)
project(elfio-examples LANGUAGES CXX)
if(NOT TARGET elfio::elfio)
  find_package(elfio REQUIRED)
endif()

function(build_example name)
  file(GLOB Sources "${name}/*.cpp")
  add_executable("${name}" ${Sources})
  target_link_libraries("${name}" PRIVATE elfio::elfio)
endfunction()

build_example(anonymizer)
build_example(elfdump)
# source files are missing for RelocationTable
build_example(tutorial)
build_example(write_obj)
build_example(writer)
