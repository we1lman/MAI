cmake_minimum_required(VERSION 3.10)
project(BinaryTreeSearch LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

set(SOURCES src/main.cpp)

add_executable(main ${SOURCES})
