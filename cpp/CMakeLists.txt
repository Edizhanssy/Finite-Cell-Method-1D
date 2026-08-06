cmake_minimum_required(VERSION 4.1)
project(Finite_Cell_Method)

set(CMAKE_CXX_STANDARD 14)

add_executable(fcm1d apps/fcm1d.cpp)
target_include_directories(fcm1d PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)