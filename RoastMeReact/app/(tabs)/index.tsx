// index.tsx
import { StyleSheet, Pressable, Text, SafeAreaView, TextInput, View } from 'react-native';
import { useState } from 'react';
import CameraComponent from '@/components/CameraComponent';

export default function HomeScreen() {
  const [isGreen, setIsGreen] = useState(false);
  
  const handlePhotoTaken = (uri: string) => {
    console.log('Photo taken:', uri);
  };

  const handleGreenHeartPress = () => {
    setIsGreen(!isGreen);
  };

  const handleRoastMePress = () => {
    console.log('Roast Me button pressed!');
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: isGreen ? "#1B3D2F" : '#200000' }]}>
      <SafeAreaView elevation={5} style={[styles.CameraContainer, { backgroundColor: isGreen ? '#255A3B' : '#3A0000' }]}>
        <Pressable 
          style={[styles.roastCompliment, {backgroundColor: isGreen ?'#200000' : '#1B3D2F'}]} 
          onPress={handleGreenHeartPress}
        >
          <Text style={styles.greenHeart}>{isGreen ? '🔥' : '💚'}</Text>
        </Pressable>
        '💚Compliment Mode💚'
        <Text style={styles.header}>
          {isGreen ? '💚Compliment Mode💚' : '🔥 Roast Mode 🔥'}
        </Text>

        <View style={styles.cameraView}>
          <CameraComponent 
            onPhotoTaken={handlePhotoTaken}
          />
        </View>

        <TextInput 
          style={[styles.response, {backgroundColor: isGreen ? '#2E4C43' : '#4A0000'}]}
        />

        <Pressable 
          style={[styles.button, {backgroundColor: isGreen ? '#4caf50' : '#ff4c4c'}]} 
          onPress={handleRoastMePress}
        >
          <Text style={styles.text}>{isGreen ? 'Compliment me' : 'Roast me'}</Text>
        </Pressable>
      </SafeAreaView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  CameraContainer: {
    height: '70%',
    width: '90%',
    borderRadius: 10,
    // iOS shadow properties
    shadowColor: '#000',  // Shadow color
    shadowOffset: { width: 0, height: 4 },  // Shadow direction
    shadowOpacity: 0.2,  // Shadow opacity
    shadowRadius: 6,  // Shadow blur

    elevation: 5,  // Elevation for Android devices
  },
  cameraView: {
    height: '50%',
    width: '80%',
    alignSelf: 'center',
    marginTop: 20,
    overflow: 'hidden',
    borderRadius: 10,
  },
  roastCompliment: {
    height: 40,
    width: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'absolute',
    top: 10,
    right: 10,
  },
  greenHeart: {
    fontSize: 25,
  },
  response: {
    height: "15%",
    width: "80%",
    alignSelf: "center",
    marginTop: 20,
    color: "white",
  },
  header: {
    alignSelf: "center",
    color: "white",  
    fontSize: 18,
    marginTop: 10,
    textAlign: "center",  
  },
  button: {
    width: "80%",
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    alignSelf: 'center',  
    marginTop: 'auto',    
    marginBottom: 20,     
  },
  text: {
    fontWeight: '800',
    fontSize: 15,
    color: "white"
  },
});