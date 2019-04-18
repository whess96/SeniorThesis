////////////////////////////////////////////////////////////////////////////////
// streamPlaneState.cpp
//
// Custom app for thesis that only reads the relevant state information of the 
// plane. Uses the Vicon DataStream SDK.
//
// Local Translation: (X: Left, Y: Towards computers, Z: Up)
// Local Rotation:    (Pitch, Roll, Yaw)
////////////////////////////////////////////////////////////////////////////////

#include "DataStreamClient.h"
#include <lcm/lcm-cpp.hpp>
#include "../planeDataT/viconState.hpp"

#include <iostream>
#include <fstream>
#include <cassert>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <string.h>
#include <unistd.h> // For sleep()
#include <time.h>
#include <sys/time.h>

using namespace ViconDataStreamSDK::CPP;

#define output_stream std::cout 

namespace
{
  std::string Adapt( const bool i_Value )
  {
    return i_Value ? "True" : "False";
  }

  std::string Adapt( const Direction::Enum i_Direction )
  {
    switch( i_Direction )
    {
      case Direction::Forward:
        return "Forward";
      case Direction::Backward:
        return "Backward";
      case Direction::Left:
        return "Left";
      case Direction::Right:
        return "Right";
      case Direction::Up:
        return "Up";
      case Direction::Down:
        return "Down";
      default:
        return "Unknown";
    }
  }

  std::string Adapt( const DeviceType::Enum i_DeviceType )
  {
    switch( i_DeviceType )
    {
      case DeviceType::ForcePlate:
        return "ForcePlate";
      case DeviceType::Unknown:
      default:
        return "Unknown";
    }
  }

  std::string Adapt( const Unit::Enum i_Unit )
  {
    switch( i_Unit )
    {
      case Unit::Meter:
        return "Meter";
      case Unit::Volt:
        return "Volt";
      case Unit::NewtonMeter:
        return "NewtonMeter";
      case Unit::Newton:
        return "Newton";
      case Unit::Kilogram:
        return "Kilogram";
      case Unit::Second:
        return "Second";
      case Unit::Ampere:
        return "Ampere";
      case Unit::Kelvin:
        return "Kelvin";
      case Unit::Mole:
        return "Mole";
      case Unit::Candela:
        return "Candela";
      case Unit::Radian:
        return "Radian";
      case Unit::Steradian:
        return "Steradian";
      case Unit::MeterSquared:
        return "MeterSquared";
      case Unit::MeterCubed:
        return "MeterCubed";
      case Unit::MeterPerSecond:
        return "MeterPerSecond";
      case Unit::MeterPerSecondSquared:
        return "MeterPerSecondSquared";
      case Unit::RadianPerSecond:
        return "RadianPerSecond";
      case Unit::RadianPerSecondSquared:
        return "RadianPerSecondSquared";
      case Unit::Hertz:
        return "Hertz";
      case Unit::Joule:
        return "Joule";
      case Unit::Watt:
        return "Watt";
      case Unit::Pascal:
        return "Pascal";
      case Unit::Lumen:
        return "Lumen";
      case Unit::Lux:
        return "Lux";
      case Unit::Coulomb:
        return "Coulomb";
      case Unit::Ohm:
        return "Ohm";
      case Unit::Farad:
        return "Farad";
      case Unit::Weber:
        return "Weber";
      case Unit::Tesla:
        return "Tesla";
      case Unit::Henry:
        return "Henry";
      case Unit::Siemens:
        return "Siemens";
      case Unit::Becquerel:
        return "Becquerel";
      case Unit::Gray:
        return "Gray";
      case Unit::Sievert:
        return "Sievert";
      case Unit::Katal:
        return "Katal";

      case Unit::Unknown:
      default:
        return "Unknown";
    }
  }
}

