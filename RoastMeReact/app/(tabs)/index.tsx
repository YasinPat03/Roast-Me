import { StyleSheet, Platform, Pressable, Text, SafeAreaView } from 'react-native';
import { useState } from 'react';
import CameraComponent from '@/components/CameraComponent';
import { ThemedView } from '@/components/ThemedView';
import { ThemedText } from '@/components/ThemedText';

export default function HomeScreen() {
  // Initialize showCamera as true to show camera on boot
  const [showCamera, setShowCamera] = useState(true);
  
  const handlePhotoTaken = (uri: string) => {
    console.log('Photo taken:', uri);
    setShowCamera(false);
    // Handle the photo URI here - maybe show it in your UI
  };

  if (showCamera) {
    return (
      <SafeAreaView style={styles.container}>
        <CameraComponent 
          onPhotoTaken={handlePhotoTaken}
          onClose={() => setShowCamera(false)}
        />
      </SafeAreaView>
    );
  }

  return (
    <ThemedView style={styles.container}>
      <ThemedText style={styles.title}>Welcome</ThemedText>
      <Pressable 
        style={styles.button}
        onPress={() => setShowCamera(true)}>
        <Text style={styles.buttonText}>Open Camera</Text>
      </Pressable>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 20,
  },
  button: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    margin: 20,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  }
});