int main( int argc, char* argv[] )
{
  // Program options
  std::string HostName = "169.254.128.253:801";
  if( argc > 1 )
  {
    HostName = argv[1];
  }

  std::string LogFile = "viconEfliteLogs.txt";
  std::string AxisMapping = "ZUp";

  std::ofstream ofs;
  if(!LogFile.empty())
  {
    ofs.open(LogFile.c_str());
    if(!ofs.is_open())
    {
      std::cout << "Could not open log file <" << LogFile << ">...exiting" << std::endl;
      return 1;
    }
  }
  // Make a new client
  Client MyClient;

  for(int i=0; i != 3; ++i) // repeat to check disconnecting doesn't wreck next connect
  {
    // Connect to a server
    std::cout << "Connecting to " << HostName << " ..." << std::flush;
    while( !MyClient.IsConnected().Connected )
    {
      bool ok = false;
      ok = ( MyClient.Connect( HostName ).Result == Result::Success );

      if(!ok)
      {
        std::cout << "Warning - connect failed..." << std::endl;
      }

      std::cout << ".";
      sleep(1);
    }
    std::cout << std::endl;

    // Enable some different data types
    MyClient.EnableSegmentData();
    MyClient.EnableMarkerData();
    MyClient.EnableUnlabeledMarkerData();
    MyClient.EnableMarkerRayData();
    MyClient.EnableDeviceData();
    MyClient.EnableDebugData();

    // Set the streaming mode
    //MyClient.SetStreamMode( ViconDataStreamSDK::CPP::StreamMode::ClientPull );
    // MyClient.SetStreamMode( ViconDataStreamSDK::CPP::StreamMode::ClientPullPreFetch );
    MyClient.SetStreamMode( ViconDataStreamSDK::CPP::StreamMode::ServerPush );

    // Set the global up axis
    MyClient.SetAxisMapping( Direction::Forward, 
                             Direction::Left, 
                             Direction::Up ); // Z-up

    Output_GetAxisMapping _Output_GetAxisMapping = MyClient.GetAxisMapping();
    std::cout << "Axis Mapping: X-" << Adapt( _Output_GetAxisMapping.XAxis ) 
                           << " Y-" << Adapt( _Output_GetAxisMapping.YAxis ) 
                           << " Z-" << Adapt( _Output_GetAxisMapping.ZAxis ) << std::endl;

    // Discover the version number
    Output_GetVersion _Output_GetVersion = MyClient.GetVersion();
    std::cout << "Version: " << _Output_GetVersion.Major << "." 
                             << _Output_GetVersion.Minor << "." 
                             << _Output_GetVersion.Point << std::endl;

    size_t FrameRateWindow = 1000; // frames
    size_t Counter = 0;
    clock_t LastTime = clock();

    // Store previous translational and rotational positions for calculating
    // velocities
    double prevTrans [3];
    double prevRot [3];

    // Establish LCM
    lcm::LCM lcm;

    // Loop until killed.
    while(true)
    {
      // Get a frame
      output_stream << "Waiting for new frame...";
      while( MyClient.GetFrame().Result != Result::Success )
      {
        // Sleep a little so that we don't lumber the CPU with a busy poll
        sleep(1);
        output_stream << ".";
      }
      output_stream << std::endl;
      if(++Counter == FrameRateWindow)
      {
        clock_t Now = clock();
        double FrameRate = (double)(FrameRateWindow * CLOCKS_PER_SEC) / (double)(Now - LastTime);
        if(!LogFile.empty())
        {
          time_t rawtime;
          struct tm * timeinfo;
          time ( &rawtime );
          timeinfo = localtime ( &rawtime );

          ofs << "Frame rate = " << FrameRate << " at " <<  asctime (timeinfo)<< std::endl;
        }

        LastTime = Now;
        Counter = 0;
      }

      // Get the frame number
      Output_GetFrameNumber _Output_GetFrameNumber = MyClient.GetFrameNumber();
      output_stream << "Frame Number: " << _Output_GetFrameNumber.FrameNumber << std::endl;

      Output_GetFrameRate Rate = MyClient.GetFrameRate();
      std::cout << "Frame rate: "           << Rate.FrameRateHz          << std::endl;

      // Show frame rates
      for( unsigned int FramerateIndex = 0 ; FramerateIndex < MyClient.GetFrameRateCount().Count ; ++FramerateIndex )
      {
        std::string FramerateName  = MyClient.GetFrameRateName( FramerateIndex ).Name;
        double      FramerateValue = MyClient.GetFrameRateValue( FramerateName ).Value;

        output_stream << FramerateName << ": " << FramerateValue << "Hz" << std::endl;
      }
      output_stream << std::endl;

      // Get the timecode
      Output_GetTimecode _Output_GetTimecode  = MyClient.GetTimecode();

      output_stream << "Timecode: "
                << _Output_GetTimecode.Hours               << "h "
                << _Output_GetTimecode.Minutes             << "m " 
                << _Output_GetTimecode.Seconds             << "s "
                << _Output_GetTimecode.Frames              << "f "
                << _Output_GetTimecode.SubFrame            << "sf " 
                << std::endl << std::endl;

      // Get the latency
      // output_stream << "Latency: " << MyClient.GetLatencyTotal().Total << "s" << std::endl;
      
      // for( unsigned int LatencySampleIndex = 0 ; LatencySampleIndex < MyClient.GetLatencySampleCount().Count ; ++LatencySampleIndex )
      // {
      //   std::string SampleName  = MyClient.GetLatencySampleName( LatencySampleIndex ).Name;
      //   double      SampleValue = MyClient.GetLatencySampleValue( SampleName ).Value;

      //   output_stream << "  " << SampleName << " " << SampleValue << "s" << std::endl;
      // }
      // output_stream << std::endl;

      unsigned int SubjectIndex = 0;
      // Get the subject name
      std::string SubjectName = MyClient.GetSubjectName( SubjectIndex ).SubjectName;
      output_stream << "    Name: " << SubjectName << std::endl;

      unsigned int SegmentIndex = 0;
      // Get the segment name
      std::string SegmentName = MyClient.GetSegmentName( SubjectName, SegmentIndex ).SegmentName;
      output_stream << "        Name: " << SegmentName << std::endl;


      // Get the local segment translation
      Output_GetSegmentLocalTranslation _Output_GetSegmentLocalTranslation = 
        MyClient.GetSegmentLocalTranslation( SubjectName, SegmentName );
      output_stream << "        Local Translation: (" << _Output_GetSegmentLocalTranslation.Translation[ 0 ]  << ", " 
                                                  << _Output_GetSegmentLocalTranslation.Translation[ 1 ]  << ", " 
                                                  << _Output_GetSegmentLocalTranslation.Translation[ 2 ]  << ") " 
                                                  << Adapt( _Output_GetSegmentLocalTranslation.Occluded ) << std::endl;

      // Get the local segment rotation in EulerXYZ co-ordinates
      Output_GetSegmentLocalRotationEulerXYZ _Output_GetSegmentLocalRotationEulerXYZ = 
        MyClient.GetSegmentLocalRotationEulerXYZ( SubjectName, SegmentName );
      output_stream << "        Local Rotation EulerXYZ: (" << _Output_GetSegmentLocalRotationEulerXYZ.Rotation[ 0 ]     << ", " 
                                                        << _Output_GetSegmentLocalRotationEulerXYZ.Rotation[ 1 ]     << ", " 
                                                        << _Output_GetSegmentLocalRotationEulerXYZ.Rotation[ 2 ]     << ") " 
                                                        << Adapt( _Output_GetSegmentLocalRotationEulerXYZ.Occluded ) << std::endl;
    
    // Fill and send the LCM package
    planeDataT::viconState myData;

    struct timeval currTime;
    gettimeofday(&currTime, NULL);

    // If occluded, just don't publish this timestep.
    if (!_Output_GetSegmentLocalTranslation.Occluded && 
      !_Output_GetSegmentLocalRotationEulerXYZ.Occluded) {
      double* currTrans = _Output_GetSegmentLocalTranslation.Translation;
      double* currRot = _Output_GetSegmentLocalRotationEulerXYZ.Rotation;

      myData.position[0] = currTrans[0]/1000;
      myData.position[1] = currTrans[1]/1000;
      myData.position[2] = currTrans[2]/1000;

      myData.angles[0] = currRot[0];
      myData.angles[1] = currRot[1];
      myData.angles[2] = currRot[2];

      // Calculate velocities
      myData.velocity[0] = (currTrans[0] - prevTrans[0])*Rate.FrameRateHz/1000;
      myData.velocity[1] = (currTrans[1] - prevTrans[1])*Rate.FrameRateHz/1000;
      myData.velocity[2] = (currTrans[2] - prevTrans[2])*Rate.FrameRateHz/1000;

      myData.angularRates[0] = (currRot[0] - prevRot[0])*Rate.FrameRateHz;
      myData.angularRates[1] = (currRot[1] - prevRot[1])*Rate.FrameRateHz;
      myData.angularRates[2] = (currRot[2] - prevRot[2])*Rate.FrameRateHz;

      myData.timestamp = (int64_t) currTime.tv_sec*1000000 + currTime.tv_usec;

      lcm.publish("flightState", &myData);

      // Store current values for future velocity calculations
      prevTrans[0] = currTrans[0];
      prevTrans[1] = currTrans[1];
      prevTrans[2] = currTrans[2];  
      
      prevRot[0] = currRot[0];
      prevRot[1] = currRot[1];
      prevRot[2] = currRot[2];
    }
  }
  }
}
  